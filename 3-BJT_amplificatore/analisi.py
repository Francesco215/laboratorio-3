import numpy as np
import menzalib as mz
import pylab as plt

def errore_rapporto(x,dx,y,dy):
    return(y**(-2))*np.sqrt(x**2*dy**2+y**2*dx**2)

def errore_prodotto(x, dx, y, dy) :
    return np.sqrt(y**2*dx**2 + x**2*dy**2)

R1 = 178500
R2 = 17650
Rc = 9820
Re = 1014
dR1, dR2, dRc, dRe = mz.dRdig([R1, R2, Rc, Re])

Cout = 110.7e-9
Cin = 221e-9

Vcc = 19.97
Vbe = 0.614 # ddp base emettitore al punto di lavoro
Vrc = 9.92
dVcc, dVbe, dVrc = mz.dVdig([Vcc, Vbe, Vrc])

Vbb = Vcc / (1+R1/R2)
dVbb = errore_rapporto(Vcc, dVcc, 1+R1/R2, errore_rapporto(R1, dR1, R2, dR2))
Ic_q = (Vbb-Vbe) / Re
dIc_q = errore_rapporto(Vbb-Vbe, dVbb+dVbe, Re, dRe)
Vce_q = Vcc - Ic_q*(Rc+Re)
dVce_q = dVcc + errore_prodotto(Vbb-Vbe, dVbb+dVbe, 1+(Rc/Re), errore_rapporto(Rc, dRc, Re, dRe))


print("Ic_q %f+-%f\nVce_q %f+-%f" % (Ic_q, dIc_q, Vce_q, dVce_q))
#print(18.24/R1, 1.644/R2, Ic_q/100)
print(Vrc/Rc, errore_rapporto(Vrc, dVrc, Rc, dRc))


Vin = 1
Vout, f = np.genfromtxt("/home/lorenzo/Desktop/laboratorio-3/3-BJT_amplificatore/dati/dati.txt", unpack=True)
plt.figure()
plt.plot(f, Vout/Vin, 'o')
plt.xscale("log")
plt.yscale("log")
plt.show()
