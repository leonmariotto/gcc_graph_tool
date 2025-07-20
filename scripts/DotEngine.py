"""Module DotEngine"""

import logging
import re
from .DotConfig import DotConfig
from .CIParser import CIGraph
import pydot
from graphviz import Digraph

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
                print(label)
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

    def create_svg_from_ci_graph(
        self, dot_config: DotConfig, ci_graph: CIGraph, output_path: str
    ):
        """
        Use CIGraph infos to build dot file and export it to svg.
        """
        dot = Digraph(name=dot_config.title, format="svg")

        # === Global attributes ===
        dot.attr(rankdir=dot_config.global_conf.rankdir)
        dot.attr(bgcolor=dot_config.global_conf.bgcolor)

        # === Default node attributes ===
        dot.attr(
            "node",
            # shape=dot_config.node.shape,
            style=dot_config.node.style,
            color=dot_config.node.color,
            fillcolor=dot_config.node.fillcolor,
            fontname=dot_config.node.fontname,
            fontcolor=dot_config.node.fontcolor,
        )
        dot.attr(
            "edge",
            color=dot_config.edge.color,
            arrowhead=dot_config.edge.arrowhead,
            arrowsize=dot_config.edge.arrowsize,
            fontname=dot_config.edge.fontname,
            fontsize=dot_config.edge.fontsize,
        )
        self.logger.debug("Create SVG from CI graph.")

        i = 0
        for node in ci_graph.nodes:
            dot.node(node.title, label=node.label)
            i += 1
        self.logger.debug(f"Added {i} node to graph !")
        i = 0
        for edge in ci_graph.edges:
            dot.edge(edge.sourcename, edge.targetname, label=edge.label)
            i += 1
        self.logger.debug(f"Added {i} edges to graph !")

        # === Render to SVG file ===
        dot.render(outfile=output_path, cleanup=True)
        self.logger.debug(f"Render to svg ({output_path})")

        return dot
