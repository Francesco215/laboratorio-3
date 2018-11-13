import numpy as np
import menzalib as mz
import pylab as plt
from scipy.optimize import curve_fit

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
Vbe = 0.7 # ddp base emettitore al punto di lavoro
Vrc = 9.92
dVcc, dVbe, dVrc = mz.dVdig([Vcc, Vbe, Vrc])

Vbb = Vcc / (1+R1/R2)
dVbb = mz.drapp(Vcc, dVcc, 1+R1/R2, mz.drapp(R1, dR1, R2, dR2))
Ic_q = (Vbb-Vbe) / Re
dIc_q = mz.drapp(Vbb-Vbe, dVbb+dVbe, Re, dRe)
Vce_q = Vcc - Ic_q*(Rc+Re)
dVce_q = dVcc + mz.dprod(Vbb-Vbe, dVbb+dVbe, 1+(Rc/Re), mz.drapp(Rc, dRc, Re, dRe))

print(Vbb,dVbb)
print("Ic_q %f+-%f\nVce_q %f+-%f" % (Ic_q, dIc_q, Vce_q, dVce_q))
#print(18.24/R1, 1.644/R2, Ic_q/100)
print(Vrc/Rc, mz.drapp(Vrc, dVrc, Rc, dRc))


Vin = 1
#Vout, f = np.genfromtxt("dati/dati.txt", unpack=True)
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
t3=-5
t4=-3
dVout = mz.dVosc(Vout)
Av = Vout/Vin
dAv = mz.drapp(Vout, dVout, Vin, mz.dVosc(Vin))
popt1,pcov1=curve_fit(lineare,np.log10(f[:t1]),20*np.log10(Av[:t1]), sigma=20*mz.dlog10(Av[:t1],dAv[:t1]))
popt2,pcov2=curve_fit(lineare,np.log10(f[t2:t3]),20*np.log10(Av[t2:t3]), sigma=20*mz.dlog10(Av[t2:t3],dAv[t2:t3]))
popt3,pcov3=curve_fit(lineare,np.log10(f[t4:]),20*np.log10(Av[t4:]), sigma=20*mz.dlog10(Av[t4:],dAv[t4:]))


lf,asd,dlf=int_rette(popt1,popt2,pcov1,pcov2)
print(10**lf,np.log(10)*10**lf*dlf,100*(np.log(10)*10**lf*dlf)/(10**lf))

lf,asd,dlf=int_rette(popt2,popt3,pcov2,pcov3)
print(10**lf,np.log(10)*10**lf*dlf,100*(np.log(10)*10**lf*dlf)/(10**lf))


plt.figure(1)
plt.rcParams['lines.linewidth'] = 1
plt.errorbar(f, 20*np.log10(Vout), 20*mz.dlog10(Av, dAv), fmt='.', label="dati", markersize=5)

x=np.linspace(1,2,10)
y=lineare(x,*popt1)
plt.plot(10**x,y)

x=np.linspace(1.7,5,10)
y=lineare(x,*popt2)
plt.plot(10**x,y)

x=np.linspace(4.7,6.7,10)
y=lineare(x,*popt3)
plt.plot(10**x,y)

plt.xlabel("Frequenza [Hz]")
plt.ylabel("Av [dB]")
plt.xscale("log")
plt.legend()
plt.savefig('fit.png')
plt.show()