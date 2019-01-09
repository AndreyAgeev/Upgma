# -*- coding: utf-8 -*-

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
def change_cluster(cluster, max_ind, i, j):
    for ind in range(j, len(cluster)):
        cluster[ind] = cluster[ind] + 1   
    for ind in range(0, len(cluster)):
        if(cluster[ind] < max_ind):
            print(cluster[ind], end = ' ')
    print(" ")
    return cluster

def right_ind(cluster, ind):
    return cluster[ind]

def printResult(result):
    for ind in range(0, len(result)):
        if(len(result[ind]) != 0):
            print("cluster --> ", end = " ")
            print(ind, end = " ")
            while(len(result[ind]) != 0):
                print(result[ind].pop(), end = " ")
            print(" ")
    

class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.children = []
        if parent:
            self.parent.children.append(self)
            
def print_tree(current_node, indent="", last='updown'):

    nb_children = lambda node: sum(nb_children(child) for child in node.children) + 1
    size_branch = {child: nb_children(child) for child in current_node.children}

   
    up = sorted(current_node.children, key=lambda node: nb_children(node))
    down = []
    while up and sum(size_branch[node] for node in down) < sum(size_branch[node] for node in up):
        down.append(up.pop())

    for child in up:     
        next_last = 'up' if up.index(child) is 0 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " )
        print_tree(child, indent=next_indent, last=next_last)

   
    if last == 'up': start_shape = '┌'
    elif last == 'down': start_shape = '└'
    elif last == 'updown': start_shape = ' '
    else: start_shape = '├'

    if up: end_shape = '┤'
    elif down: end_shape = '┐'
    else: end_shape = ''

    print ('{0}{1}{2}{3}'.format(indent, start_shape, current_node.data, end_shape))

    for child in down:
        next_last = 'down' if down.index(child) is len(down) - 1 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " )
        print_tree(child, indent=next_indent, last=next_last)
        
        
def createTree(data):
    Tree = Node("parent")
   
    parent = None
    max_height = 0
    for ind in range(0, len(data)):
        nodes = []
        height = len(data[ind]) + 1
        if(max_height < height):
            max_height = height
        node = Node(ind)
        nodes.append(node)
        if(len(data[ind]) != 0):
            while(len(data[ind]) != 0):
                new_data = data[ind].pop()
                node = Node(new_data)
                nodes.append(node)
            if(height > 2):
                parent = None
                for ind in range(0, len(nodes)):
                    if(len(nodes) - 1 - ind == len(nodes) - 1):
                        print(nodes[len(nodes) - 1 - ind].data)
                        node = Node(nodes[len(nodes) - 1 - ind].data, Tree)
                    else:
                        node = Node(nodes[len(nodes) - 1 - ind].data, parent)
                    if(height % 2 != 0):            
                        parent = node
                    height = height - 1
                
            else:
                parent = Tree
                check_height = 0
                while (max_height > height + check_height):
                        node = Node("empty", parent)
                        check_height = check_height + 1
                        parent = node
                if(check_height == 0):
                    parent = None
                for ind in range(0, len(nodes)):
                    print(nodes[len(nodes) - 1 - ind].data)
                    node = Node(nodes[len(nodes) - 1 - ind].data, parent)
                    if(height % 2 != 0):            
                        parent = node
                    height = height - 1
                
                
    print_tree(Tree)
            
def upgma(matrix):
    node =[set() for i in range(len(matrix))]   
    cluster = []
    for seq in matrix:
        cluster.append(1)
    count_step = len(matrix) - 2
    tree_ind = []
    _dict = {}
    new_cluster = [i for i in range(len(matrix))]
    max_ind = len(matrix)
    for step in range(0, count_step):
        i, j, height = findSimilarSequences(matrix)
        ind_cluster = right_ind(new_cluster, i)
        ind_add_elem = right_ind(new_cluster, j)
        node[ind_cluster].add(ind_add_elem)
        print(node)
        matrix = rebuilding(matrix, i, j, cluster)
        
        new_cluster = change_cluster(new_cluster, max_ind, i, j)
        
        cluster[i] = cluster[i] + cluster[j]
        tree_ind.append((i,j))
        _dict[height] = (i, j)  
    i, j, height = findSimilarSequences(matrix)
    _dict[height] = (i, j)
    print(_dict.items())
    
  #  printResult(node)
    createTree(node)
    


  
def main():
    matrix = [[0, 2.06, 4.03, 6.32, 2.08],[2.06, 0, 3.50, 4.12, 5.43],[4.03, 3.50, 0, 2.25, 3.65],[6.32, 4.12, 2.25, 0, 4.81],[2.08, 5.43, 3.65, 4.81, 0]]
    upgma(matrix)

    
    
main()
