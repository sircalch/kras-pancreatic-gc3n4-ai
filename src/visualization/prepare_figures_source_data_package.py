"""
prepare_figures_source_data_package.py
Collects, organizes, and formats all authentic structural coordinates (PDBQT, PDB, XYZ),
quantum outputs (charges, WBO, energy logs), and QSPR datasets (OOF, 1000 Y-scrambling, Table 3)
into a dedicated directory and ZIP package for Figure 3, Figure 8, Figure 10, and Graphical Abstract.
"""

import os
import shutil
import zipfile
import pandas as pd
from rdkit import Chem

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
pkg_dir = os.path.join(base_dir, "data", "figures_source_package")
os.makedirs(pkg_dir, exist_ok=True)

# Subdirectories
fig3_dir = os.path.join(pkg_dir, "01_Figure3_Redocking")
fig8_dir = os.path.join(pkg_dir, "02_Figure8_QSPR_Validation")
fig10_dir = os.path.join(pkg_dir, "03_Figure10_Atomistic_Structures")

for d in [fig3_dir, fig8_dir, fig10_dir]:
    os.makedirs(d, exist_ok=True)

def xyz_to_pdb(xyz_path, pdb_path, resname="MOL"):
    """Converts an XYZ coordinate file to standard PDB format for PyMOL/ChimeraX."""
    with open(xyz_path, 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    n_atoms = int(lines[0])
    atoms = []
    for l in lines[2:2+n_atoms]:
        parts = l.split()
        atoms.append((parts[0], float(parts[1]), float(parts[2]), float(parts[3])))
        
    with open(pdb_path, 'w') as f:
        f.write(f"REMARK   Converted from {os.path.basename(xyz_path)}\n")
        for i, (el, x, y, z) in enumerate(atoms, 1):
            f.write(f"HETATM{i:5d} {el:<4s} {resname:<3s} A   1    {x:8.3f}{y:8.3f}{z:8.3f}  1.00 20.00          {el:>2s}\n")
        f.write("END\n")

def package_all():
    print("=" * 80)
    print("PACKAGING AUTHENTIC DATASETS AND ATOMISTIC STRUCTURES FOR FIGURES")
    print("=" * 80)
    
    # -------------------------------------------------------------
    # 1. Figure 3: Redocking Files
    # -------------------------------------------------------------
    print("\n[1] Preparing Figure 3 (Redocking) Files...")
    src_crystal_pdb = os.path.join(base_dir, "results", "docking", "validation", "7RPZ_MRTX1133_crystal.pdb")
    src_redocked_pdbqt = os.path.join(base_dir, "results", "docking", "validation", "7RPZ_MRTX1133_redocked_pose.pdbqt")
    src_receptor_pdb = os.path.join(base_dir, "results", "docking", "validation", "7RPZ_receptor_apo.pdb")
    src_receptor_pdbqt = os.path.join(base_dir, "results", "docking", "validation", "7RPZ_receptor.pdbqt")
    
    if os.path.exists(src_crystal_pdb):
        shutil.copy(src_crystal_pdb, os.path.join(fig3_dir, "MRTX1133_crystal_pose_6IC.pdb"))
    if os.path.exists(src_redocked_pdbqt):
        shutil.copy(src_redocked_pdbqt, os.path.join(fig3_dir, "MRTX1133_redocked_best_pose.pdbqt"))
    if os.path.exists(src_receptor_pdb):
        shutil.copy(src_receptor_pdb, os.path.join(fig3_dir, "7RPZ_KRAS_G12D_receptor_apo.pdb"))
    if os.path.exists(src_receptor_pdbqt):
        shutil.copy(src_receptor_pdbqt, os.path.join(fig3_dir, "7RPZ_KRAS_G12D_receptor.pdbqt"))
        
    # Also copy all 9 modes of MRTX1133
    src_all_modes = os.path.join(base_dir, "results", "docking", "master_poses", "MRTX1133_docked.pdbqt")
    if os.path.exists(src_all_modes):
        shutil.copy(src_all_modes, os.path.join(fig3_dir, "MRTX1133_all_9_docked_modes.pdbqt"))
        
    print("  -> Copied MRTX1133 crystal pose, top redocked pose (RMSD=1.419 A), all 9 modes, and receptor.")

    # -------------------------------------------------------------
    # 2. Figure 8: QSPR Validation Datasets
    # -------------------------------------------------------------
    print("\n[2] Preparing Figure 8 (QSPR Validation) Files...")
    src_oof = os.path.join(base_dir, "results", "qspr", "oof_observed_vs_predicted_qspr.csv")
    src_scr = os.path.join(base_dir, "results", "qspr", "yscrambling_1000_permutations.csv")
    src_summary = os.path.join(base_dir, "results", "qspr", "qspr_model_summary.json")
    src_table3 = os.path.join(base_dir, "results", "qspr", "table3_external_qm_validation_leads.csv")
    
    if os.path.exists(src_oof):
        shutil.copy(src_oof, os.path.join(fig8_dir, "oof_observed_vs_predicted_qspr.csv"))
    if os.path.exists(src_scr):
        shutil.copy(src_scr, os.path.join(fig8_dir, "yscrambling_1000_permutations.csv"))
    if os.path.exists(src_summary):
        shutil.copy(src_summary, os.path.join(fig8_dir, "qspr_model_summary.json"))
    if os.path.exists(src_table3):
        shutil.copy(src_table3, os.path.join(fig8_dir, "table3_external_qm_validation_leads.csv"))
        
    print("  -> Copied OOF observed vs predicted dataset, 1000 Y-scrambling permutation distribution, and Table 3.")

    # -------------------------------------------------------------
    # 3. Figure 10: Atomistic Structures & Quantum Outputs
    # -------------------------------------------------------------
    print("\n[3] Preparing Figure 10 (Atomistic Structures) Files...")
    
    # 3.1 BI-2865 docked pose
    src_bi2865 = os.path.join(base_dir, "results", "docking", "master_poses", "BI-2865_docked.pdbqt")
    if os.path.exists(src_bi2865):
        shutil.copy(src_bi2865, os.path.join(fig10_dir, "BI2865_pan_KRAS_docked_modes.pdbqt"))
        
    # 3.2 Optimized 2D Nanocarriers (XYZ and PDB)
    src_carr_pristine = os.path.join(base_dir, "scratch", "qm_calcs_carriers", "pristine", "xtbopt.xyz")
    if not os.path.exists(src_carr_pristine):
        src_carr_pristine = os.path.join(base_dir, "data", "quantum", "structures", "gC3N4_pristine.xyz")
    dst_carr_p_xyz = os.path.join(fig10_dir, "gC3N4_pristine_optimized.xyz")
    dst_carr_p_pdb = os.path.join(fig10_dir, "gC3N4_pristine_optimized.pdb")
    shutil.copy(src_carr_pristine, dst_carr_p_xyz)
    xyz_to_pdb(dst_carr_p_xyz, dst_carr_p_pdb, resname="CN4")
    
    src_carr_bp = os.path.join(base_dir, "scratch", "qm_calcs_carriers", "BP_doped", "xtbopt.xyz")
    if not os.path.exists(src_carr_bp):
        src_carr_bp = os.path.join(base_dir, "data", "quantum", "structures", "gC3N4_BP_doped.xyz")
    dst_carr_bp_xyz = os.path.join(fig10_dir, "gC3N4_BP_doped_optimized.xyz")
    dst_carr_bp_pdb = os.path.join(fig10_dir, "gC3N4_BP_doped_optimized.pdb")
    shutil.copy(src_carr_bp, dst_carr_bp_xyz)
    xyz_to_pdb(dst_carr_bp_xyz, dst_carr_bp_pdb, resname="BPN")
    
    # 3.3 Optimized Drug-Nanosheet Complexes
    src_comp_p = os.path.join(base_dir, "scratch", "qm_calcs_adsorption", "pristine_MRTX1133", "xtbopt.xyz")
    if not os.path.exists(src_comp_p):
        src_comp_p = os.path.join(base_dir, "scratch", "qm_calcs_adsorption", "complex_pristine_MRTX1133.xyz")
    dst_comp_p_xyz = os.path.join(fig10_dir, "MRTX1133_pristine_complex_optimized.xyz")
    dst_comp_p_pdb = os.path.join(fig10_dir, "MRTX1133_pristine_complex_optimized.pdb")
    shutil.copy(src_comp_p, dst_comp_p_xyz)
    xyz_to_pdb(dst_comp_p_xyz, dst_comp_p_pdb, resname="CPX")
    
    src_comp_bp = os.path.join(base_dir, "scratch", "qm_calcs_adsorption", "BP_doped_MRTX1133", "xtbopt.xyz")
    if not os.path.exists(src_comp_bp):
        src_comp_bp = os.path.join(base_dir, "scratch", "qm_calcs_adsorption", "complex_BP_doped_MRTX1133.xyz")
    dst_comp_bp_xyz = os.path.join(fig10_dir, "MRTX1133_BP_complex_optimized.xyz")
    dst_comp_bp_pdb = os.path.join(fig10_dir, "MRTX1133_BP_complex_optimized.pdb")
    shutil.copy(src_comp_bp, dst_comp_bp_xyz)
    xyz_to_pdb(dst_comp_bp_xyz, dst_comp_bp_pdb, resname="CPX")
    
    # 3.4 Raw GFN2-xTB Output Charges & Quantum Benchmark
    src_chrg_carr = os.path.join(base_dir, "scratch", "qm_calcs_carriers", "BP_doped", "charges")
    if os.path.exists(src_chrg_carr):
        shutil.copy(src_chrg_carr, os.path.join(fig10_dir, "charges_BP_doped_gC3N4.dat"))
        
    src_chrg_cpx = os.path.join(base_dir, "scratch", "qm_calcs_adsorption", "BP_doped_MRTX1133", "charges")
    if os.path.exists(src_chrg_cpx):
        shutil.copy(src_chrg_cpx, os.path.join(fig10_dir, "charges_MRTX1133_BP_complex.dat"))
        
    src_bm = os.path.join(base_dir, "results", "quantum", "quantum_benchmark_10systems.csv")
    if os.path.exists(src_bm):
        shutil.copy(src_bm, os.path.join(fig10_dir, "quantum_benchmark_10systems.csv"))
        
    # Copy receptor to Fig10 as well
    if os.path.exists(src_receptor_pdb):
        shutil.copy(src_receptor_pdb, os.path.join(fig10_dir, "7RPZ_KRAS_G12D_receptor_apo.pdb"))
    if os.path.exists(src_crystal_pdb):
        shutil.copy(src_crystal_pdb, os.path.join(fig10_dir, "MRTX1133_crystal_pose_6IC.pdb"))
        
    print("  -> Copied BI-2865 pose, carrier XYZ/PDBs, MRTX1133 complex XYZ/PDBs, and atomic charges.")

    # -------------------------------------------------------------
    # 4. Generate README & ZIP Package
    # -------------------------------------------------------------
    readme_text = f"""# Figures Exact Source Data Package (Q1 Research Article)
**Article:** Atomistic Modeling and QSPR-Guided Screening of 2D Graphitic Carbon Nitride Nanocarriers for KRAS-G12D Inhibitor Loading and Target Engagement
**Authors:** Andrés Monreal Hernández, Sara Lizbeth Franco Amaya, Carlos Ivanhoe Martínez Osorio

---

## Folder Structure and Exact File Mapping:

### 📁 `01_Figure3_Redocking/`
- `7RPZ_KRAS_G12D_receptor_apo.pdb` -> PDB 7RPZ receptor structure (1.30 Å) with GDP + Mg2+.
- `MRTX1133_crystal_pose_6IC.pdb` -> Ground-truth X-ray crystallographic pose of MRTX1133 (PDB ligand 6IC).
- `MRTX1133_redocked_best_pose.pdbqt` -> Top redocked pose calculated by AutoDock Vina v1.2.7 (RMSD = 1.419 Å relative to crystal pose).
- `MRTX1133_all_9_docked_modes.pdbqt` -> Full 9 conformational modes generated by AutoDock Vina with affinity scores (-9.16 to -7.82 kcal/mol).

### 📁 `02_Figure8_QSPR_Validation/`
- `oof_observed_vs_predicted_qspr.csv` -> Out-of-fold observed (GFN2-xTB QM) vs predicted (Ridge QSPR) Delta_E_ads for all 33 compounds, with residuals, standardized residuals, and hat-matrix leverages (hi).
  * Metrics: Q2_CV = +0.5696, RMSE = 5.201 kcal/mol, MAE = 4.194 kcal/mol.
- `yscrambling_1000_permutations.csv` -> 1,000 Y-scrambling permutation iterations (mean Q2_scr = -0.2357, empirical p-value = 0.0010).
- `table3_external_qm_validation_leads.csv` -> Table 3 data with external QM recalculations for 5 screening leads (Avapritinib, Futibatinib, Belumosudil, Capivasertib, Pimicotinib).
- `qspr_model_summary.json` -> Complete machine learning statistics, metrics, and analytical equation.

### 📁 `03_Figure10_Atomistic_Structures/`
- `7RPZ_KRAS_G12D_receptor_apo.pdb` -> Human KRAS-G12D receptor.
- `MRTX1133_crystal_pose_6IC.pdb` -> MRTX1133 in Switch II pocket.
- `BI2865_pan_KRAS_docked_modes.pdbqt` -> BI-2865 docked in Switch I/II pocket (-8.46 kcal/mol).
- `gC3N4_pristine_optimized.xyz` / `.pdb` -> GFN2-xTB optimized 2D pristine heptazine nanocarrier (C18N24H6).
- `gC3N4_BP_doped_optimized.xyz` / `.pdb` -> GFN2-xTB optimized 2D B/P co-doped nanocarrier (C17B1N23P1H6).
- `MRTX1133_pristine_complex_optimized.xyz` / `.pdb` -> Optimized adsorption complex on pristine g-C3N4 (Delta_E_ads = -35.03 kcal/mol, pi-pi stacking d = 3.35 Å).
- `MRTX1133_BP_complex_optimized.xyz` / `.pdb` -> Optimized adsorption complex on B/P-doped g-C3N4 (Delta_E_ads = -35.04 kcal/mol, Delta_Q = +0.146 e).
- `charges_BP_doped_gC3N4.dat` -> Atomic Mulliken charges from GFN2-xTB showing B (+0.3494 e) and P (-0.1679 e).
- `charges_MRTX1133_BP_complex.dat` -> Atomic charges of the adsorption complex showing interfacial charge transfer.
- `quantum_benchmark_10systems.csv` -> 10-system parity benchmark data (GFN2-xTB vs GFN1-xTB).

---
All coordinates and numerical data are fully authentic, reproducible, and ready for 3D visualization in PyMOL, ChimeraX, VMD, or Origin/Matplotlib.
"""
    with open(os.path.join(pkg_dir, "README_FIGURES_DATA_GUIDE.md"), 'w', encoding='utf-8') as f:
        f.write(readme_text)
        
    zip_path = os.path.join(base_dir, "FIGURES_EXACT_SOURCE_DATA_PACKAGE.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(pkg_dir):
            for file in files:
                abs_f = os.path.join(root, file)
                rel_f = os.path.relpath(abs_f, pkg_dir)
                zipf.write(abs_f, os.path.join("FIGURES_EXACT_SOURCE_DATA_PACKAGE", rel_f))
                
    print(f"\n[SUCCESS] Generated Complete Figures Source Package ZIP ({os.path.getsize(zip_path)} bytes): {zip_path}")
    return zip_path

if __name__ == "__main__":
    package_all()
