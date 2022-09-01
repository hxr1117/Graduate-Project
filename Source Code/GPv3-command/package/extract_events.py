import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
from sklearn.neighbors import KernelDensity
from package.save_to_local import SaveToLocal
import swifter


class ExtractEvents:
    def generate_n_gram(self, data, ngram=1):
        terms = []
        for idx in range(len(data)):
            try:
                words = data[idx].strip().split()
                temp = zip(*[words[i:] for i in range(0, ngram)])
                temp = [' '.join(ngram) for ngram in temp]
                data[idx] = temp
                terms.extend(temp)
            except Exception:
                continue
        terms_list = set(terms)
        return data, terms_list

    def terms_position_freq(self, data):
        max_len = max(len(i) for i in data)
        terms = dict()
        for idx in range(len(data)):
            for idx_w in range(len(data[idx])):
                if data[idx][idx_w] not in terms:
                    terms[data[idx][idx_w]] = [0] * max_len
                terms[data[idx][idx_w]][idx_w] += 1
        return terms

    def get_cluster_min(self, arr):
        arr = np.array(arr).reshape(-1, 1)
        kde = KernelDensity(kernel='gaussian').fit(arr)
        s = np.linspace(0, np.max(arr))
        e = kde.score_samples(s.reshape(-1, 1))
        mi = argrelextrema(e, np.less)[0]
        return s[mi][0]

    def remove_var(self, row, terms_freq):
        con = row["content"].strip().split()

        new_con = []
        tmp_freq = []
        for idx_w in range(len(con)):
            try:
                tmp_freq.append(terms_freq[con[idx_w]][idx_w])
            except KeyError:
                tmp_freq.append(1)
        # find the most frequent word
        # and set it as the min frequency for a log
        try:
            min_freq = self.get_cluster_min(tmp_freq)
            flag = 0
            for idx_w in range(len(tmp_freq)):
                if tmp_freq[idx_w] >= min_freq:
                    new_con.append(con[idx_w])
                    flag += 1
            if flag == 0:
                print(tmp_freq)
            row["event"] = " ".join(new_con)
        except Exception as e:
            # mostly since empty array or all items are the same
            row["event"] = " ".join(con)
        return row

    def filter_event(self, data, row):
        data[row] = data[row].str.replace("\d", "", regex=True)
        data[row] = data[row].str.replace("[-()\"#/@;:<>{}`+=~|.!?,]", "", regex=True)
        data[row] = data[row].str.replace(" +", " ", regex=True)
        data[row] = data[row].str.strip()
        return data

    def extract_events(self, data):
        save = SaveToLocal()

        print("Starting extract variable parts")
        cons = data["content"].tolist()
        cons, df_tok = self.generate_n_gram(cons, 1)

        terms_freq = self.terms_position_freq(cons)
        data = data.swifter.apply(self.remove_var, terms_freq=terms_freq, axis=1)
        data = self.filter_event(data, "event")

        # save term frequency to local
        save.save_to_json(terms_freq, "tk_position_matrix.json")
        print("Saved token position matrix to local")

        # delete empty logs
        data = data[data["event"] != ""]

        data["event"] = pd.Categorical(data["event"])
        event = dict(enumerate(data["event"].cat.categories))

        # save events to local
        save.save_to_json(event, "events.json")
        print("Saved events to local")

        data["event"] = data["event"].cat.codes

        return data, event
