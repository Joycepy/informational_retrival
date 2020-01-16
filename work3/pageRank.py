import json
# 用于构建和操作复杂的图结构，提供分析图的算法
import networkx as nx

with open('PRInfo/pageGraph.json', 'r', encoding='UTF-8') as f:
    pagegraph = json.load(f)
f.close()


def wf(path, obj):
    file = open(path, 'w', encoding='utf-8')
    file.write(json.dumps(obj, sort_keys=True, indent=4))
    file.close()


# 初始化图
def init_graph():
    graph = nx.DiGraph()  # 初始化一个空的图
    anchor = {}
    for t in pagegraph:
        graph.add_edge(t[0], t[1])
        # 记录锚文本及其对应的链接
        an = t[2]
        if an in anchor:
            anchor[an].append(t[1])
        else:
            anchor[an] = [t[1]]
    wf('PRInfo/anchor.json', anchor)
    return graph


def cal_pr():
    G = init_graph()
    pr = nx.pagerank(G, alpha=0.85)  # 计算pr
    result = {}
    for node, value in pr.items():
        result[node] = value
    print(result)
    wf('PRInfo/pageRank.json', result)


if __name__ == "__main__":
    cal_pr()
