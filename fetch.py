import requests
import xmltodict
from config import HEADERS

def get_cid(bvid):
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    r = requests.get(url, headers=HEADERS)
    data = r.json()
    if data["code"] == 0:
        return data["data"]["cid"], data["data"]["title"]
    raise ValueError(f"视频获取失败: {data.get('message')}")

def fetch_danmaku(bvid):
    cid, title = get_cid(bvid)
    url = f"https://comment.bilibili.com/{cid}.xml"
    r = requests.get(url, headers=HEADERS)
    data = xmltodict.parse(r.content)
    danmaku_list = []
    if "i" in data and "d" in data["i"]:
        for d in data["i"]["d"]:
            danmaku_list.append(d["#text"])
    return danmaku_list, title
