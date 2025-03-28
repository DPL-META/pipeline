import argparse

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