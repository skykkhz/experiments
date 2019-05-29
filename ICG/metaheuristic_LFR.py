# -*- coding: utf-8 -*-
"""
Created on Wed May 22 17:03:02 2019

@author: Administrator
"""

from pylab import *
import random



ICG_list = [1,1,1,1,1,1,1,1,1,1,1,1,0.9987,0.730]

IG_list = [1,1,1,1,1,1,1,1,1,1,1,0.9786,0.8043,0.3947]
GA_list = [1,1,1,1,1,0.9874,0.9535,0.8653,0.8032,0.7691,0.7056,0.6343,0.586,0.343]

DBA_list = [1,1,1,1,1,1,1,0.994,0.979,0.9053,0.8052,0.6978,0.5943,0.4861]

PSO_list = [1,1,1,1,1,1,0.9992,0.9599,0.9412,0.9235,0.8977,0.6573,0.4953,0.2937]

#LPA_list = [1,1,1,1,1,1,1,1,1,0.9191,0.8148,0,0,0]
##print len(LPA_list)
#
#BGLL_list = [1,1,1,1,1,1,1,1,1,1,0.9873,0.8274,0.6576,0.3824]
##print len(BGLL_list)
#Infomap_list = [1,1,1,1,1,1,1,1,1,1,1,1,0,0]
#CICD_list = [1,0.9887,0.9796,0.9640,0.9532,0.9510,0.8956,0.8151,0.7783,0.7282,0.6219,0.5710,0.5305,0.4514]
#
#FN_list = [1,0.9874,0.9843,0.9013,0.8741,0.7943,0.7431,0.5842,0.5188,0.4313,0.4053,0.3678,0.3098,0.2195]


LPA_list = [1,1,1,1,1,1,0,0,0,0]
FN_list = [1,1,1,1,0.9748,0.9748,0.8017,0.7579,0.3431,0.2917]
BGLL_list = [1,1,1,1,1,1,1,1,0.7256,0.2885]
Infomap_list = [1,1,1,1,1,1,1,1,0,0]
CICD_list = [1,1,0.9457,0.9132,0.8847,0.7265,0.6975,0.5553,0.5114,0.3877]
ICG_list = [1,1,1,1,1,1,1,1,1,0.7827]

u_value= [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5]
plt.xlim(0.05,0.5)
#u_value = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7]
#plt.xlim(0.05,0.7)

plt.ylim(0,1.0)
plt.xticks([0.1, 0.2, 0.3, 0.4,0.5],
           [r'0.1', r'0.2', r'0.3',r'0.4',r'0.5'],fontsize = 12)
#plt.xticks([0.1, 0.2, 0.3, 0.4,0.5, 0.6, 0.7],
#           [r'0.1', r'0.2', r'0.3',r'0.4',r'0.5',r'0.6',r'0.7'],fontsize = 12)
plt.yticks([0.0,  0.2, 0.4, 0.6,  0.8,  1.0],
    [r'0.0',  r'0.2',  r'0.4', r'0.6',r'0.8',r'1.0'],fontsize = 12)
#plt.title(u"LFR(S)基准网络",fontsize=15,fontproperties=myfont)
plt.xlabel(r'$ Mix \ parameter \  $', fontsize=15, labelpad=3)
plt.ylabel(r'$  NMI  $', fontsize=15, labelpad=3)

#plt.plot(u_value,GA_list, color='c', linewidth=2, linestyle='--', marker='s',markersize = 6, label=r'$GACD$')
#plt.plot(u_value,DBA_list, color='k', linewidth=2, linestyle='--', marker='*',markersize = 6, label=r'$DBA$')
#plt.plot(u_value,PSO_list, color='y', linewidth=2, linestyle='--', marker='^',markersize = 6, label=r'$IDPSO-RO$')
#plt.plot(u_value,IG_list, color='r', linewidth=2, linestyle='--', marker='x',markersize = 6, label=r'$IG$')
#plt.plot(u_value,ICG_list, color='g', linewidth=2, linestyle='--', marker='o',markersize = 6, label=r'$ICG$')


plt.plot(u_value,FN_list, color='b', linewidth=2, linestyle='--', marker='+',markersize = 6, label=r'$FN$')
plt.plot(u_value,LPA_list, color='c', linewidth=2, linestyle='--', marker='s',markersize = 6, label=r'$LPA$')
plt.plot(u_value,BGLL_list, color='k', linewidth=2, linestyle='--', marker='*',markersize = 6, label=r'$BGLL$')
plt.plot(u_value,Infomap_list, color='y', linewidth=2, linestyle='--', marker='^',markersize = 6, label=r'$Infomap$')
plt.plot(u_value,CICD_list, color='r', linewidth=2, linestyle='--', marker='x',markersize = 6, label=r'$CICD$')
plt.plot(u_value,ICG_list, color='g', linewidth=2, linestyle='--', marker='o',markersize = 6, label=r'$ICG$')

#
plt.legend(loc='lower left',fontsize=12)

plt.savefig('C:\\Users\\Administrator\\Desktop\\GN-HEURISTIC',dpi=300)