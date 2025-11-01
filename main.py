import os
import time
import random
import pandas as pd
from config import SAVE_DIR
from search import get_search_bvids
from fetch import fetch_danmaku
from clean import clean_text
from analyze import analyze_danmaku
from visualize import generate_wordcloud

def main():
    keyword = input("请输入搜索关键词（例如：LLM、大模型）: ").strip()
    print(f"开始处理关键词：'{keyword}'")

    # 检查是否已有 360 个弹幕 Excel 文件，避免重复爬取
    existing_files = [
        f for f in os.listdir(SAVE_DIR)
        if f.endswith(".xlsx") and f.count("_") == 1 and keyword not in f
    ]
    if len(existing_files) >= 360:
        print(f"已检测到 {len(existing_files)} 个弹幕文件，跳过爬取阶段，直接分析...")
        all_danmaku = []
        for file in sorted(existing_files)[:360]:
            path = os.path.join(SAVE_DIR, file)
            try:
                df = pd.read_excel(path)
                danmaku_list = df["弹幕"].dropna().astype(str).tolist()
                all_danmaku.extend(danmaku_list)
            except Exception as e:
                print(f"读取 {file} 失败：{e}")
        print(f"\n共读取弹幕数：{len(all_danmaku)}")
    else:
        print(f"开始爬取 '{keyword}' 搜索结果前360个视频弹幕...")
        bvids = get_search_bvids(keyword, max_videos=360)
        if not bvids:
            print("未找到视频，任务结束。")
            return

        all_danmaku = []
        for i, bvid in enumerate(bvids, 1):
            save_path = os.path.join(SAVE_DIR, f"{i:03d}_{bvid}.xlsx")

            # 如果文件已存在则跳过爬取，直接读取
            if os.path.exists(save_path):
                df = pd.read_excel(save_path)
                danmaku_list = df["弹幕"].dropna().astype(str).tolist()
            else:
                try:
                    # 获取弹幕并清洗
                    danmaku_list, title = fetch_danmaku(bvid)
                    danmaku_list = [clean_text(d) for d in danmaku_list if d.strip()]
                    # 保存为 Excel 文件
                    df = pd.DataFrame(danmaku_list, columns=["弹幕"])
                    df.to_excel(save_path, index=False)
                    print(f"{i:03d}: {title} ({len(danmaku_list)} 条弹幕)")
                except Exception as e:
                    print(f"{i:03d}: BV{bvid} 获取失败：{e}")
                    continue

            all_danmaku.extend(danmaku_list)
            time.sleep(random.uniform(0.4, 0.8))  # 控制请求频率，避免被封

        print(f"\n共收集弹幕数：{len(all_danmaku)}")

    if not all_danmaku:
        print("未获取到弹幕，任务结束。")
        return

    # 分析弹幕并生成词云
    counter = analyze_danmaku(all_danmaku, keyword)
    generate_wordcloud(all_danmaku)

if __name__ == "__main__":
    main()
