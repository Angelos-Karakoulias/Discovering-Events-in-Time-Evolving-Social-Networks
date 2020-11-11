from pylab import *
import numpy as np

models = 16
a = []
for i in range(models):
    a.append([])


a[0] = events_L6_r3

a[1] = events_L6_r5

a[2] = events_L6_r6

a[3] = events_L12_r3

a[4] = events_L12_r5

a[5] = events_L12_r6

a[6] = events_L24_r3

a[7] = events_L24_r5

a[8] = events_L24_r6

a[9] = events_L48_r3

a[10] =events_L48_r5

a[11] = events_L48_r6

a[12] = events_L72_r3

a[13] = events_L72_r5

a[14] = events_L72_r6

a[15] = events_L144_r3

#print(a)
b=[]

for i in range(models):
    for j in range(len(a[i])):
        flag = True
        if (i==0) and (j==0):
            b.append([a[i][0][0],1,a[i][0][1]])
        else :
            for k in range(len(b)):
                if b[k][0] == a[i][j][0]:
                    b[k][1] += 1
                    b[k][2] += a[i][j][1]
                    flag = False
                    break
            if flag == True:
                b.append([a[i][j][0],1,a[i][j][1]])

for i in range(len(b)):
    b[i][2] = int(b[i][2] / b[i][1])
#print(b)

#print(len(b))
final_evaluation = sorted(b,key=lambda l:l[1], reverse= True)
#print(final_evaluation)
final = np.zeros((144,3),dtype=int)
m=0
#print(len(final))
#print(final_evaluation)

for i in range(final_evaluation[0][1], final_evaluation[len(final_evaluation)-1][1] -1, -1):
    help = np.zeros((len(final_evaluation), 3), dtype=int)
    n=0
    flag = False
    for j in range(len(final_evaluation)):
        if final_evaluation[j][1] == i:
            flag = True
            help[n] = final_evaluation[j]
            n+=1
        elif final_evaluation[j][1] !=i and flag ==True:
            break
    help = sorted(help, key=lambda l:l[2],reverse=True)
    #print(i,n)
    #print(help)
    for j in range(n):
        final[m][0] = help[j][0]
        final[m][1] = help[j][1]
        final[m][2] = help[j][2]
        m+=1

#print(final)

#print(final_evaluation)
for i in range(144):
    flag = True
    for j in range(len(final_evaluation)):
        if i == final[j][0]:
            flag = False
            break
    if flag == True:
        final[m][0] = i
        m+=1

print(final)
