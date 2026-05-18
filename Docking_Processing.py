#!/usr/bin/python

import pandas as pd
import numpy as np
import re

recnum = 00 # enter number of receptors
molnum = 00 # enter number of molecules in library
#also need to check .tab on line 12 and rec prefix on line 43

with open("Filename.tab", "r") as infile: #open .tab file
	data = infile.readlines() #read all lines into data variable
	IX = [] #open lists to fill later
	Name = []
	Score = []
	Nflex = []
	File = []
	for line in data: #for each line in data..
		if ("gpfs") in line: #only keep lines with gpfs (will get rid of extra lines)
			Ele = line.split() #split each line into elements and define elements
			IX.append(Ele[0]) # fill lists with values while iterating through lines
			Name.append(Ele[1])
			Score.append(Ele[2])
			Nflex.append(Ele[4])
			File.append(Ele[13])
			
a = pd.Series(IX)  # turn each list into a series
b = pd.Series(Name)
c = pd.Series(Score)
d = pd.Series(Nflex)
e = pd.Series(File)

df = pd.DataFrame() #open a datafile in pandas
df['IX'] = a.values #add columns with values from series
df['Name'] = b.values
df['pH'] = b.values
df['Score'] = c.values
df['Nflex'] = d.values
df['Rec'] = e.values
df['File'] = e.values

df.Rec = df.Rec.str.extract(r'(Receptor\_[0-9]+)', expand=False) #extract just the receptor name from that column. May need to change
df.pH = df.pH.str.extract(r'(ph.)', expand=False)
df.Name = df.Name.str.replace(r'(ph.)', '')
 
#check that file is the right length
scorenum = int(recnum)*int(molnum)
length=len(df)

check = scorenum == length
if check is True:
	print ("correct number of scores")
else:
	print ("Error: wrong number of scores") # do not continue if you get this message

df.to_csv("All_Score.csv") #save data frame

df1 = pd.read_csv('All_Score.csv', sep=',', header=0, converters={"IX":float, "Score":float})
df1 = df1.sort_values(by=['IX', 'Rec']) #sort table by IX and Rec 

array= df1.values
a = array.reshape(int(molnum),int(recnum),8) #(ligand #, rec #, column #)

IX = [] #open lists to fill later
Name = []
pH = []
Nflex = []
File = []
Avg = []
Boltz = []

IX_1 = a[:,0,1]
Name_1 = a[:,0,2]
pH_1 = a[:,0,3]
Nflex_1 = a[:,0,5]
File_1 = a[:,0,7]

for i in range(int(molnum)):	
	x = np.array(a[i,:,4], dtype=np.float128)
	Avg.append(np.mean(x))
	y = np.exp((-1000*x)/592.126)
	esum = sum(y)
	pop = y/esum
	wtscore = pop*x
	Bscore = sum(wtscore)
	Boltz.append(Bscore)

g = pd.Series(IX_1)  # turn each list into a series
h = pd.Series(Name_1)
i = pd.Series(pH_1)
j = pd.Series(Nflex_1)
k = pd.Series(File_1)
l = pd.Series(Avg)
m = pd.Series(Boltz)

pf = pd.DataFrame() #open a datafile in pandas
pf['IX'] = g.values #add columns with values from series
pf['Name'] = h.values
pf['pH'] = i.values
pf['Nflex'] = j.values
pf['File'] = k.values
pf['Av Scores'] = l.values
pf['Boltz Scores']= m.values

pf.to_csv("Score_Final.csv") #save as