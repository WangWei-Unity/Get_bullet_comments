from collections import Counter
import pandas as pd

#定义 AI 相关关键词
ai_keywords = ['AI', '人工智能', '机器学习', '深度学习', '算法', '大数据', '智能', '技术']

def analyze_danmaku(all_danmaku, keyword):
    #筛选包含关键词的弹幕
    filtered = [d for d in all_danmaku if any(kw in d for kw in ai_keywords)]

    #统计词频
    counter = Counter(filtered)
    most_common = counter.most_common(8)

    #保存为 Excel
    df = pd.DataFrame(most_common, columns=["弹幕", "数量"])
    df.to_excel(f"{keyword}_danmaku_summary.xlsx", index=False)
    print(f"已保存与 AI 相关的弹幕统计结果，共 {len(filtered)} 条。")

    return counter
