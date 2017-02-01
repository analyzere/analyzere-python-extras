import hashlib

from analyzere import LayerView
from graphviz import Digraph
try:
    from IPython.display import FileLink
    _in_notebook = True
except ImportError:
    _in_notebook = False

from sys import float_info


def _counter():
    """Simple counter for generating unique indexes in a graph"""
    i = 0
    while True:
        i += 1
        yield i


def _format_description(description):
    """Clean the description of a node for diaply in Graphviz"""
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
    terms = ''
    if hasattr(layer, 'inception_date'):
        terms += '\n[{}'.format(
            _format_DateField(layer.inception_date))
    else:
        terms += '\n[-inf'
    if hasattr(layer, 'expiry_date'):
        terms += ', {}]'.format(
            _format_DateField(layer.expiry_date))
    else:
        terms += ', inf]'

    # FilterLayer
    if hasattr(layer, 'filters') and len(layer.filters) > 0:
        terms += '\nfilter={}'.format(layer.filters[0].name)

    # CatXL, AggXL, Generic
    if hasattr(layer, 'attachment'):
        terms += '\natt={}'.format(
            _format_MoneyField(layer.attachment))
    if hasattr(layer, 'limit'):
        terms += '\nlim={}'.format(
            _format_MoneyField(layer.limit))

    # QuotaShare, AggregateQuotaShare
    if hasattr(layer, 'event_limit'):
        terms += '\nevent_lim={}'.format(
            _format_MoneyField(layer.event_limit))

    # AggXL, AggregateQuotaShare
    if hasattr(layer, 'aggregate_attachment'):
        terms += '\nagg_att={}'.format(
            _format_MoneyField(layer.aggregate_attachment))
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

    return terms


class LayerViewDigraph(object):
    """Class that provides simple visualization of Analyze Re LayerViews.

    Using the 'graphviz' python package, this class enables users to
    visualize Analyze Re LayerView objects.
    """
    def _generate_nodes(self, l, sequence, unique_nodes, edges):
        if l.type == 'NestedLayer':
            # hash the current node to see if it is unique
            node_hash = hashlib.md5(str(l).encode('utf-8')).hexdigest()
            if node_hash not in unique_nodes:
                unique_nodes[node_hash] = next(sequence)

            terms = _format_layer_terms(l.sink) if self._with_terms else ''
            name = ('Nested {} {}'.format(
                    l.sink.type, _format_description(l.description))
                    if l.description else
                    'Nested {} {}'.format(
                    l.sink.type, _format_description(l.sink.description))
                    if l.sink.description else
                    'Nested {} ({}) {}'
                    .format(l.sink.type, unique_nodes[node_hash],
                            terms))
            for source in [self._generate_nodes(s, sequence,
                                                unique_nodes, edges)
                           for s in l.sources]:
                if not (source, node_hash) in edges:
                    self._graph.attr('node', shape='box',
                                     style='filled',
                                     fillcolor='white',
                                     color='black')
                    self._graph.node(node_hash, label=name)
                    self._graph.edge(source, node_hash)
                    edges.add((source, node_hash))
        else:
            terms = _format_layer_terms(l) if self._with_terms else ''
            node_hash = hashlib.md5(str(l).encode('utf-8')).hexdigest()
            name = ('{}'.format(_format_description(l.description))
                    if l.description else
                    '{} ({}) {}'.format(l.type, next(sequence), terms))
            if l.type == 'FilterLayer':
                self._graph.attr('node', shape='cds')
                name += '  '
            self._graph.node(node_hash, label=name)
            for ls in l.loss_sets:
                ls_name = 'LossSet {} {}'.format(
                    _format_description(ls.description),
                    '({})'.format(next(sequence)) if self._verbose else '')
                if not (ls_name, node_hash) in edges:
                    self._graph.attr('node',
                                     shape='box', color='lightgrey',
                                     style='filled', fillcolor='lightgrey')
                    self._graph.node(ls_name)
                    self._graph.edge(ls_name, node_hash)
                    edges.add((ls_name, node_hash))
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

        # build filename with format:
        #    '<lv_id><-with_terms>-<rankdir>.<format>'
        self._filename = '{}{}-{}'.format(
            lv.id, '-with_terms' if with_terms else '', rankdir)

        # defaults for the Digraph, overridden by plot()
        self._graph = Digraph(format=format,
                              graph_attr={'rankdir': rankdir,
                                          'size': '400,400'})
        # now build the "tree" of nodes
        # sequencer for identifying 'ambiguous' nodes
        sequence = _counter()
        # hash map of unique nodes (prevents duplication)
        unique_nodes = {}
        # set of unique edges (prevents duplicates)
        edges = set()

        self._generate_nodes(lv.layer, sequence, unique_nodes, edges)

    @staticmethod
    def fromId(lv_id, with_terms=True, format='png', rankdir='BT'):
        """Generate a LayerViewDigraph for the given LayerView Id

        Optional parameters:

           with_terms   specify that Layer terms are included in each
                        node of the graph.

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
        return LayerViewDigraph(LayerView.retrieve(lv_id), with_terms,
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
        if format:
            self._graph.format = format
        self._filename = filename if filename else '{}{}-{}'.format(
            self._lv.id, '-with_terms' if self._with_terms else '',
            rankdir if rankdir else self._rankdir)

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
