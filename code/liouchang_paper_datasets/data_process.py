# -*- coding: utf-8 -*-
# 作者 : 王天赐

import pandas as pd
import os
import xml.etree.ElementTree as ET
from tqdm import tqdm


def read_json_data(data_path):
    laptop_data = pd.read_json(data_path)
    return laptop_data


def json_to_xml(df):
    columns = df.columns
    # 设置根标签
    root = ET.Element('sentences')

    # 遍历数据, 转换为 xml
    for column in columns:
        # 添加 sentence 标签
        sentence = ET.SubElement(root, "sentence")
        # 添加 text 标签
        text = ET.SubElement(sentence, 'text')
        # 设置 text 标签内容
        text.text = df[column]['sentence']

        # 添加 aspectTerms 标签
        aspectTerms = ET.SubElement(sentence, 'aspectTerms')
        # 添加 aspectTerms 标签, aspectTerm 表亲的父标签为 aspectTerms
        aspectTerm = ET.SubElement(aspectTerms, 'aspectTerm')
        # 设置 aspectTerm标签 属性
        aspectTerm.attrib = {
            'from': str(df[column]['from']),
            'to': str(df[column]['to']),
            'polarity': str(df[column]['polarity']),
            'term': str(df[column]['term'])
        }

    xml_data = ET.tostring(root)
    return xml_data


def save_data(xml_data, output_path):
    with open(output_path, 'w') as f:  # Write in file as utf-8
        f.write(xml_data.decode('utf-8'))


def run_func(input_path, output_path):
    df = read_json_data(input_path)
    xml_data = json_to_xml(df)
    save_data(xml_data, output_path)


if __name__ == '__main__':
    base_in_path = '..\\..\\datasets'
    base_out_path = 'save_data'
    input_path_list = []
    output_path_list = []
    files = ['dev', 'test', 'train']

    for file in tqdm(files):
        laptop_input = os.path.join(base_in_path, "laptop", file+".json")
        rest_input = os.path.join(base_in_path, "rest", file+".json")
        laptop_output = os.path.join(base_out_path, "laptop", file+".xml")
        rest_output = os.path.join(base_out_path, "rest", file+".xml")

        run_func(laptop_input, laptop_output)
        run_func(rest_input, rest_output)