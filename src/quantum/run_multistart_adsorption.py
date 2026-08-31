"""
run_multistart_adsorption.py
============================
Performs multi-start adsorption optimizations for representative drugs (5-FU, Gemcitabine, MRTX1133)
on pristine 2D g-C3N4 using GFN2-xTB.
Generates 3 distinct initial geometric orientations per drug:
  1. Standard parallel orientation (0 deg in-plane rotation)
  2. In-plane rotated orientation (+90 deg)
  3. Inverted/flipped orientation (180 deg pitch/roll)
Evaluates E_ads for each orientation, finding E_ads^min and confirming orientation convergence.
"""

import os
import sys
import subprocess
import shutil
import numpy as np
import pandas as pd
from pathlib import Path

BASE = Path(r"c:\Users\Andre\Proyectos doctorado\kras-pancreatic-gC3N4-ai")
XTB_EXE = BASE / "tools" / "xtb" / "xtb-6.7.1" / "bin" / "xtb.exe"
SCRATCH = BASE / "scratch" / "multistart_adsorption"
SCRATCH.mkdir(parents=True, exist_ok=True)
OUT_CSV = BASE / "results" / "quantum" / "multistart_adsorption_results.csv"

CARRIER_XYZ = BASE / "scratch" / "qm_calcs_carriers" / "pristine" / "xtbopt.xyz"

DRUGS = ["5-Fluorouracil", "Gemcitabine", "MRTX1133"]

def read_xyz(path: Path):
    lines = path.read_text().splitlines()
    natoms = int(lines[0].strip())
    comment = lines[1].strip()
    atoms = []
    coords = []
    for l in lines[2:]:
        if not l.strip():
            continue
        p = l.split()
        atoms.append(p[0])
        coords.append([float(p[1]), float(p[2]), float(p[3])])
    return atoms, np.array(coords), comment

def write_xyz(path: Path, atoms, coords, comment=""):
    lines = [str(len(atoms)), comment]
    for a, c in zip(atoms, coords):
        lines.append(f"{a:<4} {c[0]:14.6f} {c[1]:14.6f} {c[2]:14.6f}")
    path.write_text("\n".join(lines))

def rotate_coords(coords, angle_deg, axis='z'):
    rad = np.radians(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    if axis == 'z':
        R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    elif axis == 'x':
        R = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    elif axis == 'y':
        R = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    # Center, rotate, uncenter
    centroid = coords.mean(axis=0)
    shifted = coords - centroid
    rotated = shifted @ R.T
    return rotated + centroid

def run_xtb_sp_or_opt(xyz_path: Path, opt=True):
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
    print("=== Multi-Start Adsorption Optimization (GFN2-xTB) ===")
    c_atoms, c_coords, _ = read_xyz(CARRIER_XYZ)
    c_work = SCRATCH / "carrier"
    c_work.mkdir(exist_ok=True)
    c_xyz = c_work / "carrier.xyz"
    write_xyz(c_xyz, c_atoms, c_coords)
    E_carr = run_xtb_sp_or_opt(c_xyz, opt=False)
    print(f"Carrier E_sp = {E_carr:.6f} Eh")

    HARTREE_TO_KCAL = 627.509474
    records = []

    for drug in DRUGS:
        print(f"\n--- Processing {drug} ---")
        drug_src = BASE / "scratch" / "qm_calcs_molecules" / drug / "xtbopt.xyz"
        d_atoms, d_coords, _ = read_xyz(drug_src)
        
        d_work = SCRATCH / drug / "isolated"
        d_work.mkdir(parents=True, exist_ok=True)
        d_xyz = d_work / f"{drug}.xyz"
        write_xyz(d_xyz, d_atoms, d_coords)
        E_drug = run_xtb_sp_or_opt(d_xyz, opt=False)
        print(f"  {drug} isolated E_sp = {E_drug:.6f} Eh")

        orientations = [
            ("Orientation_1_Parallel_0deg", d_coords),
            ("Orientation_2_Rotated_90deg", rotate_coords(d_coords, 90, axis='z')),
            ("Orientation_3_Inverted_180deg", rotate_coords(d_coords, 180, axis='x')),
        ]

        for ori_name, coords_mod in orientations:
            # Place drug at z = 3.35 A above carrier
            c_zmax = c_coords[:, 2].max()
            d_zmin = coords_mod[:, 2].min()
            dz = (c_zmax + 3.35) - d_zmin
            placed_coords = coords_mod.copy()
            placed_coords[:, 2] += dz

            comp_atoms = c_atoms + d_atoms
            comp_coords = np.vstack([c_coords, placed_coords])

            comp_dir = SCRATCH / drug / ori_name
            comp_dir.mkdir(parents=True, exist_ok=True)
            comp_xyz = comp_dir / "complex.xyz"
            write_xyz(comp_xyz, comp_atoms, comp_coords)

            print(f"  Optimizing {drug} {ori_name}...")
            E_comp = run_xtb_sp_or_opt(comp_xyz, opt=True)
            if E_comp is not None:
                E_ads = (E_comp - E_carr - E_drug) * HARTREE_TO_KCAL
                print(f"    => {ori_name}: E_ads = {E_ads:.2f} kcal/mol")
                records.append({
                    "Drug": drug,
                    "Orientation": ori_name,
                    "E_complex_Eh": E_comp,
                    "E_carrier_Eh": E_carr,
                    "E_drug_Eh": E_drug,
                    "E_ads_kcal_mol": round(E_ads, 2)
                })
            else:
                print(f"    => Failed for {ori_name}")

    df = pd.DataFrame(records)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)
    print(f"\nSaved Multi-Start Adsorption Results: {OUT_CSV}")
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
