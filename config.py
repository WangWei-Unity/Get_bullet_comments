import os

# 弹幕 Excel 文件保存目录
SAVE_DIR = "danmaku_data"
os.makedirs(SAVE_DIR, exist_ok=True)  # 若目录不存在则自动创建

# 请求头配置，用于模拟浏览器访问，避免被 B 站反爬
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),  # 浏览器标识
    "Referer": "https://search.bilibili.com/",  # 来源页面，防止403
    "Origin": "https://search.bilibili.com",    # 请求来源域
    "Accept": "application/json, text/plain, */*",  # 接受的数据类型
    "Accept-Language": "zh-CN,zh;q=0.9",  # 语言偏好
    "Cookie": "buvid3=12345678-FakeCookie; CURRENT_FNVAL=4048;"  # 伪造 Cookie，避免 412 错误
}
