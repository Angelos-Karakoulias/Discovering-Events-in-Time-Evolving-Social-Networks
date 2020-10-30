import pandas as pd
import os
import numpy as np
from pylab import *


def Wintended(factors, l_size, stations, a, y):
    print("We are in repetition",y)
    candidates = []  #the r flagged as candidates
    instants = []  #save timestamps flagged as instants
    instants_values = []
    per_data_time = np.zeros(l_size)
    per_data_station = np.zeros(stations)
    threshold_1 = 1.5
    threshold_2 = 2
    threshold_3 = 90
    threshold_4 = 6
    timestamp = 144
    nodes = []
    events = []
    for i in range(factors):
        instants_values.append([])
        instants.append([])


    # INSTANT_VALUE[rank][outliers] specification of instants (number 2 in WINTENDED)
    for j in range(factors):
        for i in range(l_size):
            per_data_time[i] = a[0][1][0][i][j]
        r = plt.boxplot(per_data_time, whis=threshold_2)
        # plt.show()
        top_points = []
        top_points = r["fliers"][0].get_data()[1]
        # print(top_points)
        if (len(top_points) != 0):
            candidates.append(j)
        for k in range(len(top_points)):
            instants_values[j].append(top_points[k])


    for i in range(factors):
        for k in range(len(instants_values[i])):
            for j in range(l_size):
                if instants_values[i][k] == a[0][1][0][j][i]:
                    instants[i].append(j)
                    break

    print("The instants for repetition ", y, "are", instants)


    copy = a

    # EXTRACT nodes that are not active at all --> first threshold, (1) in paper
    # SAVE the outliers of ar,br as active nodes

    for k in range(2):
        for i in range(factors):
            for j in range(stations):
                per_data_station[j] = a[0][1][k + 1][j][i]
            r = plt.boxplot(per_data_station,whis=threshold_1)
            # plt.show()
            top_points = []
            top_points = r["fliers"][0].get_data()[1]
            for j in range(stations):
                if copy[0][1][k + 1][j][i] < np.amin(top_points):
                    copy[0][1][k + 1][j][i] = 0

    # Nodes left after first threshold
    for k in range(2):
        for i in range(factors):
            n = 0
            p = 0
            for j in range(stations):
                if (copy[0][1][k + 1][j][i]) != 0:
                    n += 1
                else:
                    p += 1
            # print("left",n,"nodes and ",p,"nodes have deleted")

    # CREATION of an ADJ matrix
    adj = np.zeros((factors, l_size, stations, stations))
    per_data_station_1 = np.zeros(stations)
    help = np.zeros((stations, stations))
    for i in range(factors):
        if (len(instants[i])) != 0:  # if there are no outlier we don't make adj, because its not a candidate
            for j in range(stations):
                per_data_station[j] = copy[0][1][1][j][i]
                per_data_station_1[j] = copy[0][1][2][j][i]
            help = np.outer(per_data_station, per_data_station_1)
            for t in range(l_size):
                adj[i][t] = help * a[0][1][0][t][i]
    #calculate the degree of the adjacency metric
    degree = np.zeros((factors, l_size, stations))

    for i in range(factors):
        if (len(instants[i])) != 0:
            for j in range(l_size):
                for k in range(stations):
                    degree[i][j][k] = degree[i][j][k] + (
                            (np.sum(adj[i][j], axis=0)[k]) + (np.sum(adj[i][j], axis=1)[k]) - adj[i][j][k][k])

    per_data_time = np.zeros(l_size)
    per_data_station = np.zeros(stations)
    degree_non_negative = np.zeros((factors, l_size))

    # CALCULATE DENSITY OF SUBGRAPH FOR EVERY TIMESTAMP
    density = np.zeros((factors, l_size))

    for i in range(factors):
        if (len(instants[i])) != 0:
            for j in range(l_size):
                n = 0
                for k in range(stations):
                    n = n + sum(adj[i][j][k])
                density[i][j] = n

    #Calculation of AVERAGE WEIGHTED NODE DEGREE INDUCED By Vr'
    average_node_degree = np.zeros((factors, l_size))

    for i in range(factors):
        if (len(instants[i])) != 0:
            for j in range(l_size):
                average_node_degree[i][j] = np.mean(degree[i][j])
    #third threshold about the strictness of cleaning procedure
    katwfli = np.zeros((factors, l_size))

    for i in range(factors):
        if len(instants[i]) != 0:
            for j in range(l_size):
                katwfli[i][j] = np.percentile(degree[i][j],threshold_3)

    solu_1 = np.zeros((factors, l_size))  #How many nodes have left after cleaning procedure for every rank

    for i in range(factors):
        if (len(instants[i])) != 0:
            for j in range(l_size):
                sort = np.argsort(degree[i][j])
                n = 0
                for k in range(stations):
                    if degree[i][j][sort[stations - 1 - k]] > np.mean(katwfli[i]):
                        n = n + 1
                    else:
                        break
                solu_1[i][j] = n
    #solu[rank][timestamp] expresses the number of nodes that each timestamp contain after cleaning procedure

    #creation of adj_2, degree_2 after cleaning procedure
    adj_2 = np.copy(adj)
    per_data_station_1 = np.zeros(stations)
    degree_2 = degree.copy()

    for i in range(factors):
        if (len(instants[i])) != 0:
            for j in range(l_size):
                sort = np.argsort(degree[i][j])
                for k in range((stations - int(solu_1[i][j]))):
                    adj_2[i][j][sort[k]] = 0
                    adj_2[i][j][:, sort[k]] = 0
                    degree_2[i][j][sort[k]] = 0



    density_2 = np.zeros((factors, l_size))
    density_2_mean = np.zeros((factors, l_size))
    for i in range(factors):
        if (len(instants[i])) != 0:
            for j in range(l_size):
                n = 0
                for k in range(stations):
                    n = n + sum(adj_2[i][j][k])
                density_2[i][j] = n

    density_3 = np.zeros((factors, l_size))

    for i in range(factors):
        if (len(instants[i])) != 0:
            for j in range(l_size):
                if density[i][j] == 0 or density_2[i][j] == 0:
                    density_3[i][j] = 0

                else:
                    density_3[i][j] = density_2[i][j] / density[i][j]
    instant_score = []  # Instant score expresses the number of metric that each instant fullfil
    for i in range(factors):
        if len(instants[i]) != 0:
            instant_score.append(np.zeros((len(instants[i])), dtype=int))
        else:
            instant_score.append([])

    # METRIC 1
    for i in range(factors):
        if len(instants[i]) != 0:
            r = plt.boxplot(density[i], whis=threshold_4)
            # plt.show()
            top_points = []
            top_points = r["fliers"][0].get_data()[1]
            # print(top_points, len(top_points))
            n = 0
            for j in range(len(top_points)):
                flag = False
                for k in range(len(instants[i])):
                    if int(top_points[j]) == int(density[i][instants[i][k]]):
                        instant_score[i][k] = instant_score[i][k] + 1
                        flag = True
                        break
                if flag == False:
                    n += 1


    length_of_outlier = np.zeros((factors), dtype=int) #number of outliers on metric2

    # METRIC 2
    for i in range(factors):
        if len(instants[i]) != 0:
            r = plt.boxplot(average_node_degree[i], whis = threshold_4)
            # plt.show()
            top_points = []
            top_points = r["fliers"][0].get_data()[1]
            # print(top_points, len(top_points))
            length_of_outlier[i] = len(top_points)
            n = 0
            for j in range(len(top_points)):
                flag = False
                for k in range(len(instants[i])):
                    if (top_points[j]) == (average_node_degree[i][instants[i][k]]):
                        instant_score[i][k] = instant_score[i][k] + 1
                        flag = True
                        break
                if flag == False:
                    n += 1

            print("after metric 2 the instant score is the following", instant_score)

    # metric3
    for i in range(factors):
        if (len(instants[i])) != 0:
            for j in range(length_of_outlier[i]):
                for k in range(len(instants[i])):
                    r = argsort(density_3[i])
                    if r[l_size - 1 - j] == instants[i][k]:
                        instant_score[i][k] = instant_score[i][k] + 1

    #print("Here we print the final formation of instant score\n", instant_score)

    # Creation of event list
    n = 0
    for i in range(factors):
        if (len(instants[i])) != 0:
            for j in range(len(instant_score[i])):
                if instant_score[i][j] == 3:
                    n += 1
    events = (np.zeros((n, 5), dtype=int))

    #if an instant fullfil all of 3 metrics, is flagged as event and we save its timestamp, its activity score and its rank
    n = 0
    for i in range(factors):
        if (len(instants[i])) != 0:
            for j in range(len(instant_score[i])):
                if instant_score[i][j] == 3:
                    events[n][0] = int(instants[i][j] + (y * l_size))
                    events[n][1] = instant_score[i][j]
                    events[n][2] = int(solu_1[i][instants[i][j]])
                    events[n][4] = i
                    n += 1
    print("Events at first\n", events)

    #if we have same timestamp for more than one ranks, then we keep this event with higher activity score
    m = []
    events = list(events)
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            if events[i][0] == events[j][0]:
                if events[i][2] < events[j][2]:
                    if (events[i][3] == 0):
                        m.append(i)
                        events[i][3] = 1
                elif events[i][2] > events[j][2]:
                    if events[j][3] == 0:
                        m.append(j)
                        events[j][3] = 1

    m = sorted(m, reverse=True)
    for i in range(len(m)):
        del events[m[i]] #delete the event with the lower activity score

    print("Follow the total events\n", events)


    # Here i store all participating nodes for each event
    for i in range(len(events)):
        n = 0
        for j in range(stations):
            if y != 0:
                if degree_2[events[i][4]][(events[i][0]) % (l_size * y)][j] != 0:
                    nodes.append([j, events[i][0]])
                    n += 1
            else:
                if degree_2[events[i][4]][(events[i][0]) % (l_size)][j] != 0:
                    nodes.append([j, events[i][0]])
                    n += 1
    return (events,nodes)
