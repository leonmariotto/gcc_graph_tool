"""Module DotEngine"""

import logging
import re
from .DotConfig import DotConfig
import pydot

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


class DotEngineError(Exception):
    """ """


class DotEngine:
    """
    Class used to manipulate dot file.
    """

    def __init__(self, input_file: str):
        """
        Init DotEngine
        """
        self.logger = logging.getLogger(__name__)
        pydot_graphs = pydot.graph_from_dot_file(input_file)
        self.pydot_graph = pydot_graphs[0]

    def modify_nodes_label(self):
        for node in self.pydot_graph.get_nodes():
            label = node.get_label()
            match = re.search(r"VCG:\\\s*\d+:\\\s*([_a-zA-Z0-9]+)", label)
            if match is None:
                raise DotEngineError()
            node.set_label(match.group(1).strip())

    def modify_attributes(self, dot_config: DotConfig):
        """
        Modify attributes.
        """
        # Modify graph attributes
        self.pydot_graph.set_bgcolor(dot_config.global_conf.bgcolor)
        self.pydot_graph.set_rankdir(dot_config.global_conf.rankdir)

        # Modify node attributes
        for node in self.pydot_graph.get_nodes():
            node.set_fontname(dot_config.node.fontname)
            node.set_style(dot_config.node.style)
            node.set_fillcolor(dot_config.node.fillcolor)
            node.set_color(dot_config.node.color)
            node.set_fontcolor(dot_config.node.fontcolor)

        # Modify edge attributes
        for edge in self.pydot_graph.get_edges():
            edge.set_color(dot_config.edge.color)
            edge.set_fontname(dot_config.edge.fontname)
            edge.set_fontsize(dot_config.edge.fontsize)
            edge.set_arrowhead(dot_config.edge.arrowhead)

    def write_svg(self, output_path: str):
        """
        Write the content of graph into a SVG file.
        """
        self.pydot_graph.write_svg(output_path)
