from lxml import html,etree
import requests
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import deepl
import zipfile
import shutil
from pathlib import Path

from docx import Document


def deepl_translate(soup, target_lang="ZH", trans_type=0):
    """
    :param target_lang:目标语言，ZH中文，JA日文，EN-US英文。更多语言支持可以参考deepl开发文档
    :param trans_type：生成样式，0为单翻译版本，1为双语对照版本
    :return:
    """
    for i in soup.findAll('p'):
        a = str(i.getText())
        if a == "":
            result = ""
        else:
            result = translator.translate_text(i.getText(), target_lang=target_lang)
            if trans_type == 1:
                i.string = i.text.replace(a, i.getText() + " \n" + result.text)
            elif trans_type == 0:
                i.string = i.text.replace(a, result.text)
            else:
                print("Error Translate Type")

    for i in soup.find_all('i', text=True):
        a = str(i.getText())
        if a == "":
            result = ""
        else:
            result = translator.translate_text(i.getText(), target_lang=target_lang)
            if trans_type == 1:
                i.string = i.text.replace(a, i.getText() + " \n" + result.text)
            elif trans_type == 0:
                i.string = i.text.replace(a, result.text)
            else:
                print("Error Translate Type")

# 初始化deepl translator, 需要deepl开发者API Key
# example your_api = "4e324f8d-543s-22d3-32c3-a6497123ae76:fx"

your_api = ""
translator = deepl.Translator(your_api)

# 目标翻译语言
target_lang = "ZH"  # 目标语言，ZH中文，JA日文，EN-US英文。更多语言支持可以参考deepl开发文档
trans_type = 0  # trans_type：生成样式，0为单翻译版本，1为双语对照版本

# 书名，如果路径、书名中有空格，替换为'_'
book_name = 'One_Hundred_Years_of_Solitude'

# .epub电子书路径
book_path = 'books\epub\{}.epub'.format(book_name)

# 获取 所有.html文件内容
book = epub.read_epub(book_path)
items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

# 解压.epub并储存于books/unzip_tmp
with zipfile.ZipFile(book_path, 'r') as zip_ref:
    zip_ref.extractall('books/unzip_tmp')

# 遍历所有.html并翻译文本
for item in items:
    soup = BeautifulSoup(item.get_body_content(), 'html.parser')
    fn = item.file_name
    deepl_translate(soup, target_lang=target_lang, trans_type=0)

    # 另存为新的.html文件
    with open("books/unzip_tmp/{}".format(fn), "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))

# 重新打包,并输出到books目录下
shutil.make_archive('books/{}_{}'.format(book_name, trans_type), 'zip', 'books/unzip_tmp')
p = Path('books/{}_{}'.format(book_name, trans_type))
p.rename(p.with_suffix('.epub'))

