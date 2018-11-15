import numpy as np
import pylab as pl
import menzalib as mz
from scipy.optimize import curve_fit

def lineare(x, a, b):
    return a*x+b

#2c-1
Vin, tmin, tmax = np.genfromtxt("dati/1c.txt", unpack=True)
tmed, dtmed = (tmin+tmax)/2, (tmax-tmin)/2
pl.errorbar(Vin, tmed, dtmed, fmt='.', label="Misure")
pl.xlabel("Vin [V]")
pl.ylabel("Durata segnale in uscita [us]")
pl.legend()
pl.savefig("dati/1c.png")
pl.close()

#2c-2
Vdiscr, Vpot = np.genfromtxt("dati/1c-2.txt", unpack=True)
dVpot, dVdiscr = mz.dVdig(Vpot), mz.dVosc(Vdiscr)
popt, pcov = mz.curve_fitdx(lineare, Vpot, Vdiscr, dVpot, dVdiscr)
chi2, pvalue = mz.chi2_pval(lineare, Vpot, Vdiscr, dVdiscr, popt, dVpot)
dpopt = np.sqrt(np.diag(pcov))
print("a={:.3}+-{:.3} b={:.3}+-{:.3}".format(popt[0],dpopt[0],popt[1],dpopt[1]))
print("Chi2rid=%0.2f" %(chi2/3))

t = np.linspace(0, 2, 1000)
pl.plot(t, lineare(t, *popt), label="Fit")
pl.errorbar(Vpot, Vdiscr, dVdiscr, dVpot, fmt='.', label="Misure")
pl.xlabel("Vpot [V]")
pl.ylabel("Vdiscr [V]")
pl.legend()
pl.savefig("dati/1c-2.png")
pl.close()