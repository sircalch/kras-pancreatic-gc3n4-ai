import pandas as pd
from pathlib import Path

base = Path(r"c:\Users\Andre\Proyectos doctorado\kras-pancreatic-gC3N4-ai")
ads_csv = base / "results" / "quantum" / "adsorption_qm_results.csv"
df = pd.read_csv(ads_csv)
pristine_df = df[df["carrier_name"] == "pristine"].copy()

print("Original E_carrier in dataset:", pristine_df["E_carrier_Eh"].iloc[0])
print("Relaxed carrier energy:       -108.88419766 Eh")

for drug in ["5-Fluorouracil", "Gemcitabine", "MRTX1133", "Methotrexate", "Futibatinib"]:
    row = pristine_df[pristine_df["drug_name"] == drug].iloc[0]
    e_comp = row["E_complex_Eh"]
    e_carr_orig = row["E_carrier_Eh"]
    e_drug = row["E_drug_Eh"]
    eads_orig = row["Delta_E_ads_kcal_mol"]
    
    # Recalculate using original unrelaxed carrier
    eads_unrelaxed = (e_comp - e_carr_orig - e_drug) * 627.5095
    # Recalculate using relaxed carrier
    eads_relaxed = (e_comp - (-108.88419766) - e_drug) * 627.5095
    
    print(f"\n{drug}:")
    print(f"  E_complex: {e_comp:.6f}, E_drug: {e_drug:.6f}")
    print(f"  E_ads (original formula in dataset): {eads_orig:6.2f} kcal/mol")
    print(f"  E_ads (with relaxed carrier):       {eads_relaxed:6.2f} kcal/mol")
