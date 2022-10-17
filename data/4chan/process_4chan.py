import json
from bs4 import BeautifulSoup
import bs4
import matplotlib.pyplot as plt
import pandas as pd


def preprocess(text):
    soup = BeautifulSoup(text, "html.parser")
    for a in soup:
        if isinstance(a, bs4.element.Tag):
            a.decompose()
    return ' '.join(soup.stripped_strings)


if __name__ == "__main__":
    file_name = "4chan_sample.txt"
    dic = {}
    i = 0
    break_flag = False
    with open(file_name, "r") as f:
        while True:
            try:
                line = f.readline().strip()
            except:
                break
            print("Line read", i)
            i += 1
            line = line.strip()
            if len(line) == 0:
                break
            if break_flag:
                break
            data_dic = json.loads(line)
            for post in data_dic["posts"]:
                try:
                    text = post["com"]
                    tox_score = float(post["perspectives"]["TOXICITY"])
                except:
                    continue
                if tox_score < 0.7:
                    continue
                clean_text = preprocess(text).strip()
                if len(clean_text) == 0:
                    continue
                dic[clean_text] = tox_score
                print(len(dic))
                if len(dic) > 100000:
                    break_flag = True

    dic = dict(sorted(dic.items(), key=lambda item: -item[1]))
    tox_scores = list(dic.values())

    figs = plt.hist(tox_scores, bins=10)  # density=False would make counts
    plt.show()

    sents = list(dic.keys())
    df_dic = {"text": sents}
    df = pd.DataFrame.from_dict(df_dic)
    df.to_csv("4chan.csv", index=False)

    pass
