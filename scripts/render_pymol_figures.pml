# PyMOL Script for DDX3X Visualisation
# Generates high-resolution figures for structural analysis

reinitialize

# Figure 1: Full-length AlphaFold model colored by pLDDT confidence
load ../data/AF-O00571-F1-model_v6.pdb, af_ddx3x
hide everything, all
show cartoon, af_ddx3x
bg_color white
set ray_shadows, 0
set antialias, 2

# AlphaFold standard color scheme by b-factor (pLDDT)
color 0x0053D6, af_ddx3x and b > 90
color 0x65CBF3, af_ddx3x and b > 70 and b <= 90
color 0xFFDB13, af_ddx3x and b > 50 and b <= 70
color 0xFF7D45, af_ddx3x and b <= 50

orient af_ddx3x
zoom af_ddx3x, 2
png ../figures/fig1_ddx3x_overall_3d_alphafold.png, width=2400, height=1800, dpi=300, ray=1

# Figure 2: Domain architecture on 3D structure
color 0x94A3B8, af_ddx3x and resi 1-167
color 0x0284C7, af_ddx3x and resi 168-403
color 0xF59E0B, af_ddx3x and resi 404-417
color 0x10B981, af_ddx3x and resi 418-607
color 0xCBD5E1, af_ddx3x and resi 608-662

png ../figures/fig2_ddx3x_structural_domains.png, width=2400, height=1800, dpi=300, ray=1

# Figure 3: Conserved catalytic motifs and functional regions
select motif_I, af_ddx3x and resi 226-234
select motif_II, af_ddx3x and resi 344-348
select motif_III, af_ddx3x and resi 376-378
select motif_V, af_ddx3x and resi 535-543
select motif_VI, af_ddx3x and resi 566-571

show sticks, motif_I or motif_II or motif_III or motif_V or motif_VI
color 0xDC2626, motif_I
color 0x9333EA, motif_II
color 0xEA580C, motif_III
color 0x059669, motif_V
color 0x2563EB, motif_VI

zoom motif_II, 12
png ../figures/fig3_ddx3x_functional_catalytic_motifs.png, width=2400, height=1800, dpi=300, ray=1

# Figure 4: Alignment of AlphaFold model with experimental crystal structure 2I4I
load ../data/2I4I.pdb, crystal_2i4i
hide everything, crystal_2i4i
show cartoon, crystal_2i4i and chain A
color 0xE11D48, crystal_2i4i and chain A
color 0x0284C7, af_ddx3x and resi 168-607
align crystal_2i4i and chain A, af_ddx3x and resi 168-607

orient crystal_2i4i and chain A
zoom crystal_2i4i and chain A, 4
png ../figures/fig4_ddx3x_alphafold_vs_experimental_2i4i.png, width=2400, height=1800, dpi=300, ray=1
