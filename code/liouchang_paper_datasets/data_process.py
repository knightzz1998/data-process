# -*- coding: utf-8 -*-
# 作者 : 王天赐

import pandas as pd
import os
import xml.etree.ElementTree as ET
from tqdm import tqdm


def read_json_data(data_path):
    laptop_data = pd.read_json(data_path)
    return laptop_data


def ensure_index(text_line, from_idx, to_idx, term):
    """
        注意细节 : 区间是 [from_, to) 的
    :param text_line:
    :param from_idx:
    :param to_idx:
    :param term:
    :return:
    """
    if text_line[from_idx:to_idx] != term:
        from_ = text_line.find(term)
        to_ = from_ + len(term) - 1
        return from_, to_
    else:
        return from_idx, to_idx


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

        text_line = df[column]['sentence']
        from_idx = df[column]['from']
        to_idx = df[column]['to']
        term = df[column]['term']

        # 验证 from 和 to 是否正确
        # 如果不正确获取新的from和to的下标
        from_idx, to_idx = ensure_index(text_line, from_idx, to_idx, term)

        # 添加 aspectTerms 标签
        aspectTerms = ET.SubElement(sentence, 'aspectTerms')
        # 添加 aspectTerms 标签, aspectTerm 表亲的父标签为 aspectTerms
        aspectTerm = ET.SubElement(aspectTerms, 'aspectTerm')
        # 设置 aspectTerm标签 属性
        aspectTerm.attrib = {
            'from': str(from_idx),
            'to': str(to_idx),
            'polarity': str(df[column]['polarity']),
            'term': str(term)
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
        laptop_input = os.path.join(base_in_path, "laptop", file + ".json")
        rest_input = os.path.join(base_in_path, "rest", file + ".json")
        laptop_output = os.path.join(base_out_path, "laptop", file + ".xml")
        rest_output = os.path.join(base_out_path, "rest", file + ".xml")

        run_func(laptop_input, laptop_output)
        run_func(rest_input, rest_output)
