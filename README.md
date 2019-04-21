# v2def
generate def file

introduction:
This is python program that converts verilog gate level netlist into a DEF file. Def fiel is used to represent the physical layout of an IC in an ASCII format. it represents the netlist and the circuit layout. We use DEF along with LEF to represent the complete physical layout of an integrated circuit while it is being designed.

limitations:
	All the pins and nets information are extraxted in nested dictionaries inside the python code but are not in the written the output file
	
how to use:
	1. insert the .lef file and the JSON formated gate level netlist in the same directory as the converter.python
	2. change the name of the files inside the python code respectively
	3. run the python code 
	
Assumptions :
	the verilog input is in the JSON format
	all the VIARULE sections shall be removed from the .lef file
	In the .lef file No line shall contain only one word except the port in the .lef pin macro 
