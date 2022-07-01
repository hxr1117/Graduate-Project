## Project Title

Real-time log analysis in cloud environment

## Background

Most current systems generate a large number of logs at runtime, which record a lot of important security information. A cloud environment, on the other hand, reduces costs, increases computing speed and is more reliable. The aim of this project is to perform real-time log detection in the cloud and alert administrators when abnormal behaviour occurs. Current log analysis methods are unsupervised and supervised, and the more common of the unsupervised methods are clustering and PCA. **For this project, I decided to use the unsupervised clustering method to analyse the widely used [apache logs](https://github.com/logpai/loghub/tree/master/Apache) in LogHub.**

## Methodology

The project has three phases. The first stage is the preparation stage, which includes data collection, cleaning, parsing and clustering analysis. Like normal text processing, the data pre-processing involves putting the logs in chronological order, removing time etc. from them; the logs are then vectorised, clustered and extracting the representatives as templates.

The second stage is the visualisation stage, which includes analysis of new logs and exception alerts, as well as data visualisation (e.g. line graphs of the number of exceptions, etc.).

The third stage is deployment in cloud Kubernetes.

## Progress to date

The current progress is to select the dataset, clean the data.

As well as defining the evaluation: accuracy is evaluated by calculating F-measure, robustness is evaluated by PA distribution, average PA and average message length, etc. Efficiency is usually measured in terms of processing time per log, data block or individual log message(Lupton 2021).

## Remaining Questions

Is it fine to analyse [Apache Web Log](https://github.com/logpai/loghub/tree/master/Apache)? Not sure whether to analyse exceptions in all logs or look for them in the error logs.

## References

Svacina, J., Raffety, J., Woodahl, C., Stone, B., Cerny, T., Bures, M., Shin, D., Frajtak, K. and Tisnovsky, P., 2020, October. On vulnerability and security log analysis: A systematic literature review on recent trends. In *Proceedings of the International Conference on Research in Adaptive and Convergent Systems* (pp. 175-180).

Lin, Q., Zhang, H., Lou, J.G., Zhang, Y. and Chen, X., 2016, May. Log clustering based problem identification for online service systems. In *2016 IEEE/ACM 38th International Conference on Software Engineering Companion (ICSE-C)* (pp. 102-111). IEEE.Vancouver

Zhu, J., He, S., Liu, J., He, P., Xie, Q., Zheng, Z. and Lyu, M.R., 2019, May. Tools and benchmarks for automated log parsing. In *2019 IEEE/ACM 41st International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP)*  (pp. 121-130). IEEE.

Lupton, S., Washizaki, H., Yoshioka, N. and Fukazawa, Y., 2021, October. Online log parsing: Preliminary literature review. In *2021 IEEE International Symposium on Software Reliability Engineering Workshops (ISSREW)* (pp. 304-305). IEEE.

## Plan

Week 1: Attempt some methods of processing and clustering data to find a more suitable one. Drafting the dashboard for log notification.

Week 2-3: Start to Development.

Week 4-5: Summarise information and evaluate the development outcome.

Week 6-9: Write the research paper and submission.
