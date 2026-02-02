# 实现图的数据结构， 属性有点，边，距离等信息

class Graph:
    def __init__(self):
        self.nodes = set()  # 点的集合
        self.edges = {}     # 边的字典，键是点，值是相邻点的列表
        self.distances = {} # 距离的字典，键是点对，值是距离

    def add_node(self, value):
        self.nodes.add(value)
        self.edges[value] = []

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)  # 无向图
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance  # 无向图

    def get_neighbors(self, node):
        return self.edges[node]

    def get_distance(self, from_node, to_node):
        return self.distances.get((from_node, to_node), float('inf'))


# 写一个 PageRank 算法
def pagerank(graph, damping=0.85, max_iter=100, tol=1e-6):
    """
    计算图中每个节点的 PageRank 值。

    PageRank 是一种用于评估节点重要性的算法，基于节点间的链接关系。
    它模拟了随机游走模型，其中 damping 因子表示用户继续浏览的概率。

    参数：
        graph (Graph): 图对象，包含节点和边信息。
        damping (float): 阻尼因子，通常为 0.85，表示用户继续浏览的概率。
        max_iter (int): 最大迭代次数。
        tol (float): 收敛阈值，当两次迭代的差值小于此值时停止。

    返回：
        dict: 每个节点的 PageRank 值，键为节点，值为排名。
    """
    # 初始化每个节点的排名，所有节点初始排名相等
    num_nodes = len(graph.nodes)
    ranks = {node: 1 / num_nodes for node in graph.nodes}

    # 迭代计算 PageRank，直到收敛或达到最大迭代次数
    for iteration in range(max_iter):
        new_ranks = {}  # 存储新一轮的排名

        # 对每个节点计算新的 PageRank 值
        for node in graph.nodes:
            rank_sum = 0  # 累加来自邻居节点的贡献

            # 遍历节点的邻居（在无向图中，邻居是连接的节点）
            for neighbor in graph.get_neighbors(node):
                # 每个邻居的贡献是其当前排名除以其出度（邻居数量）
                rank_sum += ranks[neighbor] / len(graph.get_neighbors(neighbor))

            # 计算新排名：(1 - damping)/N + damping * rank_sum
            # (1 - damping)/N 是随机跳转到任意节点的概率
            new_ranks[node] = (1 - damping) / num_nodes + damping * rank_sum

        # 检查收敛性：计算所有节点的排名变化总和
        diff = sum(abs(new_ranks[node] - ranks[node]) for node in graph.nodes)
        ranks = new_ranks  # 更新排名

        # 如果变化小于阈值，则提前停止
        if diff < tol:
            break

    return ranks

# ...existing code...


# 示例用法，
if __name__ == "__main__":
    graph = Graph()
    # 节点有 “A”到Z"
    for char in range(ord("A"), ord("Z") + 1):
        graph.add_node(chr(char))

    # 添加所有节点间连接的边
    import random
    nodes = list(graph.nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if random.random() < 0.1:  # 10% 概率添加一条边
                distance = random.randint(1, 10)
                graph.add_edge(nodes[i], nodes[j], distance)
    # 打印图的信息
    print("Nodes in the graph:", graph.nodes)
    for node in graph.nodes:
        print(f"Neighbors of {node}: {graph.get_neighbors(node)}")
    print("Distances between nodes:")
    for (from_node, to_node), distance in graph.distances.items():
        print(f"Distance from {from_node} to {to_node}: {distance}")

    # 计算并打印每个节点的 PageRank
    ranks = pagerank(graph)
    print("\n\nPageRank of nodes:")
    for node, rank in ranks.items():
        print(f"Node {node}: {rank}")







