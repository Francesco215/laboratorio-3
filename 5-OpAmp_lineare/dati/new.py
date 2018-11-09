import menzalib as l3
import numpy as np


Vout,f = np.loadtxt("2a.txt", unpack=True)
Vin = 1.14
dVin = l3.dVosc(Vin)
dVout=l3.dVosc(Vout)
Av=Vout/Vin
dAv=l3.drapp(Vout, dVout, Vin, dVin)

out = open("output.txt","w")
for i in range(len(Vout)) :
    s = "$%0.1f \pm %0.1f$& $ %0.2f \pm %0.3f$& $%0.3f\pm %0.4f$ \\\ \n"%(f[i], f[i]*0.01, Vout[i], dVout[i], Av[i], dAv[i])
    out.write(s)
out.close()