import hashlib

from analyzere import LayerView
from datetime import datetime
from graphviz import Digraph
try:
    from IPython.display import FileLink
    in_notebook = True
except ImportError:
    in_notebook = False

from sys import float_info


def _counter():
    """Simple counter for generating unique indexes in a graph"""
    i = 0
    while True:
        i += 1
        yield i


class LayerViewVisualizer(object):
    """Class that provides simple visualization of Analyze Re LayerViews.

    Using the 'graphviz' python package, this class enables users to
    visualize Analyze Re LayerView objects.
    """
    def __init__(self):
        # sequencer for identifying 'ambiguous' nodes
        self._sequence = _counter()
        # hash map of unique nodes (prevents duplication)
        self._unique_nodes = {}
        # set of unique edges (prevents duplicates)
        self._edges = set()
        # defaults for the Digraph, overridden by plot()
        self._graph = Digraph(format='pdf',
                              graph_attr={'rankdir': 'BT',
                                          'size': '120,120'})
        self._filename = ''

    def _format_description(self, description):
        """Clean the description of a node for diaply in Graphviz"""
        cleaned = (description.replace(':\\', '|')
                   .replace(':', ' ')
                   .replace('\'', ''))
        return cleaned.encode('unicode_escape')

    def _format_DateField(self, df):
        """Format a Date field, chopping off the time portion"""
        parsed = datetime.utcfromtimestamp(df.timestamp())
        return parsed.strftime('%Y-%m-%d')

    def _format_MoneyField(self, mf):
        """Format a MoneyField to '<unlimited|value> CCY' """
        formatted = 'n/a'
        if mf.value == float_info.max:
            formatted = 'unlimited'
        else:
            formatted = '{:,.0f} {}'.format(float(mf.value), mf.currency)
        return formatted

    def _format_layer_terms(self, layer):
        """Get the terms for the given layer for display in Graphviz"""
        terms = ''
        if hasattr(layer, 'inception_date'):
            terms += '\n[{}'.format(
                self._format_DateField(layer.inception_date))
        else:
            terms += '\n[-inf'
        if hasattr(layer, 'expiry_date'):
            terms += ', {}]'.format(
                self._format_DateField(layer.expiry_date))
        else:
            terms += ', inf]'

        # CatXL, AggXL, Generic
        if hasattr(layer, 'attachment'):
            terms += '\natt={}'.format(
                self._format_MoneyField(layer.attachment))
        if hasattr(layer, 'limit'):
            terms += '\nlim={}'.format(
                self._format_MoneyField(layer.limit))

        # QuotaShare, AggregateQuotaShare
        if hasattr(layer, 'event_limit'):
            terms += '\nevent_lim={}'.format(
                self._format_MoneyField(layer.event_limit))

        # AggXL, AggregateQuotaShare
        if hasattr(layer, 'aggregate_attachment'):
            terms += '\nagg_att={}'.format(
                self._format_MoneyField(layer.aggregate_attachment))
        if hasattr(layer, 'aggregate_limit'):
            terms += '\nagg_lim={}'.format(
                self._format_MoneyField(layer.aggregate_limit))

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
                self._format_MoneyField(layer.sums_insured))
        if hasattr(layer, 'retained_line'):
            terms += '\nretained_line={}'.format(
                self._format_MoneyField(layer.retained_line))
        if hasattr(layer, 'number_of_lines'):
            if layer.number_of_lines:
                terms += '\nnumber_of_lines={}'.format(layer.number_of_lines)

        # IndustryLossWarranty
        if hasattr(layer, 'trigger'):
            terms += '\ntrigger={}'.format(
                self._format_MoneyField(layer.trigger))
        if hasattr(layer, 'payout'):
            terms += '\npayout={}'.format(
                self._format_MoneyField(layer.payout))

        # CatXL, IndustryLossWarranty
        if hasattr(layer, 'nth'):
            terms += '\nnth={}'.format(layer.nth)

        # NoClaimsBonus
        if hasattr(layer, 'payout_date'):
            terms += '\npayout_date={}'.format(
                self._format_DateField(layer.payout_date))
        if hasattr(layer, 'payout_amount'):
            terms += '\npayout={}'.format(
                self._format_MoneyField(layer.payout_amount))

        return terms

    def _get_tree(self, l, include_terms):

        if l.type == 'NestedLayer':
            # hash the current node to see if it is unique
            node_hash = hashlib.md5(str(l).encode('utf-8')).hexdigest()
            if node_hash not in self._unique_nodes:
                self._unique_nodes[node_hash] = next(self._sequence)

            terms = self._format_layer_terms(l.sink) if include_terms else ''
            name = ('Nested {} {}'.format(
                    l.sink.type, self._format_description(l.description))
                    if l.description else
                    'Nested {} {}'.format(
                    l.sink.type, self._format_description(l.sink.description))
                    if l.sink.description else
                    'Nested {} ({}) {}'
                    .format(l.sink.type, self._unique_nodes[node_hash],
                            terms))
            for source in [self._get_tree(s, include_terms)
                           for s in l.sources]:
                if not (source, name) in self._edges:
                    self._graph.attr('node', shape='ellipse',
                                     style='filled', fillcolor='white',
                                     color='black')
                    self._graph.node(name)
                    self._graph.edge(source, name)
                    self._edges.add((source, name))
        else:
            terms = self._format_layer_terms(l) if include_terms else ''
            name = ('{}'.format(self._format_description(l.description))
                    if l.description else
                    '{} ({}) {}'.format(l.type, next(self._sequence), terms))
            if l.type == 'FilterLayer':
                self._graph.attr('node', shape='cds')
                name += '  '
            self._graph.node(name)
            for ls in l.loss_sets:
                ls_name = 'LossSet {}'.format(
                    self._format_description(ls.description),
                    next(self._sequence))
                if not (ls_name, name) in self._edges:
                    self._graph.attr('node',
                                     shape='box',
                                     style='filled',
                                     color='lightgrey')
                    self._graph.node(ls_name)
                    self._graph.edge(ls_name, name)
                    self._edges.add((ls_name, name))
        return name

    def _generate(self, lv_id, with_terms=True, fmt='pdf',
                  rankdir='BT', filename=None):

        # reset the internals for regeneration
        self._sequence = _counter()
        self._unique_nodes.clear()
        self._edges.clear()

        # get the LayerView by id
        lv = LayerView.retrieve(lv_id)

        # use the given filename or build filename with format
        #    '<lv_id><-with_terms>-<rankdir>.<fmt>'
        self._filename = filename if filename else '{}{}-{}'.format(
            lv.id, '-with_terms' if with_terms else '', rankdir)

        self._graph.graph_attr['rankdir'] = rankdir

        # potentially update the format
        self._graph.format = fmt

        # now build the "tree" of nodes
        self._get_tree(lv.layer, with_terms)

    def render(self, lv_id, with_terms=True, fmt='png',
               rankdir='BT', view=False, filename=None):
        """View the generated graph

        Optional parameters that control the formatting of the graph:

           with_terms   specify if the Layer terms should be included in each
                        node of the graph

           fmt          exposes the graphvis 'format' options which include
                        'pdf', 'png', etc.

           rankdir      exposes graphvis 'rankdir' option that controls the
                        orientation of the graph.  Options include
                        'TB', 'LR', 'BT', 'RL', corresponding to directed
                        graphs drawn from top to bottom, from left to right,
                        from bottom to top, and from right to left,
                        respectively.

           view         use the default rendering application to immediately
                        display the graph.

           filename     specify the filename to be used when rendering.
        """
        self._generate(lv_id, with_terms, fmt, rankdir, filename)

        try:
            # protect against use cases when the default rendering tool
            # is not able to render the result
            # if we are in a python notebook we will use the FileLink feature
            # to return a click-able link to download the file
            return (FileLink(self._graph.render(self._filename, view=view))
                    if in_notebook else
                    self._graph.render(self._filename, view=view))

        except RuntimeError:
            # if native rendering failed, revert to returning the filename
            # if we are in a python notebook we will use the FileLink feature
            # to return a click-able link to download the file
            return (FileLink(self._graph.render(self._filename, view=False))
                    if in_notebook else
                    self._graph.render(self._filename, view=False))
