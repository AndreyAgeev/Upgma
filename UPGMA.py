# -*- coding: utf-8 -*-

import numpy as np
from scipy.cluster.hierarchy import linkage
import matplotlib.pyplot as plt

def findSimilarSequences(matrix, _min = 10000):
    for cols in range(0, len(matrix)):
        for rows in range(0, len(matrix[0])):
            if(rows == cols):
                continue
            if(matrix[cols][rows] < _min):
                ans = cols, rows, matrix[cols][rows]
                _min = matrix[cols][rows]
    return ans

def rebuilding(matrix, i, j, C):
    new_matrix = [[0] * (len(matrix)-1) for i in range(len(matrix[0])-1)]
    for rows in range(0, len(matrix)):
        
        if(i == rows or j == rows):
           continue
    
        if(rows-1 == -1):
           
            new_matrix[i][rows] = new_matrix[rows][i] = (C[i]*matrix[i][rows] + C[j]*matrix[j][rows])/(C[i] + C[j])
        elif(rows -1 != -1 and len(matrix)-1 != 2):
            new_matrix[i][rows-1] = new_matrix[rows-1][i] = (C[i]*matrix[i][rows] + C[j]*matrix[j][rows])/(C[i] + C[j])
        else: 
            new_matrix[i][rows] = new_matrix[rows][i] = (C[i]*matrix[i][rows] + C[j]*matrix[j][rows])/(C[i] + C[j])
        
        
    for cols in range(0, len(new_matrix)):
        for rows in range(cols, len(new_matrix[0])):
            if(len(new_matrix) == 2):
                new_matrix[0][0] = new_matrix[1][1] = 0.0
                break
            if(rows == cols):
                new_matrix[cols][rows] = 0.0
                continue

            if(new_matrix[cols][rows] == 0.0 ):
                if(cols == 0):
                    new_matrix[cols][rows] = new_matrix[rows][cols] = matrix[cols][rows+1]
                elif(rows == 0):
                    new_matrix[cols][rows] = new_matrix[rows][cols] = matrix[cols+1][rows]
                else:
                    new_matrix[cols][rows] = new_matrix[rows][cols] = matrix[cols+1][rows+1]
    return new_matrix
          
def upgma(matrix):
    C = []
    for seq in matrix:
        C.append(1)
    count_step = len(matrix) - 2
    tree_ind = []
    _dict = {}
    for step in range(0, count_step):
        i, j, height = findSimilarSequences(matrix)
        matrix = rebuilding(matrix, i, j, C)
        C[i] = C[i] + C[j]
        tree_ind.append((i,j))
        _dict[height] = (i, j)
        for x in range(0, len(matrix)):
            print(" ")
            for y in range(0, len(matrix[0])):
                print(matrix[x][y], end = ' , ') 
        print(" ")
    i, j, height = findSimilarSequences(matrix)
    _dict[height] = (i, j)
    for x in tree_ind:
        print(x)
    print(_dict.items())

from scipy.cluster.hierarchy import dendrogram


  
def main():
    matrix = [[0, 2.06, 4.03, 6.32, 2.08],[2.06, 0, 3.50, 4.12, 5.43],[4.03, 3.50, 0, 2.25, 3.65],[6.32, 4.12, 2.25, 0, 4.81],[2.08, 5.43, 3.65, 4.81, 0]]
    upgma(matrix)
    linkage_matrix = linkage(matrix,  "average")
    show_leaf_counts = False
    dendrogram(linkage_matrix,
               color_threshold=1,
               p=5,
               show_leaf_counts=show_leaf_counts,
               )

    
    plt.show()
    
    
main()