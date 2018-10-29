import numpy as np
import menzalib as mz
import pylab as plt
from scipy.optimize import curve_fit

def errore_rapporto(x,dx,y,dy):
    return(y**(-2))*np.sqrt(x**2*dy**2+y**2*dx**2)

def errore_prodotto(x, dx, y, dy) :
    return np.sqrt(y**2*dx**2 + x**2*dy**2)

def lineare(x,q,m):
    return q+m*x

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

R1 = 178500
R2 = 17650
Rc = 9820
Re = 1014
dR1, dR2, dRc, dRe = mz.dRdig([R1, R2, Rc, Re])

Cout = 110.7e-9
Cin = 221e-9

Vcc = 19.97
Vbe = 0.614 # ddp base emettitore al punto di lavoro
Vrc = 9.92
dVcc, dVbe, dVrc = mz.dVdig([Vcc, Vbe, Vrc])

Vbb = Vcc / (1+R1/R2)
dVbb = errore_rapporto(Vcc, dVcc, 1+R1/R2, errore_rapporto(R1, dR1, R2, dR2))
Ic_q = (Vbb-Vbe) / Re
dIc_q = errore_rapporto(Vbb-Vbe, dVbb+dVbe, Re, dRe)
Vce_q = Vcc - Ic_q*(Rc+Re)
dVce_q = dVcc + errore_prodotto(Vbb-Vbe, dVbb+dVbe, 1+(Rc/Re), errore_rapporto(Rc, dRc, Re, dRe))

print(Vbb,dVbb)
print("Ic_q %f+-%f\nVce_q %f+-%f" % (Ic_q, dIc_q, Vce_q, dVce_q))
#print(18.24/R1, 1.644/R2, Ic_q/100)
print(Vrc/Rc, errore_rapporto(Vrc, dVrc, Rc, dRc))


Vin = 1
Vout, f = np.genfromtxt("dati/dati.txt", unpack=True)
plt.figure()

def ordina_2_vett(v1,v2):
	if len(v1)!=len(v2): return 0
	s1=np.sort(v1)
	s2=np.zeros(len(s1))
	for i in range(0,len(v1)):
		for j in range(0,len (v1)):
			if(s1[i]==v1[j]):
				s2[i]=v2[j]
				break
	return s1,s2

f,Vout=ordina_2_vett(f,Vout)

t1=3
t2=6
t3=-6
t4=-3
plt.plot(f, Vout, 'o')

popt1,pcov1=curve_fit(lineare,np.log10(f[:t1]),np.log10(Vout[:t1]))
popt2,pcov2=curve_fit(lineare,np.log10(f[t2:t3]),np.log10(Vout[t2:t3]))
popt3,pcov3=curve_fit(lineare,np.log10(f[t4:]),np.log10(Vout[t4:]))

x=np.linspace(1,2,10)
y=lineare(x,*popt1)
plt.plot(10**x,10**y)

x=np.linspace(1.7,5,10)
y=lineare(x,*popt2)
plt.plot(10**x,10**y)

x=np.linspace(4.7,6.7,10)
y=lineare(x,*popt3)
plt.plot(10**x,10**y)

plt.xscale("log")
plt.yscale("log")
plt.savefig('fit.png')

lf,asd,dlf=int_rette(popt1,popt2,pcov1,pcov2)
print(10**lf,np.log(10)*10**lf*dlf,100*(np.log(10)*10**lf*dlf)/(10**lf))

lf,asd,dlf=int_rette(popt2,popt3,pcov2,pcov3)
print(10**lf,np.log(10)*10**lf*dlf,100*(np.log(10)*10**lf*dlf)/(10**lf))

