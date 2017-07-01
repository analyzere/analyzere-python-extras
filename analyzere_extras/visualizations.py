import hashlib
import itertools
from collections import OrderedDict

from analyzere import LayerView
from graphviz import Digraph
try:
    from IPython.display import FileLink
    _in_notebook = True
except ImportError:
    _in_notebook = False

from sys import float_info


# 12 distinct colors for colorizing edges
color_pallette = ['#000000',
                  '#0265d8',
                  '#d9c91b',
                  '#b031b7',
                  '#6ddc8f',
                  '#ff479c',
                  '#1d5f1c',
                  '#eb0d55',
                  '#a4c2ff',
                  '#ec611a',
                  '#ff99cc',
                  '#ae2e00']


def _format_description(description):
    """Clean the description of a node for display in Graphviz"""
    return description.replace('\'', '').encode('unicode_escape').decode()


def _format_DateField(df):
    """Format a Date field, chopping off the time portion"""
    return df.date().isoformat()


def _format_MoneyField(mf):
    """Format a MoneyField to '<unlimited|value> CCY' """
    if mf.value == float_info.max:
        formatted = 'unlimited'
    else:
        formatted = '{:,.0f} {}'.format(float(mf.value), mf.currency)
    return formatted


def _format_filters(filters):
    num_filters = len(filters)
    if num_filters == 0:
        filters_value = '(empty)'
    elif num_filters < 4:
        filter_strings = []
        for f in filters:
            filter_strings.append("'{}'".format(f.name))
        filters_value = '[{}]'.format(', '.join(filter_strings))
    else:
        filters_value = '({} filters)'.format(num_filters)
    return filters_value


def _format_reinstatements(reinstatements):
    num_reinstatements = len(reinstatements)

    if num_reinstatements > 4:
        reinsts_value = '{}'.format(num_reinstatements)
    else:
        reinstatements = ['{}/{}'.format(r.premium, r.brokerage)
                          for r in reinstatements]
        reinsts_value = '[{}]'.format(', '.join(reinstatements))
    return reinsts_value


def _format_coverage(layer):
    coverage = ['{}'.format(_format_DateField(layer.inception_date))
                if hasattr(layer, 'inception_date') else '-inf',
                '{}'.format(_format_DateField(layer.expiry_date))
                if hasattr(layer, 'expiry_date') else 'inf']
    return '[{}]'.format(', '.join(coverage))


class FormattingHelper:
    def __init__(self, layer):
        self._layer = layer
        self._terms = OrderedDict()
        self.warning = False

    def append(self, required_attr, display_name=None,
               formatter=lambda x: str(x),
               condition=lambda: True,
               warning=lambda: False):
        if not display_name:
            display_name = required_attr

        if not hasattr(self._layer, required_attr) or not condition():
            return

        attr = getattr(self._layer, required_attr)
        self._terms[display_name] = formatter(attr)
        self.warning |= warning()

    def append_term(self, term, value):
        self._terms[term] = value

    def formatted_terms(self):
        leading_text = '\n' if self._terms else ''
        return (leading_text
                + '\n'.join(['{}={}'.format(key, value)
                             for key, value in self._terms.items()]))


def _format_layer_terms(layer):
    """Get the terms for the given layer for display in Graphviz"""
    formatter = FormattingHelper(layer)

    if hasattr(layer, 'inception_date') or hasattr(layer, 'expiry_date'):
        formatter.append_term('coverage', _format_coverage(layer))

    formatter.append('participation', display_name='share',
                     formatter=lambda x: '{}%'.format(x*100),
                     warning=lambda: layer.participation == 0.0)

    # LossRank
    formatter.append(required_attr='criterion', display_name='criterion')
    formatter.append(required_attr='count', display_name='count')

    # FilterLayer
    formatter.append('filters', formatter=_format_filters)

    formatter.append('invert',
                     warning=lambda: (not layer.invert
                                      and layer.type == 'FilterLayer'
                                      and len(layer.filters) == 0))

    # CatXL, AggXL, Generic
    formatter.append('attachment', display_name='occ_att',
                     formatter=_format_MoneyField,
                     warning=lambda: (layer.attachment.value
                                      >= float_info.max))

    formatter.append(required_attr='limit', display_name='occ_lim',
                     formatter=_format_MoneyField)

    # CatXL, IndustryLossWarranty
    formatter.append('nth')

    formatter.append('reinstatements', display_name='reinsts',
                     formatter=_format_reinstatements,
                     condition=lambda: layer.reinstatements)

    formatter.append('franchise', formatter=_format_MoneyField)

    # QuotaShare, AggregateQuotaShare
    formatter.append('event_limit', display_name='event_lim',
                     formatter=_format_MoneyField)

    # AggXL, AggregateQuotaShare
    formatter.append('aggregate_attachment',
                     display_name='agg_att',
                     formatter=_format_MoneyField,
                     warning=lambda: (layer.aggregate_attachment.value
                                      >= float_info.max))
    formatter.append('aggregate_limit', display_name='agg_lim',
                     formatter=_format_MoneyField)

    # AggregateQuotaShare
    formatter.append('aggregate_period', display_name='agg_period')
    formatter.append('aggregate_reset', display_name='agg_reset',
                     condition=lambda: layer.aggregate_reset > 1)

    # SurplusShare
    formatter.append('sums_insured', formatter=_format_MoneyField)
    formatter.append('retained_line', formatter=_format_MoneyField)
    formatter.append('number_of_lines')

    # IndustryLossWarranty
    formatter.append('trigger', formatter=_format_MoneyField)
    formatter.append('payout', formatter=_format_MoneyField)

    # NoClaimsBonus
    formatter.append('payout_date', formatter=_format_DateField)
    formatter.append('payout_amount', display_name='payout',
                     formatter=_format_MoneyField)

    formatter.append('premium', formatter=_format_MoneyField,
                     condition=lambda: layer.premium is not None)

    return formatter.formatted_terms(), formatter.warning


class LayerViewDigraph(object):
    """Class that provides simple visualization of Analyze Re LayerViews.

    Using the 'graphviz' python package, this class enables users to
    visualize Analyze Re LayerView objects.
    """
    def _update_filename(self, filename=None):
        # build filename with format:
        #    '<lv_id>_<rankdir>_<[not-]compact>_<with[out]-terms>\
        #    _<with[out]-warnings><_depth-><_srclimit-x>\
        #    <y-colors-by-<depth|breadth>>.<format>'
        compact = 'compact' if self._compact else 'not-compact'
        terms = 'with-terms' if self._with_terms else 'without-terms'
        warnings = ('warnings-enabled' if self._warnings
                    else 'warnings-disabled')
        depth = '_depth-{}'.format(self._max_depth) if self._max_depth else ''
        src_limit = ('_srclimit-{}'.format(self._max_sources)
                     if self._max_sources else '')
        colors = ('-{}-colors-by-{}'.format(self._colors, self._color_mode)
                  if self._colors > 1 else '')
        self._filename = (filename if filename else
                          '{}_{}_{}_{}_{}{}{}{}'.format(self._lv.id,
                                                        self._rankdir,
                                                        compact,
                                                        terms,
                                                        warnings,
                                                        depth,
                                                        src_limit,
                                                        colors))

    def _generate_nodes(self, l,
                        parent_hash=None,
                        prefix=None,
                        current_depth=0):

        # default node attributes
        self._graph.attr('node', shape='box', style='filled',
                         fillcolor='white')

        # hash the current node to see if it is unique
        node_hash = hashlib.md5((str(l)
                                 + (parent_hash or ''))
                                .encode('utf-8')).hexdigest()

        if (node_hash not in self.unique_nodes) or not self._compact:
            self.unique_nodes[node_hash] = next(self.sequence)

        if l.type == 'NestedLayer':
            prefix = ('"{}"\nNested'.format(
                      _format_description(l.description))
                      if l.description else 'Nested')

            sink_hash = self._generate_nodes(l.sink,
                                             parent_hash=node_hash,
                                             prefix=prefix,
                                             current_depth=current_depth)

            if self._max_depth is None or current_depth < self._max_depth:
                # if we are enforcing a source limit, we will return early
                # after creating a summary node
                if (self._max_sources is not None and
                   len(l.sources) > self._max_sources):
                    sources_id = '{} sources'.format(sink_hash)
                    if not(sources_id, sink_hash) in self.edges:
                        self.edges.add((sources_id, sink_hash))
                        self._graph.node(sources_id,
                                         color=color_pallette[self._color_idx],
                                         label='{} sources'.format(
                                          len(l.sources)))
                        self._graph.edge(sources_id, sink_hash,
                                         color=color_pallette[self._color_idx])

                    return sink_hash

                idx = 0
                for s in l.sources:
                    if idx > 0 and self._color_mode == 'breadth':
                        self._color_idx = (self._color_idx + 1) % self._colors
                    source = self._generate_nodes(
                        s, current_depth=current_depth+1)
                    # We have to reset the color to match the parent's color
                    if self._color_mode == 'depth':
                        self._color_idx = current_depth % self._colors
                    if not (source, sink_hash) in self.edges:
                        self._graph.edge(source, sink_hash,
                                         color=color_pallette[self._color_idx])
                        self.edges.add((source, sink_hash))
                    idx += 1
            return sink_hash

        else:
            name = prefix + ' ' if prefix else ''
            name += l.type + ' '
            name += ('"{}"'.format(_format_description(l.description))
                     if l.description else
                     '({})'.format(self.unique_nodes[node_hash]))
            terms, warning = _format_layer_terms(l)
            name += terms if self._with_terms else ''
            if self._color_mode == 'depth':
                self._color_idx = current_depth % self._colors

            # color nodes with 'warnings' as tomato iff configured
            self._graph.node(node_hash, label=name,
                             color=color_pallette[self._color_idx],
                             fillcolor='tomato' if warning and self._warnings
                             else 'white')

            # Now process LossSets
            if self._color_mode == 'depth':
                self._color_idx = (current_depth+1) % self._colors

            idx = 0
            for ls in l.loss_sets:
                if idx > 0 and self._color_mode == 'breadth':
                    self._color_idx = (self._color_idx + 1) % self._colors
                ls_name = '{} "{}"'.format(
                    ls.type, _format_description(ls.description))
                ls_id = '{}{}'.format(ls.id,
                                      ' ({})'.format(next(self.sequence))
                                      if not self._compact else '')
                if not (ls_id, node_hash) in self.edges:
                    self._graph.node(ls_id, label=ls_name,
                                     color=color_pallette[self._color_idx],
                                     fillcolor='lightgrey')
                    self._graph.edge(ls_id, node_hash,
                                     color=color_pallette[self._color_idx])
                    self.edges.add((ls_id, node_hash,))
                idx += 1
        return node_hash

    def __init__(self, lv, with_terms=True, compact=True,
                 format='png', rankdir='BT', warnings=True,
                 max_depth=None, max_sources=None, colors=1,
                 color_mode='breadth'):
        """Generate a Graphviz.Digraph for the given LayerView

        Optional parameters that control the visualization:

           with_terms   specify that Layer terms are included in each
                        node of the graph (default=True).

           compact      controls if duplicate nodes should be omitted
                        (default=True).

           format       exposes the graphviz 'format' option which include
                        'pdf', 'png', etc. (default='png').

           rankdir      exposes the graphviz 'rankdir' option that controls
                        the orientation of the graph.  Options include
                        'TB', 'LR', 'BT', 'RL', corresponding to directed
                        graphs drawn from top to bottom, from left to right,
                        from bottom to top, and from right to left,
                        respectively (default='BT').

           warnings     highlight nodes with suspicious terms by coloring them
                        red (default=True).

           max_depth    The maximum depth of the graph to process.

           max_sources  The maximum number of Loss sources to graph in detail
                        for a single node.

           colors       The number of colors to be used when coloring edges.

           color_mode   The mode to use when applying colors.
                        Options include: ['breadth', 'depth']
        """
        # sanity check on the input
        if not isinstance(lv, LayerView):
            raise ValueError('must supply a valid LayerView instance')

        self._lv = lv
        self._with_terms = with_terms
        self._rankdir = rankdir
        self._format = format
        self._compact = compact
        self._warnings = warnings
        self._max_depth = max_depth
        self._max_sources = max_sources
        self._colors = colors
        self._color_idx = 0
        self._color_mode = color_mode

        # initialize the filename
        self._update_filename()

        # defaults for the Digraph, overridden by plot()
        self._graph = Digraph(format=format,
                              graph_attr={'rankdir': rankdir})
        # now build the "tree" of nodes
        # sequencer for identifying 'ambiguous' nodes
        self.sequence = itertools.count()
        # hash map of unique nodes (prevents duplication)
        self.unique_nodes = {}
        # set of unique edges (prevents duplicates)
        self.edges = set()

        self._generate_nodes(lv.layer)

    @staticmethod
    def from_id(lv_id, with_terms=True, compact=True,
                format='png', rankdir='BT',
                max_depth=None, max_sources=None,
                colors=1, color_mode='breadth'):
        """Generate a LayerViewDigraph for the given LayerView Id
        Optional parameters:
           with_terms   specify that Layer terms are included in each
                        node of the graph.
           compact      controls if duplicate nodes should be omitted
                        (default=True).
           format       exposes the graphviz 'format' option which include
                        'pdf', 'png', etc.
           rankdir      exposes the graphviz 'rankdir' option that controls
                        the orientation of the graph.  Options include
                        'TB', 'LR', 'BT', 'RL', corresponding to directed
                        graphs drawn from top to bottom, from left to right,
                        from bottom to top, and from right to left,
                        respectively.

           max_depth    The maximum depth of the graph to process.

           max_sources  The maximum number of Loss sources to graph in detail
                        for a single node.

           colors       The number of colors to be used when coloring edges.

           color_mode   The mode to use when applying colors.
                        Options include: ['breadth', 'depth']
        """
        # This will raise and exception if any of the following analyzere
        # variables are not defined:
        #       - analyzere.base_url
        #       - analyzere.username
        #       - analyzere.password
        return LayerViewDigraph(LayerView.retrieve(lv_id), with_terms, compact,
                                format=format, rankdir=rankdir,
                                max_depth=max_depth, max_sources=max_sources)

    def render(self, filename=None, view=False, format=None, rankdir=None):
        """Render a LayerViewDigraph with the Graphviz engine

        Optional parameters:

           filename     specify the filename to be used when rendering.

           view         exposes the graphviz 'view' option that uses the
                        default application to open the rendered graph
                        (default=False).

           format       exposes the graphviz 'format' option which include
                        'pdf', 'png', etc.

           rankdir      exposes the graphviz 'rankdir' option that controls
                        the orientation of the graph.  Options include
                        'TB', 'LR', 'BT', 'RL', corresponding to directed
                        graphs drawn from top to bottom, from left to right,
                        from bottom to top, and from right to left,
                        respectively.
        """
        # check for 'render-time' overrides
        if rankdir:
            self._graph.graph_attr['rankdir'] = rankdir
            self._rankdir = rankdir
        if format:
            self._graph.format = format
            self._format = format

        # update the filename
        self._update_filename(filename)

        try:
            # protect against use cases when the default rendering tool
            # is not able to render the result
            # if we are in a python notebook we will use the FileLink feature
            # to return a click-able link to download the file
            if not view:
                return (FileLink(self._graph.render(self._filename, view=view))
                        if _in_notebook else
                        self._graph.render(self._filename, view=view))
            else:
                # view=True, do not return the FileLink or filename
                self._graph.render(self._filename, view=view)

        except RuntimeError:
            # native display failed, revert to returning a clickable FileLink
            # iff we are in a python notebook, otherwise return the filename.
            return (FileLink(self._graph.render(self._filename, view=False))
                    if _in_notebook else
                    self._graph.render(self._filename, view=False))
