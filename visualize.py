from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(all_danmaku):
    # 若弹幕列表为空则退出
    if not all_danmaku:
        print("无法生成词云图：弹幕为空")
        return

    # 设置中文字体路径（确保支持中文）
    font_path = r"C:\Windows\Fonts\simhei.ttf"

    # 创建词云对象
    wordcloud = WordCloud(
        width=800,
        height=600,
        background_color="white",
        font_path=font_path,
        max_words=300
    ).generate(" ".join(all_danmaku))  # 将弹幕合并为一个字符串

    # 保存词云图到文件
    wordcloud.to_file("danmaku_data/wordcloud.png")

    # 显示词云图
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    print("词云生成完成。")
