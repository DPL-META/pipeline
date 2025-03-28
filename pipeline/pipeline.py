#!/usr/bin/env python3

import argparse
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
GITHUB_WORKFLOWS_DIR = BASE_DIR.parent / ".github" / "workflows"
CUSTOM_PIPELINE_FILE = GITHUB_WORKFLOWS_DIR / "custom.yml"

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
    return path.read_text()

def insert_project_name_env_block(content: str, project: str) -> str:
    if "env:" in content:
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if line.strip() == "env:":
                lines.insert(i + 1, f"  PROJECT_NAME: {project}")
                break
        return "\n".join(lines)
    else:
        return f"env:\n  PROJECT_NAME: {project}\n" + content

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

    content = load_template(TEMPLATES_DIR / "base.yml")
    content = insert_project_name_env_block(content, project)

    for step in steps:
        step_path = TEMPLATES_DIR / lang / f"{step}.yml"
        step_content = load_template(step_path)
        if step_content:
            content += step_content
        else:
            print(f"⚠️  Step '{step}' não encontrado para '{lang}'. Ignorado.")

    CUSTOM_PIPELINE_FILE.write_text(content)
    print(f"✅ Pipeline gerado em: {CUSTOM_PIPELINE_FILE}")

def main():
    args = parse_args()
    steps = [s.strip() for s in args.steps.split(",")] if args.steps else []
    generate_pipeline(args.lang, args.project, steps)

if __name__ == "__main__":
    main()