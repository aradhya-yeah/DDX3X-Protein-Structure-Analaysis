from pathlib import Path
import urllib.request
import json
import gzip
import shutil

project_root = Path(__file__).resolve().parent.parent
data_dir = project_root / "data"
data_dir.mkdir(exist_ok=True)

uniprot_accession = "O00571"
uniprot_fasta_url = f"https://rest.uniprot.org/uniprotkb/{uniprot_accession}.fasta"
uniprot_json_url = f"https://rest.uniprot.org/uniprotkb/{uniprot_accession}.json"

fasta_path = data_dir / "DDX3X_human_O00571.fasta"
annotation_path = data_dir / "DDX3X_human_O00571_uniprot.json"

request_headers = {"User-Agent": "ComputationalBiology-UndergradResearch/1.0"}

if not fasta_path.exists():
    req = urllib.request.Request(uniprot_fasta_url, headers=request_headers)
    with urllib.request.urlopen(req, timeout=30) as response, open(fasta_path, "wb") as out_file:
        shutil.copyfileobj(response, out_file)

if not annotation_path.exists():
    req = urllib.request.Request(uniprot_json_url, headers=request_headers)
    with urllib.request.urlopen(req, timeout=30) as response, open(annotation_path, "wb") as out_file:
        shutil.copyfileobj(response, out_file)

af_api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_accession}"
req = urllib.request.Request(af_api_url, headers=request_headers)
with urllib.request.urlopen(req, timeout=30) as response:
    af_meta = json.loads(response.read().decode())
    pdb_url = af_meta[0]["pdbUrl"]

af_pdb_path = data_dir / "AF-O00571-F1-model_v6.pdb"
if not af_pdb_path.exists():
    req = urllib.request.Request(pdb_url, headers=request_headers)
    with urllib.request.urlopen(req, timeout=60) as response, open(af_pdb_path, "wb") as out_file:
        shutil.copyfileobj(response, out_file)

pdb_ids = ["2I4I", "5E7I"]
for pdb_id in pdb_ids:
    target_path = data_dir / f"{pdb_id}.pdb"
    if not target_path.exists():
        rcsb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        req = urllib.request.Request(rcsb_url, headers=request_headers)
        with urllib.request.urlopen(req, timeout=60) as response, open(target_path, "wb") as out_file:
            shutil.copyfileobj(response, out_file)
