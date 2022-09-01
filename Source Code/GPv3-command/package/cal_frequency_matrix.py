import pandas as pd
import numpy as np
from sklearn import preprocessing
import pickle
from package.save_to_local import SaveToLocal


class CalculateFrequencyMatrix:
    """
    This class is to group logs by time or their signs,
    and calculate the idf-matricx
    """

    def __init__(self, log_type, group_type):
        self.log_type = log_type  # HDFS, Apache
        self.group_type = group_type  # Block id for HDFS, time interval for Apache {"blk_num", "datetime"}

    def remove_duplicates(self, data):
        if self.log_type == "2":
            data = data.drop_duplicates([self.group_type, "event"]).set_index(self.group_type)
        elif self.log_type == "1":
            data[self.group_type] = data[self.group_type].dt.strftime("%Y-%d-%m %H:00:00")
            data = data.drop_duplicates([self.group_type, "event"]).set_index(self.group_type)
        return data

    def get_log_weight(self, data, events):
        n = len(data)
        weight = {}
        col = data.columns
        for i in events:
            if i in col:
                ni = data[i].sum()
                if ni == 0:
                    weight[i] = 0  # 这个事件没有出现过
                else:
                    weight[i] = np.log(n / ni)
        return weight

    def get_idf_weight(self, freq, events):
        save = SaveToLocal()
        weight = self.get_log_weight(freq, events)
        save.save_to_json(weight, "events_weight.json")
        for i in weight.keys():
            freq[[i]] = freq[[i]] * weight[i]
        return freq

    def get_freq_matrix(self, data, events):
        data = self.remove_duplicates(data)
        dummies = pd.get_dummies(data["event"])
        freq = dummies.groupby(self.group_type).sum()
        freq = self.get_idf_weight(freq, events)

        scaler = preprocessing.StandardScaler()
        scaler.fit(freq)
        nor_freq = scaler.transform(freq)

        # save scaler to reuse it
        pickle.dump(scaler, open("../data/preprocessing/scaler.pkl", "wb"))

        return nor_freq, freq
