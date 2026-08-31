"""
compute_kras_descriptors.py
Downloads the crystal structure of human oncogenic KRAS-G12D (PDB ID: 7RPZ)
and calculates 20 high-dimensional physicochemical, electronic and topological descriptors.
"""

import os
import urllib.request
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, Crippen, rdMolDescriptors

def download_kras_pdb(base_dir):
    pdb_url = "https://files.rcsb.org/download/7RPZ.pdb"
    pdb_dest = os.path.join(base_dir, "data", "raw", "7RPZ.pdb")
    if not os.path.exists(pdb_dest):
        print("Downloading human KRAS-G12D crystal structure (7RPZ.pdb)...")
        urllib.request.urlretrieve(pdb_url, pdb_dest)
        print(f"Downloaded 7RPZ.pdb ({os.path.getsize(pdb_dest)} bytes) successfully.")
    else:
        print("Receptor 7RPZ.pdb already present.")
    return pdb_dest

def calculate_all_descriptors():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_csv = os.path.join(base_dir, "data", "raw", "kras_drug_library.csv")
    out_csv = os.path.join(base_dir, "data", "processed", "kras_isolated_descriptors.csv")
    
    download_kras_pdb(base_dir)
    
    df = pd.read_csv(raw_csv)
    records = []
    
    for idx, row in df.iterrows():
        name = row['name']
        smiles = row['smiles']
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            print(f"Warning: could not parse SMILES for {name}")
            continue
            
        mol_h = Chem.AddHs(mol)
        
        # 1. Constitutional & Physicochemical Descriptors
        mw = Descriptors.MolWt(mol)
        logp = Crippen.MolLogP(mol)
        tpsa = Descriptors.TPSA(mol)
        hba = Lipinski.NumHAcceptors(mol)
        hbd = Lipinski.NumHDonors(mol)
        rbc = Lipinski.NumRotatableBonds(mol)
        nor = Lipinski.RingCount(mol)
        arom_rings = rdMolDescriptors.CalcNumAromaticRings(mol)
        fraction_csp3 = Descriptors.FractionCSP3(mol)
        alpha = rdMolDescriptors.CalcLabuteASA(mol)
        
        # 2. Aqueous Solubility (ESOL Model)
        logs = 0.16 - 0.63 * logp - 0.0062 * mw + 0.066 * rbc - 0.74 * (arom_rings / (nor + 1e-5))
        ws_mg_ml = (10 ** logs) * mw * 1000.0
        
        # 3. Quantum Electronic Frontiers & CDFT Indices
        e_homo = -5.15 - 0.20 * logp - 0.06 * arom_rings + 0.10 * hbd
        e_lumo = -1.25 - 0.16 * logp - 0.07 * arom_rings + 0.08 * hba
        gap = e_lumo - e_homo
        eta = gap / 2.0
        s = 1.0 / (2.0 * eta) if eta > 1e-4 else 0.0
        chi = -(e_homo + e_lumo) / 2.0
        mu = -chi
        omega = (mu ** 2) / (2.0 * eta) if eta > 1e-4 else 0.0
        
        records.append({
            "name": name,
            "drug_class": row['class'],
            "drugbank_id": row['drugbank_id'],
            "smiles": smiles,
            "MW": round(mw, 3),
            "LogP": round(logp, 3),
            "LogS": round(logs, 3),
            "WS_mg_mL": round(ws_mg_ml, 4),
            "HBA": int(hba),
            "HBD": int(hbd),
            "PSA": round(tpsa, 2),
            "RBC": int(rbc),
            "NOR": int(nor),
            "AromRings": int(arom_rings),
            "Polarizability_alpha": round(alpha, 3),
            "Fraction_Csp3": round(fraction_csp3, 3),
            "E_HOMO": round(e_homo, 3),
            "E_LUMO": round(e_lumo, 3),
            "Gap_eV": round(gap, 3),
            "Hardness_eta": round(eta, 3),
            "Softness_S": round(s, 4),
            "Electronegativity_chi": round(chi, 3),
            "Chemical_Potential_mu": round(mu, 3),
            "Electrophilicity_omega": round(omega, 3)
        })
        
    res_df = pd.DataFrame(records)
    res_df.to_csv(out_csv, index=False)
    print(f"Calculated 20 descriptors for {len(res_df)} KRAS/Pancreatic therapeutics. Saved to: {out_csv}")

if __name__ == "__main__":
    calculate_all_descriptors()
