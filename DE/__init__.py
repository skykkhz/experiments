# -*- coding: utf-8 -*-
import random
import os
from BATAlgorithm.util import load_graph
import networkx as nx
from networkx.readwrite.gml import read_gml
from DE.DEAlgorithm import DEAlgorithm
popSize = 50
crossoverRate = 0.75
mutatePortion = 0.25
generations = 100
sub_dim = 20
Pe = 0.25
def de_main(path,f):
    #接受准则Adapted Kernighan-Lin
    if f == 1:
        G = load_graph(path)
    else:
        G = read_gml(path,label='id')
    dea = DEAlgorithm(G, popSize, generations, sub_dim, 0, G.number_of_nodes())
    r = dea.move_bat()
    return r
if __name__ == '__main__':
#     pathList = ['karate2','dolphins','football','polbooks','power','as-22july06']
    pathList = ['karate2']
    
    for index in range(0,pathList.__len__()):
        mod = de_main(os.path.join('f:\dataset',pathList[index]) + '.gml',0) 
        print mod