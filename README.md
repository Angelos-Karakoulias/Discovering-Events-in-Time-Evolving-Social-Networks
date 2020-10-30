# Event-detection-in-real-time-data-
Processing time-evolving social networks in order to detect anomaly instants, namely moments when the network behavior deviates from the remaining by using a sliding window decomposition with statistical tools.

## File Structure & running
Contains 2 .py files 
basic.py, method.py
- Output events.csv, nodes.csv, final_evaluation.csv
From basic.py and for every window W of length L we call the method.py sending the values:
- Factors, which is the number of fuctor in tensor decomposition.
- l_size, which is the Length of every Window in timestamps.
- stations, which is the number of stations, participating in our network.
- a, which is the decomposed list of the current window W
- y, the number of the repetion we are currently executing.
