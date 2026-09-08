"""
run_entire_kras_study.py
Master end-to-end pipeline for Article 3 (KRAS-G12D / 2D g-C3N4, PDAC).
Reproduces every real number and figure in the manuscript from raw inputs.
"""
import os
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))


def run_step(n, total, title, rel_path, args=""):
    script = os.path.join(BASE, rel_path)
    print(f"\n{'='*70}\n  [Step {n}/{total}] {title}\n{'='*70}")
    t0 = time.time()
    ret = os.system(f'python "{script}" {args}')
    if ret != 0:
        print(f"[ERROR] Step {n}: {title} (exit {ret})")
        return False
    print(f"[OK] Step {n} in {time.time()-t0:.1f}s")
    return True


def main():
    print("=" * 70)
    print("  KRAS-G12D / g-C3N4 : MASTER REPRODUCIBILITY PIPELINE")
    print("=" * 70)
    steps = [
        ("Drug-library curation", "src/descriptors/curate_kras_dataset.py"),
        ("RDKit + GFN2-xTB descriptors", "src/descriptors/compute_kras_descriptors.py"),
        ("Real AutoDock Vina docking (KRAS-G12D, PDB 7RPZ)", "src/docking/run_kras_real_docking.py"),
        ("Residue-level contact analysis", "src/docking/analyze_kras_interactions.py"),
        ("GFN2-xTB adsorption on pristine + B/P-doped g-C3N4", "src/quantum/run_adsorption_qm.py"),
        ("OECD applicability domain (Williams)", "src/ml_models/compute_kras_oecd_applicability_domain.py"),
        ("Master figure suite", "src/visualization/generate_kras_master_figures.py"),
        ("Word manuscript", "src/visualization/generate_kras_word_manuscript.py"),
        ("Supporting information", "src/visualization/generate_supporting_information.py"),
    ]
    for i, (title, path) in enumerate(steps, 1):
        if not run_step(i, len(steps), title, path):
            sys.exit(1)
    print("\n" + "=" * 70)
    print(">>> PIPELINE COMPLETE <<<")
    print("  manuscript/Beilstein_Manuscript_KRAS_gC3N4_Monreal_Hernandez_et_al.docx")
    print("=" * 70)


if __name__ == "__main__":
    main()
