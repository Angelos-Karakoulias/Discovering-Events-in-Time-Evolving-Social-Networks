import pandas as pd
from pylab import *
from tensorly.decomposition import parafac
from scipy.sparse import coo_matrix
from method import Wintended

candidates = []  # which r are candidates
instants = []  # t as an instant
instants_values = []
stations = 551
l_size = 12
factors = 3
per_data_time = np.zeros(l_size)
per_data_station = np.zeros(stations)
antistixisi =[]
antistixisi.append(0)
timestamp = 144
times = int(timestamp / l_size) #number of repetitions until all data are covered
final_event = []
nodes = []
events = []
final_events = []
final_nodes = []



df = pd.read_csv(ianeikosi.csv)
df = df.rename(columns = {'Start station number' : 'start number', 'End station number':'end number','Start date':'start date'}, inplace = False)
#We  keep the data from the first 6 days
df = df.loc[df['start date'] < '2020-01-07 00:00:30']
table1 = np.zeros((31305),dtype=int)
df['start date'] = pd.to_datetime(df['start date'])



df2 = df.loc[0:31304,'start date'].dt.hour
df3 = df.loc[0:31304,'start date'].dt.day
df3 = df3.tolist()
df2 = df2.tolist()
#Here we correspond every journey (0-31304) to 1-144 hours (every hour of the 6 days).

for i in range(len(table1)):
    table1[i] = int(df2[i])+ ((df3[i]-1)*24)

df2 = df.loc[:,['start number','end number']]
df3 = df2['start number'].tolist()
df2 = df['end number'].tolist()
#In list antistixisi we calculate the participating stations
for i in range(31305):
    flag = False
    for j in range(len(antistixisi) - 1 ):
        if df3[i] == antistixisi[j]:
            flag= True
            break
    if flag == False:
        antistixisi[(len(antistixisi)-1)] = df3[i]
        antistixisi.append(0)
for i in range(31305):
    flag = False
    for j in range(len(antistixisi) - 1 ):
        if df2[i] == antistixisi[j]:
            flag= True
            break
    if flag == False:
        antistixisi[(len(antistixisi)-1)] = df2[i]
        antistixisi.append(0)
del antistixisi[-1]

#table --> 3D adjacency matrix of all data
table = np.zeros((timestamp,stations,stations),dtype=int)
for i in range (31305):
    flag= False
    flag2=False
    deiktis2=-1
    flag3=False
    deiktis3=-1
    for j in range(len(antistixisi)):
        if (flag2==False and antistixisi[j]==df2[i]):
            flag2 = True
            deiktis2 = j
        if (flag3 == False and antistixisi[j] == df3[i]):
            flag3 = True
            deiktis3 = j
        if (flag3 == True and flag2==True):
            flag = True
            break
    if flag == True:
        table[(table1[i])][deiktis3][deiktis2] = table[(table1[i])][deiktis3][deiktis2] + 1


print(len(table))  #3D adjacency metrix of all data


for y in range(times): # Event detection for every window
    nodes = []
    events = []

    table3 = table[(y * l_size):((y * l_size) + l_size)][:][:] #3d Adjacency matrix of the current window
    print(len(table3))


    table3 = coo_matrix.asfptype(table3)

    a = parafac(table3, rank=factors, return_errors=True, non_negative=True) #Tensor decomposition of current window
    (events,nodes) = Wintended(factors, l_size, stations, a, y)  #We call Wintended by sending the values factors (R), l_size(L), stations ($ of stations), a (decomposed window), y the repetition.
    print(events)
    #print("edw nodes",nodes)
    for i in range(len(events)):
        final_event.append([events[i][0], events[i][2]]) #we add currents events to total events
    for i in range(len(nodes)):
        final_nodes.append([nodes[i][0],nodes[i][1]])  #we add currents participating nodes to total participating nodes

print(final_event,len(final_events))
print(final_nodes,len(final_nodes))
