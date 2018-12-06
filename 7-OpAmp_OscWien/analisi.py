import menzalib as mz
import numpy as np
import pylab as pl
from numpy import floor,log10,absolute,round,vectorize,transpose


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


def numero_con_errore_latex(x,dx):
	if x!=0:
		exp=int(floor(log10(absolute(x))))#guardo l'ordine di grandezza di x
		if absolute(exp)==1: exp=0 #nel caso l'esponente è uno o meno uno non uso la n.s.
		x=x/10**exp     #porto la virgola dopo la prima cifra
		dx=dx/10**exp   #porto la virgola dove si trova quella della x
	if dx!=0: cifr=int(floor(log10(absolute(dx))))  #guardo l'ordine di grandezza di dx
	if x==0: 
		if dx!=0: 
			dx=round(dx/10**cifr)#arrotondo dx
			return "$0\\pm"+str(round(dx))+"\\times 10^{"+str(cifr)+"}$"
		else: return "$0\\pm0$"
	#taglio le di x con un ordine di grandezza inferiore a dx
	x=round(x,absolute(cifr))       
	dx=round(dx,absolute(cifr)) #taglio le cifre significative di dx dopo la prima
	#ritorno la stringa in latex
	if exp==0:
		return  "$"+str(x)+"\\pm"+str(dx)+"$" 
	return  "$("+str(x)+"\\pm"+str(dx)+")\\times 10^{"+str(exp)+"}$"
#vettorizzo la funzione
ne_tex=vectorize(numero_con_errore_latex)


Vt,dVt=[0.260,mz.dVosc(0.260)]#voltaggio in ingresso


f,df,deltaf,ddeltaf,V=np.genfromtxt('dati/1.txt',unpack='True')#aggiusta l'errore sullo sfasamento
ddeltaf=np.sqrt((0.02*deltaf)**2+ddeltaf**2)
#calcolo la fase
fase=360*f/deltaf
dfase=360*mz.drapp(f,df,deltaf,ddeltaf)

#metto i dati alla frequenza di taglio
f=np.append(f,1598.34)#frequenza di tagli
df=np.append(df,0.04)
V=np.append(V,182)#ampiezza di taglio
fase=np.append(fase,0)
dfase=np.append(dfase,0.0007*360/2*np.pi)#aggiusta l'errore sullo sfasamento

#ordino in i dati
f_temp=f
f,fase=ordina_2_vett(f,fase)
f,V=ordina_2_vett(f_temp,V)
f,dfase=ordina_2_vett(f_temp,dfase)


fase[-2:]=-fase[-2:]#inverto la fase degli ultimi due dati
V=V/1000#passo in milivolt
dV=mz.dVosc(V)#calcolo l'errore del voltaggio
A=V/Vt#calcolo l'attenuazione
dA=mz.drapp(V,dV,Vt,dVt)#errore attenuazione

M=[mz.ne_tex(f,df),ne_tex(V,dV),ne_tex(20*np.log10(A),20* mz.dlog10(A,dA)),ne_tex(fase,dfase)]
mz.mat_tex(M,'$f$[Hz] & $V_A$[V] & $V_A/V_{in}[dB]$ & fase [gradi]','relazione/tabella.tex')


pl.errorbar(f,fase,yerr=dfase,fmt='.')
pl.plot([400,3000],[0,0])#linea x=0
pl.xlim(400,3000)
pl.xscale('log')
pl.ylabel('fase del segnale [gradi]')
pl.xlabel('frequenza in ingresso [Hz]')
pl.savefig('relazione/figure/1.png')
#pl.show()
pl.close()


pl.errorbar(f,20*np.log10(A),yerr=20* mz.dlog10(A,dA),fmt='.')
pl.plot([400,3000],[0,0])#linea x=0
pl.xlim(400,3000)
pl.ylabel('A*beta[dB]')
pl.xlabel('frequenza in ingresso [Hz]')
pl.xscale('log')
pl.savefig('relazione/figure/2.png')
pl.close()
