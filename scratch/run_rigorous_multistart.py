import subprocess, re, numpy as np, pandas as pd
from pathlib import Path

base = Path(r"c:\Users\Andre\Proyectos doctorado\kras-pancreatic-gC3N4-ai")
xtb = base / "tools" / "xtb" / "xtb-6.7.1" / "bin" / "xtb.exe"
carr_xyz = base / "data" / "quantum" / "structures" / "gC3N4_pristine.xyz"
scratch = base / "scratch" / "rigorous_multistart"
scratch.mkdir(parents=True, exist_ok=True)

def read_xyz(filepath):
    lines = [l.strip() for l in filepath.read_text().splitlines() if l.strip()]
    n = int(lines[0])
    atoms = []
    for l in lines[2:2+n]:
        p = l.split()
        atoms.append((p[0], float(p[1]), float(p[2]), float(p[3])))
    return atoms

def save_xyz(atoms, filepath):
    with open(filepath, "w") as f:
        f.write(f"{len(atoms)}\nGenerated complex\n")
        for el, x, y, z in atoms:
            f.write(f"{el:<3s} {x:12.6f} {y:12.6f} {z:12.6f}\n")

def rotate_coords(coords, angle_deg, axis='z'):
    rad = np.radians(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    if axis == 'z':
        R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    elif axis == 'x':
        R = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    centroid = coords.mean(axis=0)
    shifted = coords - centroid
    return (shifted @ R.T) + centroid

def run_sp(xyz_file):
    res = subprocess.run([str(xtb), xyz_file.name, "--gfn", "2", "--sp", "--chrg", "0"], cwd=xyz_file.parent, capture_output=True)
    out = res.stdout.decode("utf-8", errors="ignore")
    m = re.search(r"TOTAL ENERGY\s+([\-\d\.]+)\s+Eh", out)
    return float(m.group(1)) if m else None

# 1. Carrier SP
c_atoms = read_xyz(carr_xyz)
carr_work = scratch / "carrier.xyz"
save_xyz(c_atoms, carr_work)
E_carr = run_sp(carr_work)
print(f"Carrier E = {E_carr:.8f} Eh")

drugs = ["5-Fluorouracil", "Gemcitabine", "MRTX1133"]
results = []

for drug in drugs:
    d_file = base / "scratch" / "qm_calcs_molecules" / drug / "xtbopt.xyz"
    if not d_file.exists():
        d_file = base / "data" / "quantum" / "structures" / f"{drug}.xyz"
    d_atoms = read_xyz(d_file)
    d_work = scratch / f"{drug}_isolated.xyz"
    save_xyz(d_atoms, d_work)
    E_drug = run_sp(d_work)
    
    d_coords = np.array([[a[1], a[2], a[3]] for a in d_atoms])
    center = np.mean(d_coords, axis=0)
    
    orientations = [
        ("0 deg Parallel", d_coords),
        ("+90 deg In-Plane Rotated", rotate_coords(d_coords, 90, axis='z')),
        ("180 deg Inverted Flip", rotate_coords(d_coords, 180, axis='x')),
    ]
    
    for ori_name, coords_mod in orientations:
        # Translate to z = 3.35 A above carrier
        t_drug = []
        c_mod = coords_mod - coords_mod.mean(axis=0)
        zmin = np.min(c_mod[:, 2])
        for idx, (el, _, _, _) in enumerate(d_atoms):
            nx = c_mod[idx, 0]
            ny = c_mod[idx, 1]
            nz = (c_mod[idx, 2] - zmin) + 3.35
            t_drug.append((el, nx, ny, nz))
            
        comp_atoms = c_atoms + t_drug
        comp_xyz = scratch / f"{drug}_{ori_name.replace(' ', '_')}.xyz"
        save_xyz(comp_atoms, comp_xyz)
        E_comp = run_sp(comp_xyz)
        
        E_ads = (E_comp - E_carr - E_drug) * 627.5095
        print(f"{drug} ({ori_name}): E_comp = {E_comp:.6f}, E_ads = {E_ads:6.2f} kcal/mol")
        results.append({
            "drug": drug,
            "orientation": ori_name,
            "E_complex_Eh": E_comp,
            "E_carrier_Eh": E_carr,
            "E_drug_Eh": E_drug,
            "E_ads_kcal_mol": round(E_ads, 2)
        })

df = pd.DataFrame(results)
out_csv = base / "results" / "quantum" / "multistart_adsorption_results.csv"
df.to_csv(out_csv, index=False)
print("\nUpdated multistart adsorption results saved to:", out_csv)
print(df[["drug", "orientation", "E_ads_kcal_mol"]].to_string(index=False))
