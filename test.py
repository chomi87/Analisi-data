import Tkinter
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from Tkinter import *

from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename
from tkFileDialog import askopenfilenames

#for 3D maps
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
root = Tkinter.Tk() ; root.withdraw()

#Selects the files to be opened
#Opens the files
#Returns a matrix with the data in nm, one with data in eV and one with the names
def seleziona():
    filez = askopenfilenames(parent=root,title='Choose a file')
    files = root.tk.splitlist(filez) 
    i=0
    fi=apri(files[i])
    #AllData index 1 is the number of file, index 2 is the energy/wl, index 3 is the intensity
    AllDataWl = np.zeros((len(files),len(fi),2))
    AllDataeV = np.zeros((len(files),len(fi),2))
    Names = []

    for i in range(0,len(files)):
        fi=apri(files[i])
        AllDataWl[i]=trasferisci(fi)
        AllDataeV[i]=transform(AllDataWl[i])
        Names.append(files[i])

    return [AllDataWl,AllDataeV,Names]

def multifile():
    res=1340
    filename = askopenfilename(parent=root)
    fi=apri(filename)
    WL=trasferisci(fi)
    EV=transform(WL)

    NSpectra=len(WL)/res

    ResultWL=np.zeros((res,1+NSpectra))
    ResultWL[:,0]=WL[0:res,0]
    ResultEV=np.zeros((res,1+NSpectra))
    ResultEV[:,0]=EV[0:res,0]

    for i in range(1,(NSpectra+1)):
        group=range((i-1)*res,(i)*res)
        ResultWL[:,i]=WL[group,1]
        ResultEV[:,i]=EV[group,1]
    return [ResultWL,ResultEV]




#Opens a single filea and returns a list
def apri(filename):
    # Open file
    f = open(filename, 'r')

    data = []
    # Loop over lines and extract variables of interest
    for line in f:
            line = line.strip()
            columns = line.split()
            source = {}
            source['wl'] = columns[0]
            source['I'] = columns[3]
            data.append(source)
    f.close()
    #close file
    return data

#Transfers data from a list to a matrix
def trasferisci(data):
    #transfer data in a matrix
    Dat = np.zeros((len(data),2))
    for i in range(0,len(data)):
        Dat[i,0]=data[i]['wl']
        Dat[i,1]=data[i]['I']

    return(Dat)

#Transforms the data from nm to eV
def transform(data):
    h=6.626E-34
    c=299792458
    e=1.602E-19
    dataeV = np.zeros((len(data),2))
    dataeV[:,0]=h*c/(1E-9*e*data[:,0])
    # BISOGNA AGGIUSTARE LE INTENSITA
    dataeV[:,1]=data[:,1]
    return dataeV

#removes spike with a level 3 algorithm
#Parameters: n1,n2,n3 define how many STDEV of tolerance at each level of depth
#N_sottinsiemi defines in how many blocks to devide the data
def spikeremove(spectre):
    n1=2
    n2=2
    n3=3
    N_sottoinsiemi=100

    copia1=np.copy(spectre)
    copia2=np.copy(spectre)
    copia3=np.copy(spectre)
    punti=len(spectre)
    L_sottoinsiemi=int(punti/N_sottoinsiemi)

    for i in range(0,N_sottoinsiemi):
        blocco=range(i*L_sottoinsiemi,(i+1)*L_sottoinsiemi)
        media=np.mean(spectre[blocco,1])
        stdev=np.std(spectre[blocco,1])
        for j in blocco:
            if spectre[j,1]>(media+n1*stdev): copia1[j,1]=media
        
    for i in range(0,N_sottoinsiemi):
        blocco=range(i*L_sottoinsiemi,(i+1)*L_sottoinsiemi)
        media=np.mean(copia1[blocco,1])
        stdev=np.std(copia1[blocco,1])
        for j in blocco:
            if spectre[j,1]>(media+n2*stdev): copia2[j,1]=media 

    for i in range(0,N_sottoinsiemi):
        blocco=range(i*L_sottoinsiemi,(i+1)*L_sottoinsiemi)
        media=np.mean(copia2[blocco,1])
        stdev=np.std(copia2[blocco,1])
        for j in blocco:
            if spectre[j,1]>(media+n3*stdev): copia3[j,1]=media    
    
    return copia3

#plots a data set
def plotta(data):
    plt.plot(data[:,0], data[:,1],linewidth=2)
    plt.show()

#Plots 2 graphs at a time. 
#Useful to compare data in nm and eV or raw versions VS versions without spikes
def plotta2(data1,data2):
    # Two subplots, unpack the axes array immediately
    f, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(data1[:,0], data1[:,1])

    ax2.plot(data2[:,0], data2[:,1])
    plt.show()

#Plots 4 graphs at a time. Useful to compare data in nm and eV VS the versions without spikes
def plotta4(data1,data2,data3,data4):
    # Two subplots, unpack the axes array immediately
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.plot(data1[:,0], data1[:,1])
    ax2.plot(data2[:,0], data2[:,1])
    ax3.plot(data3[:,0], data3[:,1])
    ax4.plot(data4[:,0], data4[:,1])
    plt.show()

#Plots all the data in a column
#Useful to compare all the raw data at a glance
def plottamolti(data, how_many):
    
    x = data[0,:,0]
    subplots_adjust(hspace=0.000)
    number_of_subplots=how_many

    for i,v in enumerate(xrange(number_of_subplots)):
        v = v+1
        y = data[i,:,1]
        ax1 = subplot(number_of_subplots,1,v)
        ax1.plot(x,y)

    plt.show()


def plotta3D(Multidata,flag):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    def cc(arg):
        return colorConverter.to_rgba(arg, alpha=0.6)

    def multispike(tempSpe,ys,flag):
        if flag==1:
            tempSpe[:,1]=ys
            tempSpe=spikeremove(tempSpe)
            ys = tempSpe[:,1]
        return ys

    #xs = np.arange(0, 10, 0.4)
    xmin=np.min(Multidata[:,0])
    xmax=np.max(Multidata[:,0])
    xs = Multidata[:,0]
    N=(len(Multidata[0])-1)
    verts = []
    zs = range(0,N)
    tempSpe = np.zeros((len(Multidata),2))
    tempSpe[:,0]=xs
    
    #multispikes removes the spikes if flag=1, does nothing if flag!=1
    for z in zs:
        ys = multispike(tempSpe,Multidata[:,(z+1)],flag)
        verts.append(list(zip(xs, ys)))

#    poly = PolyCollection(verts, facecolors=[cc('r'), cc('g'), cc('b'),
 #                                        cc('y')])
    poly = PolyCollection(verts,closed=False)
    poly.set_alpha(0.7)
    ax.add_collection3d(poly, zs=zs, zdir='y')

    ax.set_xlabel('X')
    ax.set_xlim3d(xmin, xmax)
    ax.set_ylabel('Y')
    ax.set_ylim3d(-1, N)
    ax.set_zlabel('Z')
    #CAMBIARE zmax per cambiare l'asse 
    zmax=5000
    ax.set_zlim3d(-1, zmax)

    plt.show()

#Saves the data in a new file.
#Requires the original name of the file, the data and a type (WL or EV) in a string
def salva(data,nome,tipo):
    indice=nome.replace(".ascii",tipo)
    indice=indice+'.ascii'
    savetxt(indice, column_stack((data[:,0],data[:,1])) )



######################### GUI for main################
class App:
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
    self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=root.destroy)
    self.button.pack(side=RIGHT)

    self.slogan = Button(frame,
                         text="Un file",
                         command=self.uno)
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                         text="Overall peek",
                         command=self.look_many)
    self.slogan.pack(side=LEFT)
  
  def write_slogan(self):
    print "Tkinter is easy to use!"

  def uno(self):
    [AllDataWl,AllDataeV,Names]=seleziona()
    for i in range(0,len(AllDataWl)):     
        altdataW=spikeremove(AllDataWl[i])
        altdataV=spikeremove(AllDataeV[i])
        plotta4(AllDataWl[i],AllDataeV[i],altdataW,altdataV)
  def look_many(self):
    [AllDataWl,AllDataeV,Names]=seleziona()
    plottamolti(AllDataeV,len(AllDataeV))
      



########################MAIN ########################
root = Tkinter.Tk()
app = App(root)
root.mainloop()

#[MultiWL,MultiEV]=multifile()
#plotta3D(MultiWL,1)


#[AllDataWl,AllDataeV,Names]=seleziona()


#altdata=spikeremove(AllDataeV[0])
#plotta2(AllDataeV[0],altdata)
# for i in range(0,len(AllDataWl)):
#     altdataW=spikeremove(AllDataWl[i])
#     salva(altdataW,Names[i],'WL')
#     altdataV=spikeremove(AllDataeV[i])
#     salva(altdataV,Names[i],'EV')
#     plotta4(AllDataWl[i],AllDataeV[i],altdataW,altdataV)