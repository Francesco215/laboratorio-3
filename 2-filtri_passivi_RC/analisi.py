import numpy as np
import menzalib as mz
import pylab as pl
from scipy.optimize import curve_fit

def attenuazione_passa_basso(f,ft,dft):
    A=1/np.sqrt(1+f**2/ft**2)
    dA=(1+f**2/ft**2)**(-3/2)*f**2*ft**(-3)*dft
    return A,dA

def attenuazione_passa_alto(f,ft,dft):
    A=1/np.sqrt(1-ft**2/f**2)
    dA=(1-ft**2/f**2)**(-3/2)*ft*f**(-2)*dft
    return A,dA

def errore_rapporto(x,dx,y,dy):
    return(y**(-2))*np.sqrt(x**2*dy**2+y**2*dx**2)

def lineare(x,q,m):
    return q+m*x

def frequenza_di_taglio(R,C,dR,dC):
    ft=1/(R*C*2*np.pi)
    dft=np.sqrt(dR**2*C**2+dC**2*R**2)/(R*C*2*np.pi)
    return ft,dft

"""funzione che calcola l'intersezione ed errore tra due rette indipendenti
    con equazioni y=x*m1+q1 e y=x*m2+q2"""

def int_rette(popt1,popt2,pcov1,pcov2):
    q1,q2=popt1[0],popt2[0]
    m1,m2=popt1[1],popt2[1]
    pcov=np.zeros((4,4))
    pcov[:2,:2]=pcov1
    pcov[2:,2:]=pcov2
    gradientex=([1/(m1-m2),-(q1-q2)/(m1-m2)**2,
               -1/(m1-m2), (q1-q2)/(m1-m2)**2])
    x=(q2-q1)/(m1-m2)
    y=(q2*m1-q1*m2)/(m1-m2)
    dx=np.sqrt(np.linalg.multi_dot([gradientex,pcov,gradientex]))
    return ([x,y,dx])

#resistenze e capacità con errori
R1=3.29e3
C1=9.88e-9
dR1=mz.dRdig(R1)
dC1=mz.dCdig(C1)

#errore frequenza di taglio (punto 1a)
Ft1,dFt1=frequenza_di_taglio(R1,C1,dR1,dC1)

#Attenzuazione e errore (punto 1c e 1d)
A1=([attenuazione_passa_basso(2e3,Ft1,dFt1),attenuazione_passa_basso(2e4,Ft1,dFt1)])

#qua faccio il plot del diagramma di bode
Vout,freq=np.genfromtxt('dati/2.txt',unpack=True)
Vin=12.5
dVin=mz.dVosc(12.5)
A=Vout/Vin
dA=errore_rapporto(Vout,mz.dVosc(Vout),Vin,dVin)
pl.errorbar(freq,20*np.log10(A),yerr=dA,fmt='.',markersize=3)
#qua faccio il punto 2.b.ii
#la retta obliqua
popt1,pcov1=curve_fit(lineare,np.log10(freq[7:]),np.log10(A[7:]),(1,1),dA[7:]/(A[7:]*np.log(10)))
x=np.linspace(3.5,6.5,10)
pl.plot(10**x,20*(lineare(x,*popt1)))
#la retta parallela
popt2,pcov2=curve_fit(lineare,np.log10(freq[:4]),np.log10(A[:4]),(1,1),dA[:4]/(A[:4]*np.log(10)))
x=np.linspace(1,4,10)
pl.plot(10**x,20*(lineare(x,*popt2)))
#l'intersezione delle due rette
x,y,dx=int_rette(popt1,popt2,pcov1,pcov2)
#print(int_rette(popt1,popt2,pcov1,pcov2)) 
pl.plot(10**x,20*y,'.')


pl.ylabel('Vout/Vin')
pl.xscale('log')
pl.xlabel('Frequenza [Hz]')
pl.savefig('figure/a.png')


#punto 2
Vin,Vout,freq=np.genfromtxt('dati/2a.txt',unpack=True)
dVin=mz.dVosc(Vin)
dVout=mz.dVosc(Vout)
Amis=Vout/Vin
dAmis=errore_rapporto(Vout,dVout,Vin,dVin)
#print(Amis,dAmis,A1)#stampo il guadagno misurato e il guadagno teorico

#punto 3
ft=1.1/(np.pi*74e-6)
dft=errore_rapporto(1.1/np.pi,0,74e-6,2e-6)
print(ft,dft)

#punto 5
R2=3.3e3
C2=111.7e-9
dR2=mz.dRdig(R2)
dC2=mz.dCdig(C2)

Ft2,dFt2=frequenza_di_taglio(R2,C2,dR2,dC2)
#il punto 5b poi si fa a cazzo


