# Reproducibility Guide: Structural Analysis of Human DDX3X

This guide provides instructions to reproduce all data downloads, structural coordinate analyses, and scientific figure exports from source.

## 1. System Requirements and Environment Setup

- **Python Version:** Python 3.10 or higher
- **Operating System:** Windows, macOS, or Linux
- **RAM:** Minimum 2 GB

### Virtual Environment Setup
```bash
# Navigate to project directory
cd BIOLOGY_RESEARCH_PROJECTS/01_DDX3X_Structural_Analysis

# Create an isolated virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

---

## 2. Step-by-Step Execution

### Option A: Complete Pipeline via Orchestrator
Execute the entire workflow with a single command from the project root:
```bash
python main.py
```

### Option B: Modular Execution

1. **Retrieve Biological Sequences and Structural Coordinates:**
   ```bash
   python scripts/01_retrieve_data.py
   ```
   - Connects to UniProt and downloads `DDX3X_human_O00571.fasta` and annotations.
   - Connects to AlphaFold EBI API and downloads `AF-O00571-F1-model_v6.pdb`.
   - Connects to RCSB PDB and downloads experimental crystal structures `2I4I.pdb` and `5E7I.pdb`.

2. **Extract Coordinates and Parse Functional Motifs:**
   ```bash
   python scripts/02_analyze_structure.py
   ```
   - Extracts Cα atoms and pLDDT values.
   - Computes structural coverage and domain boundaries.
   - Generates `data/processed/ddx3x_structural_summary.json`.

3. **Generate High-Resolution Publication Figures:**
   ```bash
   python scripts/03_generate_figures.py
   ```
   - Renders 5 scientific figures at 300 DPI inside `figures/`.

---

## 3. Molecular Graphics Visualization via PyMOL (Optional)

If PyMOL is installed on your workstation:
```bash
cd scripts
pymol render_pymol_figures.pml
```
This script loads the coordinate files, applies standard cartoon representations, sets background and clipping planes, and exports ray-traced structural renders.

---

## 4. Verification Checklist

To confirm successful reproduction, verify the presence of:
- `data/DDX3X_human_O00571.fasta` (773 bytes)
- `data/AF-O00571-F1-model_v6.pdb` (425,735 bytes)
- `data/2I4I.pdb` (328,212 bytes)
- `data/5E7I.pdb` (868,077 bytes)
- `figures/fig1_ddx3x_overall_3d_structure.png`
- `figures/fig2_ddx3x_structural_domains_3d.png`
- `figures/fig3_ddx3x_functional_catalytic_motifs.png`
- `figures/fig4_ddx3x_comparison_alphafold_vs_experimental.png`
- `figures/fig5_ddx3x_domain_architecture_and_plddt.png`
