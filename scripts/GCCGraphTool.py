"""Module GCCGraphTool"""

import logging
import click
from typing import List
from .DotConfig import DotConfig
from .YamlParser import YamlParser
from .DotEngine import DotEngine


@click.command()
@click.option(
    "--yamls",
    "-y",
    default=[],
    multiple=True,
    type=str,
    help="Yaml configuration, can be done multiple time",
)
@click.option(
    "--input_file",
    "-i",
    type=str,
    show_default=True,
    help="Input file",
)
@click.option(
    "--output_file",
    "-o",
    type=str,
    show_default=True,
    help="Output file",
)
def gcc_graph_tool(
    yamls: List[str],
    input_file: str,
    output_file: str,
):
    """
    A tool to concate a lot of image
    """
    yaml_parser = YamlParser()
    for y in yamls:
        logging.debug("Loading yml {%s}", y)
        yaml_parser.parse(y)
    dot_config = DotConfig(**yaml_parser.data)
    dot_engine = DotEngine(input_file)
    dot_engine.modify_attributes(dot_config)
    dot_engine.modify_nodes_label()
    dot_engine.write_svg(output_file)
