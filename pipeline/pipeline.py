#!/usr/bin/env python3

import argparse
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
GITHUB_WORKFLOWS_DIR = BASE_DIR.parent / ".github" / "workflows"
PIPELINE_FILE = GITHUB_WORKFLOWS_DIR / "custom.yml"
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
  python pipeline.py --lang python --steps test,deploy
  python pipeline.py --lang python
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--lang",
        required=True,
        choices=["python", "node"],
        help="Linguagem do projeto"
    )
    parser.add_argument(
        "--steps",
        required=False,
        help="Steps desejados separados por vírgula"
    )
    return parser.parse_args()

def load_template(path: Path) -> str:
    if not path.exists():
        print(f"⚠️  Arquivo não encontrado: {path}")
        return ""
    return path.read_text()

def generate_pipeline(lang: str, steps: List[str]):
    print(f"📦 Gerando pipeline para linguagem: {lang}")

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
    for step in steps:
        step_path = TEMPLATES_DIR / lang / f"{step}.yml"
        step_content = load_template(step_path)
        if step_content:
            content += step_content
        else:
            print(f"⚠️  Step '{step}' não encontrado para '{lang}'. Ignorado.")

    PIPELINE_FILE.write_text(content)
    print(f"✅ Pipeline gerado em: {PIPELINE_FILE}")

def main():
    args = parse_args()
    steps = [step.strip() for step in args.steps.split(",")] if args.steps else []
    generate_pipeline(args.lang, steps)

if __name__ == "__main__":
    main()
