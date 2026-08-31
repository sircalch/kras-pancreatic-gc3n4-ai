# Graphical Abstract Design Blueprint (Q1 Standard)

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
  - $g	ext{-}C_3N_4$ sheet: Planar heptazine framework in ball-and-stick or stick format (Carbons: Gray, Nitrogens: Deep Blue, B dopant: Pink/Magenta, P dopant: Orange).
  - MRTX1133 drug: Hovering at $d = 3.35	ext{ \AA}$ above the sheet.
  - Subtle electrostatic polarization arrow between B ($\delta^+$) and P ($\delta^-$).
  - Label: *"2D B/P-g-C3N4 Nanocarrier"* & *"$\Delta E_{	ext{ads}} = -35.04	ext{ kcal/mol}$ (GFN2-xTB)"*.

### Stage 3 (Right Scene): High-Throughput QSPR & Prioritized Leads
- **Visual Elements**:
  - Small funnel or arrow diagram: $33 	ext{ QM Ref} 	o 	ext{Surrogate QSPR } (Q^2_{	ext{CV}}=0.57) 	o 350 	ext{ Screen} 	o 	ext{328 Inside AD } (h^*=0.455)$.
  - 3 Small 2D chemical structures or 3D stick poses for the Top 3 Leads:
    1. **Avapritinib**: Vina $-9.43	ext{ kcal/mol}$, $	ext{LE} = 0.255$, $	ext{QM } \Delta E_{	ext{ads}} = -13.13	ext{ kcal/mol}$.
    2. **Futibatinib**: Vina $-9.04	ext{ kcal/mol}$, $	ext{LE} = 0.292$, $	ext{QM } \Delta E_{	ext{ads}} = -16.39	ext{ kcal/mol}$.
    3. **Belumosudil**: Vina $-8.99	ext{ kcal/mol}$, $	ext{LE} = 0.264$, $	ext{QM } \Delta E_{	ext{ads}} = -17.36	ext{ kcal/mol}$.
  - Label: *"Prioritized Clinical Leads & Target Confirmation"*.

---

## Recommended Dimensions & Typography:
- **Aspect Ratio**: $2:1$ (Standard Journal Graphical Abstract, e.g. $1200 	imes 600	ext{ px}$ or $16 	imes 8	ext{ cm}$).
- **Resolution**: $300 - 600	ext{ DPI}$, RGB, White Background.
- **Font**: Arial, Helvetica, or Times New Roman ($10 - 14	ext{ pt}$, clean and uncluttered).
- **Rule of Thumb**: Keep textual labels to concise keywords; let the authentic 3D structures carry the narrative.
