import menzalib as mz
import numpy as np
import pylab as pl

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



Vt,dVt=[0.260,mz.dVosc(0.260)]#voltaggio in ingresso


f,df,deltaf,ddeltaf,V=np.genfromtxt('dati/1.txt',unpack='True')#aggiusta l'errore sullo sfasamento

#calcolo la fase
fase=2*np.pi*f/deltaf
dfase=2*np.pi*mz.drapp(f,df,deltaf,ddeltaf)

#metto i dati alla frequenza di taglio
f=np.append(f,1598.34)#frequenza di tagli
df=np.append(df,0.04)
V=np.append(V,182)#ampiezza di taglio
fase=np.append(fase,0)
dfase=np.append(dfase,0)#aggiusta l'errore sullo sfasamento

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

"""
for i in [f,df,V,dV,fase,dfase]:
	print(i)
	print(len(i))
	print(type(i))
"""
nef=mz.ne_tex(f,df)
neV=mz.ne_tex(V,dV)
print(fase)
#nefase=mz.ne_tex(fase,dfase)
"""
M=[mz.ne_tex(f,df),mz.ne_tex(V,dV),mz.ne_tex(fase,dfase)]
mz.mat_tex(M)


pl.errorbar(f,fase,yerr=dfase,fmt='.')
pl.plot([400,3000],[0,0])#linea x=0
pl.xlim(400,3000)
pl.xscale('log')
pl.ylabel('fase del segnale [rad]')
pl.xlabel('frequenza in ingresso [Hz]')
pl.savefig('figure/1.png')
pl.show()
pl.close()


pl.errorbar(f,20*np.log10(A),yerr=20* mz.dlog10(A,dA),fmt='.')
pl.plot([400,3000],[0,0])#linea x=0
pl.xlim(400,3000)
pl.ylabel('A*beta[dB]')
pl.xlabel('frequenza in ingresso [Hz]')
pl.xscale('log')
pl.savefig('figure/2.png')
pl.close()

"""