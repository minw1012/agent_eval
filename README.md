# Agent-Based Multimodal Eval Demo

This repo is a small, runnable demo of an agent-based evaluation system for multimodal model outputs. It starts with image generation, but the architecture is designed to extend to text, audio, and video.

<img src="docs/assets/schema.png" alt="Agent-based multimodal evaluation system architecture" width="100%">

## Why This Exists

Most simple eval demos ask an LLM judge a broad question like:

```text
Is this output good?
```

That is hard to trust because the judge may score from intuition. This demo uses a more inspectable flow:

```text
Prompt + model output
  -> parse user intent
  -> load or generate a rubric
  -> choose evidence tools
  -> extract structured evidence
  -> run deterministic hard checks
  -> score soft quality dimensions
  -> write a traceable report
```

The important idea is: **rubrics are explicit configuration, and judges score from evidence.**

## What Works Now

```text
Rubric authoring
  natural-language requirements
  -> draft rubric config
  -> human review/edit
```

```text
Image eval execution
  eval case
  -> intent parser
  -> tool planner
  -> mock image analyzer / OCR / safety checker
  -> hard checks + weighted soft scores
  -> JSON report
```

```text
Public dataset path
  DiffusionDB sample
  -> eval case JSON
  -> same eval runner
  -> report JSON
```

This is still a demo: OCR, image analysis, and safety checks are mocked behind stable interfaces. The point is to make the full agentic eval loop work before replacing mocks with real tools.

## Quick Start

Run the built-in image case:

```bash
python3 runner.py \
  --case cases/golden/golden_image_001.json \
  --rubric configs/rubrics/image_generation_general_v1.yaml
```

Run a public DiffusionDB sample:

```bash
python3 runner.py \
  --case cases/golden/diffusiondb_geodesic_landscape_001.json \
  --rubric configs/rubrics/generated_diffusiondb_art_v1.yaml
```

Example output:

```text
Case: golden_image_001
Pass: true
Overall score: 4.95
Recommendation: Accept
Report saved to reports/golden_image_001/result.json
```

## Generate A Rubric

Create a draft rubric from user requirements:

```bash
python3 rubric_generator.py \
  --requirements "Evaluate image outputs for prompt alignment, visual coherence, safety, and user acceptability." \
  --rubric-id custom_image_art_v1 \
  --name "Custom Image Art Rubric" \
  --output configs/rubrics/custom_image_art_v1.yaml
```

The generated rubric is intentionally marked as a draft. A human should review/edit it before using it as a reproducible evaluation standard.

## Import Dataset Sample

Generate the included DiffusionDB eval case:

```bash
python3 dataset_importer.py \
  --dataset diffusiondb \
  --output cases/golden/diffusiondb_geodesic_landscape_001.json
```

DiffusionDB is a public text-to-image prompt/image dataset:

```text
https://huggingface.co/datasets/poloclub/diffusiondb
https://poloclub.github.io/diffusiondb/
```

## Report Shape

Each run writes a JSON report with:

```text
pass/fail
overall score
recommendation
hard constraint results
soft scores
failure modes
structured evidence
tool versions
rubric version
metadata
```

## Test

```bash
python3 -m unittest discover tests
```
