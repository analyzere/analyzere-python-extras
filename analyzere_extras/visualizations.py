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

    # FilterLayer
    formatter.append('filters', formatter=_format_filters)

    formatter.append('invert',
                     warning=lambda: (not layer.invert
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
        #    _<with[out]-warnings>.<format>'
        self._filename = (filename if filename else
                          '{}_{}_{}_{}_{}'.format(self._lv.id,
                                                  self._rankdir,
                                                  'compact'
                                                  if self._compact
                                                  else 'not-compact',
                                                  'with-terms'
                                                  if self._with_terms
                                                  else 'without-terms',
                                                  'warnings-enabled'
                                                  if self._warnings
                                                  else 'warnings-disabled'))

    def _generate_nodes(self, l, sequence, unique_nodes, edges,
                        parent_hash=None, prefix=None):
        # hash the current node to see if it is unique
        node_hash = hashlib.md5((str(l)
                                 + (parent_hash or ''))
                                .encode('utf-8')).hexdigest()

        if (node_hash not in unique_nodes) or not self._compact:
            unique_nodes[node_hash] = next(sequence)

        if l.type == 'NestedLayer':
            prefix = ('"{}"\nNested'.format(_format_description(l.description))
                      if l.description else
                      'Nested')
            sink_hash = self._generate_nodes(l.sink, sequence, unique_nodes,
                                             edges, parent_hash=node_hash,
                                             prefix=prefix)
            for source in [self._generate_nodes(s, sequence,
                                                unique_nodes, edges)
                           for s in l.sources]:
                if not (source, sink_hash) in edges:
                    self._graph.edge(source, sink_hash)
                    edges.add((source, sink_hash))

            return sink_hash

        else:
            name = prefix + ' ' if prefix else ''
            name += l.type + ' '
            name += ('"{}"'.format(_format_description(l.description))
                     if l.description else
                     '({})'.format(unique_nodes[node_hash]))
            terms, warning = _format_layer_terms(l)
            name += terms if self._with_terms else ''

            self._graph.attr('node', shape='box',
                             style='filled',
                             fillcolor='white',
                             color='black')
            # color nodes with 'warnings' as red iff configured
            if warning and self._warnings:
                self._graph.attr('node', color='red', fillcolor='red')

            self._graph.node(node_hash, label=name)
            for ls in l.loss_sets:
                ls_name = '{} "{}"'.format(
                    ls.type, _format_description(ls.description))
                ls_id = '{}{}'.format(ls.id,
                                      ' ({})'.format(next(sequence))
                                      if not self._compact else '')
                if not (ls_id, node_hash) in edges:
                    self._graph.attr('node',
                                     shape='box', color='lightgrey',
                                     style='filled', fillcolor='lightgrey')
                    self._graph.node(ls_id, label=ls_name)
                    self._graph.edge(ls_id, node_hash)
                    edges.add((ls_id, node_hash))
        return node_hash

    def __init__(self, lv, with_terms=True, compact=True,
                 format='png', rankdir='BT', warnings=True):
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

        # initialize the filename
        self._update_filename()

        # defaults for the Digraph, overridden by plot()
        self._graph = Digraph(format=format,
                              graph_attr={'rankdir': rankdir,
                                          'size': '400,400'})
        # now build the "tree" of nodes
        # sequencer for identifying 'ambiguous' nodes
        sequence = itertools.count()
        # hash map of unique nodes (prevents duplication)
        unique_nodes = {}
        # set of unique edges (prevents duplicates)
        edges = set()

        self._generate_nodes(lv.layer, sequence, unique_nodes, edges)

    @staticmethod
    def from_id(lv_id, with_terms=True, compact=True,
                format='png', rankdir='BT'):
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
        """
        # This will raise and exception if any of the following analyzere
        # variables are not defined:
        #       - analyzere.base_url
        #       - analyzere.username
        #       - analyzere.password
        return LayerViewDigraph(LayerView.retrieve(lv_id), with_terms, compact,
                                format=format, rankdir=rankdir)

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
