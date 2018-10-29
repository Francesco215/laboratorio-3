import menzalib as l3
import numpy as np


Vout,f = np.loadtxt("dati.txt", unpack=True)
Vin = 1.
dVout=l3.dVosc(Vout)
dVin=l3.dVosc(Vin)
Av=Vout/Vin
dAv=l3.drapp(Vout, dVout, Vin, dVin)

out = open("output.txt","w")
for i in range(len(Vout)) :
    s = "%0.1f& %0.1f& %0.2f& %0.3f& %0.3f& %0.4f& %0.4f&\n"%(f[i], Vin, dVin, Vout[i], dVout[i], Av[i], dAv[i])
    out.write(s)
out.close()