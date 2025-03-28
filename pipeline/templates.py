from pathlib import Path


def load_template(path: Path) -> str:
    if not path.exists():
        print(f"⚠️  Arquivo não encontrado: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def insert_env_variables(content: str, project: str) -> str:
    image_lines = [
        "  IMAGE_NAME: >",
        f"    ghcr.io/${{{{ github.repository_owner }}}}/{project}-app:${{{{ github.sha }}}}"
    ]

    if "env:" in content:
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if line.strip() == "env:":
                lines.insert(i + 1, f"  PROJECT_NAME: {project}")
                lines[i + 2:i + 2] = image_lines
                break
        return "\n".join(lines)
    else:
        return (
            "env:\n"
            f"  PROJECT_NAME: {project}\n"
            + "\n".join(image_lines) + "\n"
            + content
        )