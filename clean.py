import re

def clean_text(text):
    # 移除所有空白字符（包括空格、换行、制表符）
    return re.sub(r"\s+", "", text)
