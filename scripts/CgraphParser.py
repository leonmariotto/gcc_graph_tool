"""
Module CgraphParser
Used to parse GCC IPA wpa .cgraph file outputed with -flto and -fdump-ipa-cgraph
The .wpa.*.cgraph file contain Whole Program Analysis of I
There is no official spec for this format.

The file include a list of symbols with some informations for each. The list of symbols
start with the string "Symbol table:" and an empty line.
The list terminate when a line start with "Writing partition ".

Here is a sample of a single symbol entry :

nm_bin_parse_syms/484 (nm_bin_parse_syms)
  Type: function definition analyzed
  Visibility: externally_visible semantic_interposition prevailing_def_ironly public
  References:
  Referring:
  Read from file: build/obj/nm_bin_parse.o
  Availability: available
  Unit id: 4
  Function flags: count:1073741824 (estimated locally)
  Called by: nm_bin_parse/120 (275991376 (estimated locally),0.26 per call)
  Calls: nm_bin_parse_syms64/481 (348169376 (estimated locally),0.32 per call) nm_bin_parse_syms32/482 (179359984 (estimated locally),0.17 per call) nm_bin_get_sym_sections/483 (1055058721 (estimated locally),0.98 per call)

I should be able to create a list of SymbolInfo.
The calls and called_by lists contains a hash of entry.
hash is obtained using sha256 on symbol name.
"""

import logging
import re
from typing import List
from pydantic import BaseModel
import hashlib
from .DotEngine import DotEngine
from .DotConfig import DotConfig

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


class CgraphParserError(Exception):
    """ """


class SymbolInfo(BaseModel):
    """Extracted info entry"""

    s_name: str
    s_type: str
    s_visibility: str
    s_references: str
    s_refering: str
    s_from_file: str
    s_availability: str
    s_unit_id: int
    s_function_flags: str
    s_called_by: List[bytes]
    s_calls: List[bytes]
    s_calls_name: List[str]


class CgraphParser:
    """ """

    def __init__(self, input_file: str):
        """ """
        self.logger = logging.getLogger(__name__)
        self.symbol_table: dict[bytes, SymbolInfo] = {}
        self.sym_info = {}
        self.reset_sym_info()
        self.parse_syms(input_file)
        self.logger.setLevel(logging.INFO)

    @staticmethod
    def make_hash(name: str) -> bytes:
        return hashlib.sha256(name.encode()).digest()

    def reset_sym_info(self):
        self.sym_info = {
            "s_name": "",
            "s_type": "",
            "s_visibility": "",
            "s_references": "",
            "s_refering": "",
            "s_from_file": "",
            "s_availability": "",
            "s_unit_id": 0,
            "s_function_flags": "",
            "s_called_by": [],
            "s_calls": [],
            "s_calls_name": [],
        }

    def parse_sym_calls(self, line: str):
        """Parse Calls line"""
        # Calls: nm_bin_parse_syms64/481 (348169376 (estimated locally),0.32 per call) nm_bin_parse_syms32/482 (179359984 (estimated locally),0.17 per call) nm_bin_get_sym_sections/483 (1055058721 (estimated locally),0.98 per call)
        all_words = re.findall(r"(\w+)/\d+ \([^)]+\)", line)
        words = list(dict.fromkeys(all_words))
        for word in words:
            self.sym_info["s_calls"] += [CgraphParser.make_hash(word)]
            self.sym_info["s_calls_name"] += [word]

    def parse_syms(self, input_file: str):
        """
        Iterate over the symbols list.
        """
        with open(input_file, "r") as f:
            for line in f:
                # self.logger.debug("line=[%s]", line)
                if line == "Symbol table:\n":
                    next(f)
                    break
            i = 0
            in_entry = False
            for line in f:
                if in_entry is True:
                    if line[:2] != "  ":
                        self.symbol_table[
                            CgraphParser.make_hash(self.sym_info["s_name"])
                        ] = SymbolInfo(**self.sym_info)
                        # self.logger.debug("Registered new symbol name=%s", self.sym_info["s_name"])
                        self.reset_sym_info()
                        in_entry = False
                        i += 1
                    else:
                        if "  Calls: " in line:
                            self.parse_sym_calls(line)
                        continue
                if "Writing partition " in line:
                    self.logger.debug("End parsing symbol list, found %d entries.", i)
                    break
                else:
                    in_entry = True
                    match = re.search(r".*\(([\w\._]+)\)", line)
                    if match is None:
                        self.logger.error("ERROR searching symbol name line=[%s]", line)
                        raise CgraphParserError()
                    self.sym_info["s_name"] = match.group(1)

    def create_node(self, sym: SymbolInfo, dot_engine: DotEngine):
        dot_engine.create_and_add_node(sym.s_name, label=sym.s_name)
        for callee_hash, callee_name in zip(sym.s_calls, sym.s_calls_name):
            try:
                callee_sym = self.symbol_table[callee_hash]
            except KeyError:
                self.logger.error("Error hash not found! callee_name=%s", callee_name)
                continue
            self.create_node(callee_sym, dot_engine)
            dot_engine.create_and_connect_edge(
                sym.s_name,
                self.symbol_table[callee_hash].s_name,
            )

    def create_callgraph(self, dot_config: DotConfig, output_file: str):
        """ """
        dot_engine = DotEngine()
        dot_engine.create_dot()
        main_sym = self.symbol_table[CgraphParser.make_hash("main")]
        self.create_node(main_sym, dot_engine)
        dot_engine.modify_attributes(dot_config)
        dot_engine.write_svg(output_file)
