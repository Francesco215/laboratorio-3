import numpy as np
import pylab as pl
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
    Vin, Vout = dati[0], dati[1]
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
    pl.errorbar(Vin, Vout, dVin, dVout, fmt='o')
    pl.plot(temp, funzione_fit(temp, *popt))

    
#res_b=[974,1182]
#res_c=[3.8e6,4.81e6]
    
dati_2b = np.genfromtxt('dati\dati_2b.txt', skip_header=2, unpack=True)
dati_2c = np.genfromtxt('dati\dati_2c.txt', skip_header=2, unpack=True)
dati_3b = np.genfromtxt('dati\dati_3b.txt', skip_header=2, unpack=True)
dati_3c = np.genfromtxt('dati\dati_3c.txt', skip_header=2, unpack=True)


popt, pcov = fit_data(dati_2b)
plot_data(dati_2b, popt)
popt_err = np.sqrt(np.diag(pcov))
print("a = %.4f +- %.4f \nb = %.5f +- %.5f" % (popt[0], popt[1], popt_err[0], popt_err[1]))

dati_4cursore=[[990,9.8e3,1e5,9.9e5],
        [10,1e2,1e3,1e3]]#questi sono gli errori
dati_4oscilloscopio=[997,9.9e3,99.9e3,1.004e6]

pl.show()
