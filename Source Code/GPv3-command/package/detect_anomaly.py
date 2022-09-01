import json
import pickle
import time

import numpy as np
from pandas import DataFrame, Series
import os

from package.extract_events import ExtractEvents


class DetectAnomaly:
    def __init__(self, log_type):
        self.cluster_flag = None
        self.weights = None
        self.cluster_center: dict = {}
        self.position_matrix = None
        self.sequences = None
        self.events = None
        self.prev_blk = None
        self.cur_blk = None
        self.cur_time = None
        self.log_type = log_type
        self.reg = {
            "1": r"\[(?P<datetime>.*?20[0-9]{2})\] \[(?P<type>\w+)\] (?P<client>\[.*?\])?(?P<content>.*)",
            "2": r"(?P<content>.*(?P<blk_num>blk_\S+).*)"
        }
        self.type = {
            "1": "datetime",
            "2": "blk_num"
        }
        self.prev_logs = None  # Dataframe
        self.cur_logs = None  # Dataframe
        self.modify_time = None
        self.ex = ExtractEvents()

        self.load_data()

    def load_data(self):
        with open("./data/preprocessing/events.json") as eve_file:
            self.events = json.load(eve_file)
            self.events = {y: x for x, y in self.events.items()}
        with open("./data/preprocessing/sequences.json") as seq_file:
            self.sequences = json.load(seq_file)
        with open("./data/preprocessing/tk_position_matrix.json") as posi_file:
            self.position_matrix = json.load(posi_file)
        with open("./data/preprocessing/cluster_center.json") as cen_file:
            self.cluster_center = json.load(cen_file)
        with open("./data/preprocessing/events_weight.json") as wei_file:
            self.weights = json.load(wei_file)
        with open("./data/preprocessing/cluster_flags.json") as flag_file:
            self.cluster_flag = json.load(flag_file)

    def parse_cur_log(self, log):
        if self.log_type == "2":  # HDFS
            log = log.str.extract(self.reg[self.log_type], expand=True)
            blk = log[self.type[self.log_type]].values[0]
            log = self.extract_events(log.squeeze())
            if blk != self.cur_blk:
                # 结算上一个blk
                self.prev_blk = self.cur_blk
                self.cur_blk = blk
                # detect anomaly
                if self.cur_logs is not None:
                    self.prev_logs = self.cur_logs
                else:
                    self.prev_logs = log
                self.detect_anomaly()
                # create a new sequence
                self.cur_logs = log
            else:
                # 加到当前log结尾

                self.cur_logs = self.cur_logs.append(log)
            self.modify_time = time.time()

    def extract_events(self, log):
        # remove the variable part
        log = DataFrame([self.ex.remove_var(log, terms_freq=self.position_matrix)])
        log = self.ex.filter_event(log, "event")

        # matching the event number
        log["event"] = self.events[log["event"].values[0]]

        return log

    def match_cluster(self, arr):
        dis = []
        for key, center in self.cluster_center.items():
            dis.append([key, np.linalg.norm(center - arr)])
        dis = sorted(dis, key=lambda x: x[1])
        print(dis)
        return dis[0][0]

    def combine_sequence(self, seq: DataFrame):
        eve = seq["event"].drop_duplicates()
        seq_arr = [0] * len(self.events)

        # combine weights and events
        for i in eve:
            seq_arr[int(i)] = self.weights[i]

        scaler = pickle.load(open("./data/preprocessing/scaler.pkl", "rb"))
        # print((np.array(seq_arr).reshape(-1, 1)))
        seq_arr = scaler.transform(np.array(seq_arr).reshape(1, -1))
        return seq_arr

    def read_log(self, log_path):
        # when the log file is modified, read it
        # print("------------------------")
        while True:
            # print("Starting...")
            if os.path.getmtime(log_path) != self.modify_time:
                # read the latest log line
                log_file = open(log_path, "rb")
                log_file.seek(0, os.SEEK_END)
                while log_file.read(1) != b'\n':
                    log_file.seek(-2, os.SEEK_CUR)
                last_line = log_file.readline().decode()
                # print(last_line)
                self.parse_cur_log(Series(last_line))

                self.modify_time = os.path.getmtime(log_path)
            print("Waiting For Logs...")
            time.sleep(1)

    def detect_anomaly(self):
        # 检查已结算的上一个日志序列
        seq_arr = self.combine_sequence(self.prev_logs)
        clu = self.match_cluster(seq_arr)
        print()
        print(f"clu: {clu}", f"blk: {self.prev_blk}", set(self.prev_logs["event"].tolist()))
        if self.cluster_flag[clu] == "1":
            print(
                f"""
                !!! ALERT !!!
                --- Anomaly Log {self.prev_blk} Detect ---
                """
            )
        print()

# if __name__ == '__main__':
