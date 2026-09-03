"""
run_dft_benchmark.py
====================
DFT benchmark: B3LYP-D3BJ single-points on GFN2-xTB optimized geometries.
  - Small systems (<90 atoms): def2-TZVP
  - Large systems (>=90 atoms): def2-SVP (ORCA default recommendation for >100 atoms)
Computes E_ads(DFT) = E_complex - E_carrier - E_drug for 5-8 strategic systems.
Saves results to results/quantum/dft_benchmark_b3lyp_d3bj.csv
"""

import os, sys, subprocess, re, time
from pathlib import Path


def _project_root(marker="MANIFEST_SHA256.txt"):
    from pathlib import Path as _P
    here = _P(__file__).resolve()
    for anc in [here.parent, *here.parents]:
        if (anc / marker).exists() or ((anc / "data").is_dir() and (anc / "README.md").exists()):
            return anc
    return here.parent


def _find_xtb():
    import shutil
    from pathlib import Path as _P
    w = shutil.which("xtb") or shutil.which("xtb.exe")
    if w:
        return _P(w)
    for anc in [_P(__file__).resolve().parent, *_P(__file__).resolve().parents]:
        hits = list(anc.glob("**/xtb-*/bin/xtb.exe")) or list(anc.glob("**/xtb-*/bin/xtb"))
        if hits:
            return hits[0]
    return _P("xtb")


import pandas as pd

BASE = _project_root()
ORCA_EXE = Path(r"C:\ORCA_6.1.1\orca.EXE")
SCRATCH_ADC = BASE / "scratch" / "qm_calcs_adsorption"
SCRATCH_MOL = BASE / "scratch" / "qm_calcs_molecules"
SCRATCH_CAR = BASE / "scratch" / "qm_calcs_carriers"
DFT_DIR = BASE / "scratch" / "dft_benchmark"
DFT_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV = BASE / "results" / "quantum" / "dft_benchmark_b3lyp_d3bj.csv"

HARTREE_TO_KCAL = 627.509474

# 5 strategic systems: (compound, natoms_complex, GFN2xTB_Eads_kcal)
TARGETS = [
    ("5-Fluorouracil",  "pristine_5-Fluorouracil",  60,  -4.98),
    ("Gemcitabine",     "pristine_Gemcitabine",      77,  -14.21),
    ("Methotrexate",    "pristine_Methotrexate",     103, -39.17),
    ("Futibatinib",     "pristine_Futibatinib",      105, -24.67),
    ("MRTX1133",        "pristine_MRTX1133",         123, -35.03),
]

CARRIER_DIR = SCRATCH_CAR / "pristine"  # 48-atom C18N24H6

ATOMIC_NUMBERS = {
    'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10,
    'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18,
    'K': 19, 'Ca': 20, 'Br': 35, 'I': 53
}

def count_electrons(xyz_file: Path, charge=0) -> int:
    lines = xyz_file.read_text().splitlines()[2:]
    atoms = [l.split()[0].capitalize() for l in lines if l.strip()]
    total_z = sum(ATOMIC_NUMBERS.get(a, 6) for a in atoms)
    return total_z - charge

def basis_for_natoms(n):
    return "def2-SVP"  # def2-SVP is fast and well-behaved with RIJCOSX/def2/J for large complexes (>60-120 atoms)

def orca_input(xyz_file: Path, label: str, charge=0, ncores=4) -> str:
    lines = xyz_file.read_text().splitlines()
    natoms = int(lines[0].strip())
    basis = basis_for_natoms(natoms)
    coords = "\n".join(lines[2:])
    
    ne = count_electrons(xyz_file, charge=charge)
    mult = 1 if ne % 2 == 0 else 2
    
    return f"""! B3LYP D3BJ {basis} RIJCOSX def2/J TightSCF
%pal nprocs {ncores} end
%maxcore 3000
* xyz {charge} {mult}
{coords}
*
"""

def run_orca(inp_path: Path) -> float | None:
    """Run ORCA, return total energy in Hartree or None on failure."""
    out_path = inp_path.with_suffix(".out")
    print(f"  Running ORCA: {inp_path.name} ...", flush=True)
    t0 = time.time()
    try:
        result = subprocess.run(
            [str(ORCA_EXE), str(inp_path)],
            stdout=open(out_path, "w"),
            stderr=subprocess.STDOUT,
            timeout=7200,   # 2 hours max per calculation
            cwd=inp_path.parent,
        )
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT: {inp_path.name}")
        return None

    elapsed = time.time() - t0
    out_text = out_path.read_text(errors="ignore")
    
    # Extract final single-point energy
    match = re.findall(r"FINAL SINGLE POINT ENERGY\s+([-\d.]+)", out_text)
    if match:
        energy = float(match[-1])
        print(f"  Done in {elapsed:.0f}s => E = {energy:.8f} Eh")
        return energy
    else:
        print(f"  FAILED: {inp_path.name} (see {out_path.name})")
        return None

def extract_drug_xyz(complex_xyz: Path, carrier_xyz: Path) -> Path:
    """Extract drug atoms = complex - carrier atoms by index (first N_carrier atoms = carrier)."""
    comp_lines = complex_xyz.read_text().splitlines()
    carr_lines  = carrier_xyz.read_text().splitlines()
    n_comp = int(comp_lines[0].strip())
    n_carr = int(carr_lines[0].strip())
    n_drug = n_comp - n_carr
    drug_lines = comp_lines[2 + n_carr:]   # remaining = drug
    drug_xyz = complex_xyz.parent / "drug_extracted.xyz"
    drug_xyz.write_text(f"{n_drug}\nDrug extracted from complex\n" + "\n".join(drug_lines[:n_drug]))
    return drug_xyz

def main():
    if not ORCA_EXE.exists():
        print(f"ERROR: ORCA not found at {ORCA_EXE}")
        sys.exit(1)

    # ---- Step 1: Run carrier SP ----
    print("\n=== [1/3] Carrier (pristine C18N24H6) SP ===")
    carr_xyz = CARRIER_DIR / "xtbopt.xyz"
    if not carr_xyz.exists():
        print(f"ERROR: carrier xyz not found: {carr_xyz}")
        sys.exit(1)

    carr_dir = DFT_DIR / "carrier_pristine"
    carr_dir.mkdir(exist_ok=True)
    carr_inp = carr_dir / "carrier.inp"
    carr_inp.write_text(orca_input(carr_xyz, "carrier"))
    E_carrier = run_orca(carr_inp)
    if E_carrier is None:
        print("ERROR: carrier calculation failed. Cannot continue.")
        sys.exit(1)
    print(f"  E_carrier = {E_carrier:.8f} Eh  ({E_carrier * HARTREE_TO_KCAL:.2f} kcal/mol)")

    # ---- Step 2: Run each system ----
    results = []
    print("\n=== [2/3] Drug + Complex SP for each target system ===")

    for compound, folder, natoms, gfn2_eads in TARGETS:
        print(f"\n>>> {compound} (complex: {natoms} atoms) <<<")
        comp_xyz = SCRATCH_ADC / folder / "xtbopt.xyz"
        if not comp_xyz.exists():
            print(f"  SKIP: complex xyz not found: {comp_xyz}")
            continue

        drug_xyz_src = SCRATCH_MOL / compound / "xtbopt.xyz"
        if not drug_xyz_src.exists():
            print(f"  INFO: isolated drug xyz not found at {drug_xyz_src}, extracting from complex...")
            drug_xyz_src = extract_drug_xyz(comp_xyz, carr_xyz)

        sdir = DFT_DIR / compound.replace(" ", "_").replace("-", "_")
        sdir.mkdir(exist_ok=True)

        # --- Drug SP ---
        drug_inp = sdir / "drug.inp"
        drug_inp.write_text(orca_input(drug_xyz_src, f"{compound}_drug"))
        E_drug = run_orca(drug_inp)

        # --- Complex SP ---
        comp_inp = sdir / "complex.inp"
        comp_inp.write_text(orca_input(comp_xyz, f"{compound}_complex"))
        E_complex = run_orca(comp_inp)

        if E_drug is not None and E_complex is not None:
            E_ads_dft = (E_complex - E_carrier - E_drug) * HARTREE_TO_KCAL
            basis = basis_for_natoms(natoms)
            print(f"  => E_ads(B3LYP-D3BJ/{basis}) = {E_ads_dft:.3f} kcal/mol  |  GFN2-xTB = {gfn2_eads:.3f} kcal/mol  |  Diff = {E_ads_dft - gfn2_eads:+.3f}")
            results.append({
                "Compound": compound,
                "N_atoms_complex": natoms,
                "Basis": basis,
                "E_complex_Eh": E_complex,
                "E_carrier_Eh": E_carrier,
                "E_drug_Eh": E_drug,
                "E_ads_DFT_kcal_mol": round(E_ads_dft, 3),
                "E_ads_GFN2xTB_kcal_mol": gfn2_eads,
                "Delta_kcal_mol": round(E_ads_dft - gfn2_eads, 3),
            })
        else:
            results.append({
                "Compound": compound,
                "N_atoms_complex": natoms,
                "Basis": basis_for_natoms(natoms),
                "E_complex_Eh": None, "E_carrier_Eh": E_carrier, "E_drug_Eh": E_drug,
                "E_ads_DFT_kcal_mol": None,
                "E_ads_GFN2xTB_kcal_mol": gfn2_eads,
                "Delta_kcal_mol": None,
            })

    # ---- Step 3: Save ----
    print("\n=== [3/3] Saving results ===")
    df = pd.DataFrame(results)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)
    print(f"\nResults saved: {OUT_CSV}")
    print(df[["Compound","Basis","E_ads_DFT_kcal_mol","E_ads_GFN2xTB_kcal_mol","Delta_kcal_mol"]].to_string(index=False))
    
    completed = df["E_ads_DFT_kcal_mol"].notna().sum()
    print(f"\n{'='*60}")
    print(f"DFT Benchmark complete: {completed}/{len(results)} systems converged")
    if completed > 0:
        mae = df["Delta_kcal_mol"].dropna().abs().mean()
        print(f"MAE(DFT vs GFN2-xTB) = {mae:.2f} kcal/mol")

if __name__ == "__main__":
    main()
