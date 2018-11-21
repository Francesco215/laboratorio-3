import numpy as np
import pylab as pl
import menzalib as mz
from scipy.optimize import curve_fit

def lineare(x, a, b):
    return a*x+b

def logaritmico(x, a, b):
    f = a*np.log(b*x)
#   f[f<0]=0
    return f

def dlogaritmico(x, a, b):
    return a/x


#2c-1
Vin, tmin, tmax = np.genfromtxt("dati/1c.txt", unpack=True)
#tmin, tmax = tmin*10**-6, tmax*10**-6

dVin, dtmax = mz.dVosc(Vin), mz.dtosc(tmax)
tmax, dtmax = tmin, mz.dtosc(tmin)
popt, pcov, dpopt, chi2, pvalue = mz.curve_fitdx(logaritmico, Vin, tmax, dVin, dtmax, dlogaritmico)
print(popt,dpopt, chi2/2)

t = np.linspace(0.2, 10, 2000)
pl.errorbar(Vin, tmax, dtmax, dVin, fmt='.', label="Misure")
pl.plot(t, logaritmico(t, *popt), label="Fit")
pl.xlabel("Vin [V]")
pl.ylabel("Durata segnale in uscita [us]")
pl.legend()
pl.savefig("dati/1c.png")
pl.close()

#2c-2
Vdiscr, Vpot = np.genfromtxt("dati/1c-2.txt", unpack=True)
dVpot, dVdiscr = mz.dVdig(Vpot), mz.dVosc(Vdiscr)
popt, pcov, dpopt, chi2, pvalue = mz.curve_fitdx(lineare, Vpot, Vdiscr, dVpot, dVdiscr)
print("a={:.3}+-{:.3} b={:.3}+-{:.3}".format(popt[0],dpopt[0],popt[1],dpopt[1]))
print("Chi2rid=%0.2f" %(chi2/3))

t = np.linspace(0, 2, 1000)
pl.errorbar(Vpot, Vdiscr, dVdiscr, dVpot, fmt='.', label="Misure")
pl.plot(t, lineare(t, *popt), label="Fit")
pl.xlabel("Vpot [V]")
pl.ylabel("Vs [V]")
pl.legend()
pl.savefig("dati/1c-2.png")
pl.show()