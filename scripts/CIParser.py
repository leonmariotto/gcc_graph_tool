"""
Module CIParser
Used to parse .ci file. CI stand for "compiler internal", probably.
There is no official spec for this format. It is based on VCG (now obsolete).
"""

# !!!! WARNING !!!!
# This code is unused, .ci file are not the great way to get usefull stuff from GCC.
# There is better way (GCC's .dot, to get stack usage we can parse .su file)

import logging
import re
from typing import List
from pydantic import BaseModel

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


class CIEdgeInfo(BaseModel):
    """Extracted info from label"""

    filepath: str
    line: int
    column: int


class CINodeInfo(BaseModel):
    """Extracted info from label"""

    filepath: str
    line: int
    column: int
    stack_usage: int
    heap_usage: int


class CINode(BaseModel):
    title: str
    label: str


class CIEdge(BaseModel):
    sourcename: str
    targetname: str
    label: str


class CIGraph(BaseModel):
    title: str
    nodes: List[CINode]
    edges: List[CIEdge]


class CIParserError(Exception):
    """ """


class CIParser:
    """
    Class used to parse CI file.
    """

    def __init__(self, input_file: str):
        """
        Init
        """
        self.logger = logging.getLogger(__name__)
        with open(input_file, "r") as f:
            self.input = f.read()
        self.parse_graph()

    @staticmethod
    def select_function_name(s: str) -> str:
        if s.count(":") == 1:
            left, right = s.split(":", 1)
            return right
        return s

    def parse_graph(self):
        match = re.search(r'graph:\s+{\s+title:\s+"((?:[\w\-.+/]+)+)"', self.input)
        if match is None:
            raise CIParserError()
        graph_title = match.group(1)
        i = 0
        nodes_list = []
        edges_list = []
        for line in self.input.splitlines()[1:]:
            if line == "}":
                break
            elif line[0:4] == "edge":
                # edge: { sourcename: "myputstr" targetname: "strlen" label: "src/simple_test.c:11:21" }
                match = re.search(
                    r'edge:\s+{\s+sourcename:\s*"([^"]+)"\s+targetname:\s*"([^"]+)"(?:\s+label:\s*"([^"]+)")?',
                    # r'edge:\s+{\s+sourcename:\s"((?:[\w\-.+/:]+)+)"\s+targetname:\s+"(\w+)"\s+label:\s+"((?:[\w\-.+/:]+)+)"',
                    line,
                )
                if match is None:
                    raise CIParserError()
                if match.group(3) is None:
                    label = ""
                else:
                    label = match.group(3)
                edges_list += [
                    {
                        "sourcename": CIParser.select_function_name(match.group(1)),
                        "targetname": CIParser.select_function_name(match.group(2)),
                        "label": label,
                    }
                ]
                self.logger.debug(
                    f"Found edge at index={i} sourcename={match.group(1)} targetname={match.group(2)}"
                )
            elif line[0:4] == "node":
                # node: { title: "write" label: "write\n/usr/include/unistd.h:378:16" shape : ellipse }
                match = re.search(
                    # r'node:\s+{\s+title:\s"(\w+)"\s+label:\s+"((?:[\w\-.+/:|]+)+)"\s+shape\s+:\s+(\w+)',
                    r'node:\s+{\s+title:\s"((?:[\w\-.+/:]+)+)"\s+label:\s+"(.+)"',
                    line,
                )
                if match is None:
                    raise CIParserError()
                nodes_list += [
                    {
                        "title": CIParser.select_function_name(match.group(1)),
                        "label": match.group(2),
                    }
                ]
                self.logger.debug(f"Found node at index={i} title={match.group(1)}")
            else:
                self.logger.error("Unknow line! index={i} line=[{line}]")
                raise CIParserError()
            i += 1
        self.logger.debug("Parsing done, transfom to pydantic class")
        self.ci_graph = CIGraph(
            **{
                "title": graph_title,
                "nodes": nodes_list,
                "edges": edges_list,
            }
        )
