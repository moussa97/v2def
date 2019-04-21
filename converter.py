# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 15:43:52 2019

@author: lenovo
"""


import json as json



with open('mux4x1_json') as f:
    data = json.load(f)
    
out = open('output.txt' , 'w' ) ;
lef = open( 'osu035.lef' , 'r' );

#lefFile = lef.readlines() ;

    
# print(data['modules']['mux4x1']['ports']['a']) ;  

case = 0 ;
type = "null" ;
via_layer = "null" ;
layers_metal = {} ;
vias = {} ;


with open('osu035.lef') as mylef:  
    for line in mylef:

        #keep looking for cases
        if (case == 0 ):
            try:
                first = line.split()[0];
                second = line.split()[1];
                if( first == 'LAYER'):
                   case = 1 ; # inside metal layer
                   #print(second);
                   if( second=='metal1' or type=='metal2' or type=='metal3' or type=='metal4' or  type=='metal5' or  type=='metal6' ):
                        type = second;
                        layers_metal[second] = {} ;
                if( first == 'VIA' ):
                    case = 2 ; #inside VIA layer
                    if ( second=="M2_M1" or second=="M3_M2" or second=="M4_M3" or second=="M5_M4" or second=="M5_M6" ) :
                        type = second ;
                        vias[second] = {} ;

            except:
                pass

        #inside a case
        else:
            try:
                first = line.split()[0];
                second = line.split()[1];
                # inside first case (layer case)
                if (first == "END"):
                    case = 0 ;  # not inside any of the cases
                    type = "null";
                    via_layer = "null" ;
                else:
                    #print(first, second, case, type)
                    if (case == 1): #metal Layer
                        if( type=='metal1' or type=='metal2' or type=='metal3' or type=='metal4' or  type=='metal5' or  type=='metal6' ):
                            if( first == "PITCH" ):
                                layers_metal[type]["pitch"] = second;
                            if (first == "WIDTH"):
                                layers_metal[type]["width"] = second;
                            if (first == "SPACING"):
                                layers_metal[type]["spacing"] = second;
                            if (first == "OFFSET"):
                                layers_metal[type]["offset"] = second;
                    if ( case == 2 ) : #Vias
                        if( type=="M2_M1" or type=="M3_M2" or type=="M4_M3" or type=="M5_M4" or type=="M5_M6" ) :
                            if (first=="LAYER"):
                                via_layer = second
                            else:
                                vias[type][via_layer] =  line.rstrip(";\n\r") ;


                    # if (case == 2):
                    #     print(first , second) ;
            except:
                pass


print(layers_metal);
print(vias);