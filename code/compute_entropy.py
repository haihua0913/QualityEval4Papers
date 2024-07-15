#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/7/6 8:35
# @Author : Haoxuan Zhang

import pandas as pd
import math
import networkx as nx
from collections import Counter
from statistics import mean
# 确定threshold
def calculate_degree_and_betweenness_structure_entropy(graph_file, degree_threshold=0, betweenness_threshold=0):
    # 读取CSV文件并转换为DataFrame对象
    df = pd.read_csv(graph_file, usecols=['entity1', 'entity2', 'co_count'], dtype={'entity1': str, 'entity2': str, 'co_count': float})

    # 过滤权重大于阈值的边
    df_degree = df[df['co_count'] > degree_threshold]
    df_betweenness = df[df['co_count'] > betweenness_threshold]

    # 创建带权重的无向图
    G_degree = nx.from_pandas_edgelist(df_degree, 'entity1', 'entity2', 'co_count', create_using=nx.Graph())
    G_betweenness = nx.from_pandas_edgelist(df_betweenness, 'entity1', 'entity2', 'co_count', create_using=nx.Graph())

    # 使用字典存储每个节点的邻居节点和对应的权重
    neighbors_dict = {}
    for row in df_degree.itertuples(index=False):
        entity1, entity2, oc_count = row
        if entity1 not in neighbors_dict:
            neighbors_dict[entity1] = {}
        if entity2 not in neighbors_dict:
            neighbors_dict[entity2] = {}
        neighbors_dict[entity1][entity2] = oc_count
        neighbors_dict[entity2][entity1] = oc_count

    DegreeStructureEntropy_list = []
    BetweennessStructureEntropy_list = []
    StructureEntropyRatio_list = []

    # 对每个连通子图分别计算度结构熵、介数结构熵和结构熵比
    for subgraph in nx.connected_components(G_degree):
        G_subgraph = nx.subgraph(G_degree, subgraph)
        neighbors_dict_subgraph = {node: neighbors_dict[node] for node in subgraph}
        weighted_degrees = pd.Series({node: sum(neighbors_dict_subgraph[node].values()) for node in subgraph})
        weighted_degree_distribution = dict(Counter(weighted_degrees.values))
        weighted_degree_probability_distribution = {degree: count / math.fsum(weighted_degree_distribution.values()) for degree, count in weighted_degree_distribution.items()}
        log2 = math.log2
        weighted_degree_entropy = -sum(p * log2(p) for p in weighted_degree_probability_distribution.values())
        DegreeStructureEntropy = weighted_degree_entropy / nx.average_shortest_path_length(G_subgraph, weight='co_count')
        DegreeStructureEntropy_list.append(DegreeStructureEntropy)

        G_subgraph_betweenness = nx.subgraph(G_betweenness, subgraph)
        betweenness = nx.betweenness_centrality_subset(G_subgraph_betweenness, sources=subgraph, targets=subgraph, weight='co_count')
        betweenness_distribution = dict(Counter(betweenness.values()))
        betweenness_probability_distribution = {b: count / math.fsum(betweenness_distribution.values()) for b, count in betweenness_distribution.items()}
        betweenness_entropy = -sum(p * log2(p) for p in betweenness_probability_distribution.values())
        BetweennessStructureEntropy = betweenness_entropy / nx.average_shortest_path_length(G_subgraph_betweenness, weight='co_count')
        BetweennessStructureEntropy_list.append(BetweennessStructureEntropy)

        if DegreeStructureEntropy != 0:
            StructureEntropyRatio = (DegreeStructureEntropy - BetweennessStructureEntropy) / DegreeStructureEntropy
        else:
            StructureEntropyRatio = 0
        StructureEntropyRatio_list.append(StructureEntropyRatio)


    # 计算所有连通子图的平均值
    DegreeStructureEntropy = mean(DegreeStructureEntropy_list)
    BetweennessStructureEntropy = mean(BetweennessStructureEntropy_list)
    StructureEntropyRatio = mean(StructureEntropyRatio_list)

    return DegreeStructureEntropy, BetweennessStructureEntropy, StructureEntropyRatio


import os
import csv
from tqdm import tqdm

# subgraphs文件夹路径
subgraphs_folder = 's_entropy/concat'

# 输出结果的CSV文件路径
output_file = 'concat_structure_entropy.csv'

# 获取subgraphs文件夹下的所有CSV文件路径
csv_files = [os.path.join(subgraphs_folder, file) for file in os.listdir(subgraphs_folder) if file.endswith('.csv')]

# 打开输出文件并创建CSV写入器
with open(output_file, mode='w', newline='') as f:
    writer = csv.writer(f)

    # 写入表头
    writer.writerow(['Graph File', 'Structure Entropy', 'Degree Structure Entropy', 'Betweenness Structure Entropy', 'Structure Entropy Ratio'])

    # 循环处理每个CSV文件
    for csv_file in tqdm(csv_files, desc='Processing Files', unit='file'):
        # 计算结构熵、度结构熵、介数结构熵和结构熵比率
        degree_structure_entropy, betweenness_structure_entropy, structure_entropy_ratio = calculate_degree_and_betweenness_structure_entropy(csv_file)

        # 输出处理进度和计算结果
        print(f"{csv_file}: Degree Structure Entropy = {float(degree_structure_entropy):.4f}, Betweenness Structure Entropy = {float(betweenness_structure_entropy):.4f}, Structure Entropy Ratio = {float(structure_entropy_ratio):.4f}")

        # 将结果写入CSV文件
        writer.writerow([csv_file, degree_structure_entropy, betweenness_structure_entropy, structure_entropy_ratio])