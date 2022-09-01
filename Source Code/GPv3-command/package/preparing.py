from package.read_data import DataPreprocess
from package.extract_events import ExtractEvents
from package.cluster_sequences import ClusterSequences
from package.cal_frequency_matrix import CalculateFrequencyMatrix
from package.flag_clusters import FlagClusters


class Preparation:
    def __init__(self):
        self.log_type = None
        self.group_type = {
            "1": "datetime",
            "2": "blk_num"
        }

    def preparing(self):
        # self.log_type = input("please choose the log type:(1) for Apache Server Log, (2) for HDFS Log.")
        # print(self.log_type)
        self.log_type = "2"

        # read logs from local
        print(" Preparing Stage ".center(50, "-"))
        print(" Reading Logs ".center(50, "-"))
        data_preprocess = DataPreprocess(self.log_type)
        logs = data_preprocess.get_logs()
        print(" Reading Finished ".center(50, "-"))

        # extract events
        print(" Extracting Log Events ".center(50, "-"))
        extractor = ExtractEvents()
        logs, log_events = extractor.extract_events(logs)
        print(" Extracting Finished ".center(50, "-"))

        # events matrix
        print(" Calculating Event Matrix ".center(50, "-"))
        calculater = CalculateFrequencyMatrix(self.log_type, self.group_type[self.log_type])
        norm_freq, sequence_matrix = calculater.get_freq_matrix(logs, log_events)
        print(" Calculating Finished ".center(50, "-"))

        # cluster sequences
        print(" Clustering Log Sequences ".center(50, "-"))
        cluster = ClusterSequences()
        log_sequences = cluster.get_log_sequences(norm_freq, sequence_matrix)
        print(" Clustering Finished ".center(50, "-"))

        # flag clusters
        print(" Please tag clusters ".center(50, "-"))
        flag = FlagClusters()
        flag.flag_clusters(log_sequences, log_events, "cluster_flags.json")
        print(" Tagging Finished ".center(50, "-"))
        print(" Preparing Stage Finished ".center(50, "-"))


if __name__ == '__main__':
    prepare = Preparation()
    prepare.preparing()
