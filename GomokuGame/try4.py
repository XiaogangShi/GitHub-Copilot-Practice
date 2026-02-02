"""示例程序：
在当前目录创建一个名为 data.txt 的文本文件，随机写入 10 个单词（每行一个），
然后关闭文件；接着读取该文件，把单词放入列表并按 ASCII 升序排序，最后用逗号分隔打印。

要点：
- 使用 `string.ascii_lowercase` 生成小写字母池
- 每个单词长度在 2 到 10 之间随机
- 写入与读取都使用文本模式；排序使用默认字符串排序（ASCII/字典序）
"""

import random
import string
from typing import List


def generate_random_word(length: int) -> str:
    """生成一个指定长度的随机小写单词。

    参数:
        length: 单词长度（正整数）

    返回:
        由小写字母组成的随机单词字符串
    """
    # 使用 ascii_lowercase 作为字母池（a-z）
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def write_random_words_to_file(path: str, count: int = 10) -> None:
    """在指定路径创建文本文件，并写入 count 个随机单词（每行一个）。"""
    with open(path, 'w', encoding='utf-8') as f:
        for _ in range(count):
            # 单词长度在 2 到 10 之间随机
            word = generate_random_word(random.randint(2, 10))
            f.write(word + '\n')


def read_words_and_print_sorted(path: str) -> None:
    """读取文件中的单词，按 ASCII 升序排序并用逗号分隔打印出来。"""
    # 读取所有行并去除行尾换行符和多余空白
    with open(path, 'r', encoding='utf-8') as f:
        words: List[str] = [line.strip() for line in f if line.strip()]

    # 按默认字符串比较进行排序（对 ASCII/字典序敏感）
    words.sort()

    # 用逗号连接并打印
    print(','.join(words))


def main() -> None:
    """主函数：写入 data.txt，读取并打印排序结果。"""
    data_file = 'data.txt'

    # 第一步：创建并写入随机单词文件
    write_random_words_to_file(data_file, count=10)

    # 第二步：读取并按 ASCII 升序打印
    read_words_and_print_sorted(data_file)


if __name__ == '__main__':
    main()


