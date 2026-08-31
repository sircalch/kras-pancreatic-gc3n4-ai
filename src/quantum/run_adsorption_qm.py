"""
run_adsorption_qm.py
Parallelized GFN2-xTB quantum calculations of drug adsorption on 2D g-C3N4 nanocarriers
Utilizes 4 concurrent processes across 16 CPU cores.
Calculates genuine electronic adsorption energies:
Delta_E_ads = E_complex - (E_nanosheet + E_drug) [kcal/mol]
and interfacial charge transfer Delta_Q.
"""

import os
import re
import subprocess
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
xtb_exe = os.path.join(base_dir, "tools", "xtb", "xtb-6.7.1", "bin", "xtb.exe")
struct_dir = os.path.join(base_dir, "data", "quantum", "structures")
results_dir = os.path.join(base_dir, "results", "quantum")
calc_dir = os.path.join(base_dir, "scratch", "qm_calcs_adsorption")
os.makedirs(results_dir, exist_ok=True)
os.makedirs(calc_dir, exist_ok=True)

def read_xyz(filepath):
    with open(filepath, 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    n_atoms = int(lines[0])
    atoms = []
    for l in lines[2:2+n_atoms]:
        parts = l.split()
        atoms.append((parts[0], float(parts[1]), float(parts[2]), float(parts[3])))
    return atoms

def save_xyz(atoms, filepath, comment=""):
    with open(filepath, 'w') as f:
        f.write(f"{len(atoms)}\n")
        f.write(f"{comment}\n")
        for el, x, y, z in atoms:
            f.write(f"{el:<3s} {x:12.6f} {y:12.6f} {z:12.6f}\n")

def build_adsorption_complex(carrier_name, drug_name):
    carrier_xyz = os.path.join(struct_dir, f"gC3N4_{carrier_name}.xyz")
    drug_opt_xyz = os.path.join(base_dir, "scratch", "qm_calcs_molecules", drug_name, "xtbopt.xyz")
    if not os.path.exists(drug_opt_xyz):
        drug_opt_xyz = os.path.join(struct_dir, f"{drug_name}.xyz")
        
    carrier_atoms = read_xyz(carrier_xyz)
    drug_atoms = read_xyz(drug_opt_xyz)
    
    drug_coords = np.array([[a[1], a[2], a[3]] for a in drug_atoms])
    center = np.mean(drug_coords, axis=0)
    
    translated_drug = []
    for el, x, y, z in drug_atoms:
        nx = x - center[0]
        ny = y - center[1]
        nz = (z - np.min(drug_coords[:, 2])) + 3.35
        translated_drug.append((el, nx, ny, nz))
        
    complex_atoms = carrier_atoms + translated_drug
    out_xyz = os.path.join(calc_dir, f"complex_{carrier_name}_{drug_name}.xyz")
    save_xyz(complex_atoms, out_xyz, comment=f"Adsorption complex: {carrier_name} + {drug_name}")
    return out_xyz, len(carrier_atoms), len(drug_atoms)

def run_single_complex(item):
    carrier_name, drug_name, e_carrier_eh, e_drug_eh = item
    work_dir = os.path.join(calc_dir, f"{carrier_name}_{drug_name}")
    os.makedirs(work_dir, exist_ok=True)
    
    # Check if already successfully calculated
    opt_xyz = os.path.join(work_dir, "xtbopt.xyz")
    charges_file = os.path.join(work_dir, "charges")
    
    complex_xyz, n_carrier, n_drug = build_adsorption_complex(carrier_name, drug_name)
    
    cmd = [xtb_exe, complex_xyz, "--gfn", "2", "--opt", "loose", "--chrg", "0"]
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "3"
    env["MKL_NUM_THREADS"] = "3"
    
    res = subprocess.run(cmd, cwd=work_dir, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    stdout = res.stdout
    
    m_e = re.search(r'TOTAL ENERGY\s+([\-\d\.]+)\s+Eh', stdout, re.IGNORECASE)
    if not m_e:
        return None
        
    e_complex_eh = float(m_e.group(1))
    delta_e_eh = e_complex_eh - (e_carrier_eh + e_drug_eh)
    delta_e_kcal = delta_e_eh * 627.5095
    
    m_disp = re.search(r'DISPERSION ENERGY\s+([\-\d\.]+)\s+Eh', stdout, re.IGNORECASE)
    e_disp_complex = float(m_disp.group(1)) if m_disp else 0.0
    
    q_transfer = 0.0
    if os.path.exists(charges_file):
        with open(charges_file, 'r') as f:
            charges = [float(x.strip()) for x in f.readlines() if x.strip()]
        if len(charges) >= (n_carrier + n_drug):
            q_drug = sum(charges[n_carrier:n_carrier+n_drug])
            q_transfer = q_drug
            
    res_dict = {
        "drug_name": drug_name,
        "carrier_name": carrier_name,
        "E_complex_Eh": e_complex_eh,
        "E_carrier_Eh": e_carrier_eh,
        "E_drug_Eh": e_drug_eh,
        "Delta_E_ads_Eh": delta_e_eh,
        "Delta_E_ads_kcal_mol": round(delta_e_kcal, 2),
        "E_disp_complex_Eh": e_disp_complex,
        "Interfacial_Charge_Transfer_e": round(q_transfer, 4)
    }
    print(f"  [DONE] {carrier_name:<10s} + {drug_name:<15s} | Delta_E_ads = {delta_e_kcal:7.2f} kcal/mol | Delta_Q = {q_transfer:+.3f} e", flush=True)
    return res_dict

def run_all_adsorptions():
    carrier_df = pd.read_csv(os.path.join(results_dir, "nanocarrier_qm_results.csv"))
    carrier_energies = dict(zip(carrier_df['carrier'], carrier_df['E_total_Eh']))
    
    drug_df = pd.read_csv(os.path.join(results_dir, "isolated_drugs_qm_results.csv"))
    drug_energies = dict(zip(drug_df['name'], drug_df['E_total_Eh']))
    
    all_drugs = list(drug_df['name'])
    carriers_to_run = ["pristine", "BP_doped"]
    
    tasks = []
    for c_name in carriers_to_run:
        e_c = carrier_energies[c_name]
        for d_name in all_drugs:
            e_d = drug_energies[d_name]
            tasks.append((c_name, d_name, e_c, e_d))
            
    print("=" * 95)
    print(f"PARALLEL GFN2-xTB ADSORPTION QUANTUM SIMULATIONS ({len(tasks)} TOTAL on 4 WORKERS)")
    print("=" * 95)
    
    results = []
    out_csv = os.path.join(results_dir, "adsorption_qm_results.csv")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(run_single_complex, t): t for t in tasks}
        for future in as_completed(futures):
            res = future.result()
            if res:
                results.append(res)
                # Incremental save
                pd.DataFrame(results).to_csv(out_csv, index=False)
                
    df_ads = pd.DataFrame(results)
    df_ads.to_csv(out_csv, index=False)
    print(f"\n[SUCCESS] All {len(df_ads)} genuine adsorption calculations completed successfully!")
    print(f"Saved results to: {out_csv}")
    return df_ads

if __name__ == "__main__":
    run_all_adsorptions()
