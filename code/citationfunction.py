#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/5/26 10:19
# @Author : Haoxuan Zhang

from transformers import pipeline
import csv

classifier = pipeline("text-classification", model="allenai/multicite-multilabel-scibert", top_k=1)
device = "cuda:0"
# 打开CSV文件
with open('output.csv') as f:
    reader = csv.reader(f)

    # 读取每一行
    for row in reader:
        # 取出第二列的数据
        col2 = row[1]

        # 写入新的CSV文件
        with open('output_class.csv', 'a') as f1:
            writer = csv.writer(f1)
            writer.writerow([classifier(col2)])

