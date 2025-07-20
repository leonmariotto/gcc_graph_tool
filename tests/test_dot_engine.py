from scripts.DotEngine import DotEngine


def test_dot_engine():
    dot_engine = DotEngine("resources/dots/list_test.c.callgraph.dot")
    dot_engine.modify_nodes_label()
