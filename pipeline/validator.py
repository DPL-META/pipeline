import subprocess
from pathlib import Path

def validate_yaml(path: Path):
    print(f"🧪 Validando {path.name} com yamllint...")
    try:
        subprocess.run(
            ["yamllint", str(path)],
            check=True,
            capture_output=True
        )
        print(f"✅ {path.name} passou na validação do yamllint.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ {path.name} falhou na validação do yamllint:")
        print(e.stdout.decode())