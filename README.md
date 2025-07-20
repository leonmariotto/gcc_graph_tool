# GCC Graphs Tools

A ENTRY symbol should be specified, so only called function from this entry will be displayed
in the output graph.
TODO:
    - rename datastore to dotconfig
    - can use the feature of dot-file modification (from fanalyzer-callgraph dot file) and
        the feature of dot file generation from .ci file (compiler internal from -fdump-graph)

## uv

Use uv for dependency management:
Run the following command to install dependency.
```'(shell)
uv sync
```

```
uv run ./gcc_graph_tool.py -y yml/callgraph.yml  -i resources/dots/list_test.c.callgraph.dot  -o test.svg
```

## Note for github actions

Every yml files in .github/workflows generate an action.
In Settings->Actions->General activate "Read and write permissions" for workflow.
Also in Settings->Pages set the deployment from "gh-pages" "/(root)".
Site is here: https://leonmariotto.github.io/img_process/
