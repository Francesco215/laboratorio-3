import numpy as np
import lab3lib as l3
import pylab as pl
from scipy.optimize import curve_fit

def errore_capacità(C):
	ep=C*0.04 #questo è l'errore percentuale
	if C<2e-9: 	return ep+3e-9
	if C<2e-8:	return ep+3e-8
	if C<2e-7:	return ep+3e-7
	if C<2e-6:	return ep+3e-6
	if C<2e-5:	return ep+3e-5

def attenuazione(f,ft,dft):
	A=1/np.sqrt(1+f**2/ft**2)
	dA=(1+f**2/ft**2)**(-3/2)*f**2*ft**(-3)*dft
	return A,dA

def errore_osc_volt(V):
	scala=np.sort([2e-3,2e-2,2e-1,2,5e-3,5e-2,5e-1,5,1e-2,1e-1,1])
	for i in range(0,len(scala)):
		if V<scala[i]*8:
			return np.sqrt((V*0.04)**2+(scala[i]/10)**2)
	return 0
dVosc=np.vectorize(errore_osc_volt)

def errore_rapporto(x,dx,y,dy):
    return(y**(-2))*np.sqrt(x**2*dy**2+y**2*dx**2)

def lineare(x,m,q):
	return m*x+q


#resistenze e capacità con errori
R=3.29e3
C=9.88e-9
dR=l3.dRdig(R)
dC=errore_capacità(C)

#errore frequenza di taglio (punto 1a)
Ft=1/(R*C*2*np.pi)
dFt=np.sqrt(dR**2*C**2+dC**2*R**2)/(R*C*2*np.pi)

#Attenzuazione e errore (punto 1c e 1d)
A1=([attenuazione(2e3,Ft,dFt),attenuazione(2e4,Ft,dFt)])

Vout,freq=np.genfromtxt('dati/2.txt',unpack=True)
Vin=12.5
dVin=errore_osc_volt(12.5)
A=Vout/Vin
dA=errore_rapporto(Vout,dVosc(Vout),Vin,dVin)
pl.errorbar(freq,A,yerr=dA,fmt='.',markersize=1)
#qua faccio il punto 2.b.ii
#la retta obliqua
popt,pcov=curve_fit(lineare,np.log10(freq[7:]),np.log10(A[7:]))
print(popt)
x=np.linspace(3.5,6.5,10)
pl.plot(10**x,10**(lineare(x,*popt)))
#la retta parallela
popt,pcov=curve_fit(lineare,np.log10(freq[:4]),np.log10(A[:4]))
print(popt)
x=np.linspace(1,4,10)
pl.plot(10**x,10**(lineare(x,*popt)))

pl.yscale('log')
pl.ylabel('Vout/Vin')
pl.xscale('log')
pl.xlabel('frequenza')
pl.savefig('figure/a.png')
pl.close()


#inizo punto 2
Vin,Vout,freq=np.genfromtxt('dati/2a.txt',unpack=True)
dVin=dVosc(Vin)
dVout=dVosc(Vout)

Amis=Vout/Vin
dAmis=errore_rapporto(Vout,dVout,Vin,dVin)

#print(Amis,dAmis,A1)#stampo il guadagno misurato e il guadagno teorico

