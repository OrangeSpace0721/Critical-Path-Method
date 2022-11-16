'''
XuDong Wu: 31196462
YuHao Wang: 31263046
Chakkwan Cheng: 31502105
Dian Yu: 31294952
'''

import numpy as np
import random
from numpy import inf as inf

x = np.array([[-1,2,10,-1,-1,-1],[-1,-1,0,-1,12,-1],[-1,-1,-1,1,-1,-1],[-1,-1,-1,-1,0,3],[-1,-1,-1,-1,-1,5],[-1,-1,-1,-1,-1,-1]])
y = np.array([[-1,4,-1,-1],[-1,-1,7,10],[-1,-1,-1,1],[-1,-1,-1,-1]])

def EET(matrix):
    r = list(range(0, matrix.shape[1]))                 #define the size of the matrix with r representing the row index
    c = list(range(0, matrix.shape[1]))                 #c represents the column index
    eet = [0 for k in matrix]                           #the final list of EET with the index representing the nodes repectively
    max_p = [0 for k in matrix]                         #Tempory List to manipulate
    for k in r:                                         #Loop over the entire row
        for p in c:                                     #Loop over the entire column
            if matrix[k,p] == -1:                       #If the nodes are not connected, skip it and move on
                continue
            if max_p[p] < matrix[k,p] + max_p[k]:       #If the tempory lables for node p are not the maximum, update it
                max_p[p] = matrix[k,p] + max_p[k]
        
    eet = max_p
    print("So the Earliest Event Time with respect to the nodes is", eet)
    return eet

def LET(matrix):
    min_p = [inf for k in matrix]                       #Tempory List to manipulate
    min_p[-1]=EET(matrix)[-1]
    matrix=np.transpose(matrix)
    r = list(range(0, matrix.shape[1]))                 #define the size of the matrix with r representing the column index
    c = list(range(0, matrix.shape[1]))                 #c represents the row index
    let = [inf for k in matrix]                         #the final list of E=LET with the index representing the nodes repectively
    for k in r[::-1]:                                   #Loop over the entire column in reverse
        for p in c:                                     #Loop over the entire row
            if matrix[k,p] == -1:                       #If the nodes are not connected, skip it and move on
                continue
            if min_p[p] > min_p[k] - matrix[k,p]:       #If the tempory lables for node p are not the minimum, update it
                min_p[p] = min_p[k] - matrix[k,p]
                
    let = min_p
    print("So the Latest Event Time with respect to the nodes is", let)
    return let

def TF(matrix):
    tf = np.empty(matrix.shape)
    tf[:] = inf                                         #define a matrix of infinity with (k, p) presenting the arc and the entries represents the total float of that arc.
    eet = EET(matrix)
    let = LET(matrix)
    r = list(range(0, matrix.shape[1]))                 #define the size of the matrix with r representing the row index
    c = list(range(0, matrix.shape[1]))                 #c represents the column index
    for k in r:                                         #Loop over the entire row
        for p in c:                                     #Loop over the entire column
            if matrix[k,p] == -1:                       #If the nodes are not connected, assign the float matrix -1 at arc (k,p)
                    tf[k,p] = matrix[k,p]
            else:
                tf[k,p] = let[p] - eet[k] - matrix[k,p]     #Assign the arc (k,p) the total float
    
    print("So the Total float with respect to the arcs is:")
    print(tf)
    return tf


def CPM(matrix):
    print("The adjacency matrix is:")
    print(matrix)
    tf=TF(matrix)
    critical = np.argwhere(tf == 0)                     #find the position of event that has tf=0
    print("The critical events are")
    print(critical)
    return critical


def rand_graph(x):
    matrix = np.empty((x,x))                            #Define a matrix size x with all entries -1
    matrix[:] = -1
    k = 1                                               #Define 2 counters thats used to slice the matrix
    l = 0
    
    for i in range(1,x):                                                       #Assign random values from 1 to 10 to column 1 to x, leaving column 0 as the starting node i.e. no in-degrees
        rand_index = np.random.randint(0,x, np.random.randint(5))              #select a random row (excluding the last row), at most 4 per column. This makes the last row our end node
        for j in rand_index:
                matrix[j,i] = random.randint(0,10)                             #Assign the value generated
    
    while k < x+1:                                      #This ensures the graph is acyclic by assigning -1 to the lower triangle of the matrix so the they cannot backtrack and form a cycle.
        while l < x+1:
            matrix[l:x,k-1:k] = [-1]*np.ones((x-l, 1))
            l = l+1
            break
        k = k+1
        
    for r in range(x-1):                                #Scans all row, excluding the last row as that will be the ending node
        if len(set(matrix[r,])) == 1:                                           #if the row has only one element when transformed into set notation (ie only contains -1)
            matrix[r, random.randint(r+1, x-1)] = random.randint(1, 10)         #Assign a random value to the row at a random column, excluding the column r, this is added to avoid having 2 ending node
        continue
    
    for r in range(1,x):                                #Scans all column, excluding the first column as that will be the starting node
        if len(set(matrix[:x,r:r+1].flatten())) == 1:                           #if the column has only one element when transformed into set notation (ie only contains -1)
            matrix[random.randint(0, r-1), r] = random.randint(1, 10)           #Assign a random value to the column at a random row, up the row r-1 so it doesnt affect the lower triangle. This is added to avoid have 2 starting node
        continue

    return matrix

#CPM(y)
#CPM(x)

CPM(rand_graph(30))
