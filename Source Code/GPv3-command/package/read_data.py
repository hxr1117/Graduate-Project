import numpy as np
import pandas as pd


class DataPreprocess(object):
    def __init__(self, log_type):
        self.log_type = log_type
        # 1 for apache
        # 2 for hdfs
        self.reg = {
            "1": r"\[(?P<datetime>.*?20[0-9]{2})\] \[(?P<type>\w+)\] (?P<client>\[.*?\])?(?P<content>.*)",
            "2": r"(?P<content>.*(?P<blk_num>blk_\S+).*)"
        }

    def read_data(self, path=""):
        if not path:
            print("Please input correct log path...", )

        data = pd.read_csv(path, lineterminator='\n', on_bad_lines='skip', header=None).squeeze("columns")
        return data

    def random_selection(self, data, percentage=0.01):
        """
        :param percentage:
        :param data: Logs DataFrame
        :return:
        """
        if self.log_type == "1":  # for Apache Logs
            pass
        else:  # for HDFS Logs
            groups_num = np.random.choice(data["blk_num"].unique(), int(len(data) * percentage))
            data = data.set_index("blk_num").loc[groups_num]
            data = data.reset_index()
        return data

    def get_logs(self):
        # log_path = input("please input the log's path:")
        log_path = "/Users/hexinrong/Downloads/HDFS_1/HDFS.log"

        print("Start reading logs...")
        logs = self.read_data(log_path)
        print("Reading logs finished...")

        print("Start preprocessing logs...")
        logs = logs.str.extract(self.reg[self.log_type], expand=True)

        print("Start randomly selecting logs...")
        logs = self.random_selection(logs, 0.001)

        if self.log_type == "1":
            logs["datetime"] = pd.to_datetime(logs["datetime"])
            logs["datetime"] = logs["datetime"].dt.strftime("%Y-%d-%m %H:00:00")

        logs["content"] = logs["content"].fillna("")
        print("Processing finished...")

        return logs

