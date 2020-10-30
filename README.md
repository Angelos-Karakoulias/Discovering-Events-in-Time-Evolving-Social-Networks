# Event-detection-in-real-time-data-
Processing time-evolving social networks in order to detect anomaly instants, namely moments when the network behavior deviates from the remaining by using a sliding window decomposition with statistical tools.

## File Structure & running
Contains 2 .py files 
basic.py, method.py
- Output events.csv, nodes.csv, final_evaluation.csv.

From basic.py and for every window W of length L we call the method.py sending the values:
- Factors, which is the number of fuctors R in tensor decomposition.
- l_size, which is the Length L of every Window in timestamps.
- stations, which is the number of stations (nodes), participating in our network.
- a, which is the decomposed list of the current window W
- y, the number of the repetion we are currently executing.

## Input Data format

In basic.py, we import our data which are bike trips between stations in Washington, D.C.
Then we have to format this data to a list in order to decompose them. For this purpose, we format our data (section table in basic.py) in an 3D Adjacency matrix where the list correspond to (Time x Nodes x Nodes):
 - Time (the hour the trip took place)
 - Nodes (the starting station)
 - Nodes (the ending station)

 
## Output Data format
Events.csv: a file containing the events detected from our algorithm with the following format: ``` Window Length, Number of factors, Event Timestamp, Event activity score```

Nodes.csv: a file containing the nodes participating on a event with the format:```Window Length, Number of Factors, Event Timestamp, Event Activity score, Participating Node```

Final_results.csv: a file which is not an immediate result from our code, but result from his execution using every time different model (factors, window length). Here we rank our events based on the number of sifferent models detecting them (total of 16 models) and their activity score Format:```Timestamp, number of models detecting it, activity score, Rank```

## Reference
Fernandes S., Fanaee-T H., Gama J. (2019) Evolving Social Networks Analysis via Tensor Decompositions: From Global Event Detection Towards Local Pattern Discovery and Specification. In: Kralj Novak P., Šmuc T., Džeroski S. (eds) Discovery Science. DS 2019. Lecture Notes in Computer Science, vol 11828. Springer, Cham. https://doi.org/10.1007/978-3-030-33778-0_29


