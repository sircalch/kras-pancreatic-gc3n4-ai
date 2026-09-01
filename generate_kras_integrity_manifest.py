"""
generate_kras_integrity_manifest.py
===================================
Generates MANIFEST_SHA256.txt containing exact cryptographic SHA-256 hashes
for all computational datasets, quantum logs, docking outputs, QSPR models,
figures, supporting information, and manuscripts in the KRAS-G12D project.
"""

import os
import hashlib
from pathlib import Path

base_dir = Path(r"c:\Users\Andre\Proyectos doctorado\kras-pancreatic-gC3N4-ai")

def hash_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

files_to_hash = [
    "data/processed/MASTER_COMPOUNDS_CURATED.csv",
    "data/raw/7RPZ.pdb",
    "data/raw/7RPZ_receptor.pdbqt",
    "results/quantum/quantum_benchmark_10systems.csv",
    "results/qspr/table3_external_qm_validation_leads.csv",
    "figures/fig1_kras_3d_superposition.png",
    "figures/fig2_kras_gC3N4_workflow.png",
    "figures/fig3_redocking_validation_final.jpg",
    "figures/fig4_kras_group_discrimination.png",
    "figures/fig6_multilevel_quantum_benchmark.jpg",
    "figures/fig8_qspr_validation_final.jpg",
    "figures/fig9_kras_virtual_screening_distribution.png",
    "figures/fig10_atomistic_multiscale_final.jpg",
    "figures/fig_graphical_abstract_final.jpg",
    "manuscript/KRAS_gC3N4_Full_Q1_Research_Paper_Monreal_Hernandez_et_al.docx",
    "manuscript/KRAS_gC3N4_Supporting_Information_Table_S1.docx",
    "manuscript/submission_ready/01_Cover_Letter_Beilstein_KRAS.docx",
    "manuscript/submission_ready/02_Manuscript_KRAS_gC3N4_Full_Q1_Research_Paper.docx"
]

manifest_lines = ["# KRAS-G12D / g-C3N4 Research Package Integrity Manifest (SHA-256)",
                  "# Generated for Reviewer Audit & Q1 Journal Reproducibility Verification\n"]

for rel_p in files_to_hash:
    full_p = base_dir / rel_p
    if full_p.exists():
        sha = hash_file(full_p)
        size_b = full_p.stat().st_size
        manifest_lines.append(f"{sha}  {size_b:>10} bytes  {rel_p}")
    else:
        print(f"Warning: {rel_p} not found.")

manifest_p = base_dir / "MANIFEST_SHA256.txt"
manifest_p.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
print(f"[SUCCESS] Generated {manifest_p} ({len(manifest_lines)} entries).")
