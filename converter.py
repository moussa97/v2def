# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 15:43:52 2019

@author: lenovo
"""


import numpy as np
import json as json


with open('mux4x1_json') as f:
    data = json.load(f)
    
out = open('output.txt' , 'w' ) ;
lef = open( 'osu035.lef' , 'r' );

lefFile = lef.readlines() ;

for i in range(5) :
    out.write( lefFile[i] );  
    print ( lefFile[i] ) ;
print(data) ;
f.close() 