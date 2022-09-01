import random
import time

import pandas as pd


def get_data(path="/Users/hexinrong/Downloads/HDFS_1/HDFS.log"):
    print("%%%%%% Generating Logs %%%%%%")
    data = pd.read_csv(path, lineterminator='\n', on_bad_lines='skip', header=None).squeeze("columns")
    data = data.str.extract(r"(?P<content>.*(?P<blk_num>blk_\S+).*)", expand=True)
    blk = data["blk_num"].unique()
    random.shuffle(blk)
    # time.sleep(60)
    print("Ready...")
    for i in range(0, 100):
        print(f"###### Writing block {blk[i]} ######")
        tt = data[data["blk_num"] == blk[i]].content
        for t in tt:
            file = open("./data/simulation.log", "a+")
            file.write(t+"\n")
            file.close()
            time.sleep(3)
        time.sleep(5)

    print("%%%%%% Finished %%%%%%")


if __name__ == '__main__':
    get_data()
