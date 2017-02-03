import hashlib
import itertools

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
    formatted = 'n/a'
    if mf.value == float_info.max:
        formatted = 'unlimited'
    else:
        formatted = '{:,.0f} {}'.format(float(mf.value), mf.currency)
    return formatted


def _format_layer_terms(layer):
    """Get the terms for the given layer for display in Graphviz"""
    warning = False
    terms = ''
    if hasattr(layer, 'inception_date') or hasattr(layer, 'expiry_date'):
        coverage = []
        coverage.append('{}'.format(_format_DateField(layer.inception_date))
                        if hasattr(layer, 'inception_date') else '-inf')
        coverage.append('{}'.format(_format_DateField(layer.expiry_date))
                        if hasattr(layer, 'expiry_date') else
                        'inf')
        terms += '\ncoverage=[{}]'.format(', '.join(coverage))

    # FilterLayer
    if hasattr(layer, 'filters'):
        terms += '\nfilters='
        if len(layer.filters) == 0:
            terms += '(empty)'
        elif len(layer.filters) < 4:
            filter_strings = []
            for f in layer.filters:
                filter_strings.append("'{}'".format(f.name))
            terms += '[{}]'.format(', '.join(filter_strings))
        else:
            terms += '({} filters)'.format(len(layer.filters))

    if hasattr(layer, 'invert'):
        terms += '\ninvert={}'.format(layer.invert)
        if not layer.invert and len(layer.filters) == 0:
            warning = True

    if hasattr(layer, 'participation'):
        terms += '\nshare={}%'.format(layer.participation*100)
        if layer.participation == 0.0:
            warning = True

    # CatXL, AggXL, Generic
    if hasattr(layer, 'attachment'):
        terms += '\nocc_att={}'.format(
            _format_MoneyField(layer.attachment))
        warning = warning or layer.attachment.value >= float_info.max

    if hasattr(layer, 'limit'):
        terms += '\nocc_lim={}'.format(
            _format_MoneyField(layer.limit))
    if hasattr(layer, 'reinstatements') and len(layer.reinstatements) > 0:
        num_reinstatements = len(layer.reinstatements)
        terms += '\nreinsts='
        if num_reinstatements > 4:
            terms += '{}'.format(num_reinstatements)
        else:
            reinstatements = []
            for r in layer.reinstatements:
                reinstatements.append('{}/{}'.format(r.premium, r.brokerage))
            terms += '[{}]'.format(', '.join(reinstatements))

    # QuotaShare, AggregateQuotaShare
    if hasattr(layer, 'event_limit') and layer.event_limit is not None:
        terms += '\nevent_lim={}'.format(
            _format_MoneyField(layer.event_limit))

    # AggXL, AggregateQuotaShare
    if hasattr(layer, 'aggregate_attachment'):
        terms += '\nagg_att={}'.format(
            _format_MoneyField(layer.aggregate_attachment))
        warning = warning or layer.aggregate_attachment.value >= float_info.max
    if hasattr(layer, 'aggregate_limit'):
        terms += '\nagg_lim={}'.format(
            _format_MoneyField(layer.aggregate_limit))

    # AggregateQuotaShare
    if hasattr(layer, 'aggregate_period'):
        if layer.aggregate_period > 0.0:
            terms += '\nagg_period={}'.format(layer.aggregate_period)
    if hasattr(layer, 'aggregate_reset'):
        if layer.aggregate_reset > 1:
            terms += '\nagg_reset={}'.format(layer.aggregate_reset)

    # SurplusShare
    if hasattr(layer, 'sums_insured'):
        terms += '\nsums_insured={}'.format(
            _format_MoneyField(layer.sums_insured))
    if hasattr(layer, 'retained_line'):
        terms += '\nretained_line={}'.format(
            _format_MoneyField(layer.retained_line))
    if hasattr(layer, 'number_of_lines'):
        if layer.number_of_lines:
            terms += '\nnumber_of_lines={}'.format(layer.number_of_lines)

    # IndustryLossWarranty
    if hasattr(layer, 'trigger'):
        terms += '\ntrigger={}'.format(
            _format_MoneyField(layer.trigger))
    if hasattr(layer, 'payout'):
        terms += '\npayout={}'.format(
            _format_MoneyField(layer.payout))

    # CatXL, IndustryLossWarranty
    if hasattr(layer, 'nth'):
        terms += '\nnth={}'.format(layer.nth)

    # NoClaimsBonus
    if hasattr(layer, 'payout_date'):
        terms += '\npayout_date={}'.format(
            _format_DateField(layer.payout_date))
    if hasattr(layer, 'payout_amount'):
        terms += '\npayout={}'.format(
            _format_MoneyField(layer.payout_amount))

    if hasattr(layer, 'premium') and layer.premium is not None:
        terms += '\npremium={}'.format(
            _format_MoneyField(layer.premium))

    return terms, warning


class LayerViewDigraph(object):
    """Class that provides simple visualization of Analyze Re LayerViews.

    Using the 'graphviz' python package, this class enables users to
    visualize Analyze Re LayerView objects.
    """
    def _update_filename(self, filename=None):
        # build filename with format:
        #    '<lv_id>_<rankdir>+<verbose><_with_terms>.<format>'
        self._filename = (filename if filename else
                          '{}_{}{}{}'.format(self._lv.id,
                                             self._rankdir,
                                             '_verbose' if self._verbose
                                             else '',
                                             '_with_terms' if self._with_terms
                                             else ''))

    def _generate_nodes(self, l, sequence, unique_nodes, edges,
                        parent_hash=None, prefix=None):
        # hash the current node to see if it is unique
        node_hash = hashlib.md5((str(l)
                                 + (parent_hash or ''))
                                .encode('utf-8')).hexdigest()

        if (node_hash not in unique_nodes) or self._verbose:
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
            if warning:
                self._graph.attr('node', color='red',
                                 fillcolor='red')

            self._graph.node(node_hash, label=name)
            for ls in l.loss_sets:
                ls_name = '{} "{}" {}'.format(
                    ls.type,
                    _format_description(ls.description),
                    '({})'.format(next(sequence)) if self._verbose else '')
                if not (ls_name, node_hash) in edges:
                    self._graph.attr('node',
                                     shape='box', color='lightgrey',
                                     style='filled', fillcolor='lightgrey')
                    self._graph.node(ls.id, label=ls_name)
                    self._graph.edge(ls.id, node_hash)
                    edges.add((ls.id, node_hash))
        return node_hash

    def __init__(self, lv, with_terms=True, verbose=False,
                 format='png', rankdir='BT'):
        """Generate a Graphviz.Digraph for the given LayerView

        Optional parameters that control the visualization:

           with_terms   specify that Layer terms are included in each
                        node of the graph.

           verbose      controls if duplicate nodes should be omitted

           format       exposes the graphviz 'format' option which include
                        'pdf', 'png', etc.

           rankdir      exposes the graphviz 'rankdir' option that controls
                        the orientation of the graph.  Options include
                        'TB', 'LR', 'BT', 'RL', corresponding to directed
                        graphs drawn from top to bottom, from left to right,
                        from bottom to top, and from right to left,
                        respectively.
        """
        # sanity check on the input
        if not isinstance(lv, LayerView):
            raise ValueError('must supply a valid LayerView instance')

        self._lv = lv
        self._with_terms = with_terms
        self._rankdir = rankdir
        self._format = format
        self._verbose = verbose

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
    def fromId(lv_id, with_terms=True, verbose=False,
               format='png', rankdir='BT'):
        """Generate a LayerViewDigraph for the given LayerView Id

        Optional parameters:

           with_terms   specify that Layer terms are included in each
                        node of the graph.

           verbose      controls if duplicate nodes should be omitted

           format       exposes the graphviz 'format' option which include
                        'pdf', 'png', etc.

           rankdir      exposes the graphviz 'rankdir' option that controls
                        the orientation of the graph.  Options include
                        'TB', 'LR', 'BT', 'RL', corresponding to directed
                        graphs drawn from top to bottom, from left to right,
                        from bottom to top, and from right to left,
                        respectively.
        """
        # This raise and exception if any of the following analyzere variables
        # are not defined:
        #       - analyzere.base_url
        #       - analyzere.username
        #       - analyzere.password
        return LayerViewDigraph(LayerView.retrieve(lv_id), with_terms, verbose,
                                format=format, rankdir=rankdir)

    def render(self, filename=None, view=True, format=None, rankdir=None):
        """Render a LayerViewDigraph with the Graphviz engine

        Optional parameters:

           filename     specify the filename to be used when rendering.

           view         exposes the graphviz 'view' option that uses the
                        default application to open the rendered graph.

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
            # iff we arein a python notebook, otherwise return the filename.
            return (FileLink(self._graph.render(self._filename, view=False))
                    if _in_notebook else
                    self._graph.render(self._filename, view=False))
