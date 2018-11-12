import menzalib as mz
import numpy as np
import pylab as pl

def lineare(x,a,b):
	return a*x + b
def costante (x,a,b):
	return a



#Punto 1.a
R1=1.187e3
dR1=mz.dRdig(R1)
R2=12.16e3
dR2=mz.dRdig(R2)

Aexp=R2/R1
dAexp=mz.drapp(R2,dR2,R1,dR1)

#punto 1.c
Vin,Vout=np.genfromtxt('dati/1c.txt',unpack='True')
dVin=mz.dVosc(Vin)
dVout=mz.dVosc(Vout)
A=Vout/Vin
dA=mz.drapp(Vout,dVout,Vin,dVin)


tab1=[mz.ne_tex(Vin,dVin),
	  mz.ne_tex(Vout,dVout),
	  mz.ne_tex(A,dA)]

mz.stampa_matrice_latex(tab1)
popt,pcov=mz.curve_fitdx(lineare,Vin,Vout,dx=dVin,dy=dVout)
chi2,pval=mz.chi2_pval(lineare,Vin,Vout,dVout,popt,dx=dVin,df=costante)


#-------------------------------------------------------
#punto 2.a
Vout,f=np.genfromtxt('dati/2a.txt',unpack='True')
Vin=np.ones(len(Vout))*1.14
pl.plot(f,(Vout/Vin)**20,'.')
pl.plot(7.519,(10/np.sqrt(2))**20,'.')
pl.plot(210100,(10/np.sqrt(2))**20,'.')
pl.xscale('log')
pl.yscale('log')
pl.ylabel('A[dB]')
pl.xlabel('f[Hz]')
pl.savefig('dati/2a.png')
pl.close()


#--------------------------------------------------------
#punto 3.a
Vout,f,Vin,faset=np.genfromtxt('dati/3a.txt',unpack='True')
pl.plot(f,(Vout/Vin)**20,'.')
pl.xscale('log')
pl.yscale('log')
pl.ylabel('A[dB]')
pl.xlabel('f[Hz]')
pl.savefig('dati/3a.png')
pl.close()

dVin=mz.dVosc(Vin)
dVout=mz.dVosc(Vout)
A=Vout/Vin
dA=mz.drapp(Vout,dVout,Vin,dVin)
dA=20*mz.dlog10(A,dA)
A=20*np.log10(A)
df=mz.dpoli(1/f,mz.dtosc(1/f),-1)
dfaset=mz.dtosc(faset)
fase=2*faset*f
dfase=2*mz.dprod(faset,dfaset,f,df)
tab3a=[mz.ne_tex(f,df),mz.ne_tex(Vout,dVout),mz.ne_tex(A,dA),
		mz.ne_tex(faset,dfaset),mz.ne_tex(fase,dfase)]
mz.stampa_matrice_latex(tab3a)

