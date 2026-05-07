# Agent-Based Multimodal Eval Demo

Image-first demo for an agentic evaluation system based on `agent_based_multimodal_eval_system_v2.md`.

```mermaid
flowchart LR
    A1[User Prompt / Task] --> A4
    A2[Model Output<br/>Image now<br/>Text / Audio / Video later] --> A4
    A3[Metadata<br/>model / app / device / latency] --> A4

    subgraph A[1. Input / Eval Case]
        A4[Golden / Regression / Adversarial / Production Sample]
    end

    A4 --> B1

    subgraph B[2. Eval Agent Orchestration]
        B1[Intent Parser<br/>explicit constraints<br/>implicit expectations]
        B2[Rubric Generator<br/>hard constraints<br/>soft scores<br/>thresholds]
        B3[Human Review<br/>approve / edit / version rubric]
        B4[Tool Planner<br/>choose OCR / image / safety tools]
        B5[Execution Orchestrator<br/>run tools + aggregate outputs]
        B1 --> B2 --> B3 --> B4 --> B5
    end

    B5 --> C

    subgraph C[3. Evidence Extraction]
        C1[Text Analyzer<br/>correctness / completeness / format]
        C2[OCR<br/>extract rendered text]
        C3[Image / VLM Analyzer<br/>objects / style / artifacts]
        C4[ASR<br/>audio/video transcript]
        C5[Video Analyzer<br/>duration / frames / consistency]
        C6[Safety Checker<br/>policy / compliance / risk]
        C7[RAG / Retriever<br/>docs / context]
        C8[Search<br/>web / knowledge]
        C9[Structured Evidence<br/>facts the scorer can cite]
        C1 --> C9
        C2 --> C9
        C3 --> C9
        C4 --> C9
        C5 --> C9
        C6 --> C9
        C7 --> C9
        C8 --> C9
    end

    C9 --> D

    subgraph D[4. Judge / Scoring Layer]
        D1[Rule-Based Checks<br/>safety / exact text / format / forbidden objects]
        D2[Evidence-Grounded Judge<br/>alignment / quality / completeness / acceptability]
        D3[Eval Result<br/>pass/fail + score + failure modes + recommendation]
        D1 --> D3
        D2 --> D3
    end

    D3 --> E1

    subgraph E[5. Result Storage & Analysis]
        E1[Report Store<br/>JSON / traces / evidence]
        E2[Dashboard<br/>version comparison / regression / slice analysis]
        E3[Experiment Tracking<br/>model / prompt / agent versions]
    end

    E1 --> F1
    E2 --> F1
    E3 --> F1

    subgraph F[6. Continuous Improvement Loop]
        F1[Human Review / Calibration]
        F2[User Behavior Signals<br/>regenerate / save / edit / report]
        F3[Update Dataset & Rubric<br/>weights / thresholds / tool strategy]
        F1 --> F2 --> F3
    end

    F3 -.-> A4
    F3 -.-> B1
    F3 -.-> D1

    K[Key Idea<br/>Do not let the LLM score by intuition alone.<br/>Extract evidence first, then evaluate with a rubric.] -.-> C9

    style A fill:#eef6ff,stroke:#2563eb
    style B fill:#eef6ff,stroke:#2563eb
    style C fill:#eef6ff,stroke:#2563eb
    style D fill:#ecfdf3,stroke:#16a34a
    style E fill:#eef6ff,stroke:#2563eb
    style F fill:#f4f0ff,stroke:#7c3aed
    style K fill:#fff7ed,stroke:#f59e0b
```

## Demo Paths

```text
User requirements
  -> rubric_generator.py
  -> draft rubric
  -> human edit / approve
  -> eval run
```

```text
DiffusionDB sample
  -> dataset_importer.py
  -> eval case
  -> evidence extraction
  -> score + report
```

```text
Image output
  -> image analyzer + OCR + safety checker
  -> hard checks + soft scores
  -> reports/<case_id>/result.json
```

## Run

```bash
python3 runner.py \
  --case cases/golden/golden_image_001.json \
  --rubric configs/rubrics/image_generation_general_v1.yaml
```

```bash
python3 runner.py \
  --case cases/golden/diffusiondb_geodesic_landscape_001.json \
  --rubric configs/rubrics/generated_diffusiondb_art_v1.yaml
```

```bash
python3 rubric_generator.py \
  --requirements "Evaluate image outputs for prompt alignment, visual coherence, safety, and user acceptability." \
  --rubric-id custom_image_art_v1 \
  --name "Custom Image Art Rubric" \
  --output configs/rubrics/custom_image_art_v1.yaml
```

```bash
python3 dataset_importer.py \
  --dataset diffusiondb \
  --output cases/golden/diffusiondb_geodesic_landscape_001.json
```

## Dataset

```text
DiffusionDB
  -> text-to-image prompt/image dataset
  -> https://huggingface.co/datasets/poloclub/diffusiondb
  -> https://poloclub.github.io/diffusiondb/
```

## Test

```bash
python3 -m unittest discover tests
```
