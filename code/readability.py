#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/5/18 11:14
# @Author : Haoxuan Zhang
import csv
import textstat

# 打开txt文件
with open('abstact.txt', 'r',encoding='utf-8') as f:
    # 读取所有行，并去除末尾的换行符
    lines = [line.strip() for line in f.readlines()]

# 创建csv文件，写入表头
with open('readability_scores.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Line', 'Flesch-Kincaid Grade Level', 'SMOG Index', 'Coleman-Liau Index', 'ARI', 'Linsear Write Formula', 'Gunning Fog Index'])

    # 对每一行进行可读性计算，并写入csv文件
    for i, line in enumerate(lines, start=1):
        # 使用textstat包中的函数计算可读性
        flesch_score = textstat.flesch_kincaid_grade(line)
        smog_score = textstat.smog_index(line)
        coleman_score = textstat.coleman_liau_index(line)
        auto_score = textstat.automated_readability_index(line)
        linsear_score = textstat.linsear_write_formula(line)
        gunning_score= textstat.gunning_fog(line)

        # 写入csv文件
        writer.writerow([i, flesch_score, smog_score, coleman_score, auto_score, linsear_score, gunning_score])
