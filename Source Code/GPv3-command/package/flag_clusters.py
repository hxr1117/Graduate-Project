from package.save_to_local import SaveToLocal


class FlagClusters:
    def flag_clusters(self, clusters: dict, events: dict, file_name: str, path="../data/preprocessing/"):
        flags = {}
        for clu in clusters.keys():
            print(f"<<< Cluster {clu}: >>>")
            print(clusters[clu])
            for e in clusters[clu]:
                print(events[e])
            flags[clu] = input(f"Please input the tag for cluster {clu}, (1) for abnormal; (2) for normal:")
            print()
        save = SaveToLocal()
        save.save_to_json(flags, file_name)
