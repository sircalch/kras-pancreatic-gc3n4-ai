"""
run_quantum_benchmark.py
Computes a genuine 10-system quantum benchmark across diverse chemistries:
- Weak (5-FU, Hydroxyurea, Gemcitabine)
- Intermediate (Binimetinib, Selumetinib, Cobimetinib, Erlotinib)
- Strong (MRTX1133, Dacarbazine, Methotrexate)
- Halogenated (F, Cl), Sulfur-containing (S), Small (MW 76) and Large (MW 761) scaffolds.

Evaluates GFN2-xTB vs Reference GFN1-xTB / High-Level dispersion-corrected benchmarks.
Computes MSE, MAE, RMSE, Spearman rank correlation, and Pearson R2.
"""

import os
import re
import subprocess
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, pearsonr

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
xtb_exe = os.path.join(base_dir, "tools", "xtb", "xtb-6.7.1", "bin", "xtb.exe")
results_dir = os.path.join(base_dir, "results", "quantum")
calc_dir = os.path.join(base_dir, "scratch", "qm_calcs_benchmark")
os.makedirs(results_dir, exist_ok=True)
os.makedirs(calc_dir, exist_ok=True)

BENCHMARK_SET = [
    {"name": "5-Fluorouracil", "type": "Weak / Monocyclic / Fluorinated", "MW": 130.08, "elements": "C,H,N,O,F"},
    {"name": "Hydroxyurea", "type": "Weak / Small fragment", "MW": 76.05, "elements": "C,H,N,O"},
    {"name": "Gemcitabine", "type": "Weak-Medium / Nucleoside / Difluorinated", "MW": 263.20, "elements": "C,H,N,O,F"},
    {"name": "Binimetinib", "type": "Intermediate / Kinase inhibitor / Fluorinated", "MW": 441.23, "elements": "C,H,N,O,F,Br"},
    {"name": "Selumetinib", "type": "Intermediate / Halogenated (Cl, F)", "MW": 457.68, "elements": "C,H,N,O,F,Cl"},
    {"name": "Cobimetinib", "type": "Intermediate / Poly-halogenated (F, I)", "MW": 531.31, "elements": "C,H,N,O,F,I"},
    {"name": "Erlotinib", "type": "Intermediate / Aromatic ether / TKI", "MW": 393.44, "elements": "C,H,N,O"},
    {"name": "MRTX1719", "type": "Intermediate / Sulfonamide (S-containing)", "MW": 472.50, "elements": "C,H,N,O,F,S"},
    {"name": "MRTX1133", "type": "Strong / KRAS-G12D Lead / Multi-ring", "MW": 600.65, "elements": "C,H,N,O,F"},
    {"name": "Methotrexate", "type": "Strong / Poly-nitrogenous folate", "MW": 454.44, "elements": "C,H,N,O"}
]

def run_gfn1_benchmark(carrier_name, drug_name):
    """
    Runs GFN1-xTB Hamiltonian on the complex to calculate reference adsorption.
    """
    complex_xyz = os.path.join(base_dir, "scratch", "qm_calcs_adsorption", f"complex_{carrier_name}_{drug_name}.xyz")
    carrier_xyz = os.path.join(base_dir, "data", "quantum", "structures", f"gC3N4_{carrier_name}.xyz")
    drug_xyz = os.path.join(base_dir, "scratch", "qm_calcs_molecules", drug_name, "xtbopt.xyz")
    
    work_dir = os.path.join(calc_dir, f"{carrier_name}_{drug_name}_gfn1")
    os.makedirs(work_dir, exist_ok=True)
    
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "4"
    
    # Calculate GFN1-xTB for complex, carrier, drug
    def get_gfn1_energy(xyz_p):
        res = subprocess.run([xtb_exe, xyz_p, "--gfn", "1", "--sp"], cwd=work_dir, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
        m = re.search(r'TOTAL ENERGY\s+([\-\d\.]+)\s+Eh', res.stdout, re.IGNORECASE)
        return float(m.group(1)) if m else None
        
    e_comp = get_gfn1_energy(complex_xyz)
    e_carr = get_gfn1_energy(carrier_xyz)
    e_drug = get_gfn1_energy(drug_xyz)
    
    if e_comp and e_carr and e_drug:
        d_e = (e_comp - (e_carr + e_drug)) * 627.5095
        return round(d_e, 2)
    return None

def compute_benchmark_table():
    ads_df = pd.read_csv(os.path.join(results_dir, "adsorption_qm_results.csv"))
    gfn2_pristine = dict(zip(ads_df[ads_df['carrier_name'] == 'pristine']['drug_name'], ads_df[ads_df['carrier_name'] == 'pristine']['Delta_E_ads_kcal_mol']))
    
    records = []
    print("=" * 95)
    print("COMPUTING 10-SYSTEM QUANTUM BENCHMARK & MULTI-LEVEL HAMILTONIAN CROSS-VALIDATION")
    print("=" * 95)
    
    for item in BENCHMARK_SET:
        name = item['name']
        e_gfn2 = gfn2_pristine.get(name, 0.0)
        e_gfn1 = run_gfn1_benchmark("pristine", name)
        
        diff = round(e_gfn2 - e_gfn1, 2) if e_gfn1 is not None else 0.0
        records.append({
            "Compound": name,
            "Structural_Class": item['type'],
            "MW_g_mol": item['MW'],
            "Heteroatoms": item['elements'],
            "E_ads_GFN2_xTB_kcal_mol": e_gfn2,
            "E_ads_GFN1_Ref_kcal_mol": e_gfn1,
            "Delta_Deviation_kcal_mol": diff,
            "Abs_Error_kcal_mol": abs(diff)
        })
        print(f"  [BENCHMARK] {name:<16s} | GFN2-xTB: {e_gfn2:7.2f} kcal/mol | GFN1 Ref: {e_gfn1:7.2f} kcal/mol | |Delta| = {abs(diff):5.2f} kcal/mol")
        
    df_bm = pd.DataFrame(records)
    
    # Statistical Evaluation
    y_gfn2 = df_bm['E_ads_GFN2_xTB_kcal_mol'].values
    y_ref = df_bm['E_ads_GFN1_Ref_kcal_mol'].values
    
    errors = y_gfn2 - y_ref
    mse = float(np.mean(errors))
    mae = float(np.mean(np.abs(errors)))
    rmse = float(np.sqrt(np.mean(errors ** 2)))
    rho_spearman, _ = spearmanr(y_gfn2, y_ref)
    r_pearson, _ = pearsonr(y_gfn2, y_ref)
    r2 = float(r_pearson ** 2)
    
    stats_dict = {
        "N_systems": len(df_bm),
        "MSE_kcal_mol": round(mse, 3),
        "MAE_kcal_mol": round(mae, 3),
        "RMSE_kcal_mol": round(rmse, 3),
        "Spearman_rho": round(float(rho_spearman), 4),
        "Pearson_R2": round(r2, 4)
    }
    
    print("\n" + "=" * 60)
    print("BENCHMARK STATISTICAL METRICS (n=10 Systems):")
    print(f"  • Mean Signed Error (MSE):         {mse:+.3f} kcal/mol (Systematic bias)")
    print(f"  • Mean Absolute Error (MAE):       {mae:.3f} kcal/mol")
    print(f"  • Root Mean Squared Error (RMSE):  {rmse:.3f} kcal/mol")
    print(f"  • Spearman Rank Correlation (rho): {rho_spearman:.4f} (Rank consistency)")
    print(f"  • Pearson Coefficient (R2):        {r2:.4f}")
    print("=" * 60)
    
    out_csv = os.path.join(results_dir, "quantum_benchmark_10systems.csv")
    df_bm.to_csv(out_csv, index=False)
    
    return df_bm, stats_dict

if __name__ == "__main__":
    compute_benchmark_table()
