# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from __future__ import division
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:26:32 2018

@author: Administrator
"""

from igraph import *
#import Ground_Truth as GT
#import initial_graph as ig  
import math
import random
import copy
import time
import numpy as np

class Stats:
  
    def __init__(self, sequence):
        # sequence of numbers we will process
        # convert all items to floats for numerical processing
        self.sequence = [float(item) for item in sequence]
  
    def sum(self):
        if len(self.sequence) < 1:
            return None
        else:
            return sum(self.sequence)
  
    def count(self):
        return len(self.sequence)
  
    def min(self):
        if len(self.sequence) < 1:
            return None
        else:
            return min(self.sequence)
  
    def max(self):
        if len(self.sequence) < 1:
            return None
        else:
            return max(self.sequence)
  
    def avg(self):
        if len(self.sequence) < 1:
            return None
        else:
            return sum(self.sequence) / len(self.sequence)   
  
    def median(self):
        if len(self.sequence) < 1:
            return None
        else:
            self.sequence.sort()
            return self.sequence[len(self.sequence) // 2]
  
    def stdev(self):
        if len(self.sequence) < 1:
            return None
        else:
            avg = self.avg()
            sdsq = sum([(i - avg) ** 2 for i in self.sequence])
            stdev = (sdsq / (len(self.sequence) - 1)) ** .5
            return stdev
  
    def percentile(self, percentile):
        if len(self.sequence) < 1:
            value = None
        elif (percentile >= 100):
            sys.stderr.write('ERROR: percentile must be < 100.  you supplied: %s\n'% percentile)
            value = None
        else:
            element_idx = int(len(self.sequence) * (percentile / 100.0))
            self.sequence.sort()
            value = self.sequence[element_idx]
        return value
    
def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功")
    
    

def construction(G):
    
#    candidate_list = list(G.vs())
#    candidate_list = [v.index for v in G.vs()]
    candidate_list = [i for i in range(G.vcount())]
    node_list = []
#    membership = [i for i in range(G.vcount())]

    m = G.ecount()
    n = G.vcount()
    clusters = []
#初始化
    node = random.choice(candidate_list)
#print node
    candidate_list.remove(node)
    
    node_list.append(node)
    
    clusters.append([node])
    
    while candidate_list != []:    
        node = random.choice(candidate_list)
        candidate_list.remove(node)
        node_list.append(node)
#    print node.degree()
#    before = g.modularity(membership)
#    after = g.modularity(membership)
        MAX_Q = 0
        pos = -1
        for index,community in enumerate(clusters):    
            Kbv = G.es.select(_between = ([node], community))
        
            db = sum([G.vs()[v].degree() for v in community])
            delta_Q = 1/m * len(Kbv) - G.vs[node].degree()/(2*m**2)*db
            if delta_Q > MAX_Q:
                MAX_Q = delta_Q
                pos = index
    
        if MAX_Q > 0:
            clusters[pos].append(node)
        else:
            clusters.append([node])

#print clusters
        
#    membership = [0 for i in range(G.vcount())]
#    for i in range(len(clusters)):
#        for index in clusters[i]:
#            membership[index] = i
            
    return  clusters, node_list
       
#print g.modularity(membership)
#print membership
def Modularity(G,membership):
    m = G.ecount()
    Q = 0
    for u in G.vs():
        if membership[u.index] == None:
            continue
        for v in G.vs():
            if membership[v.index] == None:
                continue
                
            if v in u.neighbors():
                Auv = 1
            else:
                Auv = 0
                
            if membership[u.index] == membership[v.index]:
                Q += 1/(2*m) * (Auv - u.degree()*v.degree() / (2*m))
    return Q   


def destruction(G,clusters,node_list, belta):

    cut_len = int(G.vcount() * (1-belta))
#    drop_node = []
#    preserve_node = []
#    for node in node_list:
#        
#        if random.random() < belta:
#             drop_node.append(node)
#        else:
#            preserve_node.append(node)
            
    preserve_node = node_list[:cut_len]

    drop_node = node_list[cut_len:]
    
    for i in range(len(clusters)-1,-1,-1):
        for j in range(len(clusters[i])-1,-1,-1):
            if clusters[i][j] in drop_node:
                clusters[i].pop(j)
                
        if clusters[i] == []:
            clusters.pop(i)

#    for community in clusters:
#        temp = [node for node in community if node in drop_node]
#        for v in temp:
#            community.remove(v)
#    community for community in cluster
##                
#        if community == []:
#            clusters.remove(community)
                
#    membership = [None for i in range(G.vcount())]
#    for i in range(len(clusters)):
#        for index in clusters[i]:
#            membership[index] = i
#    print '破坏之后社区划分', clusters            
    return preserve_node, drop_node, clusters




def crousel(G, clusters,preserve_node,drop_node, alpha):
#    print clusters
    m = G.ecount()
    iterations = int(alpha*G.vcount())
#    print iterations
    for i in range(iterations):
#        print '迭代', i


        
        node = preserve_node.pop(0)
#        print '丢弃节点', node
        drop_node.append(node)
#        membership[node] = None
#        print drop_node
#        print preserve_node
        for community in clusters:
            for v in community:
                if node == v:
                    community.remove(v)
                    if community == []:
                        clusters.remove([])
        
        
        selected_node = random.choice(drop_node)
        drop_node.remove(selected_node)
        preserve_node.append(selected_node)
#        print '选择节点', selected_node
#        print drop_node
#        print preserve_node
        
        MAX_Q = 0
        pos = -1
        for index,community in enumerate(clusters):    
            Kbv = G.es.select(_between = ([selected_node], community))
        
            db = sum([G.vs()[v].degree() for v in community])
            delta_Q = 1/m * len(Kbv) - G.vs[selected_node].degree()/(2*m**2)*db
            if delta_Q > MAX_Q:
                MAX_Q = delta_Q
                pos = index
                

    
        if MAX_Q > 0:
            if selected_node not in clusters[pos]:    
                clusters[pos].append(selected_node)
        else:
            clusters.append([selected_node])
            
#        print '社区划分',clusters
            
#    membership = [None for i in range(G.vcount())]
#    for i in range(len(clusters)):
#        for index in clusters[i]:
#            membership[index] = i
            
    return clusters,drop_node
            
def reconstruction(G,clusters,drop_node):
    m = G.ecount()
    random.shuffle(drop_node)
    for node in drop_node:
        MAX_Q = 0
        pos = -1
        for index,community in enumerate(clusters):    
            Kbv = G.es.select(_between = ([node], community))
        
            db = sum([G.vs()[v].degree() for v in community])
            delta_Q = 1/m * len(Kbv) - G.vs[node].degree()/(2*m**2)*db
            if delta_Q > MAX_Q:
                MAX_Q = delta_Q
                pos = index
    
        if MAX_Q > 0:
            clusters[pos].append(node)
        else:
            clusters.append([node])
        
    
#    membership = [0 for i in range(G.vcount())]
#    for i in range(len(clusters)):
#        for index in clusters[i]:
#            membership[index] = i
            
    return clusters


def localsearch(G, clusters):
    n = G.vcount()
    m = G.ecount()
    node_list = [i for i in range(n)]
    count = 0
#    iterations = 0
    while count < n:
#        iterations += 1
        count = 0
        random.shuffle(node_list)
        for node in node_list:
            Q = []
            degree = G.vs()[node].degree()
            for community in clusters:
                if node in community:
                    self_community = community
                    Kav = G.es.select(_between = ([node], self_community))
                    da = sum([G.vs()[v].degree() for v in self_community])
                    break            
            for index,community in enumerate(clusters):
                if node in community:
                    delta_Q = 0
                    before = index
                    Q.append(delta_Q)
                else:
                    Kbv = G.es.select(_between = ([node], community))
                    db = sum([G.vs()[v].degree() for v in community])
#                    delta_Q = (1/m) * len(Kbv) + (degree/(2*m**2))*(da - db - degree)
                    delta_Q = (1/m) * (len(Kbv)-len(Kav)) + (degree/(2*m**2))*(da - db - degree)
#                    print '1111111111'
#                    print delta_Q, community
#                    print '2222222222'
                    Q.append(delta_Q)
#            print clusters.count([])
#            print max(Q)
#            print Q
#            print node
            if max(Q) > 0:
                pos = Q.index(max(Q))
#                print before,pos
#                print clusters[before], clusters[pos]
                clusters[pos].append(node)
    
                clusters[before].remove(node)
                if clusters[before] == []:
                    del clusters[before]
#               membership[node] = pos

            else:
                count += 1

#    membership = [0 for i in range(n)]
#    for i in range(len(clusters)):
#        for index in clusters[i]:
#            membership[index] = i
    return clusters
                        
def trans(clusters,G):
    n = G.vcount()
    membership = [0 for i in range(n)]
    for i in range(len(clusters)):
        for index in clusters[i]:
            membership[index] = i
    return membership
    
def main():
#    pathList = ['0.05','0.1','0.15','0.2','0.25','0.3','0.35','0.4','0.45','0.5','0.55','0.6']
#    graph = Graph.Read_GML("C:\\Users\\46296\\\\Desktop\\dataset\\gml\\karate\\karate.gml")
#    graph = Graph.Read_GML("C:\\Users\\46296\\Desktop\\dataset\\gml\\polbooks\\polbooks.gml")
#    graph = Graph.Read_GML("C:\\Users\\46296\\Desktop\\dataset\\gml\\dolphins\\dolphins.gml")
#    graph = Graph.Read_GML("C:\\Users\\46296\\Desktop\\dataset\\gml\\football\\football.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\netscience\\netscience.gml")
#    graph = Graph.Read_GML("C:\\Users\\46296\\Desktop\\dataset\\gml\\lesmis\\lesmis.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\lesmis\\lesmis.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\jazz\\jazz1.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\metabolic\\metabolic.gml")
#    graph = ig.graph('C:\\Users\\Administrator\\Desktop\\LFR\\GN\\0.5\\network.dat')
#    True_partition = GT.ground_truth('C:\\Users\\Administrator\\Desktop\\LFR\\GN\\0.5\\community.dat')
    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\amazon\\amazon.gml)

    n = graph.vcount()
    m = graph.ecount()
    start = time.time()
#构造       
    clusters, node_list = construction(graph)

#局部搜索
    clusters = localsearch(graph,  clusters)
    solution = trans(clusters,graph)
    Q_best = graph.modularity(solution)
    Q1 = graph.modularity(solution)
    print '初始模块度', graph.modularity(solution)
    T_init = 0.025*graph.modularity(solution)
    T = T_init
    Q = [graph.modularity(solution)]
    Time = [0]
    interval = time.time()-start

    while interval < n/10:


#        Q1 = graph.modularity(solution)

        incumbent_clusters = copy.deepcopy(clusters)
#        incumbent_solution = copy.copy(solution)
#破坏    
        preserve_node, drop_node, clusters = destruction(graph, clusters, node_list, 0.3)
#旋转
#        print graph.modularity(solution)
#        print '破坏解'
#        print clusters
#        print solution
#        print '扰动部分'
#        print preserve_node, drop_node
        clusters, drop_node = crousel(graph,clusters,preserve_node, drop_node, 2)
#        print clusters
#        print solution
#        print graph.modularity(solution)
#重构
        clusters = reconstruction(graph,clusters, drop_node)
#        print '重构解'
#        print clusters
#        print solution
#        print graph.modularity(solution)
        clusters = localsearch(graph, clusters)
        solution = trans(clusters,graph)
        
        Q2 = graph.modularity(solution)
        
        if Q2 > Q_best:
            Q_best = Q2

        P = random.random()
        interval = time.time()-start
        Time.append(interval)
        if Q2 >= Q1:
            Q1 = Q2 
            print Q2
            Q.append(Q2)
            
        elif P < math.exp((Q2-Q1)/T):
            Q1 = Q2
#            print math.exp((Q1-Q2)/T)
            print Q2
            Q.append(Q2)
        else:
            clusters = copy.deepcopy(incumbent_clusters)
#            solution = copy.copy(incumbent_solution)
            print Q1
            Q.append(Q1)
            

        T = T*0.9

    text_save("E://ICGModlesmis.txt",Q)
    text_save("E://ICGTimelesmis.txt",Time)
#        interval = time.time()-start
        
    print  Q_best
        
        

if __name__ == '__main__':
    main()

