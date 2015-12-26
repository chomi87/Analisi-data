import Tkinter

from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename

import numpy as np
import matplotlib.pyplot as plt

root = Tkinter.Tk() ; root.withdraw()

def gainvalue(argument):
    switcher = {
        6: 33,
        5: 3.3,
        4: 0.33,
        3: 0.033,
    }
    return switcher.get(argument, "nothing")

#APRE UN FILE, LO PULISCE E LO RESTITUISCE IN UNA LISTA
def apri(tipo):
	filename = askopenfilename(parent=root)

	# Open file
	f = open(filename, 'r')

	# Read and ignore header lines
	header1 = f.readline()
	header2 = f.readline()
	header3 = f.readline()
	header4 = f.readline()
	header5 = f.readline()
	header6 = f.readline()

	data = []
	# Loop over lines and extract variables of interest
	for line in f:
    		line = line.strip()
    		columns = line.split()
    		source = {}
    		source['bias'] = columns[0]
    		source['y'] = float(columns[1])
    		data.append(source)

	f.close()
	#close file
	return data

def trasferisci(data,tipo):
	#transfer data in a matrix
	Dat = np.zeros((len(data),2))
	for i in range(0,len(data)):
		Dat[i,0]=data[i]['bias']
		Dat[i,1]=data[i]['y']

	#inverse bias
	if (tipo==(1 or 2)):
		Dat[:,0]=-Dat[:,0]

	if (tipo==1):
		#correct current for gain
		gain = raw_input('Enter the gain (1,2,3,4,5,6): ')
		gain = int(float(gain))
		Dat[:,1]=Dat[:,1]/gainvalue(gain)

	return(Dat)

def plotta(data, tipo):
	if (tipo==1): 
		xl='Bias (V)'
		yl='Current (A)'
	if (tipo==2): 
		xl='Bias (V)'
		yl='dI/dV (arb. units)'
	if (tipo==3): 
		xl='Photon Energy (eV)'
		yl='Photon Intensity (arb. units)'

	plt.plot(data[:,0], data[:,1],linewidth=2)
	plt.ylabel(yl)
	plt.xlabel(xl)
	plt.show()

	

tipo= raw_input('Chose the file type (1=I(V), 2=dI/dV(V), 3=LE): ')
tipo= int(float(tipo))
data=apri(tipo)

matrice=trasferisci(data,tipo)
plotta(matrice,tipo)


#plot the data
#plt.plot(matrice[:,0], matrice[:,1],linewidth=2)
#plt.ylabel('Current (A)')
#plt.xlabel('Bias (V)')
#plt.show()

