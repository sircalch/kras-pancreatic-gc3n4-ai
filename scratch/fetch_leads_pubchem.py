import urllib.request
import json
import urllib.parse
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
from sklearn.preprocessing import StandardScaler

names = ['Avapritinib', 'Futibatinib', 'Belumosudil', 'Capivasertib', 'Pimicotinib']
df_train = pd.read_csv('data/processed/MASTER_COMPOUNDS_CURATED.csv')
features = ['MW', 'PSA', 'Polarizability_alpha', 'Electrophilicity_omega']
scaler = StandardScaler()
X_train_s = scaler.fit_transform(df_train[features].values)
inv_cov = np.linalg.pinv(X_train_s.T @ X_train_s)
h_star = 3.0 * (4 + 1) / 33

print(f"=== TRUE PUBCHEM AUDIT & LEVERAGE CALCULATION (h* = {h_star:.4f}) ===")
for n in names:
    try:
        url_cid = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{urllib.parse.quote(n)}/cids/JSON"
        req = urllib.request.Request(url_cid, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            cid = json.loads(resp.read().decode())['IdentifierList']['CID'][0]
            
        url_prop = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/MolecularWeight,MolecularFormula,SMILES,TPSA/JSON"
        req = urllib.request.Request(url_prop, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())['PropertyTable']['Properties'][0]
            form = data['MolecularFormula']
            smi = data['SMILES']
            mol = Chem.MolFromSmiles(smi)
            mw = Descriptors.MolWt(mol)
            psa = Descriptors.TPSA(mol)
            alpha = Descriptors.MolMR(mol) * 1.5
            n_elec = mol.GetNumElectrons()
            omega = (n_elec / (mw + 1e-5)) * 10.0
            heavy = mol.GetNumHeavyAtoms()
            
            x_raw = np.array([[mw, psa, alpha, omega]])
            x_s = scaler.transform(x_raw)
            h_i = (x_s @ inv_cov @ x_s.T)[0,0]
            ad_status = "IN" if h_i <= h_star else "OUT"
            print(f"{n:15s} | CID:{cid:10d} | Form:{form:18s} | MW:{mw:6.2f} | Heavy:{heavy:2d} | PSA:{psa:6.2f} | hi={h_i:.4f} ({ad_status})")
    except Exception as e:
        print(f"{n}: {e}")
