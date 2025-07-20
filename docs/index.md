# Overview

This tool is intended to parse gcc graph production. 
This include exploded graph, callgraph and supergraph.
The tool parse it and produce output according to a yaml configuration.

Usage :
```
uv run ./gcc_graph_tool.py -y yml/callgraph.yml [FILES]
```
