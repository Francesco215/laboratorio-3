import numpy as np
import matplotlib.pyplot as pl
import scipy.optimize

def errore_volt_digitale(V):
    if V<0.2: return np.sqrt(V**2*25e-6+1e-8)
    if V<2:   return np.sqrt(V**2*25e-6+1e-6)
    if V<20:  return np.sqrt(V**2*25e-6+1e-4)
    if V<200: return np.sqrt(V**2*25e-6+1e-2)

vf=np.vectorize(errore_volt_digitale)

def errore_res_digitale(R):
    if R<200: return np.sqrt(R**2*64e-6+9e-2)
    if R<2e3: return np.sqrt(R**2*64e-6+1)
    if R<2e4: return np.sqrt(R**2*64e-6+1e2)
    if R<2e5: return np.sqrt(R**2*64e-6+1e4)
    if R<2e6: return np.sqrt(R**2*64e-6+1e6)
    if R<2e7: return np.sqrt(R**2*1e-4+1e8)

def funzione_fit(x, a, b) :
    return a*x + b

def fit_data(dati) :
    Vin, Vout = dati[1], dati[0]
    dVin, dVout = vf(Vin), vf(Vout)
    sigma_eff = dVout
    for i in range(10) :
        popt, pcov = scipy.optimize.curve_fit(funzione_fit, Vin, Vout, sigma=sigma_eff)
        sigma_eff = np.sqrt(dVout**2 + (popt[0]*dVin)**2)
    return [popt, pcov]
    
def plot_data(dati, popt) :
    Vin, Vout = dati[0], dati[1]
    dVin, dVout = vf(Vin), vf(Vout)
    temp = np.linspace(0, 10, 2000)
    pl.figure()
    pl.xlabel("Vin [V]")
    pl.ylabel("Vout [V]")
    pl.errorbar(Vin, Vout, dVin, dVout, fmt='.', label="Dati")
    pl.plot(temp, funzione_fit(temp, *popt), linewidth=1, label="fit")
    pl.legend()
    pl.savefig("plot_2c.png")
    pl.show()

def errore_rapporto(x,dx,y,dy):
    return(y**(-2))*np.sqrt(x**2*dy**2+y**2*dx**2)

#res_b=[974,1182]
#res_c=[3.8e6,4.81e6]
    
dati_2b = np.genfromtxt('dati/dati_2b.txt', skip_header=2, unpack=True)
dati_2c = np.genfromtxt('dati/dati_2c.txt', skip_header=2, unpack=True)
dati_3b = np.genfromtxt('dati/dati_3b.txt', skip_header=2, unpack=True)
dati_3c = np.genfromtxt('dati/dati_3c.txt', skip_header=2, unpack=True)
dati_4cursore = np.genfromtxt('dati/dati_4cursore.txt', skip_header=1, unpack=True)
dati_4oscilloscopio = np.genfromtxt('dati/dati_4oscilloscopio.txt', skip_header=1, unpack=True)

popt, pcov = fit_data(dati_3c)
popt_err = np.sqrt(np.diag(pcov))
print("a = %.4f +- %.4f \nb = %.5f +- %.5f" % (popt[0], popt[1], popt_err[0], popt_err[1]))

R2=4.81e6
dR2=errore_res_digitale(R2)
R1=3.80e6
dR1=errore_res_digitale(R1)
a=popt[0]-1-R1/R2
da=errore_rapporto(R1,dR1,R2,dR2)
print(a,da)
print(R1/a,errore_rapporto(R1,dR1,a,da))

Vinn,Voutt=dati_3c
print(Vinn,Vinn*0.04,Voutt,Voutt*0.04)
print(Voutt/Vinn,errore_rapporto(Voutt,Voutt*0.04,Vinn,Vinn*0.04))

#plot_data(dati_2b, popt)

dati_4cursore=[[990,9.8e3,1e5,9.9e5],
        [10,1e2,1e3,1e3]]#questi sono gli errori
dati_4oscilloscopio=[997,9.9e3,99.9e3,1.004e6]

pl.show()

