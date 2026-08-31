import urllib.request
import json
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
from sklearn.preprocessing import StandardScaler

cids = {
    'Avapritinib': 118607832,
    'Futibatinib': 118984457,
    'Belumosudil': 46843936,
    'Capivasertib': 25227436,
    'Pimicotinib': 163073748
}

df_train = pd.read_csv('data/processed/MASTER_COMPOUNDS_CURATED.csv')
features = ['MW', 'PSA', 'Polarizability_alpha', 'Electrophilicity_omega']
scaler = StandardScaler()
X_train_s = scaler.fit_transform(df_train[features].values)
inv_cov = np.linalg.pinv(X_train_s.T @ X_train_s)
h_star = 3.0 * (4 + 1) / 33

print(f"Warning leverage threshold h* = {h_star:.4f}")
for name, cid in cids.items():
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/CanonicalSMILES,MolecularWeight,TPSA,MolecularFormula/JSON"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))['PropertyTable']['Properties'][0]
            smi = data['CanonicalSMILES']
            mol = Chem.MolFromSmiles(smi)
            mw = Descriptors.MolWt(mol)
            psa = Descriptors.TPSA(mol)
            alpha = Descriptors.MolMR(mol) * 1.5
            n_elec = mol.GetNumElectrons()
            omega = (n_elec / (mw + 1e-5)) * 10.0
            
            x_raw = np.array([[mw, psa, alpha, omega]])
            x_s = scaler.transform(x_raw)
            h_i = (x_s @ inv_cov @ x_s.T)[0,0]
            ad_status = "IN" if h_i <= h_star else "OUT"
            print(f"{name:15s} (CID:{cid:10d}): MW={mw:6.2f}, PSA={psa:6.2f}, alpha={alpha:6.2f}, omega={omega:5.2f} -> hi={h_i:.4f} ({ad_status})")
    except Exception as e:
        print(f"{name}: {e}")
