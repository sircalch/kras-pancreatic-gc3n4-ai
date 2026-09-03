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

base = _project_root()
calc_dir = base / "scratch" / "qm_calcs_adsorption"
res_dir = base / "results" / "quantum"

# Load current master results
df_master = pd.read_csv(res_dir / "adsorption_qm_results.csv")
pristine_master = df_master[df_master["carrier_name"] == "pristine"].copy()

print(f"Total pristine complexes in master: {len(pristine_master)}")
print("\nComparing Step 1 (Rigid Interaction) vs Step Final (Relaxed Adsorption):")

rows = []
for idx, r in pristine_master.iterrows():
    drug = r["drug_name"]
    log_file = calc_dir / f"pristine_{drug}" / "xtbopt.log"
    if log_file.exists():
        lines = log_file.read_text().splitlines()
        energies = [float(l.split()[1]) for l in lines if "energy:" in l]
        e_step1 = energies[0]
        e_final = energies[-1]
        n_steps = len(energies)
        
        # Step 1 delta with unrelaxed carrier (-107.765351) & drug
        e_ads_rigid = (e_step1 - (-107.7653505323) - r["E_drug_Eh"]) * 627.5095
        
        # Final delta with relaxed carrier (-108.88419766) & drug
        e_ads_relaxed = (e_final - (-108.88419766) - r["E_drug_Eh"]) * 627.5095
        
        rows.append({
            "drug": drug,
            "n_steps": n_steps,
            "E_step1_Eh": e_step1,
            "E_final_Eh": e_final,
            "E_ads_rigid_kcal": round(e_ads_rigid, 2),
            "E_ads_master_in_csv": r["Delta_E_ads_kcal_mol"],
            "E_ads_relaxed_kcal": round(e_ads_relaxed, 2),
        })

comp_df = pd.DataFrame(rows)
print(comp_df[["drug", "n_steps", "E_ads_master_in_csv", "E_ads_rigid_kcal", "E_ads_relaxed_kcal"]].head(15).to_string())
