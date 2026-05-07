from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.agents.eval_executor_agent import run_eval
from src.datasets.case_loader import load_case
from src.datasets.diffusiondb_importer import build_diffusiondb_card_sample_case, write_diffusiondb_card_sample_case
from src.rubrics.rubric_generator import generate_rubric_from_requirements, write_generated_rubric
from src.rubrics.rubric_loader import load_rubric


ROOT = Path(__file__).resolve().parents[1]
DIFFUSIONDB_CASE = ROOT / "cases" / "golden" / "diffusiondb_geodesic_landscape_001.json"
DIFFUSIONDB_RUBRIC = ROOT / "configs" / "rubrics" / "generated_diffusiondb_art_v1.yaml"


class AuthoringAndDatasetTests(unittest.TestCase):
    def test_template_rubric_generator_includes_text_checks_when_requested(self) -> None:
        rubric = generate_rubric_from_requirements(
            requirements='Images must include exact readable sale text and avoid logos.',
            rubric_id="test_text_image_v1",
            name="Test Text Image Rubric",
        )

        hard_ids = {item["id"] for item in rubric["hard_constraints"]}
        soft_ids = {item["id"] for item in rubric["soft_scores"]}
        self.assertIn("required_text_exact", hard_ids)
        self.assertIn("negative_visual_constraints", hard_ids)
        self.assertIn("text_rendering", soft_ids)

    def test_template_rubric_generator_writes_valid_rubric(self) -> None:
        rubric = generate_rubric_from_requirements(
            requirements="Evaluate DiffusionDB art images for prompt alignment, visual quality, and safety.",
            rubric_id="test_diffusiondb_art_v1",
            name="Test DiffusionDB Art Rubric",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "rubric.yaml"
            write_generated_rubric(rubric, output_path)
            loaded = load_rubric(output_path)
            self.assertEqual(loaded.rubric_id, "test_diffusiondb_art_v1")

    def test_diffusiondb_importer_builds_real_dataset_case_metadata(self) -> None:
        case = build_diffusiondb_card_sample_case()
        self.assertEqual(case["metadata"]["dataset"], "poloclub/diffusiondb")
        self.assertIn("huggingface.co/datasets/poloclub/diffusiondb", case["metadata"]["dataset_url"])
        self.assertEqual(case["output"]["dataset_annotations"]["seed"], 38753269)

    def test_diffusiondb_importer_writes_case_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "diffusiondb_case.json"
            write_diffusiondb_card_sample_case(output_path)
            eval_case = load_case(output_path)
            self.assertEqual(eval_case.case_id, "diffusiondb_geodesic_landscape_001")

    def test_diffusiondb_case_runs_with_generated_rubric(self) -> None:
        eval_case = load_case(DIFFUSIONDB_CASE)
        rubric = load_rubric(DIFFUSIONDB_RUBRIC)
        report = run_eval(eval_case, rubric)

        self.assertTrue(report.passed)
        self.assertEqual(report.recommendation, "Accept")
        self.assertIn("dataset_annotations", report.evidence["image_analyzer"])


if __name__ == "__main__":
    unittest.main()
