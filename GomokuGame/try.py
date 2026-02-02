# 编写一个程序，按次数升序显示文件中所有的中文文字或者英文单词或者一串数字，忽略标点符号和大小写。并标注出现的次数。

import re
import sys
import argparse
from collections import Counter


def display_tokens_by_count(file_path):
    r"""
    读取指定文件，并按出现次数升序显示三类 token：
      - 连续的中文字符（尽可能把整个汉字词/短语作为一个 token）
      - 英文单词（连续字母，忽略大小写）
      - 连续数字（作为一串数字整体统计）
    忽略标点符号和其它非上述三类的字符。

    输出格式：<token>: <count>
    """

    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}", file=sys.stderr)
        return
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        return

    # 使用正则一次性提取三类 token：连续中文、英文单词、数字串
    tokens = re.findall(r'[\u4e00-\u9fff]+|[A-Za-z]+|\d+', text)

    # 归一化：英文转小写，中文和数字保持原样
    alpha_re = re.compile(r'^[A-Za-z]+$')
    normalized = [t.lower() if alpha_re.match(t) else t for t in tokens]

    # 统计并按 (count, token.lower()) 排序（次数升序，次数相同时按不区分大小写的字典序）
    counts = Counter(normalized)
    sorted_items = sorted(counts.items(), key=lambda kv: (kv[1], kv[0].lower()))

    # 输出结果
    for token, count in sorted_items:
        print(f"{token}: {count}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Display Chinese-character sequences, English words, or digit sequences in ascending order with counts (ignore punctuation and English case).'
    )
    parser.add_argument('file', nargs='?', default='README.md', help='Path to the file to process')
    args = parser.parse_args()
    display_tokens_by_count(args.file)


# 以下为 pytest 单元测试，覆盖基本及边界情况
import pytest
from io import StringIO
import os


def test_display_tokens_by_count_basic(monkeypatch, tmp_path):
    # 基本测试：英文、数字、中文短语
    content = 'Hello 123 你好'
    p = tmp_path / 't1.txt'
    p.write_text(content, encoding='utf-8')

    monkeypatch.setattr(sys, 'stdout', StringIO())
    display_tokens_by_count(str(p))
    out = sys.stdout.getvalue()
    assert out == '123: 1\nhello: 1\n你好: 1\n'


def test_display_tokens_by_count_repeats(monkeypatch, tmp_path):
    # 测试重复和大小写忽略
    content = 'a A a bb 你好 你 你 123 123'
    p = tmp_path / 't2.txt'
    p.write_text(content, encoding='utf-8')

    monkeypatch.setattr(sys, 'stdout', StringIO())
    display_tokens_by_count(str(p))
    out = sys.stdout.getvalue().splitlines()

    # 构建期望列表并按 (count, token.lower()) 排序
    expected = sorted([
        ('bb', 1),
        ('你好', 1),
        ('a', 3),
        ('你', 2),
        ('123', 2),
    ], key=lambda kv: (kv[1], kv[0].lower()))

    expected_lines = [f"{k}: {v}" for k, v in expected]
    assert out == expected_lines


def test_display_tokens_by_count_empty(monkeypatch, tmp_path):
    # 空文件
    p = tmp_path / 'empty.txt'
    p.write_text('', encoding='utf-8')

    monkeypatch.setattr(sys, 'stdout', StringIO())
    display_tokens_by_count(str(p))
    out = sys.stdout.getvalue()
    assert out == ''