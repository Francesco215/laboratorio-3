import numpy as np

# Errore della misura di ddp del multimetro digitale
# supponendo che si sia scelta La scala corretta
# Author: Francesco Sacco
def errore_ddp_digitale(V):
    if V<0.2: return np.sqrt(V**2*25e-6+1e-8)
    if V<2:   return np.sqrt(V**2*25e-6+1e-6)
    if V<20:  return np.sqrt(V**2*25e-6+1e-4)
    if V<200: return np.sqrt(V**2*25e-6+1e-2)

errore_ddp_dig=np.vectorize(errore_ddp_digitale)

# Errore della misura di resistenza del multimetro digitale
# supponendo che si sia scelta La scala corretta
# Author: Francesco Sacco
def errore_res_digitale(R):
    if R<200: return np.sqrt(R**2*64e-6+9e-2)
    if R<2e3: return np.sqrt(R**2*64e-6+1)
    if R<2e4: return np.sqrt(R**2*64e-6+1e2)
    if R<2e5: return np.sqrt(R**2*64e-6+1e4)
    if R<2e6: return np.sqrt(R**2*64e-6+1e6)
    if R<2e7: return np.sqrt(R**2*1e-4+1e8)
    
errore_res_dig=np.vectorize(errore_ddp_digitale)