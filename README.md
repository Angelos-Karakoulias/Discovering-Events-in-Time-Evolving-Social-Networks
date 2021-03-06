# Discovering Events in Time Evolving Social Networks
Processing time-evolving social networks in order to detect anomaly instants, namely moments when the network behavior deviates from the remaining by using a sliding window decomposition with statistical tools.

## File Structure & running
Contains 3 Python 3.x version files: *basic.py*, *method.py*, *final_results.py*. It will also be necessary to have Tensorly, Numpy, Pandas.
- Output events.csv, nodes.csv, final_results.csv.

From *basic.py* and for every window W of length L we call the *method.py*, sending the values:
- Factors, which is the number of factors R in tensor decomposition.
- l_size, which is the Length L of every Window W in timestamps.
- stations, which is the number of stations (nodes), participating in our network.
- a, which is the decomposed list (contains the 3 parafac metrics) of the current window W.
- y, the number of the repetition we are currently executing.

## Input Data format

In *basic.py*, we import our data which are bike trips between stations in Washington, D.C.
Then we have to format this data to a list in order to decompose them. For this purpose, we format our data (section table in basic.py) in an 3D Adjacency matrix which structure is the following (Time x Nodes x Nodes):
 - Time (the hour the trip took place)
 - Nodes (the starting station)
 - Nodes (the ending station)

In *final_results.py* we import all events results from *basic.py* for the 16 different models.
 
## Output Data format
*Events.csv*: a file containing the detected events from our algorithm with the following format: ``` Window Length, Number of factors, Event Timestamp, Event activity score```

*Nodes.csv*: a file containing the nodes participating on a event with the format:```Window Length, Number of Factors, Event Timestamp, Event Activity score, Participating Node```

*Final_results.csv*: a file which emerges from *final_results.py* where we rank the events detected from different models (window length L, factors R) based on the number of models detecting them (total of 16 models) and their activity score Format:```Timestamp, number of models detecting it, activity score, Rank```

## Reference
Fernandes S., Fanaee-T H., Gama J. (2019), *Evolving Social Networks Analysis via Tensor Decompositions: From Global Event Detection Towards Local Pattern Discovery and Specification*. In: Kralj Novak P., Šmuc T., Džeroski S. (eds) Discovery Science. DS 2019. Lecture Notes in Computer Science, vol 11828. Springer, Cham. https://doi.org/10.1007/978-3-030-33778-0_29


