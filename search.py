import requests
import time
import random
from config import HEADERS

def get_search_bvids(keyword, max_videos=360):
    # 从 B 站搜索接口获取指定关键词的 BV 号列表（按弹幕数排序）
    results = []
    page = 1

    while len(results) < max_videos:
        # 构造搜索接口 URL，order=dm 表示按弹幕数排序
        url = (
            f"https://api.bilibili.com/x/web-interface/search/type"
            f"?search_type=video&keyword={keyword}&order=dm&page={page}"
        )

        # 发起请求
        r = requests.get(url, headers=HEADERS)

        # 处理反爬拦截
        if r.status_code == 412:
            print("被反爬机制拦截（HTTP 412），请稍后重试。")
            break
        if r.status_code != 200:
            print(f"请求失败：HTTP {r.status_code}")
            break

        # 解析 JSON 响应
        try:
            data = r.json()
        except:
            print("返回非JSON格式，可能被风控。")
            break

        # 接口返回错误
        if data.get("code") != 0:
            print("接口错误：", data.get("message"))
            break

        # 提取视频列表
        videos = data["data"].get("result", [])
        if not videos:
            break

        # 提取 BV 号并去重
        for v in videos:
            bv = v.get("bvid")
            if bv and bv not in results:
                results.append(bv)

        print(f"第 {page} 页，累计获取 {len(results)} 个视频...")
        page += 1
        time.sleep(random.uniform(0.4, 0.8))  # 控制请求频率，避免被封

        if page > 30:  # 防止死循环
            break

    print(f"共提取到 {len(results)} 个视频。")
    return results[:max_videos]
