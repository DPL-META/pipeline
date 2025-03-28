#!/usr/bin/env python3

import argparse
from pathlib import Path
import subprocess

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
GITHUB_WORKFLOWS_DIR = BASE_DIR.parent / ".github" / "workflows"
CUSTOM_PIPELINE_FILE = GITHUB_WORKFLOWS_DIR / "custom.yml"
DEFAULT_PIPELINE_FILE = GITHUB_WORKFLOWS_DIR / "default.yml"

AVAILABLE_STEPS = {
    "python": ["build", "test", "deploy"],
    "node": ["build", "test", "deploy"]
}

def parse_args():
    parser = argparse.ArgumentParser(
        description="Gera pipeline GitHub Actions baseado na linguagem e steps selecionados.",
        epilog="""Steps disponíveis por linguagem:
  python: build, test, deploy
  node:   build, test, deploy

Exemplos de uso:
  python pipeline.py --lang python --project products --steps test,deploy
  python pipeline.py --lang node --project users
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--lang", required=True, choices=["python", "node"], help="Linguagem do projeto")
    parser.add_argument("--project", required=True, help="Nome do diretório do projeto em 'projects/'")
    parser.add_argument("--steps", required=False, help="Steps desejados separados por vírgula")
    return parser.parse_args()

def load_template(path: Path) -> str:
    if not path.exists():
        print(f"⚠️  Arquivo não encontrado: {path}")
        return ""
    return path.read_text(encoding="utf-8")

def insert_env_variables(content: str, project: str) -> str:
    if "env:" in content:
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if line.strip() == "env:":
                lines.insert(i + 1, f"  PROJECT_NAME: {project}")
                lines.insert(i + 2, "  IMAGE_NAME: >")
                lines.insert(i + 3, f"    ghcr.io/${{{{ github.repository_owner }}}}/")
                lines.insert(i + 4, f"    {project}-app:${{{{ github.sha }}}}")
                break
        return "\n".join(lines)
    else:
        return (
            f"env:\n"
            f"  PROJECT_NAME: {project}\n"
            f"  IMAGE_NAME: >\n"
            f"    ghcr.io/${{{{ github.repository_owner }}}}/\n"
            f"    {project}-app:${{{{ github.sha }}}}\n" + content
        )

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

def generate_pipeline(lang: str, project: str, steps: list[str]):
    print(f"📦 Gerando pipeline para linguagem: {lang}, projeto: {project}")

    project_path = BASE_DIR.parent / "projects" / project
    if not project_path.exists():
        raise FileNotFoundError(f"❌ Projeto '{project}' não encontrado em 'projects/'")

    if not steps:
        print("ℹ️ Nenhum step informado. Usando configuração padrão: build,test")
        steps = ["build", "test"]

    if "build" not in steps:
        print("🔒 Step obrigatório 'build' não foi incluído. Adicionando automaticamente.")
        steps.insert(0, "build")
    else:
        steps = ["build"] + [s for s in steps if s != "build"]

    print(f"⚙️ Steps finais aplicados: {steps}")
    GITHUB_WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)

    # custom.yml
    content = load_template(TEMPLATES_DIR / "base.yml")
    content = insert_env_variables(content, project)
    if not content.endswith("\n"):
        content += "\n"

    for step in steps:
        step_path = TEMPLATES_DIR / lang / f"{step}.yml"
        step_content = load_template(step_path)
        if step_content:
            content += "\n" + step_content
        else:
            print(f"⚠️  Step '{step}' não encontrado para '{lang}'. Ignorado.")

    CUSTOM_PIPELINE_FILE.write_text(content.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    print(f"✅ custom.yml gerado em: {CUSTOM_PIPELINE_FILE}")
    validate_yaml(CUSTOM_PIPELINE_FILE)

    # default.yml (com todos os steps)
    full_content = load_template(TEMPLATES_DIR / "base.yml")
    full_content = insert_env_variables(full_content, project)

    full_lines = full_content.splitlines()
    full_lines = [line for line in full_lines if "branches-ignore" not in line]

    clean_lines = []
    in_on_block = False
    for line in full_lines:
        if line.strip() == "on:":
            clean_lines.append(line)
            in_on_block = True
            continue
        if in_on_block:
            if line.startswith("  "):
                continue
            else:
                in_on_block = False
        clean_lines.append(line)

    for i, line in enumerate(clean_lines):
        if line.strip() == "on:":
            clean_lines.insert(i + 1, "  pull_request:")
            clean_lines.insert(i + 2, "    branches:")
            clean_lines.insert(i + 3, "      - main")
            clean_lines.insert(i + 4, "      - develop")
            clean_lines.insert(i + 5, "      - release/**")
            break

    full_content = "\n".join(clean_lines)
    if not full_content.endswith("\n"):
        full_content += "\n"

    for step in AVAILABLE_STEPS[lang]:
        step_path = TEMPLATES_DIR / lang / f"{step}.yml"
        step_content = load_template(step_path)
        if step_content:
            full_content += "\n" + step_content
        else:
            print(f"⚠️  Step '{step}' não encontrado para '{lang}'. Ignorado.")

    DEFAULT_PIPELINE_FILE.write_text(full_content.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    print(f"✅ default.yml gerado em: {DEFAULT_PIPELINE_FILE}")
    validate_yaml(DEFAULT_PIPELINE_FILE)

def main():
    args = parse_args()
    steps = [s.strip() for s in args.steps.split(",")] if args.steps else []
    generate_pipeline(args.lang, args.project, steps)

if __name__ == "__main__":
    main()
