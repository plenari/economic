# -*- coding: utf-8 -*-
"""
Created on Wed May 17 14:17:55 2017

@author: linner
"""
p1=input(r'first addres:')
p2=input(r'second addres:')
from difflib import *
with open(p1,'r') as f:
    t1=f.readlines()
with open(p2,'r') as f:
    t2=f.readlines()
    
result = HtmlDiff.make_file(HtmlDiff(),t1,t2)

with open("result.html","w") as f:
    f.write(result)