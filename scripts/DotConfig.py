"""
Module DotConfig
"""

import logging
from pydantic import BaseModel

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


class GlobalConfig(BaseModel):
    rankdir: str
    bgcolor: str
    fontname: str
    fontsize: int
    splines: bool


class NodeConfig(BaseModel):
    shape: str
    style: str
    color: str
    fillcolor: str
    fontcolor: str
    fontname: str
    fontsize: int


class EdgeConfig(BaseModel):
    color: str
    arrowhead: str
    style: str
    arrowsize: str
    fontname: str
    fontsize: str
    fontcolor: str


class DotConfig(BaseModel):
    title: "str"
    global_conf: GlobalConfig
    node: NodeConfig
    edge: EdgeConfig
    layout_engine: str
