from package import preparing
from package import detect_anomaly


def preparation():
    pre = preparing.Preparation()
    pre.preparing()


def detection():
    log_path = input("Please input the path for the keep updating log file:")
    det = detect_anomaly.DetectAnomaly(log_type="2")
    det.read_log(log_path)


if __name__ == '__main__':
    fun = {
        "1": preparation,
        "2": detection
    }
    ch = input("Please choose (if you need to detect, please run preparation first): (1) Preparation (2) Detection;")
    fun[ch]()
