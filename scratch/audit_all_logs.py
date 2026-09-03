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


import re

base = _project_root()
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
