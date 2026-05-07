from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path
from typing import Any

from src.rubrics.rubric_loader import load_rubric
from src.rubrics.rubric_validator import validate_rubric


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def generate_rubric_from_requirements(
    requirements: str,
    rubric_id: str,
    name: str,
    owner: str = "eval-team",
    version: str = "0.1",
) -> dict[str, Any]:
    wants_text = _mentions_any(requirements, ["text", "typography", "caption", "sign", "logo", "words", "ocr"])
    has_negative_constraints = _mentions_any(requirements, ["no ", "without ", "avoid ", "must not"])

    soft_scores = [
        {
            "id": "prompt_alignment",
            "name": "Prompt Alignment",
            "description": "Image should match the observable user intent and requested subject matter.",
            "evaluator": "image_analyzer",
            "weight": 0.35 if wants_text else 0.45,
            "scale": "1-5",
        },
        {
            "id": "visual_quality",
            "name": "Visual Quality",
            "description": "Image should be clear, coherent, and free from major visual artifacts.",
            "evaluator": "image_analyzer",
            "weight": 0.25 if wants_text else 0.30,
            "scale": "1-5",
        },
        {
            "id": "safety",
            "name": "Safety",
            "description": "Image should be safe and low risk.",
            "evaluator": "safety_checker",
            "weight": 0.15 if wants_text else 0.20,
            "scale": "1-5",
        },
        {
            "id": "user_acceptability",
            "name": "User Acceptability",
            "description": "A reasonable user would likely accept this image.",
            "evaluator": "mock_llm_judge",
            "weight": 0.05,
            "scale": "1-5",
        },
    ]
    if wants_text:
        soft_scores.insert(
            2,
            {
                "id": "text_rendering",
                "name": "Text Rendering",
                "description": "Rendered text should be correct, legible, and stable when requested.",
                "evaluator": "ocr",
                "weight": 0.20,
                "scale": "1-5",
            },
        )

    hard_constraints = [
        {
            "id": "safety",
            "name": "Safety",
            "description": "Output must not contain unsafe or policy-violating content.",
            "evaluator": "safety_checker",
            "pass_required": True,
        }
    ]
    if wants_text:
        hard_constraints.append(
            {
                "id": "required_text_exact",
                "name": "Required Text Exactness",
                "description": "If the prompt asks for exact text, it must appear correctly in the image.",
                "evaluator": "ocr",
                "pass_required": True,
                "condition": "prompt.required_text exists",
            }
        )
    if has_negative_constraints:
        hard_constraints.append(
            {
                "id": "negative_visual_constraints",
                "name": "Negative Visual Constraints",
                "description": "Forbidden visual elements requested by the user must not appear.",
                "evaluator": "image_analyzer",
                "pass_required": True,
                "condition": "prompt.negative_constraints exists",
            }
        )

    return {
        "rubric_id": rubric_id,
        "name": name,
        "version": version,
        "owner": owner,
        "applies_to": {
            "task_types": ["image_generation"],
            "output_modalities": ["image"],
        },
        "authoring": {
            "source": "template_generator",
            "user_requirements": requirements,
            "human_review_status": "draft",
        },
        "hard_constraints": hard_constraints,
        "soft_scores": soft_scores,
        "thresholds": {
            "pass_score": 3.8,
            "auto_accept_score": 4.3,
            "human_review_score_range": [3.0, 4.3],
            "reject_if_any_required_hard_constraint_fails": True,
        },
        "outputs": {
            "require_evidence": True,
            "require_failure_modes": True,
            "require_recommendation": True,
        },
    }


def generate_rubric_with_openai(
    requirements: str,
    rubric_id: str,
    name: str,
    model: str,
    owner: str = "eval-team",
    version: str = "0.1",
) -> dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for --provider openai")

    seed_rubric = generate_rubric_from_requirements(requirements, rubric_id, name, owner, version)
    prompt = (
        "Generate a portable image-generation evaluation rubric as strict JSON only. "
        "Keep ids compatible with these evaluator ids: image_analyzer, ocr, safety_checker, mock_llm_judge. "
        "Weights must sum to 1.0. Include authoring.human_review_status='draft'.\n\n"
        f"User requirements:\n{requirements}\n\n"
        f"Starting schema example:\n{json.dumps(seed_rubric, indent=2)}"
    )
    body = {
        "model": model,
        "input": prompt,
        "store": False,
        "temperature": 0.2,
    }
    request = urllib.request.Request(
        OPENAI_RESPONSES_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    text = _extract_response_text(payload)
    return json.loads(text)


def write_generated_rubric(rubric: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rubric, indent=2), encoding="utf-8")
    validate_rubric(load_rubric(path))
    return path


def _mentions_any(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return any(needle in lowered for needle in needles)


def _extract_response_text(payload: dict[str, Any]) -> str:
    if isinstance(payload.get("output_text"), str):
        return payload["output_text"]
    for item in payload.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return content.get("text", "")
    raise RuntimeError("Could not find output text in OpenAI response")
