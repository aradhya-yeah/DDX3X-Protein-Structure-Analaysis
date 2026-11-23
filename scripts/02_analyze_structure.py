from pathlib import Path
import json

project_root = Path(__file__).resolve().parent.parent
data_dir = project_root / "data"
processed_dir = data_dir / "processed"
processed_dir.mkdir(exist_ok=True)

fasta_path = data_dir / "DDX3X_human_O00571.fasta"
with open(fasta_path, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]
    header = lines[0]
    sequence = "".join(lines[1:])

seq_info = {
    "header": header,
    "accession": "O00571",
    "gene": "DDX3X",
    "organism": "Homo sapiens",
    "length": len(sequence),
    "sequence": sequence
}

af_pdb = data_dir / "AF-O00571-F1-model_v6.pdb"
af_residues = {}
with open(af_pdb, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            res_num = int(line[22:26].strip())
            res_name = line[17:20].strip()
            b_factor = float(line[60:66].strip())
            af_residues[res_num] = {
                "residue_name": res_name,
                "plddt": b_factor
            }

pdb_2i4i = data_dir / "2I4I.pdb"
pdb_2i4i_residues = []
with open(pdb_2i4i, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("ATOM") and line[12:16].strip() == "CA" and line[21] == "A":
            pdb_2i4i_residues.append(int(line[22:26].strip()))

pdb_5e7i = data_dir / "5E7I.pdb"
pdb_5e7i_residues = []
with open(pdb_5e7i, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("ATOM") and line[12:16].strip() == "CA" and line[21] == "A":
            pdb_5e7i_residues.append(int(line[22:26].strip()))

structural_coverage = {
    "uniprot_length": len(sequence),
    "alphafold_residues_modeled": len(af_residues),
    "alphafold_mean_plddt": sum(r["plddt"] for r in af_residues.values()) / len(af_residues),
    "pdb_2i4i_chain_A_count": len(pdb_2i4i_residues),
    "pdb_2i4i_chain_A_range": [min(pdb_2i4i_residues), max(pdb_2i4i_residues)] if pdb_2i4i_residues else [],
    "pdb_5e7i_chain_A_count": len(pdb_5e7i_residues),
    "pdb_5e7i_chain_A_range": [min(pdb_5e7i_residues), max(pdb_5e7i_residues)] if pdb_5e7i_residues else []
}

domains = [
    {"name": "N-terminal extension", "start": 1, "end": 167, "type": "disordered/regulatory"},
    {"name": "RecA-like Domain 1", "start": 168, "end": 403, "type": "core_catalytic"},
    {"name": "Inter-domain Linker", "start": 404, "end": 417, "type": "flexible_hinge"},
    {"name": "RecA-like Domain 2", "start": 418, "end": 607, "type": "core_catalytic"},
    {"name": "C-terminal extension", "start": 608, "end": 662, "type": "disordered/regulatory"}
]

motifs = [
    {"name": "Q-motif", "start": 178, "end": 194, "sequence": "GGFKSPTVYGFNTGSKG", "function": "Adenine base recognition and ATP binding specificity"},
    {"name": "Motif I (Walker A)", "start": 226, "end": 234, "sequence": "AQTGSGKT", "function": "ATP phosphate binding loop (P-loop)"},
    {"name": "Motif Ia", "start": 257, "end": 265, "sequence": "PTRELALQI", "function": "RNA oligonucleotide binding"},
    {"name": "Motif Ib", "start": 286, "end": 293, "sequence": "TDLLARGV", "function": "RNA oligonucleotide binding"},
    {"name": "Motif II (Walker B / DEAD-box)", "start": 344, "end": 348, "sequence": "DEAD", "function": "Mg2+ cofactor coordination and ATP hydrolysis catalysis"},
    {"name": "Motif III", "start": 376, "end": 378, "sequence": "SAT", "function": "Coupling of ATP hydrolysis with RNA unwinding"},
    {"name": "Motif IV", "start": 472, "end": 475, "sequence": "LVFL", "function": "RNA binding interface on RecA-like domain 2"},
    {"name": "Motif V", "start": 535, "end": 543, "sequence": "TDVAARGID", "function": "Coordination between RNA substrate and nucleotide binding sites"},
    {"name": "Motif VI", "start": 566, "end": 571, "sequence": "HRIGRT", "function": "ATP binding cleft closure and RNA interaction"}
]

output_data = {
    "sequence_metadata": seq_info,
    "structural_coverage": structural_coverage,
    "domains": domains,
    "motifs": motifs,
    "per_residue_af": af_residues
}

with open(processed_dir / "ddx3x_structural_summary.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2)
