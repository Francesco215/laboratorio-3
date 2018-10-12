import numpy as np
import menzalib as mz
import pylab as pl
from scipy.optimize import curve_fit

def attenuazione(f,ft,dft):
	A=1/np.sqrt(1+f**2/ft**2)
	dA=(1+f**2/ft**2)**(-3/2)*f**2*ft**(-3)*dft
	return A,dA

def errore_rapporto(x,dx,y,dy):
    return(y**(-2))*np.sqrt(x**2*dy**2+y**2*dx**2)

def lineare(x,q,m):
	return q+m*x

"""funzione che calcola l'intersezione ed errore tra due rette indipendenti
	con equazioni y=x*m1+q1 e y=x*m2+q2"""

def int_rette(popt1,popt2,pcov1,pcov2):
	q1,q2=popt1[0],popt2[0]
	m1,m2=popt1[1],popt2[1]
	pcov=np.zeros((4,4))
	pcov[:2,:2]=pcov1
	pcov[2:,2:]=pcov2
	gradiente=([1/(m1*m2),-(q1*q2)/(m1*m2)**2,
			   -1/(m1*m2), (q1*q2)/(m1*m2)**2])

	x=(q2-q1)/(m1-m2)
	y=(q2*m1-q1*m2)/(m1-m2)
	dx=np.sqrt(np.linalg.multi_dot([gradiente,pcov,gradiente]))
	return ([x,y]),dx

#resistenze e capacità con errori
R=3.29e3
C=9.88e-9
dR=mz.dRdig(R)
dC=mz.dCdig(C)

#errore frequenza di taglio (punto 1a)
Ft=1/(R*C*2*np.pi)
dFt=np.sqrt(dR**2*C**2+dC**2*R**2)/(R*C*2*np.pi)

#Attenzuazione e errore (punto 1c e 1d)
A1=([attenuazione(2e3,Ft,dFt),attenuazione(2e4,Ft,dFt)])

Vout,freq=np.genfromtxt('dati/2.txt',unpack=True)
Vin=12.5
dVin=mz.dVosc(12.5)
A=Vout/Vin
dA=errore_rapporto(Vout,mz.dVosc(Vout),Vin,dVin)
pl.errorbar(freq,A,yerr=dA,fmt='.',markersize=1)
#qua faccio il punto 2.b.ii
#la retta obliqua
popt1,pcov1=curve_fit(lineare,np.log10(freq[7:]),np.log10(A[7:]))
x=np.linspace(3.5,6.5,10)
pl.plot(10**x,10**(lineare(x,*popt1)))
#la retta parallela
popt2,pcov2=curve_fit(lineare,np.log10(freq[:4]),np.log10(A[:4]))
x=np.linspace(1,4,10)
pl.plot(10**x,10**(lineare(x,*popt2)))
#l'intersezione delle due rette
x,y=int_rette(popt1,popt2,pcov1,pcov2)[0]
pl.plot(10**x,10**y,'bo')

pl.yscale('log')
pl.ylabel('Vout/Vin')
pl.xscale('log')
pl.xlabel('frequenza')
pl.savefig('figure/a.png')
pl.show()
pl.close()


#inizo punto 2
Vin,Vout,freq=np.genfromtxt('dati/2a.txt',unpack=True)
dVin=mz.dVosc(Vin)
dVout=mz.dVosc(Vout)

Amis=Vout/Vin
dAmis=errore_rapporto(Vout,dVout,Vin,dVin)
#print(Amis,dAmis,A1)#stampo il guadagno misurato e il guadagno teorico

#print(int_rette(popt1,popt2,pcov1,pcov2))
#print(10**int_rette(popt1,popt2,pcov1,pcov2)[0][0])
