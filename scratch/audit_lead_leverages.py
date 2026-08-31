import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Master training
df_train = pd.read_csv('data/processed/MASTER_COMPOUNDS_CURATED.csv')
features = ['MW', 'PSA', 'Polarizability_alpha', 'Electrophilicity_omega']
scaler = StandardScaler()
X_train_s = scaler.fit_transform(df_train[features].values)
n, p = X_train_s.shape
h_star = 3.0 * (p + 1) / n
inv_cov = np.linalg.pinv(X_train_s.T @ X_train_s)

# Virtual screening candidates
leads = [
    {'name': 'Avapritinib', 'MW': 498.57, 'PSA': 89.24, 'Polarizability_alpha': 152.4, 'Electrophilicity_omega': 2.85, 'Vina': -9.43, 'N_heavy': 37, 'E_ads_DFTB': -52.40, 'E_ads_DFT': -50.80},
    {'name': 'Futibatinib', 'MW': 418.46, 'PSA': 92.15, 'Polarizability_alpha': 136.8, 'Electrophilicity_omega': 3.12, 'Vina': -9.04, 'N_heavy': 31, 'E_ads_DFTB': -48.60, 'E_ads_DFT': -47.10},
    {'name': 'Belumosudil', 'MW': 452.52, 'PSA': 84.60, 'Polarizability_alpha': 144.2, 'Electrophilicity_omega': 2.94, 'Vina': -8.99, 'N_heavy': 34, 'E_ads_DFTB': -50.10, 'E_ads_DFT': -48.70},
    {'name': 'Capivasertib', 'MW': 428.92, 'PSA': 87.50, 'Polarizability_alpha': 138.5, 'Electrophilicity_omega': 2.78, 'Vina': -8.45, 'N_heavy': 30, 'E_ads_DFTB': -46.80, 'E_ads_DFT': -45.30},
    {'name': 'Pimicotinib', 'MW': 476.54, 'PSA': 96.30, 'Polarizability_alpha': 148.1, 'Electrophilicity_omega': 3.05, 'Vina': -8.21, 'N_heavy': 35, 'E_ads_DFTB': -51.20, 'E_ads_DFT': -49.60}
]

print(f"Training warning limit h* = {h_star:.4f}")
for l in leads:
    x_raw = np.array([[l['MW'], l['PSA'], l['Polarizability_alpha'], l['Electrophilicity_omega']]])
    x_s = scaler.transform(x_raw)
    h_i = (x_s @ inv_cov @ x_s.T)[0,0]
    l['h_i'] = h_i
    l['LE'] = abs(l['Vina']) / l['N_heavy']
    ad_status = "IN" if h_i <= h_star else "OUT"
    print(f"{l['name']:15s}: hi = {h_i:.4f} (h* = {h_star:.4f}) -> {ad_status:3s} | Vina = {l['Vina']:.2f} kcal/mol | LE = {l['LE']:.3f} kcal/mol/atom | DFTB = {l['E_ads_DFTB']:.2f} | DFT = {l['E_ads_DFT']:.2f}")
