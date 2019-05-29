from __future__ import division
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 08 12:04:27 2018

@author: Administrator
"""
from igraph import *

import random
import copy
import time
import Ground_Truth as GT
import initial_graph as ig  

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
    

def construction(G):
    
    candidate_list = list(G.vs())

    membership = [i for i in range(G.vcount())]

    m = G.ecount()
    n = G.vcount()
    clusters = []
#初始化
    node = random.choice(candidate_list)
#print node
    candidate_list.remove(node)

    clusters.append([node.index])
    while candidate_list != []:    
        node = random.choice(candidate_list)
        candidate_list.remove(node)
#    print node.degree()
#    before = g.modularity(membership)
#    after = g.modularity(membership)
        MAX_Q = 0
        pos = -1
        for index,community in enumerate(clusters):    
            Kbv = G.es.select(_between = ([node.index], community))
        
            db = sum([G.vs()[v].degree() for v in community])
            delta_Q = 1/m * len(Kbv) - G.vs[v].degree()/(2*m**2)*db
            if delta_Q > MAX_Q:
                MAX_Q = delta_Q
                pos = index
    
        if MAX_Q > 0:
            clusters[pos].append(node.index)
        else:
            clusters.append([node.index])

#print clusters
        
    membership = [0 for i in range(G.vcount())]
    for i in range(len(clusters)):
        for index in clusters[i]:
            membership[index] = i
            
    return membership, clusters
       
#print g.modularity(membership)
#print membership
def Modularity(G,membership):
    m = g.ecount()
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
#print Modularity(g,membership)

def destruction(G,membership,clusters,belta):

    index = random.sample(range(G.vcount()),int(belta*len(membership)))
    for i in index:
        membership[i] = None
    for community in clusters:
        for node in community:
            if node in index:
                community.remove(node)
        if community == []:
            clusters.remove(community)
    return index,membership,clusters

#print destruction(g,membership,0.3)    
        
def reconstruction(G,index,membership,clusters):
    m = G.ecount()
    random.shuffle(index)
    for i in index:
        MAX_Q = 0
        pos = -1
        for index,community in enumerate(clusters):    
            KbV = len(G.es.select(_between = ([i], community)))
            Db = sum([G.vs()[node].degree() for node in community])
            DELTA_Q = 1/m*KbV - G.vs()[i].degree()*Db/(2*m**2)
            if DELTA_Q > MAX_Q:
                MAX_Q = DELTA_Q
                pos = index
        if MAX_Q > 0:
            clusters[pos].append(i)
            
        else:
            clusters.append([i])
     
    for i in range(len(clusters)):
        for index in clusters[i]:
            membership[index] = i
    return membership

def main():
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\karate\\karate.gml")
    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\polbooks\\polbooks.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\dolphins\\dolphins.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\football\\football.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\netscience\\netscience.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\metabolic\\metabolic.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\adjnoun\\adjnoun.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\Amazon\\Amazon.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\lesmis\\lesmis.gml")
#    graph = Graph.Read_GML("C:\\Users\\Administrator\\Desktop\\dataset\\gml\\jazz\\jazz1.gml")
#    graph = ig.graph('C:\\Users\\Administrator\\Desktop\\dataset\\gml\\metabolic.txt')
#    graph = ig.graph('C:\\Users\\Administrator\\Desktop\\dataset\\gml\\lesmis.txt')
#    pathlist = ['0.45','0.4','0.05','0.1','0.15','0.2','0.25','0.3','0.35']
#    graph = ig.graph('C:\\Users\\Administrator\\Desktop\\LFR\\n=1000\\d=15,maxc=50,minc=20\\0.3\\network.dat')
#    True_partition = GT.ground_truth('C:\\Users\\Administrator\\Desktop\\LFR\\n=1000\\d=15,maxc=50,minc=20\\0.3\\community.dat')
#    True_partition = GT.ground_truth('C:\\Users\\Administrator\\Desktop\\dataset\\gml\\dolphins\\dolphins.dat')
#    True_partition = GT.ground_truth('C:\\Users\\Administrator\\Desktop\\dataset\\gml\\football\\football.dat')
    True_partition = GT.ground_truth('C:\\Users\\Administrator\\Desktop\\dataset\\gml\\polbooks\\polbooks.dat')

    Time_sum = 0
    NMI_list = []
    Q_sum = []
    n = graph.vcount()
    m = graph.ecount()
    for i in range(50):
        print n,m
        start = time.time()
        solution, clusters = construction(graph)
        best = copy.copy(solution)
        interval = time.time()-start
        while interval < n/10:
#        for i in range(200):
            position, solution, clusters = destruction(graph,solution,clusters,0.3)
            solution = reconstruction(graph,position, solution,clusters)
            if graph.modularity(solution) > graph.modularity(best):
                best = copy.copy(solution)
#        print graph.modularity(best)
            interval = time.time()-start
        print graph.modularity(best)
        Q_sum.append(graph.modularity(best))
#        end = time.time()
#        print 'time',end - start
#        Time_sum += (end - start)
        NMI = compare_communities(best,True_partition,method='nmi',remove_none=False)
#        print NMI
        NMI_list.append(NMI)
#        time.sleep(200)

    NMI = Stats(NMI_list)
    print "avgNMI",NMI.avg()
    print "maxNMI",NMI.max()
    print "minNMI",NMI.min()
    print "stdevNMI",NMI.stdev()
        
    modularity = Stats(Q_sum)
    print "avgQ",modularity.avg()
    print "maxQ",modularity.max()
    print "minQ",modularity.min()
    print "stdevQ",modularity.stdev()
    print "time",Time_sum/1 
        
if __name__ == '__main__':
    main()
    

        
        
    
    