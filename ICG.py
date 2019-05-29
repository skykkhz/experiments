from __future__ import division
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:26:32 2018

@author: Administrator
"""

from igraph import *
import Ground_Truth as GT
import initial_graph as ig  
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
    
def density(g,cluster):
    D = 0
    for community in cluster:
        internal = len(g.es.select(_within = (community)))
        degree = sum([g.vs()[node].degree() for node in community])
        external = degree - 2*internal
        number = len(community)
        
        D += (internal - external)/number
        
    return D



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

    for community in clusters:
        temp = [node for node in community if node in drop_node]
        for v in temp:
            community.remove(v)
#        for node in community:
#            if node in drop_node:
#                community.remove(node)
#                
        if community == []:
            clusters.remove(community)
                
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
#        if iterations > 30:
#            break
#    print membership
    membership = [0 for i in range(n)]
    for i in range(len(clusters)):
        for index in clusters[i]:
            membership[index] = i
    return membership, clusters
                        

def main():
#    pathList = ['0.05','0.1','0.15','0.2','0.25','0.3','0.35','0.4','0.45','0.5','0.55','0.6']
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\karate\\karate.gml")
    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\polbooks\\polbooks.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\dolphins\\dolphins.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\Football\\football.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\netscience\\netscience.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\lesmis\\lesmis.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\lesmis\\lesmis.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\jazz\\jazz1.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\metabolic\\metabolic.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\adjnoun\\adjnoun.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\celegansneural\\celegansneural.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\amazon\\amazon.gml")
#    graph = ig.graph('C:\\Users\\Administrator\\Desktop\\LFR\\GN\\0.45\\network.dat')
##    graph = ig.graph('C:\\Users\\Administrator\\Desktop\\dataset\\gml\\metabolic.txt')
#    True_partition = GT.ground_truth("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\Football\\football_comm.dat")
#    True_partition = GT.ground_truth("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\karate\\karate1.dat")
#    True_partition = GT.ground_truth("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\dolphins\\dolphins.dat")
    True_partition = GT.ground_truth("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\polbooks\\polbooks_comm.dat")
#    True_partition = GT.ground_truth('C:\\Users\\Administrator\\Desktop\\LFR\\GN\\0.45\\community.dat')
    
#    graph = ig.graph('C:\\Users\\Administrator\\Desktop\\LFR\\n=1000\\d=15,maxc=50,minc=20\\0.7\\network.dat')
#    True_partition = GT.ground_truth('C:\\Users\\Administrator\\Desktop\\LFR\\n=1000\\d=15,maxc=50,minc=20\\0.7\\community.dat')
#    alpha = [1,2,3,4,5,6,7,8,9,10]
#    belta = [0.05,0.1,0.15,0.2,0.25,0.3]

    n = graph.vcount()
    m = graph.ecount()
    best_cluster = []
    print n,m
    Q_sum = []
    Time_sum = 0
    NMI_list = []
    for i in range(10):
        start = time.time()
    #构造       
        clusters, node_list = construction(graph)

    #局部搜索
        solution, clusters = localsearch(graph,  clusters)

        Gbest = copy.copy(solution)
#        print Gbest
        T_init = 0.025*graph.modularity(solution)
        T = T_init
        interval = time.time()-start
        while interval < n/10:
            
#        for i in range(30):
            Q1 = graph.modularity(solution)

            incumbent_clusters = copy.deepcopy(clusters)

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
            solution, clusters = localsearch(graph, clusters)
#                    print graph.modularity(solution)
            
            Q2 = graph.modularity(solution)
            
            if Q2 > graph.modularity(Gbest):
                Gbest = copy.copy(solution)
                best_cluster = copy.deepcopy(clusters)

                
            
            
            P = random.random()
            if Q2 < Q1 and P > math.exp((Q2-Q1)/T):
#                print clusters
#                print incumbent_clusters
                clusters = copy.deepcopy(incumbent_clusters)
                
#                node_list = copy.copy(incumbent_list)
                T = T_init
            elif Q2 >= Q1:
                T = T_init
            else:
                T = T*0.9
            
            interval = time.time()-start

                
#        print Gbest        
        graph.vs["community"] = Gbest
#        graph.write_gml("C:\\Users\\Administrator\\Desktop\\polbooks.gml")   
        print graph.modularity(Gbest)
        print density(graph,best_cluster)
        Q_sum.append(graph.modularity(Gbest))        
#        print graph.modularity(Gbest)
        NMI = compare_communities(Gbest,True_partition,method='nmi',remove_none=False)
        print 'NMI',NMI
#        graph.write_gml("C:\\Users\\Administrator\\Desktop\\b.gml")
        NMI_list.append(NMI)
        end = time.time()
        t = end-start
        Time_sum += t
    NMI = Stats(NMI_list)    
    modularity = Stats(Q_sum)
    print 'maxNMI',NMI.max()
    print 'avgNMI',NMI.avg()
    print 'minNMI',NMI.min()
    print 'stdevNMI',NMI.stdev()
    
    print "maxQ",modularity.max()
    print "avgQ",modularity.avg()
    print "minQ",modularity.min()
    print "stdevQ",modularity.stdev()
#    print "time",Time_sum/10        
#    print 'NMI',NMI_sum/10
if __name__ == '__main__':
    main()