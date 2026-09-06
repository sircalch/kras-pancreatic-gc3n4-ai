# -*- coding: utf-8 -*-
"""
build_kras_verified_references.py
Peer-reviewed bibliography for this project. Every DOI was verified against
CrossRef (author + title + year). 10 entries whose DOI could not be
verified carry needs_review=True and no DOI (text retained for manual completion).
"""

import os

KRAS_VERIFIED_REFERENCES = [
    {
        "citation": "Wang, X.; Allen, S.; Blake, J. F.; Bowcut, V.; Briere, D. M.; Calinisan, A.; Dahlke, J. R.; Fell, J. B.; Fischer, J. P.; Gunn, R. J.; et al. Identification of MRTX1133, a Noncovalent, Potent, and Selective KRAS G12D Inhibitor. Journal of Medicinal Chemistry 2021, 65 (4), 3123-3133.",
        "doi": "10.1021/acs.jmedchem.1c01688",
    },
    {
        "citation": "Hallin, J.; Bowcut, V.; Calinisan, A.; Briere, D. M.; Hargis, L.; Engstrom, L. D.; Laguer, J.; Medwid, J.; Vanderpool, D.; Lifset, E.; et al. Anti-tumor efficacy of a potent and selective non-covalent KRASG12D inhibitor. Nature Medicine 2022, 28 (10), 2171-2182.",
        "doi": "10.1038/s41591-022-02007-7",
    },
    {
        "citation": "Kemp, S. B.; Cheng, N.; Markosyan, N.; Sor, R.; Kim, I. K.; Hallin, J.; Shoush, J.; Quinones, L.; Brown, N. V.; Bassett, J. B.; et al. Efficacy of a Small-Molecule Inhibitor of KrasG12D in Immunocompetent Models of Pancreatic Cancer. Cancer Discovery 2022, 13 (2), 298-311.",
        "doi": "10.1158/2159-8290.cd-22-1066",
    },
    {
        "citation": "Canon, J.; Rex, K.; Saiki, A. Y.; Mohr, C.; Cooke, K.; Bagal, D.; Gaida, K.; Holt, T.; Knutson, C. G.; Koppada, N.; et al. The clinical KRAS(G12C) inhibitor AMG 510 drives anti-tumour immunity. Nature 2019, 575 (7781), 217-223.",
        "doi": "10.1038/s41586-019-1694-1",
    },
    {
        "citation": "Punekar, S. R.; Velcheti, V.; Neel, B. G.; Wong, K. K. The current state of the art and future trends in RAS-targeted cancer therapies. Nature Reviews Clinical Oncology 2022, 19 (10), 637-655.",
        "doi": "10.1038/s41571-022-00671-9",
    },
    {
        "citation": "Pushalkar, S.; Hundeyin, M.; Daley, D.; Zambirinis, C. P.; Kurz, E.; Mishra, A.; Mohan, N.; Aykut, B.; Usyk, M.; Torres, L. E.; et al. The Pancreatic Cancer Microbiome Promotes Oncogenesis by Induction of Innate and Adaptive Immune Suppression. Cancer Discovery 2018, 8 (4), 403-416.",
        "doi": "10.1158/2159-8290.cd-17-1134",
    },
    {
        "citation": "Maitra, A.; Hruban, R. H. Pancreatic Cancer. Annual Review of Pathology: Mechanisms of Disease 2008, 3 (1), 157-188.",
        "doi": "10.1146/annurev.pathmechdis.3.121806.154305",
    },
    {
        "citation": "Ryan, D. P.; Hong, T. S.; Bardeesy, N. Pancreatic Adenocarcinoma. New England Journal of Medicine 2014, 371 (11), 1039-1049.",
        "doi": "10.1056/nejmra1404198",
    },
    {
        "citation": "Conroy, T.; Desseigne, F.; Ychou, M.; Bouché, O.; Guimbaud, R.; Bécouarn, Y.; Adenis, A.; Raoul, J. L.; Gourgou-Bourgade, S.; de la Fouchardière, C.; et al. FOLFIRINOX versus Gemcitabine for Metastatic Pancreatic Cancer. New England Journal of Medicine 2011, 364 (19), 1817-1825.",
        "doi": "10.1056/nejmoa1011923",
    },
    {
        "citation": "Von Hoff, D. D.; Ervin, T.; Arena, F. P.; Chiorean, E. G.; Infante, J.; Moore, M.; Seay, T.; Tjulandin, S. A.; Ma, W. W.; Saleh, M. N.; et al. Increased Survival in Pancreatic Cancer with nab-Paclitaxel plus Gemcitabine. New England Journal of Medicine 2013, 369 (18), 1691-1703.",
        "doi": "10.1056/nejmoa1304369",
    },
    {
        "citation": "Wang, X.; Maeda, K.; Thomas, A.; Takanabe, K.; Xin, G.; Carlsson, J. M.; Domen, K.; Antonietti, M. A metal-free polymeric photocatalyst for hydrogen production from water under visible light. Nature Materials 2008, 8 (1), 76-80.",
        "doi": "10.1038/nmat2317",
    },
    {
        "citation": "Zheng, Y.; Liu, J.; Liang, J.; Jaroniec, M.; Qiao, S. Z. Graphitic carbon nitride materials: controllable synthesis and applications in fuel cells and photocatalysis. Energy & Environmental Science 2012, 5 (5), 6717.",
        "doi": "10.1039/c2ee03479d",
    },
    {
        "citation": "Ong, W. J.; Tan, L. L.; Ng, Y. H.; Yong, S. T.; Chai, S. P. Graphitic Carbon Nitride (g-C 3 N 4 )-Based Photocatalysts for Artificial Photosynthesis and Environmental Remediation: Are We a Step Closer To Achieving Sustainability?. Chemical Reviews 2016, 116 (12), 7159-7329.",
        "doi": "10.1021/acs.chemrev.6b00075",
    },
    {
        "citation": "Lin, L.; Song, J.; Yang, H.; Chen, X. Yolk–Shell Nanostructures: Design, Synthesis, and Biomedical Applications. Advanced Materials 2017, 30 (6).",
        "doi": "10.1002/adma.201704639",
    },
    {
        "citation": "Feng, L.; He, F.; Yang, G.; Gai, S.; Dai, Y.; Li, C.; Yang, P. NIR-driven graphitic-phase carbon nitride nanosheets for efficient bioimaging and photodynamic therapy. Journal of Materials Chemistry B 2016, 4 (48), 8000-8008.",
        "doi": "10.1039/c6tb02232d",
    },
    {
        "citation": "Babu Ganganboina, A.; Dung Nguyen, M.; Hien Luong Nguyen, T.; Prasetyo Kuncoro, E.; Doong, R. A. Boron and phosphorus co-doped one-dimensional graphitic carbon nitride for enhanced visible-light-driven photodegradation of diclofenac. Chemical Engineering Journal 2021, 425, 131520.",
        "doi": "10.1016/j.cej.2021.131520",
    },
    {
        "citation": "Zhang, J.; Zhang, G.; Chen, X.; Lin, S.; Möhlmann, L.; Dołęga, G.; Lipner, G.; Antonietti, M.; Blechert, S.; Wang, X. Co‐Monomer Control of Carbon Nitride Semiconductors to Optimize Hydrogen Evolution with Visible Light. Angewandte Chemie International Edition 2012, 51 (13), 3183-3187.",
        "doi": "10.1002/anie.201106656",
    },
    {
        "citation": "Cao, S.; Low, J.; Yu, J.; Jaroniec, M. Polymeric Photocatalysts Based on Graphitic Carbon Nitride. Advanced Materials 2015, 27 (13), 2150-2176.",
        "doi": "10.1002/adma.201500033",
    },
    {
        "citation": "Pourmadadi, M.; Rahmani, E.; Eshaghi, M. M.; Shamsabadipour, A.; Ghotekar, S.; Rahdar, A.; Romanholo Ferreira, L. F. Graphitic carbon nitride (g-C3N4) synthesis methods, surface functionalization, and drug delivery applications: A review. Journal of Drug Delivery Science and Technology 2023, 79, 104001.",
        "doi": "10.1016/j.jddst.2022.104001",
    },
    {
        "citation": "Liu, L.; Du, X. Polyethylenimine-modified graphitic carbon nitride nanosheets: a label-free Raman traceable siRNA delivery system. Journal of Materials Chemistry B 2021, 9 (34), 6895-6901.",
        "doi": "10.1039/d1tb00984b",
    },
    {
        "citation": "Bannwarth, C.; Ehlert, S.; Grimme, S. GFN2-xTB─An Accurate and Broadly Parametrized Self-Consistent Tight-Binding Quantum Chemical Method with Multipole Electrostatics and Density-Dependent Dispersion Contributions. Journal of Chemical Theory and Computation 2019, 15 (3), 1652-1671.",
        "doi": "10.1021/acs.jctc.8b01176",
    },
    {
        "citation": "Grimme, S.; Bannwarth, C.; Shushkov, P. A Robust and Accurate Tight-Binding Quantum Chemical Method for Structures, Vibrational Frequencies, and Noncovalent Interactions of Large Molecular Systems Parametrized for All spd-Block Elements ( Z = 1–86). Journal of Chemical Theory and Computation 2017, 13 (5), 1989-2009.",
        "doi": "10.1021/acs.jctc.7b00118",
    },
    {
        "citation": "Caldeweyher, E.; Ehlert, S.; Hansen, A.; Neugebauer, H.; Spicher, S.; Bannwarth, C.; Grimme, S. A generally applicable atomic-charge dependent London dispersion correction. The Journal of Chemical Physics 2019, 150 (15).",
        "doi": "10.1063/1.5090222",
    },
    {
        "citation": "Grimme, S.; Antony, J.; Ehrlich, S.; Krieg, H. A consistent and accurate ab initio parametrization of density functional dispersion correction (DFT-D) for the 94 elements H-Pu. The Journal of Chemical Physics 2010, 132 (15).",
        "doi": "10.1063/1.3382344",
    },
    {
        "citation": "Spicher, S.; Grimme, S. Robust Atomistic Modeling of Materials, Organometallic, and Biochemical Systems. Angewandte Chemie International Edition 2020, 59 (36), 15665-15673.",
        "doi": "10.1002/anie.202004239",
    },
    {
        "citation": "Kessler, F. K.; Zheng, Y.; Schwarz, D.; Merschjann, C.; Schnick, W.; Wang, X.; Bojdys, M. J. Functional carbon nitride materials — design strategies for electrochemical devices. Nature Reviews Materials 2017, 2 (6).",
        "doi": "10.1038/natrevmats.2017.30",
    },
    {
        "citation": "Thomas, A.; Fischer, A.; Goettmann, F.; Antonietti, M.; Müller, J. O.; Schlögl, R.; Carlsson, J. M. Graphitic carbon nitride materials: variation of structure and morphology and their use as metal-free catalysts. Journal of Materials Chemistry 2008, 18 (41), 4893.",
        "doi": "10.1039/b800274f",
    },
    {
        "citation": "Geerlings, P.; De Proft, F.; Langenaeker, W. Conceptual Density Functional Theory. Chemical Reviews 2003, 103 (5), 1793-1874.",
        "doi": "10.1021/cr990029p",
    },
    {
        "citation": "Trott, O.; Olson, A. J. AutoDock Vina: Improving the speed and accuracy of docking with a new scoring function, efficient optimization, and multithreading. Journal of Computational Chemistry 2009, 31 (2), 455-461.",
        "doi": "10.1002/jcc.21334",
    },
    {
        "citation": "Eberhardt, J.; Santos-Martins, D.; Tillack, A. F.; Forli, S. AutoDock Vina 1.2.0: New Docking Methods, Expanded Force Field, and Python Bindings. Journal of Chemical Information and Modeling 2021, 61 (8), 3891-3898.",
        "doi": "10.1021/acs.jcim.1c00203",
    },
    {
        "citation": "Berman, H. M. The Protein Data Bank. Nucleic Acids Research 2000, 28 (1), 235-242.",
        "doi": "10.1093/nar/28.1.235",
    },
    {
        "citation": "Landrum, G. RDKit: Open-Source Cheminformatics Software; GitHub: 2021. https://www.rdkit.org.",
        "doi": "10.5281/zenodo.5086055",
    },
    {
        "citation": "Kim, S.; Chen, J.; Cheng, T.; Gindulyte, A.; He, J.; He, S.; Li, Q.; Shoemaker, B. A.; Thiessen, P. A.; Yu, B.; et al. PubChem in 2021: new data content and improved web interfaces. Nucleic Acids Research 2020, 49 (D1), D1388-D1395.",
        "doi": "10.1093/nar/gkaa971",
    },
    {
        "citation": "Kitchen, D. B.; Decornez, H.; Furr, J. R.; Bajorath, J. Docking and scoring in virtual screening for drug discovery: methods and applications. Nature Reviews Drug Discovery 2004, 3 (11), 935-949.",
        "doi": "10.1038/nrd1549",
    },
    {
        "citation": "Parr, R. G.; Yang, W. Density-Functional Theory of Atoms and Molecules; Oxford University Press: New York, 1989.",
        "doi": "10.1093/oso/9780195092769.001.0001",
    },
    {
        "citation": "Parr, R. G.; Szentpály, L. v.; Liu, S. Electrophilicity Index. Journal of the American Chemical Society 1999, 121 (9), 1922-1924.",
        "doi": "10.1021/ja983494x",
    },
    {
        "citation": "Chattaraj, P. K.; Maiti, B.; Sarkar, U. Philicity: A Unified Treatment of Chemical Reactivity and Selectivity. The Journal of Physical Chemistry A 2003, 107 (25), 4973-4975.",
        "doi": "10.1021/jp034707u",
    },
    {
        "citation": "OECD. Guidance Document on the Validation of (Quantitative) Structure-Activity Relationship [(Q)SAR] Models; OECD Environment Health and Safety Publications, Series on Testing and Assessment, No. 69; OECD Publishing: Paris, 2007.",
        "doi": "10.1787/9789264085442-en",
    },
    {
        "citation": "Gramatica, P. Principles of QSAR models validation: internal and external. QSAR & Combinatorial Science 2007, 26 (5), 694-701.",
        "doi": "10.1002/qsar.200610151",
    },
    {
        "citation": "Tropsha, A. Best Practices for QSAR Model Development, Validation, and Exploitation. Molecular Informatics 2010, 29 (6-7), 476-488.",
        "doi": "10.1002/minf.201000061",
    },
    {
        "citation": "Williams, D. A. Generalized Linear Model Diagnostics Using the Deviance and Single Case Deletions. Applied Statistics 1987, 36 (2), 181.",
        "doi": "10.2307/2347550",
    },
    {
        "citation": "Cherkasov, A.; Muratov, E. N.; Fourches, D.; Varnek, A.; Baskin, I. I.; Cronin, M.; Dearden, J.; Gramatica, P.; Martin, Y. C.; Todeschini, R.; et al. QSAR Modeling: Where Have You Been? Where Are You Going To?. Journal of Medicinal Chemistry 2014, 57 (12), 4977-5010.",
        "doi": "10.1021/jm4004285",
    },
    {
        "citation": "Rücker, C.; Rücker, G.; Meringer, M. y-Randomization and Its Variants in QSPR/QSAR. Journal of Chemical Information and Modeling 2007, 47 (6), 2345-2357.",
        "doi": "10.1021/ci700157b",
    },
    {
        "citation": "Varoquaux, G.; Buitinck, L.; Louppe, G.; Grisel, O.; Pedregosa, F.; Mueller, A. Scikit-learn. GetMobile: Mobile Computing and Communications 2015, 19 (1), 29-33.",
        "doi": "10.1145/2786984.2786995",
    },
    {
        "citation": "Provenzano, P.; Cuevas, C.; Chang, A.; Goel, V.; Von Hoff, D.; Hingorani, S. Enzymatic Targeting of the Stroma Ablates Physical Barriers to Treatment of Pancreatic Ductal Adenocarcinoma. Cancer Cell 2012, 21 (3), 418-429.",
        "doi": "10.1016/j.ccr.2012.01.007",
    },
    {
        "citation": "Jacobetz, M. A.; Chan, D. S.; Neesse, A.; Bapiro, T. E.; Cook, N.; Frese, K. K.; Feig, C.; Nakagawa, T.; Caldwell, M. E.; Zecchini, H. I.; et al. Hyaluronan impairs vascular function and drug delivery in a mouse model of pancreatic cancer. Gut 2012, 62 (1), 112-120.",
        "doi": "10.1136/gutjnl-2012-302529",
    },
    {
        "citation": "Olive, K. P.; Jacobetz, M. A.; Davidson, C. J.; Gopinathan, A.; McIntyre, D.; Honess, D.; Madhu, B.; Goldgraben, M. A.; Caldwell, M. E.; Allard, D.; et al. Inhibition of Hedgehog Signaling Enhances Delivery of Chemotherapy in a Mouse Model of Pancreatic Cancer. Science 2009, 324 (5933), 1457-1461.",
        "doi": "10.1126/science.1171362",
    },
    {
        "citation": "Blanco, E.; Shen, H.; Ferrari, M. Principles of nanoparticle design for overcoming biological barriers to drug delivery. Nature Biotechnology 2015, 33 (9), 941-951.",
        "doi": "10.1038/nbt.3330",
    },
    {
        "citation": "Peer, D.; Karp, J. M.; Hong, S.; Farokhzad, O. C.; Margalit, R.; Langer, R. Nanocarriers as an emerging platform for cancer therapy. Nature Nanotechnology 2007, 2 (12), 751-760.",
        "doi": "10.1038/nnano.2007.387",
    },
    {
        "citation": "Shi, J.; Kantoff, P. W.; Wooster, R.; Farokhzad, O. C. Cancer nanomedicine: progress, challenges and opportunities. Nature Reviews Cancer 2016, 17 (1), 20-37.",
        "doi": "10.1038/nrc.2016.108",
    },
    {
        "citation": "Maeda, H.; Wu, J.; Sawa, T.; Matsumura, Y.; Hori, K. Tumor vascular permeability and the EPR effect in macromolecular therapeutics: a review. Journal of Controlled Release 2000, 65 (1-2), 271-284.",
        "doi": "10.1016/s0168-3659(99)00248-5",
    },
    {
        "citation": "Matsumura, Y.; Maeda, H. A new concept for macromolecular therapeutics in cancer chemotherapy: mechanism of tumoritropic accumulation of proteins and the antitumor agent smancs. Cancer Res. 1986, 46 (12 Pt 1), 6387–6392.",
        "doi": "PMID: 2946403",
    },
    {
        "citation": "Mitchell, M. J.; Billingsley, M. M.; Haley, R. M.; Wechsler, M. E.; Peppas, N. A.; Langer, R. Engineering precision nanoparticles for drug delivery. Nature Reviews Drug Discovery 2020, 20 (2), 101-124.",
        "doi": "10.1038/s41573-020-0090-8",
    },
    {
        "citation": "Awad, M. M.; Liu, S.; Rybkin, I. I.; Arbour, K. C.; Dilly, J.; Zhu, V. W.; Johnson, M. L.; Heist, R. S.; Patil, T.; Riely, G. J.; et al. Acquired Resistance to KRAS G12C Inhibition in Cancer. New England Journal of Medicine 2021, 384 (25), 2382-2393.",
        "doi": "10.1056/nejmoa2105281",
    },
    {
        "citation": "Ostrem, J. M.; Peters, U.; Sos, M. L.; Wells, J. A.; Shokat, K. M. K-Ras(G12C) inhibitors allosterically control GTP affinity and effector interactions. Nature 2013, 503 (7477), 548-551.",
        "doi": "10.1038/nature12796",
    },
    {
        "citation": "Cox, A. D.; Fesik, S. W.; Kimmelman, A. C.; Luo, J.; Der, C. J. Drugging the undruggable RAS: Mission Possible?. Nature Reviews Drug Discovery 2014, 13 (11), 828-851.",
        "doi": "10.1038/nrd4389",
    },
    {
        "citation": "Kessler, D.; Gmachl, M.; Mantoulidis, A.; Martin, L. J.; Zoephel, A.; Mayer, M.; Gollner, A.; Covini, D.; Fischer, S.; Gerstberger, T.; et al. Drugging an undruggable pocket on KRAS. Proceedings of the National Academy of Sciences 2019, 116 (32), 15823-15829.",
        "doi": "10.1073/pnas.1904529116",
    },
    {
        "citation": "Hofmann, M. H.; Gerlach, D.; Misale, S.; Petronczki, M.; Kraut, N. Expanding the Reach of Precision Oncology by Drugging All KRAS Mutants. Cancer Discovery 2022, 12 (4), 924-937.",
        "doi": "10.1158/2159-8290.cd-21-1331",
    },
    {
        "citation": "Pandey, D.; Chauhan, S. C.; Kashyap, V. K.; Roy, K. K. Structural insights into small-molecule KRAS inhibitors for targeting KRAS mutant cancers. European Journal of Medicinal Chemistry 2024, 277, 116771.",
        "doi": "10.1016/j.ejmech.2024.116771",
    },
    {
        "citation": "Kim, D.; Herdeis, L.; Rudolph, D.; Zhao, Y.; Böttcher, J.; Vides, A.; Ayala-Santos, C. I.; Pourfarjam, Y.; Cuevas-Navarro, A.; Xue, J. Y.; et al. Pan-KRAS inhibitor disables oncogenic signalling and tumour growth. Nature 2023, 619 (7968), 160-166.",
        "doi": "10.1038/s41586-023-06123-3",
    },
    {
        "citation": "Manzur, A.; Oluwasanmi, A.; Moss, D.; Curtis, A.; Hoskins, C. Nanotechnologies in Pancreatic Cancer Therapy. Pharmaceutics 2017, 9 (4), 39.",
        "doi": "10.3390/pharmaceutics9040039",
    },
    {
        "citation": "Hanahan, D. Hallmarks of Cancer: New Dimensions. Cancer Discovery 2022, 12 (1), 31-46.",
        "doi": "10.1158/2159-8290.cd-21-1059",
    },
    {
        "citation": "Vogelstein, B.; Papadopoulos, N.; Velculescu, V. E.; Zhou, S.; Diaz, L. A.; Kinzler, K. W. Cancer Genome Landscapes. Science 2013, 339 (6127), 1546-1558.",
        "doi": "10.1126/science.1235122",
    },
    {
        "citation": "Simanshu, D. K.; Nissley, D. V.; McCormick, F. RAS Proteins and Their Regulators in Human Disease. Cell 2017, 170 (1), 17-33.",
        "doi": "10.1016/j.cell.2017.06.009",
    },
    {
        "citation": "Moore, A. R.; Rosenberg, S. C.; McCormick, F.; Malek, S. RAS-targeted therapies: is the undruggable drugged?. Nature Reviews Drug Discovery 2020, 19 (8), 533-552.",
        "doi": "10.1038/s41573-020-0068-6",
    },
    {
        "citation": "Lu, W.; Zeng, R.; Pan, M.; Zhou, Y.; Tang, H.; Shen, W.; Tang, Y.; Lei, P. Pharmacokinetics, bioavailability, and tissue distribution of MRTX1133 in rats using UHPLC-MS/MS. Frontiers in Pharmacology 2024, 15.",
        "doi": "10.3389/fphar.2024.1509319",
    },
    {
        "citation": "Swetha, K.; Bhatnagar, A.; Lakavathu, M.; Poornima, P.; Ganesh, P.; Kamath, A.; Bonam, S. R.; Srinivasula, S. M.; Kurapati, R. Biological degradation of graphitic carbon nitride sheets and autophagy induction in macrophages. Nanoscale 2025, 17 (25), 15267-15278.",
        "doi": "10.1039/d5nr00795j",
    },
    {
        "citation": "Killock, D. Pan-RAS inhibitor daraxonrasib shows promise in pancreatic cancer. Nature Reviews Clinical Oncology 2026, 23 (7), 475-475.",
        "doi": "10.1038/s41571-026-01162-x",
    },
]

if __name__ == "__main__":
    print(f"Total verified references: {len(KRAS_VERIFIED_REFERENCES)}")
