# Methodology: Structural Analysis of Human DDX3X Protein

## 1. Sequence and Structure Retrieval Protocol

### 1.1 Target Accession Verification
The canonical sequence of human DEAD-box helicase 3 X-linked was verified in UniProtKB under accession number `O00571`.
- Organism: *Homo sapiens* (Human)
- Gene symbol: *DDX3X*
- Polypeptide length: 662 amino acids
- Molecular mass: 73,243 Da

Primary sequence and functional feature annotations were acquired directly via the UniProt REST API:
- FASTA URL: `https://rest.uniprot.org/uniprotkb/O00571.fasta`
- JSON Metadata URL: `https://rest.uniprot.org/uniprotkb/O00571.json`

### 1.2 Coordinate Datasets Retrieval
Two independent structural modalities were acquired:
1. **Predicted Full-Length Monomer:** 
   Retrieved from the AlphaFold Protein Structure Database (Model ID: `AF-O00571-F1-model_v6`). The model covers residues 1 to 662.
2. **Experimental X-ray Crystallography Coordinates:**
   Retrieved from the RCSB Protein Data Bank (RCSB PDB):
   - **PDB ID: 2I4I** – Apo conformation of the human DDX3X catalytic helicase core (residues 132–607) resolved at 2.20 Å resolution (Högbom et al., 2007).
   - **PDB ID: 5E7I** – Closed ternary complex of human DDX3X (residues 168–582) bound to the ATP analogue AMP-PNP, magnesium cofactor, and a 6-mer single-stranded RNA oligonucleotide resolved at 2.80 Å resolution (Floor et al., 2016).

---

## 2. Data Processing and Quality Metric Extraction

The structural files in standard PDB format were parsed using custom Python routines:
1. **Backbone Cα Coordinates:** Extracted for all standard amino acid residues (`ATOM` records with atom name `CA`).
2. **AlphaFold Confidence Scoring (pLDDT):** AlphaFold stores the per-residue predicted Local Distance Difference Test (pLDDT) score in the B-factor column of the PDB coordinate file. The pLDDT scale ranges from 0 to 100:
   - pLDDT > 90: Very high confidence (reliable sidechain and backbone conformation).
   - 70 < pLDDT ≤ 90: Confident (reliable backbone fold).
   - 50 < pLDDT ≤ 70: Low confidence.
   - pLDDT < 50: Very low confidence (highly indicative of intrinsic disorder).
3. **Domain Boundary Assignment:** Established using UniProt sequence feature tables and consensus structural literature:
   - N-terminal extension: Residues 1–167
   - RecA-like Domain 1: Residues 168–403
   - Inter-domain Linker: Residues 404–417
   - RecA-like Domain 2: Residues 418–607
   - C-terminal extension: Residues 608–662

---

## 3. Structural Alignment and Superposition Algorithm

To quantitatively compare the AlphaFold predicted coordinates with experimental crystal structures without introducing software dependencies, the Kabsch algorithm was implemented:
1. **Coordinate Subsetting:** Only common, structurally resolved Cα atoms present in both the experimental PDB (Chain A) and AlphaFold model were matched by residue index ($N = 405$ shared residues for PDB 2I4I).
2. **Translation to Centroid:** Both coordinate sets $P$ (AlphaFold) and $Q$ (experimental) were translated such that their geometric centroids coincided at $(0, 0, 0)$.
3. **Rotation Matrix Optimization:** The $3 \times 3$ cross-covariance matrix $H$ was calculated:
   $$H = Q^T P$$
   Singular Value Decomposition (SVD) was performed on $H$:
   $$H = U S V^T$$
   The optimal rotation matrix $R$ was determined:
   $$R = V \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & \det(V U^T) \end{pmatrix} U^T$$
4. **RMSD Calculation:** The experimental coordinates were rotated, and the root-mean-square deviation across all shared Cα pairs was computed:
   $$\text{RMSD} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} \| P_i - (R Q_i) \|^2}$$

---

## 4. Visualisation and Scientific Figure Generation

Scientific visualizations were rendered using Matplotlib with high-resolution vector and raster export (300 DPI, white background, distinct non-conflicting color palettes). Additionally, a complete PyMOL macro script (`render_pymol_figures.pml`) was prepared to enable standard ray-traced cartoon representations for interactive molecular graphics workstations.
