from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DIFFUSIONDB_DATASET_URL = "https://huggingface.co/datasets/poloclub/diffusiondb"
DIFFUSIONDB_PROJECT_URL = "https://poloclub.github.io/diffusiondb/"


def build_diffusiondb_card_sample_case() -> dict[str, Any]:
    prompt = "geodesic landscape, john chamberlain, christopher balaskas, tadao ando, 4 k, "
    image_name = "f3501e05-aef7-4225-a9e9-f516527408ac.png"
    return {
        "case_id": "diffusiondb_geodesic_landscape_001",
        "prompt": prompt,
        "output_modality": "image",
        "linked_rubric_id": "generated_diffusiondb_art_v1",
        "output": {
            "type": "dataset_image",
            "asset_path": "hf://poloclub/diffusiondb/images/part-000001/f3501e05-aef7-4225-a9e9-f516527408ac.png",
            "dataset_annotations": {
                "dataset": "poloclub/diffusiondb",
                "dataset_url": DIFFUSIONDB_DATASET_URL,
                "project_url": DIFFUSIONDB_PROJECT_URL,
                "image_name": image_name,
                "part_id": "part-000001",
                "prompt": prompt,
                "seed": 38753269,
                "cfg": 12.0,
                "steps": 50,
                "sampler": "k_lms",
            },
            "mock_evidence": {
                "caption": "A stylized geodesic landscape with abstract sculptural forms and architectural composition.",
                "objects": ["landscape", "abstract forms", "architectural structure"],
                "style": "geodesic architectural digital art",
                "artifacts": [],
                "composition_quality": "good",
                "prompt_alignment_signals": [
                    "geodesic landscape",
                    "abstract sculptural forms",
                    "architectural influence",
                    "high-resolution digital art",
                ],
                "ocr_text": "",
                "ocr_confidence": 0.0,
                "text_legibility": "not_applicable",
                "safety_flags": [],
                "risk_level": "low",
            },
        },
        "metadata": {
            "source": "DiffusionDB Hugging Face dataset card sample",
            "dataset": "poloclub/diffusiondb",
            "dataset_url": DIFFUSIONDB_DATASET_URL,
            "project_url": DIFFUSIONDB_PROJECT_URL,
            "model_version": "Stable Diffusion",
            "prompt_version": "diffusiondb-card-sample",
        },
        "eval_spec": {
            "task_type": "image_generation",
            "constraints": {
                "source_dataset": "DiffusionDB",
                "expected_prompt_alignment": [
                    "geodesic landscape",
                    "john chamberlain",
                    "christopher balaskas",
                    "tadao ando",
                    "4k quality",
                ],
            },
        },
    }


def write_diffusiondb_card_sample_case(output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_diffusiondb_card_sample_case(), indent=2), encoding="utf-8")
    return path
