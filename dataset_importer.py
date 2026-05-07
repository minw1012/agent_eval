from __future__ import annotations

import argparse

from src.datasets.diffusiondb_importer import write_diffusiondb_card_sample_case


def main() -> None:
    parser = argparse.ArgumentParser(description="Import public dataset examples as eval cases.")
    parser.add_argument("--dataset", choices=["diffusiondb"], default="diffusiondb")
    parser.add_argument(
        "--output",
        default="cases/golden/diffusiondb_geodesic_landscape_001.json",
        help="Where to write the generated eval case JSON.",
    )
    args = parser.parse_args()

    if args.dataset == "diffusiondb":
        path = write_diffusiondb_card_sample_case(args.output)
        print(f"Imported DiffusionDB sample eval case to {path}")


if __name__ == "__main__":
    main()
