import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
scripts_dir = project_root / "scripts"

subprocess.run([sys.executable, str(scripts_dir / "01_retrieve_data.py")], check=True)
subprocess.run([sys.executable, str(scripts_dir / "02_analyze_structure.py")], check=True)
subprocess.run([sys.executable, str(scripts_dir / "03_generate_figures.py")], check=True)
