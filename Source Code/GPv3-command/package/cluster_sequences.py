from sklearn.cluster import AgglomerativeClustering
from package.save_to_local import SaveToLocal


class ClusterSequences:
    def __init__(self):
        self.label_pred = None
        self.agg_clu = None

    def __int__(self, log_type, group_type):
        self.log_type = log_type  # HDFS, Apache
        self.group_type = group_type  # Block id for HDFS, time interval for Apache {"blk_num", ""}

    def clustering(self, norm_freq, distance_threshold=0.5):
        self.agg_clu = AgglomerativeClustering(n_clusters=None, distance_threshold=distance_threshold).fit(norm_freq)
        self.label_pred = self.agg_clu.labels_

    def get_log_sequences(self, norm_freq, matrix):
        """
        :param norm_freq: normalized frequency matrix
        :param matrix: sequence matrix
        :return: log sequences
        """
        self.clustering(norm_freq)
        label_center = {}
        # 保存的是标准化后的集群中心
        cluster = {}
        for i in range(self.agg_clu.n_clusters_):
            _ = matrix[self.label_pred == i]
            # calculate the center
            mean = _.mean()
            seq = []
            for j in range(len(mean)):
                if mean[j] != 0:
                    seq.append(j)
            # print(f"Seq{i}\t{'-'.join(seq)}")
            cluster[i] = seq
            label_center[i] = norm_freq[self.label_pred == i].mean(axis=0).tolist()

        save = SaveToLocal()
        save.save_to_json(label_center, "cluster_center.json")
        save.save_to_json(cluster, "sequences.json")

        return cluster
