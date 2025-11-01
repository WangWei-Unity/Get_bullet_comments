import requests
import time
import random
from config import HEADERS

def get_search_bvids(keyword, max_videos=360):
    results = []
    page = 1
    while len(results) < max_videos:
        url = (
            f"https://api.bilibili.com/x/web-interface/search/type"
            f"?search_type=video&keyword={keyword}&order=dm&page={page}"
        )
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 412:
            print("被反爬机制拦截（HTTP 412），请稍后重试。")
            break
        if r.status_code != 200:
            print(f"请求失败：HTTP {r.status_code}")
            break

        try:
            data = r.json()
        except:
            print("返回非JSON格式，可能被风控。")
            break

        if data.get("code") != 0:
            print("接口错误：", data.get("message"))
            break

        videos = data["data"].get("result", [])
        if not videos:
            break

        for v in videos:
            bv = v.get("bvid")
            if bv and bv not in results:
                results.append(bv)

        print(f"第 {page} 页，累计获取 {len(results)} 个视频...")
        page += 1
        time.sleep(random.uniform(0.4, 0.8))
        if page > 30:
            break

    print(f"共提取到 {len(results)} 个视频。")
    return results[:max_videos]
