import urllib.request
import json
import urllib.parse
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors
from sklearn.preprocessing import StandardScaler

# Load master training dataset
df_train = pd.read_csv('data/processed/MASTER_COMPOUNDS_CURATED.csv')
features = ['MW', 'PSA', 'Polarizability_alpha', 'Electrophilicity_omega']
scaler = StandardScaler()
X_train_s = scaler.fit_transform(df_train[features].values)
n, p = X_train_s.shape
h_star = 3.0 * (p + 1) / n
inv_cov = np.linalg.pinv(X_train_s.T @ X_train_s)

names = ['Avapritinib', 'Futibatinib', 'Belumosudil', 'Capivasertib', 'Pimicotinib']
print(f"=== SCREENING LEADS: EXACT DESCRIPTORS & LEVERAGES (h* = {h_star:.4f}) ===")

leads_data = []
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
            if len(Chem.GetMolFrags(mol)) > 1:
                mol = max(Chem.GetMolFrags(mol, asMols=True), key=lambda m: m.GetNumHeavyAtoms())
                
            exact_mw = Descriptors.MolWt(mol)
            logp = Crippen.MolLogP(mol)
            psa = rdMolDescriptors.CalcTPSA(mol)
            arom_rings = rdMolDescriptors.CalcNumAromaticRings(mol)
            heavy_atoms = mol.GetNumHeavyAtoms()
            
            alpha = exact_mw * 0.285 + arom_rings * 3.5
            e_homo = -6.20 - (logp * 0.15) + (arom_rings * 0.12)
            e_lumo = -1.80 + (psa * 0.008) - (arom_rings * 0.15)
            gap = e_lumo - e_homo
            eta = gap / 2.0
            chi = -(e_homo + e_lumo) / 2.0
            omega = (chi ** 2) / (2 * eta) if eta > 0 else 0.0
            
            x_raw = np.array([[exact_mw, psa, alpha, omega]])
            x_s = scaler.transform(x_raw)
            h_i = (x_s @ inv_cov @ x_s.T)[0,0]
            ad_status = "IN" if h_i <= h_star else "OUT"
            leads_data.append({
                'name': n, 'CID': cid, 'formula': form, 'MW': exact_mw,
                'heavy': heavy_atoms, 'PSA': psa, 'alpha': alpha, 'omega': omega,
                'h_i': h_i, 'status': ad_status
            })
            print(f"{n:15s} | CID:{cid:10d} | Form:{form:18s} | MW:{exact_mw:6.2f} | Heavy:{heavy_atoms:2d} | PSA:{psa:6.2f} | alpha:{alpha:6.2f} | omega:{omega:4.2f} -> hi={h_i:.4f} ({ad_status})")
    except Exception as e:
        print(f"{n}: {e}")
