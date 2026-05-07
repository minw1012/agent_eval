from __future__ import annotations

import argparse

from src.rubrics.rubric_generator import (
    generate_rubric_from_requirements,
    generate_rubric_with_openai,
    write_generated_rubric,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a draft rubric from user requirements.")
    parser.add_argument("--requirements", help="Natural-language quality requirements.")
    parser.add_argument("--interactive", action="store_true", help="Prompt for requirements in the terminal.")
    parser.add_argument("--rubric-id", default="custom_image_generation_v1")
    parser.add_argument("--name", default="Custom Image Generation Rubric")
    parser.add_argument("--owner", default="eval-team")
    parser.add_argument("--version", default="0.1")
    parser.add_argument("--output", default="configs/rubrics/custom_image_generation_v1.yaml")
    parser.add_argument("--provider", choices=["template", "openai"], default="template")
    parser.add_argument("--model", help="Model id to use when --provider openai is selected.")
    args = parser.parse_args()

    requirements = args.requirements
    if args.interactive:
        print("Describe the image quality bar, constraints, failure modes, and review thresholds.")
        requirements = input("Requirements: ").strip()
    if not requirements:
        raise SystemExit("Provide --requirements or use --interactive.")

    if args.provider == "openai":
        if not args.model:
            raise SystemExit("--model is required with --provider openai.")
        rubric = generate_rubric_with_openai(
            requirements=requirements,
            rubric_id=args.rubric_id,
            name=args.name,
            owner=args.owner,
            version=args.version,
            model=args.model,
        )
    else:
        rubric = generate_rubric_from_requirements(
            requirements=requirements,
            rubric_id=args.rubric_id,
            name=args.name,
            owner=args.owner,
            version=args.version,
        )

    path = write_generated_rubric(rubric, args.output)
    print(f"Draft rubric saved to {path}")
    print("Review/edit the rubric before using it for reproducible eval runs.")


if __name__ == "__main__":
    main()
