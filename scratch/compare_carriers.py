from pathlib import Path
import subprocess, re

base = Path(r"c:\Users\Andre\Proyectos doctorado\kras-pancreatic-gC3N4-ai")
xtb = base / "tools" / "xtb" / "xtb-6.7.1" / "bin" / "xtb.exe"

p1 = base / "data" / "quantum" / "structures" / "gC3N4_pristine.xyz"
p2 = base / "scratch" / "qm_calcs_carriers" / "pristine" / "xtbopt.xyz"

def get_e(p):
    res = subprocess.run([str(xtb), str(p), "--gfn", "2", "--sp", "--chrg", "0"], capture_output=True)
    out = res.stdout.decode("utf-8", errors="ignore")
    m = re.search(r"TOTAL ENERGY\s+([\-\d\.]+)\s+Eh", out)
    return float(m.group(1)) if m else None

print("p1 (data/structures/gC3N4_pristine.xyz):", get_e(p1))
print("p2 (scratch/carriers/pristine/xtbopt.xyz):", get_e(p2))

# Check coordinates difference
l1 = p1.read_text().splitlines()
l2 = p2.read_text().splitlines()
print(f"p1 lines: {len(l1)}, p2 lines: {len(l2)}")
for i in range(min(5, len(l1))):
    print("p1:", l1[i])
    print("p2:", l2[i])
