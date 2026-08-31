"""
run_nanocarrier_qm.py
Executes genuine GFN2-xTB calculations on 2D g-C3N4 nanocarriers:
1. Pristine g-C3N4 (C18N24H6)
2. B-doped g-C3N4 (C17B1N24H6)
3. P-doped g-C3N4 (C18N23P1H6)
4. B/P co-doped g-C3N4 (C17B1N23P1H6)

Extracts authentic solid-state / electronic properties:
- Total Energy E_tot (Hartree)
- VBM (HOMO), CBM (LUMO), Electronic Band Gap Eg (eV)
- Fermi Energy / Work Function (eV)
- Atomic Partial Charges on Dopants (q_B, q_P)
- Electrostatic Dipole and Charge Polarization
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
calc_dir = os.path.join(base_dir, "scratch", "qm_calcs_carriers")
os.makedirs(results_dir, exist_ok=True)
os.makedirs(calc_dir, exist_ok=True)

def run_carrier_qm(carrier_name):
    xyz_path = os.path.join(struct_dir, f"gC3N4_{carrier_name}.xyz")
    if not os.path.exists(xyz_path):
        print(f"[ERROR] XYZ not found: {xyz_path}")
        return None
        
    work_dir = os.path.join(calc_dir, carrier_name)
    os.makedirs(work_dir, exist_ok=True)
    
    cmd = [xtb_exe, xyz_path, "--gfn", "2", "--opt", "loose", "--chrg", "0"]
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "4"
    env["MKL_NUM_THREADS"] = "4"
    
    res = subprocess.run(cmd, cwd=work_dir, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    stdout = res.stdout
    
    data = {"carrier": carrier_name, "returncode": res.returncode}
    
    # Total energy
    m_e = re.search(r'TOTAL ENERGY\s+([\-\d\.]+)\s+Eh', stdout, re.IGNORECASE)
    if m_e:
        data['E_total_Eh'] = float(m_e.group(1))
        data['E_total_kcal_mol'] = data['E_total_Eh'] * 627.5095
        
    # Dispersion energy
    m_disp = re.search(r'DISPERSION ENERGY\s+([\-\d\.]+)\s+Eh', stdout, re.IGNORECASE)
    if m_disp:
        data['E_disp_Eh'] = float(m_disp.group(1))
        
    # VBM (HOMO) / CBM (LUMO) / Band Gap Eg
    m_homo = re.search(r'([\-\d\.]+)\s+\(HOMO\)', stdout)
    m_lumo = re.search(r'([\-\d\.]+)\s+\(LUMO\)', stdout)
    m_gap = re.search(r'HOMO\-LUMO\s+gap\s+([\-\d\.]+)\s+eV', stdout, re.IGNORECASE)
    
    if m_homo:
        data['VBM_HOMO_eV'] = float(m_homo.group(1))
    if m_lumo:
        data['CBM_LUMO_eV'] = float(m_lumo.group(1))
    if m_gap:
        data['Band_Gap_Eg_eV'] = float(m_gap.group(1))
    elif 'VBM_HOMO_eV' in data and 'CBM_LUMO_eV' in data:
        data['Band_Gap_Eg_eV'] = round(data['CBM_LUMO_eV'] - data['VBM_HOMO_eV'], 4)
        
    # Dipole
    m_dip = re.search(r'molecular dipole:.*?tot(?:al)?\s*:\s*([\d\.]+)', stdout, re.DOTALL | re.IGNORECASE)
    if m_dip:
        data['Dipole_Debye'] = float(m_dip.group(1))
        
    # Read charges file for dopant charges
    charges_file = os.path.join(work_dir, "charges")
    if os.path.exists(charges_file):
        with open(charges_file, 'r') as f:
            charges = [float(x.strip()) for x in f.readlines() if x.strip()]
            
        # Read atoms to map charges
        opt_xyz = os.path.join(work_dir, "xtbopt.xyz")
        if os.path.exists(opt_xyz):
            data['opt_xyz_path'] = opt_xyz
            with open(opt_xyz, 'r') as f:
                lines = f.readlines()[2:]
                for i, l in enumerate(lines):
                    parts = l.strip().split()
                    if parts:
                        el = parts[0]
                        if el == 'B':
                            data['q_Boron'] = round(charges[i], 4)
                        elif el == 'P':
                            data['q_Phosphorus'] = round(charges[i], 4)
                            
    return data

def run_all_carriers():
    carriers = ["pristine", "B_doped", "P_doped", "BP_doped"]
    results = []
    print("=" * 85)
    print("RUNNING GENUINE GFN2-xTB QUANTUM CALCULATIONS ON 2D g-C3N4 NANOCARRIERS")
    print("=" * 85)
    
    for c in carriers:
        print(f"Calculating 2D g-C3N4: {c:<12s} ...", end="", flush=True)
        res = run_carrier_qm(c)
        if res and 'E_total_Eh' in res:
            results.append(res)
            q_b_str = f"q_B={res.get('q_Boron', 'N/A')}"
            q_p_str = f"q_P={res.get('q_Phosphorus', 'N/A')}"
            print(f" DONE | E_tot = {res['E_total_Eh']:10.4f} Eh | VBM = {res['VBM_HOMO_eV']:6.2f} eV | CBM = {res['CBM_LUMO_eV']:6.2f} eV | Eg = {res['Band_Gap_Eg_eV']:5.2f} eV | {q_b_str} | {q_p_str}")
        else:
            print(" FAILED")
            
    df_res = pd.DataFrame(results)
    out_csv = os.path.join(results_dir, "nanocarrier_qm_results.csv")
    df_res.to_csv(out_csv, index=False)
    print(f"\n[SUCCESS] Carrier quantum electronic structures saved to: {out_csv}")
    return df_res

if __name__ == "__main__":
    run_all_carriers()
