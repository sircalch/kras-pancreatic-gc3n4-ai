from pathlib import Path
import re

base = Path(r"c:\Users\Andre\Proyectos doctorado\kras-pancreatic-gC3N4-ai")
calc_dir = base / "scratch" / "qm_calcs_adsorption"

for drug in ["5-Fluorouracil", "Gemcitabine", "MRTX1133", "Methotrexate", "Futibatinib"]:
    log_file = calc_dir / f"pristine_{drug}" / "xtbopt.log"
    if log_file.exists():
        lines = log_file.read_text().splitlines()
        energies = [float(l.split()[1]) for l in lines if "energy:" in l]
        print(f"{drug}:")
        print(f"  Step 1 (unrelaxed): {energies[0]:.6f} Eh")
        print(f"  Final (converged):  {energies[-1]:.6f} Eh ({len(energies)} steps)")
        print(f"  Energy drop in opt: {(energies[0] - energies[-1])*627.5095:.2f} kcal/mol")
