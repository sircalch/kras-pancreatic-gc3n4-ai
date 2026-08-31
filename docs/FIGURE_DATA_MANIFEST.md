# Guía Maestra de Datos y Especificaciones para la Generación de Figuras (Q1)

Esta guía detalla exactamente **qué debe contener cada una de las 10 figuras**, los **archivos de datos fuente**, las **columnas específicas** y los **valores numéricos exactos** obtenidos de las corridas cuánticas (**GFN2-xTB**) y de docking molecular (**AutoDock Vina**).

---

## Índice de Archivos de Datos Fuente en el Proyecto

Todos los datos numéricos y estructuras calculadas se encuentran en:
- `data/processed/MASTER_COMPOUNDS_CURATED.csv` — Cohorte maestra $N=33$ con todos los descriptores físicos, cuánticos y scores Vina.
- `results/quantum/isolated_drugs_qm_results.csv` — Estructura electrónica cuántica real de los 38 fármacos (HOMO, LUMO, Gap, $\omega$, dipolos).
- `results/quantum/nanocarrier_qm_results.csv` — Propiedades de las 4 monocapas 2D $g\text{-}C_3N_4$ (VBM, CBM, cargas $q_{\text{B}} = +0.3494\,e$, $q_{\text{P}} = -0.1679\,e$).
- `results/quantum/adsorption_qm_results.csv` — 76 simulaciones cuánticas de adsorción ($\Delta E_{\text{ads}}$, $\Delta Q$, dispersión D4).
- `results/quantum/quantum_benchmark_10systems.csv` — Benchmark cuántico multinivel en 10 sistemas (GFN2-xTB vs GFN1-xTB).
- `results/qspr/table3_external_qm_validation_leads.csv` — Validación QM externa de los 5 *leads* con leverage $h_i$, error QSPR y scores Vina.
- `results/qspr/oof_observed_vs_predicted_qspr.csv` — Datos de paridad Out-of-Fold (OOF) y residuales del modelo QSPR.
- `results/qspr/yscrambling_1000_permutations.csv` — 1,000 permutaciones Y-scrambling.
- `data/quantum/structures/` — Coordenadas atómicas 3D (XYZ) de todos los fármacos, portadores y complejos.
- `results/docking/master_poses/` — Coordenadas PDBQT de los mejores modos de acoplamiento sobre PDB 7RPZ.

---

## Especificaciones Detalladas Figura por Figura

### 🖼️ Figura 1: Graphical Abstract
- **Contenido Requerido**:
  1. **Panel Izquierdo**: Estructura de KRAS-G12D (PDB 7RPZ, 1.30 Å) con el inhibidor MRTX1133 coordinando con Asp12 y Tyr96 en el bolsillo Switch II.
  2. **Panel Central**: Nanoportador 2D $g\text{-}C_3N_4$ con dopaje B/P y fármaco adsorbido en apilamiento $\pi$-$\pi$ ($d = 3.35$ Å), indicando $\Delta E_{\text{ads}} = -35.03\text{ kcal/mol}$.
  3. **Panel Derecho**: Flujo de screening QSPR desacoplado ($350 \to \text{AD Filter } (h^*=0.455) \to \text{Recálculo Cuántico GFN2-xTB} \to \text{Validación Vina}$).
- **Textos / Etiquetas Clave**:
  - Título: *"Atomistic Modeling and QSPR-Guided Screening of 2D Graphitic Carbon Nitride Nanocarriers for KRAS-G12D Inhibitor Loading and Target Engagement"*
  - **Usar**: *"Quantum Adsorption Modeling"*, *"Loading and Target Engagement"*.
  - **NO usar**: "Quantum Chemisorption", "Triggered Release", "Targeted Delivery".
- **Fuente de Datos**: `results/quantum/adsorption_qm_results.csv`, PDB 7RPZ.

---

### 🖼️ Figura 2: Multi-Scale Computational Workflow Architecture
- **Contenido Requerido**: Diagrama de flujo científico estructurado en 4 fases metodológicas:
  1. **Fase 1 (Validación Cristalográfica)**: PDB 7RPZ (1.30 Å), extracción de ligando 6IC, AutoDock Vina v1.2.7 (RMSD = 1.419 Å).
  2. **Fase 2 (Modelado Cuántico GFN2-xTB)**: Monocapas $C_{18}N_{24}H_6$ (prístina y B/P co-dopada), optimización geométrica, corrección D4, cálculo de $\Delta E_{\text{ads}}$ y $\Delta Q$.
  3. **Fase 3 (Modelo Subrogado QSPR Anidado)**: $n=33$, $p=4$ descriptores a priori ($MW, PSA, \alpha, \omega$), $n/p = 8.25$, validación cruzada anidada 5-fold ($Q^2_{\text{CV}} = +0.5696$), 1,000 permutaciones Y-scrambling ($p = 0.0010$), Dominio de Williams ($h^* = 0.455$).
  4. **Fase 4 (Screening Desacoplado con Validación QM Externa)**: 350 candidatos DrugBank $\to$ 328 en dominio AD (93.7%) $\to$ Recálculo QM GFN2-xTB de *leads* $\to$ Confirmación Vina y Ligand Efficiency.
- **Fuente de Datos**: `src/visualization/generate_kras_full_manuscript.py`.

---

### 🖼️ Figura 3: Crystallographic Redocking Validation (PDB 7RPZ, 1.30 Å)
- **Contenido Requerido**:
  - **Panel (a)**: Superposición 3D real de la pose cristalográfica de MRTX1133 (ligando 6IC, color gris) vs la pose redockeada por AutoDock Vina (color naranja/cian).
    - Anotación clara: **$\text{RMSD} = 1.419\text{ \AA}$** (satisfactorio, $< 2.0\text{ \AA}$).
    - Zoom en los residuos clave: **Asp12** (puente salino iónico), **Tyr96** (contacto $\pi$-$\pi$), **Glu62**, **Arg68**.
  - **Panel (b)**: Histograma/gráfico de barras de afinidad de unión ($\text{kcal/mol}$) a lo largo de los 9 modos conformacionales generados por Vina (Modo 1: $-9.16$, Modo 2: $-8.82$, etc.).
- **Archivos Fuente**:
  - Receptor: `results/docking/validation/7RPZ_receptor.pdbqt`
  - Cristal Pose: ligando 6IC en PDB 7RPZ.
  - Poses Redocking: `results/docking/master_poses/MRTX1133_docked.pdbqt`

---

### 🖼️ Figura 4: Binding Score Distribution Across Pharmacological Classes
- **Contenido Requerido**:
  - Gráfico de cajas y violín (*Box & Violin Plot*) con puntos individuales superpuestos (*strip plot*) comparando la afinidad de unión en el bolsillo Switch II entre los 4 grupos:
    - **Group A: KRAS Mechanistic/State Probes** ($n=5$): Mediana = $-7.68\text{ kcal/mol}$ (MRTX1133: $-8.06$, BI-2865: $-8.46$, RMC-6236: $-3.38$, HRS-4642: $-7.58$, JDQ-443: $-7.68$).
    - **Group B: Pan-RAS / G12C Inhibitors** ($n=5$): Mediana = $-5.86\text{ kcal/mol}$ (Sotorasib: $-5.86$, Adagrasib: $-6.90$, BI-2852: $-8.78$, MRTX1719: $-5.86$, RMC-7977: $-4.69$).
    - **Group C: Downstream MAPK / RTK TKIs** ($n=8$): Mediana = $-7.82\text{ kcal/mol}$ (Abemaciclib: $-9.75$, Cobimetinib: $-9.12$, Larotrectinib: $-8.59$).
    - **Group D: Standard PDAC Cytotoxics** ($n=15$): Mediana = $-6.84\text{ kcal/mol}$ (5-FU: $-4.98$, Capecitabine: $-7.88$, Hydroxyurea: $-2.86$).
  - Anotación estadística: **Omnibus Kruskal-Wallis $H = 5.763, p = 0.1237, \eta^2 = 0.095$ ($p > 0.05$)**.
- **Archivo Fuente**: `data/processed/MASTER_COMPOUNDS_CURATED.csv` (columnas: `group`, `Real_Vina_Score_kcal_mol`, `name`).

---

### 🖼️ Figura 5: Electronic Structure and Nanocarrier Reactivity
- **Contenido Requerido**:
  - **Panel (a)**: Densidad de Estados (DOS/PDOS) o alineación de bandas de la monocapa 2D $g\text{-}C_3N_4$:
    - Prístina: $\text{VBM} = -10.27\text{ eV}$, $\text{CBM} = -10.27\text{ eV}$.
    - B-dopada: $\text{VBM} = -10.35\text{ eV}$, carga de boro $q_{\text{B}} = +0.3969\,e$ (centro ácido de Lewis).
    - P-dopada: $\text{VBM} = -10.22\text{ eV}$, carga de fósforo $q_{\text{P}} = -0.2939\,e$ (centro donador de electrones).
    - B/P co-dopada: $q_{\text{B}} = +0.3494\,e$, $q_{\text{P}} = -0.1679\,e$ (dipolo interfacial inducido).
  - **Panel (b)**: Mapa conceptual de potencial electrostático (ESP) o perfil de transferencia de carga interfacial $\Delta Q$ tras adsorción del fármaco ($\Delta Q$ positivo indica donación electrónica hacia el nanoportador).
- **Archivo Fuente**: `results/quantum/nanocarrier_qm_results.csv` y `results/quantum/adsorption_qm_results.csv`.

---

### 🖼️ Figura 6: Residue-Level Interaction Fingerprints on KRAS-G12D
- **Contenido Requerido**:
  - Frecuencia de contacto atómico ($d \le 3.8\text{ \AA}$) o mapa de calor de huella de interacción (*interaction fingerprint heatmap*) fármaco $\times$ residuo para los 33 compuestos.
  - Residuos clave:
    - **Asp12**: 81.8% (27/33 compuestos)
    - **Tyr96**: 81.8% (27/33 compuestos)
    - **Glu62**: 75.8% (25/33 compuestos)
    - **Arg68**: 69.7% (23/33 compuestos)
    - **Gln99**: 63.6% (21/33 compuestos)
    - **His95**: 57.6% (19/33 compuestos)
- **Archivo Fuente**: `data/processed/MASTER_COMPOUNDS_CURATED.csv` y archivos `.pdbqt` en `results/docking/master_poses/`.

---

### 🖼️ Figura 7: OECD Principle 3: Williams Plot (Applicability Domain)
- **Contenido Requerido**:
  - Gráfico de Williams: *Hat-matrix leverage* ($h_i$) en el eje X vs *Standardized Residuals* ($\delta_i$) en el eje Y.
  - Línea límite de leverage de advertencia: **$h^* = 0.455$** ($h^* = 3(p+1)/n = 3 \times 5 / 33$).
  - Límites de residuales estandarizados: **$\pm 3\sigma$** (bandas horizontales en $+3.0$ y $-3.0$).
  - Puntos coloreados por grupo farmacológico.
  - 32 de 33 compuestos (97.0%) dentro del dominio (Cobimetinib $h_i = 0.200$, Paclitaxel $h_i = 0.360$, todos $< 0.455$).
- **Archivo Fuente**: `results/qspr/oof_observed_vs_predicted_qspr.csv` (columnas: `Hat_Leverage_hi`, `Std_Residual`, `Group`, `Compound`).

---

### 🖼️ Figura 8: Statistical Validation of the QSPR Surrogate Model (3 Paneles)
- **Contenido Requerido**:
  - **Panel (a)**: Parity plot Out-of-Fold (OOF): $\Delta E_{\text{ads}}$ observado cuántico (GFN2-xTB) vs $\Delta E_{\text{ads}}$ predicho por QSPR (Ridge $\alpha=1.0$).
    - Línea de paridad ideal $y = x$.
    - Métricas anotadas: **$Q^2_{\text{CV}} = +0.5696$**, **$\text{RMSE} = 5.201\text{ kcal/mol}$**, **$\text{MAE} = 4.194\text{ kcal/mol}$**.
  - **Panel (b)**: Gráfico de residuales ($\text{Residual} = y_{\text{obs}} - y_{\text{pred}}$) vs valores predichos, con línea central en $0.0$.
  - **Panel (c)**: Histograma de 1,000 permutaciones $Y$-scrambling:
    - Distribución centrada en $\overline{Q^2_{\text{scrambled}}} = -0.2357$.
    - Línea vertical discontinua roja en el valor real $Q^2_{\text{CV}} = +0.5696$.
    - Anotación: **Empirical $p\text{-value} = 0.0010$ ($p < 0.001$)**, confirmando ausencia de correlación por azar.
- **Archivos Fuente**:
  - Paneles a y b: `results/qspr/oof_observed_vs_predicted_qspr.csv`
  - Panel c: `results/qspr/yscrambling_1000_permutations.csv`

---

### 🖼️ Figura 9: Multi-Objective Screening Validation Across Top Leads & Controls
- **Contenido Requerido**:
  - **Panel (a)**: Gráfico de barras comparativo de afinidad de unión Vina ($\text{kcal/mol}$) de los 5 *leads* de screening vs controles estándar en PDB 7RPZ:
    - Avapritinib ($-9.43$), Futibatinib ($-9.04$), Belumosudil ($-8.99$), Capivasertib ($-7.82$), Pimicotinib ($-7.64$).
    - Controles: MRTX1133 ($-8.06$), Gemcitabine ($-6.84$), 5-FU ($-4.98$).
  - **Panel (b)**: Frente de Pareto / Dispersión: Score Vina (eje Y) vs Ligand Efficiency (LE, eje X):
    - Tamaño del punto proporcional a la energía cuántica de adsorción $\Delta E_{\text{ads}}$.
    - Puntos etiquetados, demostrando que los *leads* alcanzan alta afinidad por complementariedad de forma y electrostática ($\text{LE} = 0.255 \text{ a } 0.292\text{ kcal/mol/atom}$) y no por inflación de peso molecular.
- **Archivos Fuente**: `results/qspr/table3_external_qm_validation_leads.csv` y `data/processed/MASTER_COMPOUNDS_CURATED.csv`.

---

### 🖼️ Figura 10: Multi-Scale Structural Architecture (6 Paneles)
- **Contenido Requerido**:
  - **Panel (a)**: Vista 3D del receptor KRAS-G12D (PDB 7RPZ, 1.30 Å) en superficie/cartoon con MRTX1133 alojado en el bolsillo alostérico Switch II.
  - **Panel (b)**: Zoom 3D en la red de coordinación de Asp12:
    - Puente salino iónico Asp12(COO⁻) $\cdots$ MRTX1133(Amine H⁺) ($d = 2.84\text{ \AA}$).
    - Enlace de hidrógeno con Tyr96 ($d = 2.95\text{ \AA}$) y contacto con Arg68 ($d = 3.42\text{ \AA}$).
  - **Panel (c)**: Vista 3D de la unión de BI-2865 en el bolsillo Switch I/II de KRAS inactivo.
  - **Panel (d)**: Geometría optimizada del complejo $g\text{-}C_3N_4(\text{prístina}) + \text{MRTX1133}$ indicando la distancia de apilamiento $\pi$-$\pi$ ($d = 3.35\text{ \AA}$) y $\Delta E_{\text{ads}} = -35.03\text{ kcal/mol}$.
  - **Panel (e)**: Geometría del complejo $g\text{-}C_3N_4(\text{B/P-dopada}) + \text{MRTX1133}$ con centros B ($\delta^+$) y P ($\delta^-$) y $\Delta E_{\text{ads}} = -35.04\text{ kcal/mol}$.
  - **Panel (f)**: Gráfico de paridad del benchmark cuántico (GFN2-xTB vs GFN1-xTB) en los 10 sistemas diversos de la Tabla 2.
- **Archivos Fuente**:
  - Coordenadas PDB 7RPZ.
  - PDBQTs en `results/docking/master_poses/`.
  - XYZs en `scratch/qm_calcs_adsorption/` (`complex_pristine_MRTX1133.xyz`, `complex_BP_doped_MRTX1133.xyz`).
  - Datos de benchmark: `results/quantum/quantum_benchmark_10systems.csv`.

---

## Resumen de Tablas en el Manuscrito y SI

| Tabla | Título | Ubicación | Archivo Fuente |
|---|---|---|---|
| **Tabla 1** | Resumen farmacológico compacto ($n$, medianas, medias de Vina y LE por grupo) | Manuscrito Principal | `generate_kras_full_manuscript.py` |
| **Tabla 2** | Benchmark cuántico multinivel en 10 sistemas diversos | Manuscrito Principal | `results/quantum/quantum_benchmark_10systems.csv` |
| **Tabla 3** | Validación QM externa de los 5 *leads* (QSPR vs QM, $h_i$, Vina, LE) | Manuscrito Principal | `results/qspr/table3_external_qm_validation_leads.csv` |
| **Tabla S1** | Base de datos maestra completa ($N=33$) con todos los descriptores | Supporting Information | `data/processed/MASTER_COMPOUNDS_CURATED.csv` |
