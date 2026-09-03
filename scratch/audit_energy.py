import subprocess, re
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



base = _project_root()
xtb = base / "tools" / "xtb" / "xtb-6.7.1" / "bin" / "xtb.exe"
carr_xyz = base / "data" / "quantum" / "structures" / "gC3N4_pristine.xyz"

def run(cmd):
    res = subprocess.run(cmd, capture_output=True)
    out = res.stdout.decode("utf-8", errors="ignore")
    m = re.search(r"TOTAL ENERGY\s+([\-\d\.]+)\s+Eh", out)
    return float(m.group(1)) if m else None

e_default = run([str(xtb), str(carr_xyz), "--gfn", "2", "--sp", "--chrg", "0"])
e_uhf1 = run([str(xtb), str(carr_xyz), "--gfn", "2", "--sp", "--chrg", "0", "--uhf", "1"])

print(f"Carrier E_default: {e_default:.8f} Eh (matches nanocarrier_qm_results.csv: {e_default == -107.7653505323 or abs(e_default - (-107.76535053)) < 1e-4})")
print(f"Carrier E_uhf1:    {e_uhf1:.8f} Eh")
print(f"Difference:        {(e_default - e_uhf1)*627.5095:.2f} kcal/mol")
