from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(all_danmaku):
    if not all_danmaku:
        print("无法生成词云图：弹幕为空")
        return
    font_path = r"C:\Windows\Fonts\simhei.ttf"
    wordcloud = WordCloud(
        width=800, height=600, background_color="white",
        font_path=font_path, max_words=300
    ).generate(" ".join(all_danmaku))

    wordcloud.to_file("danmaku_data/wordcloud.png")
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    print("词云生成完成。")
