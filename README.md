# GCC Graphs Tools

## uv

Run the following command to install dependency.
```'(shell)
uv sync
```

Run the following command to test.
```
uv run ./gcc_graph_tool.py -y yml/callgraph.yml -i resources/nm.wpa.000i.cgraph -o test.svg
```

## Note for github pages

In Settings->Actions->General activate "Read and write permissions" for workflow. </br>
Also in Settings->Pages set the deployment from "gh-pages" "/(root)". </br>
Site is here: https://leonmariotto.github.io/gcc_graph_tool/ </br>
