# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 15:43:52 2019

@author: lenovo
"""


import numpy as np
import json as json


class macro:
    size = 0  ;
    
class layer:
    direction = "" ;
    pitch = "" ;
    width = "" ;
    spacing = "" ;
    offset = "" ;
    
macros = [];
layers = [] ;

with open('mux4x1_json') as f:
    data = json.load(f)
    
out = open('output.txt' , 'w' ) ;
lef = open( 'osu035.lef' , 'r' );

#lefFile = lef.readlines() ;

    
# print(data['modules']['mux4x1']['ports']['a']) ;  

layers.append(layer);
layer.pitch = "34";


with open('osu035.lef') as mylef:  
   for line in mylef:
       try:
           first = line.split()[0] ;
           if( first == 'LAYER'):
               case = 1 ;
       except:
           pass
       