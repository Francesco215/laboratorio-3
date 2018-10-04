import numpy as np
import pylab as pl

def errore_volt_digitale(V):
	if V<0.2: return np.sqrt(V**2*25e-6+1e-8)
	if V<2:   return np.sqrt(V**2*25e-6+1e-6)
	if V<20:  return np.sqrt(V**2*25e-6+1e-4)
	if V<200: return np.sqrt(V**2*25e-6+1e-2)

def errore_res_digitale(R):
	if R<200: return np.sqrt(R**2*64e-6+9e-2)
	if R<2e3: return np.sqrt(R**2*64e-6+1)
	if R<2e4: return np.sqrt(R**2*64e-6+1e2)
	if R<2e5: return np.sqrt(R**2*64e-6+1e4)
	if R<2e6: return np.sqrt(R**2*64e-6+1e6)
	if R<2e7: return np.sqrt(R**2*1e-4+1e8)

dati_2b=[[1.928,5.94,4.24,2.650,6.19,7.28,8.41,9.79,0.868],
		 [0.868,2.68,1.91,1.194,2.80,3.29,3.80,4.42,0.392]]
res_b=[974,1182]

dati_2c=[[0.754,1.825,2.890,4.150,5.26,7.02,8.13,9.23,6.17],
		 [0.347,0.839,1.332,1.910,2.42,3.24,3.74,4.25,2.84]]
res_c=[3.8e6,4.81e6]

pl.plot(dati_2b[0],dati_2b[1])
pl.plot(dati_2c[0],dati_2c[1])

dati_3c=[[1.68,3.72,7.44,9.8],
		 [0.30,0.68,1.28,1.76]]
dati_3b=[[1.760,4.64,7.60,9.80],
		 [0.776,2.12,3.32,4.40]]

pl.plot(dati_3c[0],dati_3c[1])
pl.plot(dati_3b[0],dati_3b[1])

dati_4cursore=[[990,9.8e3,1e5,9.9e5],
		[10,1e2,1e3,1e3]]#questi sono gli errori
dati_4oscilloscopio=[997,9.9e3,99.9e3,1.004e6]

pl.show()
