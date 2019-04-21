# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 15:43:52 2019

@author: lenovo
"""


import json as json



with open('mux4x1_json') as f:
    data = json.load(f)
    
out = open('output.def' , 'w' ) ;
lef = open( 'osu035.lef' , 'r' );

#lefFile = lef.readlines() ;

    
# print(data['modules']['mux4x1']['ports']['a']) ;  

case = 0 ;
type = "null" ;
name_of_pin = "null"
name_of_port = "null"
via_layer = "null" ;
cnt = 0 ;

#dictionaries
#these are the nested components of the def file (final output)
layers_metal = {} ;
vias = {} ;
macros= {};

sizex = 0 ;
sizey = 0 ;
with open('osu035.lef') as mylef:  
    for indx, line in enumerate(mylef):

        #keep looking for cases
        if (case == 0 ):
            try:
                first = line.split()[0];
                second = line.split()[1];
                # print( first , second , "++++++++++")
                if( first == 'LAYER'):
                   case = 1 ; # inside metal layer
                   #print(second);
                   if( second=='metal1' or second=='metal2' or second=='metal3' or second=='metal4' or  second=='metal5' or  second=='metal6' ):
                        type = second;
                        layers_metal[second] = {} ;
                        # print("check" , first , second , case , "&&&&&&&&&&&&&" );
                if( first == 'VIA' ):
                    case = 2 ; #inside VIA layer
                    if ( second=="M2_M1" or second=="M3_M2" or second=="M4_M3" or second=="M5_M4" or second=="M5_M6" ) :
                        type = second ;
                        vias[second] = {} ;

                if( first == "MACRO"):
                    case = 3 #inside MACRO Layer
                    type = second ;
                    macros[second] = {};

            except:
                pass

        #inside a case
        else:
            try:
                first = line.split()[0];

                if( first != "PORT" and first != "END"):
                    second = line.split()[1];

                #print(first, second , case , type );

                if (first == "END"):
                    if(name_of_port != "null"):
                        name_of_port = "null"
                        case=4 #inside a pin inside a macro
                    else:
                        if (name_of_pin != "null"):
                            name_of_pin = "null"
                            case = 3 # inside a macro
                        else:
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
                            if (first == "DIRECTION"):
                                layers_metal[type]["direction"] = second;
                    if ( case == 2 ) : #Vias
                        if( type=="M2_M1" or type=="M3_M2" or type=="M4_M3" or type=="M5_M4" or type=="M5_M6" ) :
                            if (first=="LAYER"):
                                via_layer = second
                            else:
                                vias[type][via_layer] =  line.rstrip(";\n\r") ;

                    if (case == 4): #inside pin inside a macro
                        if (first == "PORT"):
                            case = 5 #inside a port inside a pin inside a macro
                            name_of_port = "ON"

                    if (case == 3): #MACRO
                        if( first == "PIN"):
                            case = 4 #inside a macro inside a pin
                            name_of_pin = second ;
                            #print ( name_of_pin , "@@@@" )
                            macros[type][name_of_pin] = {} ;
                        else:
                            if(first == "SIZE" ):
                                macros[type]['sizex'] = float( line.split()[1] ) * 100
                                macros[type]['sizey'] = float( line.split()[3] ) * 100

                    if (case == 6 ):
                        macros[type][name_of_pin][second] = line.split() ;

                    if (case == 5 and first == "LAYER"):
                        case = 6
                        macros[type][name_of_pin][second] = {}



            except:
                pass

#write intro
out.write( 'VERSION 5.7 ;\n DIVIDERCHAR "/" ;\n BUSBITCHARS "[]" ; \n DESIGN c17 ;\n UNITS DISTANCE MICRONS 1000 ;\n');

#calculate DIE AREA
out.write("\n")
for indx , cells in data['modules']['mux4x1']['cells'].items() :
    sizex = sizex + macros[cells['type']]['sizex'] ;
    sizey = sizey + macros[cells['type']]['sizey'];
out.write( "DIEAREA (" + str(sizex) + "," + str(sizey) + ") \n" );

#write tracks
out.write("\n");
for key, value in sorted(layers_metal.items()):
    temp =  'Y ' if layers_metal['metal1']=="HORIZIONTAL" else 'X' ;
    out.write( "TRACKS " + temp + " DO " + temp + " 400 DO 25 STEP " + str(float(layers_metal[key]["pitch"])*100) + " LAYER " + key + "\n" )

#wrtie VIAs
out.write("\n");
out.write( "VIAS " + str(len(vias)) )
for key, value in sorted(vias.items()):
    out.write( "-" + key + "\n");
    for newkey , newvalue in sorted(value.items()):
        out.write("+" + newkey + "( " + str(float(newvalue.split()[1])*1000) + "," + str(float(newvalue.split()[2])*1000) + ") (" + str(float(newvalue.split()[3])*1000) + "," +str(float(newvalue.split()[4])*1000) + ")" + "\n");
out.write("END VIAS \n")

#write componenets
out.write("\n");
out.write("COMPONENTS " + str(len(data['modules']['mux4x1']['cells'])) + "\n" );
for indx , cells in data['modules']['mux4x1']['cells'].items() :
    out.write( cells['type'] + "\n");
out.write("END COMPONENTS" + "\n");

#write pins
out.write("\n");
out.write("PINS" + str(len(data['modules']['mux4x1']['ports'].items())*2) + "\n")
for key , value in data['modules']['mux4x1']['ports'].items() :
    out.write(key + "<0> + NET " + key + "<0> \n" );
    out.write(key + "<1> + NET " + key + "<1> \n" );

out.write("END")

print(layers_metal);
print(vias);
print(macros);