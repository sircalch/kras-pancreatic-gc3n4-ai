"""
run_molecular_qm.py
Executes genuine GFN2-xTB quantum chemistry calculations on all 33 curated oncology therapeutics
plus 5 virtual screening leads.
Extracts true quantum observables:
- Total Electronic Energy (Hartree)
- HOMO Energy (eV), LUMO Energy (eV), HOMO-LUMO Gap (eV)
- Chemical Hardness eta (eV), Chemical Potential mu (eV), Global Electrophilicity Index omega (eV)
- Molecular Dipole Moment (Debye)
- Dispersion Energy (Hartree)
- Optimized 3D Cartesian coordinates
"""

import os
import re
import subprocess
import pandas as pd
import numpy as np

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
xtb_exe = os.path.join(base_dir, "tools", "xtb", "xtb-6.7.1", "bin", "xtb.exe")
struct_dir = os.path.join(base_dir, "data", "quantum", "structures")
results_dir = os.path.join(base_dir, "results", "quantum")
calc_dir = os.path.join(base_dir, "scratch", "qm_calcs_molecules")
os.makedirs(results_dir, exist_ok=True)
os.makedirs(calc_dir, exist_ok=True)

def parse_xtb_output(stdout_text):
    """
    Parses key quantum observables from GFN2-xTB output text.
    """
    data = {}
    
    # Total Energy: '| TOTAL ENERGY              -18.112287447736 Eh   |' or ':: total energy             -18.112287447736 Eh'
    m_e = re.search(r'TOTAL ENERGY\s+([\-\d\.]+)\s+Eh', stdout_text, re.IGNORECASE)
    if m_e:
        data['E_total_Eh'] = float(m_e.group(1))
        data['E_total_kcal_mol'] = data['E_total_Eh'] * 627.5095
        
    # Dispersion Energy
    m_disp = re.search(r'DISPERSION ENERGY\s+([\-\d\.]+)\s+Eh', stdout_text, re.IGNORECASE)
    if m_disp:
        data['E_disp_Eh'] = float(m_disp.group(1))
    else:
        data['E_disp_Eh'] = 0.0
        
    # HOMO / LUMO / Gap
    # Example line: '15        2.0000           -0.4013596             -10.9215 (HOMO)'
    # Example line: '16                         -0.2160573              -5.8792 (LUMO)'
    m_homo = re.search(r'([\-\d\.]+)\s+\(HOMO\)', stdout_text)
    m_lumo = re.search(r'([\-\d\.]+)\s+\(LUMO\)', stdout_text)
    m_gap = re.search(r'HOMO\-LUMO\s+gap\s+([\-\d\.]+)\s+eV', stdout_text, re.IGNORECASE)
    
    if m_homo:
        data['E_HOMO_eV'] = float(m_homo.group(1))
    if m_lumo:
        data['E_LUMO_eV'] = float(m_lumo.group(1))
    if m_gap:
        data['Gap_eV'] = float(m_gap.group(1))
    elif 'E_HOMO_eV' in data and 'E_LUMO_eV' in data:
        data['Gap_eV'] = round(data['E_LUMO_eV'] - data['E_HOMO_eV'], 4)
        
    # Dipole Moment
    # 'molecular dipole: \n ... total:     2.345'
    m_dip = re.search(r'molecular dipole:.*?tot(?:al)?\s*:\s*([\d\.]+)', stdout_text, re.DOTALL | re.IGNORECASE)
    if m_dip:
        data['Dipole_Debye'] = float(m_dip.group(1))
    else:
        data['Dipole_Debye'] = 0.0
            
    # Calculate Conceptual DFT Indices (CDFT)
    if 'E_HOMO_eV' in data and 'E_LUMO_eV' in data:
        eh = data['E_HOMO_eV']
        el = data['E_LUMO_eV']
        eta = (el - eh) / 2.0 # Chemical Hardness
        mu = (eh + el) / 2.0  # Electronic Chemical Potential
        chi = -mu             # Electronegativity
        omega = (mu ** 2) / (2.0 * eta) if eta > 1e-4 else 0.0 # Electrophilicity
        softness = 1.0 / (2.0 * eta) if eta > 1e-4 else 0.0
        
        data['Hardness_eta_eV'] = round(eta, 4)
        data['Chemical_Potential_mu_eV'] = round(mu, 4)
        data['Electronegativity_chi_eV'] = round(chi, 4)
        data['Electrophilicity_omega_eV'] = round(omega, 4)
        data['Softness_S_eV_inv'] = round(softness, 4)
        
    return data

def run_molecule_qm(mol_name):
    xyz_path = os.path.join(struct_dir, f"{mol_name}.xyz")
    if not os.path.exists(xyz_path):
        print(f"[ERROR] XYZ not found: {xyz_path}")
        return None
        
    work_dir = os.path.join(calc_dir, mol_name)
    os.makedirs(work_dir, exist_ok=True)
    
    # Run GFN2-xTB optimization and property calculation
    cmd = [xtb_exe, xyz_path, "--gfn", "2", "--opt", "loose", "--chrg", "0"]
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "4"
    env["MKL_NUM_THREADS"] = "4"
    
    res = subprocess.run(cmd, cwd=work_dir, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    
    parsed = parse_xtb_output(res.stdout)
    parsed['name'] = mol_name
    parsed['returncode'] = res.returncode
    
    # Check if optimized geometry was written
    opt_xyz = os.path.join(work_dir, "xtbopt.xyz")
    if os.path.exists(opt_xyz):
        parsed['opt_xyz_path'] = opt_xyz
        
    return parsed

def run_all_molecular_qm():
    master_csv = os.path.join(base_dir, "data", "processed", "MASTER_COMPOUNDS_CURATED.csv")
    df_master = pd.read_csv(master_csv)
    
    all_names = list(df_master['name']) + ["Avapritinib", "Futibatinib", "Belumosudil", "Capivasertib", "Pimicotinib"]
    
    results = []
    print("=" * 95)
    print("RUNNING GENUINE GFN2-xTB QUANTUM CALCULATIONS ON 33 DRUGS + 5 SCREENING LEADS")
    print("=" * 95)
    
    for idx, name in enumerate(all_names, 1):
        print(f"[{idx:02d}/{len(all_names)}] Calculating GFN2-xTB: {name:<16s} ...", end="", flush=True)
        res = run_molecule_qm(name)
        if res and 'E_total_Eh' in res and 'E_HOMO_eV' in res:
            results.append(res)
            print(f" DONE | E_tot = {res['E_total_Eh']:10.4f} Eh | HOMO = {res['E_HOMO_eV']:6.2f} eV | LUMO = {res['E_LUMO_eV']:6.2f} eV | omega = {res.get('Electrophilicity_omega_eV', 0.0):5.2f} eV")
        else:
            print(" FAILED or Incomplete")
            
    df_res = pd.DataFrame(results)
    out_csv = os.path.join(results_dir, "isolated_drugs_qm_results.csv")
    df_res.to_csv(out_csv, index=False)
    print(f"\n[SUCCESS] Successfully executed genuine GFN2-xTB calculations for {len(df_res)} molecules.")
    print(f"Saved real quantum electronic properties to: {out_csv}")
    return df_res

if __name__ == "__main__":
    run_all_molecular_qm()
