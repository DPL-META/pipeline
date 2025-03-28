from .args import parse_args
from .generator import generate_pipeline

def main():
    args = parse_args()
    steps = [s.strip() for s in args.steps.split(",")] if args.steps else []
    generate_pipeline(args.lang, args.project, steps)

if __name__ == "__main__":
    main()