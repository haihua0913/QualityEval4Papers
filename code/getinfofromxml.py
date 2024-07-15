#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/5/17 20:49
# @Author : Haoxuan Zhang
"""import csv
import os
import re
import xml.etree.ElementTree as ET

# 指定XML文件所在的目录
xml_dir = 'D:/python3.7Project/ipm_project/measurenovelty/xmlfile/'
file_list = os.listdir(xml_dir)
file_list.sort()
output_rows = []

# 遍历目录下的所有XML文件
for i, file_name in enumerate(file_list):

        tree = ET.parse(os.path.join(xml_dir, file_name))


        # 获取XML文件中所有的<figure>元素
        figures = tree.findall('.//{http://www.tei-c.org/ns/1.0}figure')

        # 获取XML文件中所有的<formula>元素
        formulas = tree.findall('.//{http://www.tei-c.org/ns/1.0}formula')

        # 获取XML文件中所有的<biblStruct>元素
        bibl_structs = tree.findall('.//{http://www.tei-c.org/ns/1.0}biblStruct')

        # 获取XML文件中的<body>元素
        body = tree.find('.//{http://www.tei-c.org/ns/1.0}body')


        # 找到<back>标签
        back = tree.find('.//{http://www.tei-c.org/ns/1.0}back')

        # 找到<table>标签
        max_table_id = 0
        for table in tree.findall('.//{http://www.tei-c.org/ns/1.0}figure[@type="table"]'):
            max_table_id += 1

        # 寻找<figure>元素中最大的xml:id属性值
        max_figure_id = 0
        for figure in figures:
            figure_id_attr = figure.get('{http://www.w3.org/XML/1998/namespace}id')
            if figure_id_attr is not None:
                figure_id = int(figure_id_attr[4:])
                if figure_id > max_figure_id:
                    max_figure_id = figure_id

        # 寻找<formula>元素中最大的xml:id属性值
        max_formula_id = 0
        for formula in formulas:
            formula_id_attr = formula.get('{http://www.w3.org/XML/1998/namespace}id')
            if formula_id_attr is not None:
                formula_id = int(formula_id_attr[8:])
                if formula_id > max_formula_id:
                    max_formula_id = formula_id

        # 寻找<biblStruct>元素中最大的xml:id属性值
        max_biblstruct_id = 0
        for bibl_struct in bibl_structs:
            biblstruct_id_attr = bibl_struct.get('{http://www.w3.org/XML/1998/namespace}id')
            if biblstruct_id_attr is not None:
                biblstruct_id = int(biblstruct_id_attr[1:])
                if biblstruct_id > max_biblstruct_id:
                    max_biblstruct_id = biblstruct_id

        # 获取<body>元素的所有文本内容
        text = ET.tostring(body, encoding='unicode', method='text')

        # 使用正则表达式从文本中匹配所有的英文单词
        english_words = re.findall(r'\b[a-zA-Z]+\b', text)

        # 计算英文单词的个数
        num_english_words = len(english_words)


        # 遍历<back>标签中的所有子标签，查找是否存在除<div type="references">之外的其他标签
        found_other_tag = 0
        for child in back:
            if child.tag == '{http://www.tei-c.org/ns/1.0}div' and child.get('type') == 'references':
                continue
            else:
                found_other_tag = 1
                break
        output_rows.append(
            {'id': i, 'file_name': file_name, 'max_figure_id': max_figure_id, 'max_table_id': max_table_id, 'max_formula_id': max_formula_id,
             'max_biblstruct_id': max_biblstruct_id,
             'num_english_words': num_english_words,'have_appendix': found_other_tag,})
        # 创建CSV文件并写入数据
        with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'file_name', 'max_figure_id', 'max_table_id','max_formula_id', 'max_biblstruct_id', 'num_english_words','have_appendix']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # 写入每个文件的输出
            for row in output_rows:
                writer.writerow(row)"""

from lxml import etree

# 读取XML文件
tree = etree.parse('D:/python3.7Project/ipm_project/measurenovelty/xmlfile/0_TxFpAsEI.xml')
root = tree.getroot()

# 查找when属性为2020年之后的date标签
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
count = len(root.xpath('.//tei:date[@when and number(substring(@when, 1, 4)) >= 2020]', namespaces=ns))

# 输出结果
print(count)