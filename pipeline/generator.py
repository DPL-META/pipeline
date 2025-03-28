from .constants import BASE_DIR, TEMPLATES_DIR, GITHUB_WORKFLOWS_DIR, CUSTOM_PIPELINE_FILE, DEFAULT_PIPELINE_FILE, AVAILABLE_STEPS
from .templates import load_template, insert_env_variables
from .validator import validate_yaml
from pathlib import Path


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

    # default.yml
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