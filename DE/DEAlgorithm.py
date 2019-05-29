# -*- coding: utf-8 -*-
'''
Created on 2018.9.6

@author: Administrator
'''
from __future__ import division 
import random 
from random import choice
import numpy as np
import copy
import math
import networkx as nx
class DEAlgorithm():
    def __init__(self, G, NP, N_Gen, SUB_D,Lower, Upper):
        self.G = G
        self.D = G.number_of_nodes()  #dimension
        self.NP = NP  #population size 
        self.N_Gen = N_Gen  #generations
        self.SUB_D = SUB_D #the number of nodes per group
        self.Lower = Lower  #lower bound
        self.Upper = Upper-1  #upper bound

        self.q_max = 0.0  #minimum fitness
        
        self.Lb = [0] * self.D  #lower bound
        self.Ub = [0] * self.D  #upper bound
        
        self.Sol = [[i for i in range(self.D)] for j in range(self.NP)]  #population of solutions
        self.Fitness = [0] * self.NP  #fitness
        self.best = [0] * self.D  #best solution

    def best_bat(self):
        i = 0
        j = 0
        for i in range(self.NP):
            if self.Fitness[i] > self.Fitness[j]:
                j = i
        for i in range(self.D):
            self.best[i] = self.Sol[j][i]
        self.q_max = self.Fitness[j]

    def init_bat(self):
        for i in range(self.D):
            self.Lb[i] = self.Lower
            self.Ub[i] = self.Upper
        
        alpha = 0.4;
        t = round(alpha * self.D)
        for i in range(self.NP):
            index = random.sample(range(self.D), int(t))
            for j in index:
                comm_id = self.Sol[i][j]
                nghIndex = [nbr for nbr in self.G[j]]
                for k in nghIndex:
                    self.Sol[i][k] = comm_id
            self.Fitness[i] = self.modularity(self.Sol[i])
        self.best_bat()   
    def modularity(self,sol,weight='weight'):
        graph = self.G
        if type(graph) != nx.Graph:
            raise TypeError("Bad graph type, use only non directed graph")
        partition = dict(zip(range(self.D),sol))
        inc = dict([])
        deg = dict([])
        links = graph.size(weight=weight)
        if links == 0:
            raise ValueError("A graph without link has an undefined modularity")

        for node in graph:
            com = partition[node]
            deg[com] = deg.get(com, 0.) + graph.degree(node, weight=weight)
            for neighbor, datas in graph[node].items():
                edge_weight = datas.get(weight, 1)
                if partition[neighbor] == com:
                    if neighbor == node:
                        inc[com] = inc.get(com, 0.) + float(edge_weight)
                    else:
                        inc[com] = inc.get(com, 0.) + float(edge_weight) / 2.

        res = 0.
        for com in set(partition.values()):
            res += (inc.get(com, 0.) / links) - \
                        (deg.get(com, 0.) / (2. * links)) ** 2
        return res
    def simplebounds(self, val, lower, upper):
        if val < lower:
            val = lower
        if val > upper:
            val = upper
        return val
    def group(self):
        dim_rand = range(self.D)
        random.shuffle(dim_rand)
        group = None
        group_num = 0
        if self.SUB_D >= self.D:
            group = [dim_rand]
            group_num = 1
        else:
            group_num = int(math.ceil(self.D / self.SUB_D))
            group = [[] for i in range(group_num)]
            myrange = 0

            for i in range(1,group_num):
                index = []
                for j in dim_rand[myrange: i*self.SUB_D]:
                    nghIndex = [nbr for nbr in self.G[j]]
                    index.extend(nghIndex)
                index_temp = []
                for k in index:
                    if k not in index_temp:
                        index_temp.append(k)
                group[i-1] = index_temp[0:self.SUB_D]
                myrange = myrange + self.SUB_D
            index = []
            for j in dim_rand[myrange: self.D]:
                nghIndex = [nbr for nbr in self.G[j]]
                index.extend(nghIndex)
            index_temp = []
            for k in index:
                if k not in index_temp:
                    index_temp.append(k)
            group[group_num-1] = index_temp[myrange:self.D]
        return group,group_num
    def move_bat(self):
        self.init_bat()
        result_list = []
        t = 0
        while t < self.N_Gen:
            group,group_num = self.group()
            for i in range(group_num):
                bestmod = self.decd_partial(group[i])
                result_list.append(bestmod)
                t = t + 1
        return result_list
    def decd_partial(self,dim_index):
        F = 0.9
        gpop = [[i for i in self.best] for j in range(self.NP)]
        gpop_fitness = []
        rot = range(self.NP)
        for i in range(self.NP):
            for j in dim_index:
                gpop[i][j] = self.Sol[i][j]
            gpop_fitness.append(self.modularity(gpop[i]))
        id = gpop_fitness.index(max(gpop_fitness))
        if gpop_fitness[id] > self.q_max:
            for i in range(self.D):
                self.best[i] = gpop[id][i]
            self.q_max = gpop_fitness[id]
        
        a1 = range(self.NP)
        random.shuffle(a1)
#         r1 = random.sample(rot,1)
        r1 = int(self.D / 3)
        a2 = a1[r1:] + a1[:r1]
#         r2 = random.sample(rot,1)
        r2 = int(self.D / 2)
        a3 = a1[r2:] + a1[:r2]
        
        tempfit = []
        for i in range(self.NP):
            for j in dim_index:
                gpop[i][j] = self.Sol[a1[i]][j] + F * (self.Sol[a2[i]][j] - self.Sol[a3[i]][j])
                gpop[i][j] = self.simplebounds(gpop[i][j], self.Lb[j],
                                                self.Ub[j])
            tempfit.append(self.modularity(gpop[i]))
        for i in range(self.NP):
            if tempfit[i] >= gpop_fitness[i]:
                for j in dim_index:
                    self.Sol[i][j] = gpop[i][j]
            self.Fitness[i] = self.modularity(self.Sol[i])
        self.best_bat()
        return self.q_max
    def __renumber(self,membership):
    #Renumber the values of the dictionary from 0 to n,[3,2,3,1] and [2,3,2,4] should be the same solution.
        dictionary = dict(zip(range(self.D),membership))
        count = 0
        ret = dictionary.copy()
        new_values = dict([])
    
        for key in dictionary.keys():
            value = dictionary[key]
            new_value = new_values.get(value, -1)
            if new_value == -1:
                new_values[value] = count
                new_value = count
                count += 1
            ret[key] = new_value

        return ret.values()
    def __neighcom(self,node,membership, weight_key):
        """
        Compute the communities in the neighborhood of node in the graph given
        with the decomposition node2com
        """
        node2com = dict(zip(range(self.D),membership))
        weights = {}
        for neighbor, datas in self.G[node].items():
            if neighbor != node:
                edge_weight = datas.get(weight_key, 1)
                neighborcom = node2com[neighbor]
                weights[neighborcom] = weights.get(neighborcom, 0) + edge_weight

        return max(weights, key=weights.get)