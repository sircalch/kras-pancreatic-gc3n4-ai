import subprocess, re
from pathlib import Path

base = Path(r"c:\Users\Andre\Proyectos doctorado\kras-pancreatic-gC3N4-ai")
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
