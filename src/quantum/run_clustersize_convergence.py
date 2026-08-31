"""
run_clustersize_convergence.py
==============================
Evaluates finite-size and edge-termination effects of the 2D g-C3N4 cluster.
Compares adsorption energies on the standard 48-atom cluster (C21N21H6)
versus an extended 96-atom 2D cluster model for representative therapeutics:
  1. 5-Fluorouracil (small pyrimidine)
  2. Gemcitabine (nucleoside analog)
  3. MRTX1133 (clinical KRAS-G12D inhibitor)
"""

import os
import sys
import subprocess
import numpy as np
import pandas as pd
from pathlib import Path

BASE = Path(r"c:\Users\Andre\Proyectos doctorado\kras-pancreatic-gC3N4-ai")
XTB_EXE = BASE / "tools" / "xtb" / "xtb-6.7.1" / "bin" / "xtb.exe"
SCRATCH = BASE / "scratch" / "cluster_size_convergence"
SCRATCH.mkdir(parents=True, exist_ok=True)
OUT_CSV = BASE / "results" / "quantum" / "cluster_size_convergence_results.csv"

SMALL_CARRIER_XYZ = BASE / "scratch" / "qm_calcs_carriers" / "pristine" / "xtbopt.xyz"

def read_xyz(path: Path):
    lines = path.read_text().splitlines()
    atoms = []
    coords = []
    for l in lines[2:]:
        if not l.strip():
            continue
        p = l.split()
        atoms.append(p[0])
        coords.append([float(p[1]), float(p[2]), float(p[3])])
    return atoms, np.array(coords)

def write_xyz(path: Path, atoms, coords, comment=""):
    lines = [str(len(atoms)), comment]
    for a, c in zip(atoms, coords):
        lines.append(f"{a:<4} {c[0]:14.6f} {c[1]:14.6f} {c[2]:14.6f}")
    path.write_text("\n".join(lines))

def build_extended_carrier(base_atoms, base_coords):
    """
    Builds a lateral extension of the heptazine sheet by translating in x and y
    and removing overlapping atoms within 1.0 A.
    """
    # Shift vector based on cluster dimensions
    xmin, xmax = base_coords[:, 0].min(), base_coords[:, 0].max()
    dx = (xmax - xmin) * 0.75
    
    # 2-unit lateral dimer sheet
    shifted_coords = base_coords.copy()
    shifted_coords[:, 0] += dx
    
    all_atoms = base_atoms + base_atoms
    all_coords = np.vstack([base_coords, shifted_coords])
    
    # Remove overlapping atoms
    keep_indices = []
    for i in range(len(all_coords)):
        is_dup = False
        for k in keep_indices:
            if np.linalg.norm(all_coords[i] - all_coords[k]) < 0.9:
                is_dup = True
                break
        if not is_dup:
            keep_indices.append(i)
            
    ext_atoms = [all_atoms[i] for i in keep_indices]
    ext_coords = all_coords[keep_indices]
    return ext_atoms, ext_coords

def run_xtb_calc(xyz_path: Path, opt=False):
    work_dir = xyz_path.parent
    cmd = [str(XTB_EXE), xyz_path.name, "--gfn", "2", "--chrg", "0", "--uhf", "1" if "complex" in xyz_path.name or "carrier" in xyz_path.name else "0"]
    if opt:
        cmd.extend(["--opt", "loose"])
    else:
        cmd.append("--sp")
        
    res = subprocess.run(cmd, cwd=work_dir, capture_output=True)
    stdout_text = res.stdout.decode('utf-8', errors='ignore') if res.stdout else ""
    energy = None
    for line in stdout_text.splitlines():
        if "TOTAL ENERGY" in line:
            parts = line.split()
            for p in parts:
                try:
                    energy = float(p)
                    break
                except ValueError:
                    pass
    return energy

def main():
    print("=== Cluster Size Convergence Test (GFN2-xTB) ===")
    s_atoms, s_coords = read_xyz(SMALL_CARRIER_XYZ)
    print(f"Small cluster: {len(s_atoms)} atoms")
    
    # Build extended cluster
    ext_atoms, ext_coords = build_extended_carrier(s_atoms, s_coords)
    print(f"Extended cluster: {len(ext_atoms)} atoms")
    
    # Optimize extended cluster
    ext_carr_dir = SCRATCH / "carrier_extended"
    ext_carr_dir.mkdir(parents=True, exist_ok=True)
    ext_carr_xyz = ext_carr_dir / "carrier_ext.xyz"
    write_xyz(ext_carr_xyz, ext_atoms, ext_coords)
    
    print("Optimizing extended carrier...")
    E_ext_carr = run_xtb_calc(ext_carr_xyz, opt=True)
    print(f"Extended Carrier E = {E_ext_carr:.6f} Eh")

    # Small carrier E
    s_carr_dir = SCRATCH / "carrier_small"
    s_carr_dir.mkdir(parents=True, exist_ok=True)
    s_carr_xyz = s_carr_dir / "carrier_small.xyz"
    write_xyz(s_carr_xyz, s_atoms, s_coords)
    E_s_carr = run_xtb_calc(s_carr_xyz, opt=False)
    print(f"Small Carrier E = {E_s_carr:.6f} Eh")

    HARTREE_TO_KCAL = 627.509474
    records = []
    
    test_drugs = ["5-Fluorouracil", "Gemcitabine", "MRTX1133"]
    for drug in test_drugs:
        print(f"\n--- Testing cluster size effect for {drug} ---")
        drug_xyz = BASE / "scratch" / "qm_calcs_molecules" / drug / "xtbopt.xyz"
        d_atoms, d_coords = read_xyz(drug_xyz)
        
        d_dir = SCRATCH / drug / "isolated"
        d_dir.mkdir(parents=True, exist_ok=True)
        d_xyz = d_dir / f"{drug}.xyz"
        write_xyz(d_xyz, d_atoms, d_coords)
        E_drug = run_xtb_calc(d_xyz, opt=False)
        
        # 1. Small cluster complex
        small_comp_xyz = BASE / "scratch" / "qm_calcs_adsorption" / f"pristine_{drug}" / "xtbopt.xyz"
        E_small_comp = run_xtb_calc(small_comp_xyz, opt=False)
        E_ads_small = (E_small_comp - E_s_carr - E_drug) * HARTREE_TO_KCAL if E_small_comp else None
        
        # 2. Extended cluster complex
        # Place drug at center of extended sheet
        c_zmax = ext_coords[:, 2].max()
        d_zmin = d_coords[:, 2].min()
        dz = (c_zmax + 3.35) - d_zmin
        p_coords = d_coords.copy()
        p_coords[:, 2] += dz
        p_coords[:, 0] += (ext_coords[:, 0].mean() - p_coords[:, 0].mean())
        p_coords[:, 1] += (ext_coords[:, 1].mean() - p_coords[:, 1].mean())
        
        ext_comp_atoms = ext_atoms + d_atoms
        ext_comp_coords = np.vstack([ext_coords, p_coords])
        
        ext_comp_dir = SCRATCH / drug / "extended_complex"
        ext_comp_dir.mkdir(parents=True, exist_ok=True)
        ext_comp_xyz = ext_comp_dir / "complex_ext.xyz"
        write_xyz(ext_comp_xyz, ext_comp_atoms, ext_comp_coords)
        
        print(f"Optimizing extended complex for {drug}...")
        E_ext_comp = run_xtb_calc(ext_comp_xyz, opt=True)
        E_ads_ext = (E_ext_comp - E_ext_carr - E_drug) * HARTREE_TO_KCAL if E_ext_comp else None
        
        delta = (E_ads_ext - E_ads_small) if (E_ads_ext is not None and E_ads_small is not None) else None
        print(f"  Small cluster E_ads: {E_ads_small:.2f} kcal/mol")
        print(f"  Extended cluster E_ads: {E_ads_ext:.2f} kcal/mol")
        print(f"  Finite-size Delta: {delta:.2f} kcal/mol")
        
        records.append({
            "Compound": drug,
            "N_atoms_small_cluster": len(s_atoms),
            "N_atoms_ext_cluster": len(ext_atoms),
            "E_ads_small_cluster_kcal_mol": round(E_ads_small, 2) if E_ads_small else None,
            "E_ads_ext_cluster_kcal_mol": round(E_ads_ext, 2) if E_ads_ext else None,
            "Finite_Size_Delta_kcal_mol": round(delta, 2) if delta else None
        })
        
    df = pd.DataFrame(records)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)
    print(f"\nSaved Cluster Size Convergence Results: {OUT_CSV}")
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
