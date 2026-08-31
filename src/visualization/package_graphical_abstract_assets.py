"""
package_graphical_abstract_assets.py
Prepares all 3D atomic structures, chemical coordinates, and visual layout specifications
specifically for designing a high-impact, publication-ready Graphical Abstract (Q1 standard).
"""

import os
import shutil
import zipfile

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ga_dir = os.path.join(base_dir, "data", "figures_source_package", "00_Graphical_Abstract")
leads_dir = os.path.join(ga_dir, "Top3_Leads_Structures")
os.makedirs(leads_dir, exist_ok=True)

def xyz_to_pdb(xyz_path, pdb_path, resname="MOL"):
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

def package_ga():
    print("=" * 80)
    print("PREPARING GRAPHICAL ABSTRACT ASSETS AND ATOMISTIC SCENES")
    print("=" * 80)
    
    # 1. Scene 1: KRAS-G12D + MRTX1133 in Switch II Cleft
    src_rec = os.path.join(base_dir, "results", "docking", "validation", "7RPZ_receptor_apo.pdb")
    src_lig = os.path.join(base_dir, "results", "docking", "validation", "7RPZ_MRTX1133_crystal.pdb")
    
    dst_rec = os.path.join(ga_dir, "Scene1_KRAS_G12D_receptor_7RPZ.pdb")
    dst_lig = os.path.join(ga_dir, "Scene1_MRTX1133_Switch_II_ligand.pdb")
    
    if os.path.exists(src_rec):
        shutil.copy(src_rec, dst_rec)
    if os.path.exists(src_lig):
        shutil.copy(src_lig, dst_lig)
        
    # Combine into a single ready-to-render complex PDB
    dst_cpx = os.path.join(ga_dir, "Scene1_KRAS_G12D_MRTX1133_complex.pdb")
    if os.path.exists(src_rec) and os.path.exists(src_lig):
        with open(dst_cpx, 'w') as out_f:
            with open(src_rec, 'r') as rf:
                for l in rf:
                    if not l.startswith("END"):
                        out_f.write(l)
            with open(src_lig, 'r') as lf:
                for l in lf:
                    out_f.write(l)
            out_f.write("END\n")
            
    print("  -> Prepared Scene 1 (KRAS-G12D + MRTX1133 complex).")

    # 2. Scene 2: 2D B/P-g-C3N4 Adsorption Scene
    src_ads_xyz = os.path.join(base_dir, "scratch", "qm_calcs_adsorption", "BP_doped_MRTX1133", "xtbopt.xyz")
    if not os.path.exists(src_ads_xyz):
        src_ads_xyz = os.path.join(base_dir, "scratch", "qm_calcs_adsorption", "complex_BP_doped_MRTX1133.xyz")
        
    dst_ads_xyz = os.path.join(ga_dir, "Scene2_gC3N4_BP_MRTX1133_adsorption.xyz")
    dst_ads_pdb = os.path.join(ga_dir, "Scene2_gC3N4_BP_MRTX1133_adsorption.pdb")
    
    if os.path.exists(src_ads_xyz):
        shutil.copy(src_ads_xyz, dst_ads_xyz)
        xyz_to_pdb(dst_ads_xyz, dst_ads_pdb, resname="ADS")
        
    print("  -> Prepared Scene 2 (B/P-g-C3N4 + MRTX1133 adsorption complex).")

    # 3. Scene 3: Top 3 Screening Leads (PDB and PDBQT)
    leads = ["Avapritinib", "Futibatinib", "Belumosudil"]
    for lead in leads:
        src_p = os.path.join(base_dir, "results", "virtual_screening", "confirmatory_poses", f"{lead}_docked.pdbqt")
        dst_p = os.path.join(leads_dir, f"{lead}_Switch_II_docked.pdbqt")
        if os.path.exists(src_p):
            shutil.copy(src_p, dst_p)
            
        src_xyz = os.path.join(base_dir, "data", "quantum", "structures", f"{lead}.xyz")
        dst_pdb = os.path.join(leads_dir, f"{lead}_3D_structure.pdb")
        if os.path.exists(src_xyz):
            xyz_to_pdb(src_xyz, dst_pdb, resname="LIG")
            
    print("  -> Prepared Scene 3 (Top 3 Leads: Avapritinib, Futibatinib, Belumosudil).")

    # 4. Write Blueprint Guide for Graphical Abstract
    blueprint_text = """# Graphical Abstract Design Blueprint (Q1 Standard)

## Visual Concept: The 3-Stage Storyline (Left to Right Flow)

```text
+---------------------------------------------------------------------------------------------------------+
|                                  GRAPHICAL ABSTRACT STORYLINE (3-STAGE FLOW)                            |
+------------------------------------+-----------------------------------+--------------------------------+
|  STAGE 1: KRAS-G12D TARGETING     |  STAGE 2: 2D QUANTUM ADSORPTION   |  STAGE 3: QSPR SCREENING &     |
|                                    |                                   |           EXTERNAL QM LEADS    |
|  [3D KRAS-G12D Ribbon + Surface]   |  [3D 2D B/P-g-C3N4 Monolayer]     |  [Nested QSPR (N=33 -> 350)]   |
|  * Pocket: Switch II Cleft         |  * Interfacial pi-pi Stacking     |  * 328/350 Inside Domain       |
|  * Key Res: Asp12, Tyr96, Arg68    |  * B (+0.35e) / P (-0.17e) Dipole |  * Top 3 Confirmed Leads:      |
|  * MRTX1133 Native Binding         |  * Delta_E_ads = -35.0 kcal/mol   |    1. Avapritinib (-9.43 kcal) |
|  * RMSD = 1.419 A (PDB 7RPZ)       |  * GFN2-xTB / D4 Dispersion       |    2. Futibatinib (-9.04 kcal) |
|                                    |                                   |    3. Belumosudil (-8.99 kcal) |
+------------------------------------+-----------------------------------+--------------------------------+
```

---

## Exact Asset Mapping for Each Stage:

### Stage 1 (Left Scene): Receptor Pocket Engagement
- **3D File to Render**: `Scene1_KRAS_G12D_MRTX1133_complex.pdb`
- **Render Style (PyMOL / ChimeraX)**:
  - KRAS protein: Cartoon / Semi-transparent surface (Color: Soft Slate Gray `#78909C` or Ice Blue `#B0BEC5`).
  - Switch II cleft: Highlight residues **Asp12** (Red `#E53935`), **Tyr96** (Cyan `#00ACC1`), and **Arg68** (Blue `#1E88E5`) as sticks.
  - MRTX1133 inhibitor: Bright Emerald / Teal sticks (`#004D40` or `#00897B`).
  - Label: *"KRAS-G12D Target Engagement (PDB 7RPZ, 1.30 Å)"* & *"RMSD = 1.419 Å"*.

### Stage 2 (Middle Scene): 2D Nanocarrier Loading
- **3D File to Render**: `Scene2_gC3N4_BP_MRTX1133_adsorption.pdb`
- **Render Style**:
  - $g\text{-}C_3N_4$ sheet: Planar heptazine framework in ball-and-stick or stick format (Carbons: Gray, Nitrogens: Deep Blue, B dopant: Pink/Magenta, P dopant: Orange).
  - MRTX1133 drug: Hovering at $d = 3.35\text{ \AA}$ above the sheet.
  - Subtle electrostatic polarization arrow between B ($\delta^+$) and P ($\delta^-$).
  - Label: *"2D B/P-g-C3N4 Nanocarrier"* & *"$\Delta E_{\text{ads}} = -35.04\text{ kcal/mol}$ (GFN2-xTB)"*.

### Stage 3 (Right Scene): High-Throughput QSPR & Prioritized Leads
- **Visual Elements**:
  - Small funnel or arrow diagram: $33 \text{ QM Ref} \to \text{Surrogate QSPR } (Q^2_{\text{CV}}=0.57) \to 350 \text{ Screen} \to \text{328 Inside AD } (h^*=0.455)$.
  - 3 Small 2D chemical structures or 3D stick poses for the Top 3 Leads:
    1. **Avapritinib**: Vina $-9.43\text{ kcal/mol}$, $\text{LE} = 0.255$, $\text{QM } \Delta E_{\text{ads}} = -13.13\text{ kcal/mol}$.
    2. **Futibatinib**: Vina $-9.04\text{ kcal/mol}$, $\text{LE} = 0.292$, $\text{QM } \Delta E_{\text{ads}} = -16.39\text{ kcal/mol}$.
    3. **Belumosudil**: Vina $-8.99\text{ kcal/mol}$, $\text{LE} = 0.264$, $\text{QM } \Delta E_{\text{ads}} = -17.36\text{ kcal/mol}$.
  - Label: *"Prioritized Clinical Leads & Target Confirmation"*.

---

## Recommended Dimensions & Typography:
- **Aspect Ratio**: $2:1$ (Standard Journal Graphical Abstract, e.g. $1200 \times 600\text{ px}$ or $16 \times 8\text{ cm}$).
- **Resolution**: $300 - 600\text{ DPI}$, RGB, White Background.
- **Font**: Arial, Helvetica, or Times New Roman ($10 - 14\text{ pt}$, clean and uncluttered).
- **Rule of Thumb**: Keep textual labels to concise keywords; let the authentic 3D structures carry the narrative.
"""
    with open(os.path.join(ga_dir, "GRAPHICAL_ABSTRACT_BLUEPRINT.md"), 'w', encoding='utf-8') as f:
        f.write(blueprint_text)
        
    # Re-build consolidated ZIP
    zip_path = os.path.join(base_dir, "FIGURES_EXACT_SOURCE_DATA_PACKAGE.zip")
    pkg_root = os.path.join(base_dir, "data", "figures_source_package")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(pkg_root):
            for file in files:
                abs_f = os.path.join(root, file)
                rel_f = os.path.relpath(abs_f, pkg_root)
                zipf.write(abs_f, os.path.join("FIGURES_EXACT_SOURCE_DATA_PACKAGE", rel_f))
                
    print(f"\n[SUCCESS] Updated Consolidated ZIP Package ({os.path.getsize(zip_path)} bytes): {zip_path}")
    return zip_path

if __name__ == "__main__":
    package_ga()
