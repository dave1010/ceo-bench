# CEO Bench

**CEO Bench** is an open evaluation suite benchmarking LLMs on leadership and management tasks. Compare large and small models on strategy, people management, communication and ethics.

## 🏆 Benchmark & Leaderboard

- **Prompt Dimensions**: Strategy, People, Communications, Risk & Ethics
- **Metrics**: Weighted rubric scores
- **Run an Eval**: triggers question generation → response generation → automated grading → leaderboard update

## 🚀 Landing Page

A Next.js front-end displays the leaderboard and explains the project.

### Setup & Run Frontend

```bash
npm install
npm run dev
```

### Deploy

Deployed on Vercel; push to `main` to update.

## Project Structure

The front end is a **Next.js** application. Python scripts power question
generation, answer generation and grading using the `llm` CLI.  Key files:

- `generate_questions.py` uses `templates/question_gen_prompt.txt` to create
  YAML question files.
- `aggregate_results.py` compiles scoring data into the leaderboard.

Important directories:

- `templates/` – prompt templates and rubrics
- `scripts/` – Python scripts for generation, evaluation and grading
  - `generate_answers.py` calls `llm` to produce an answer for a question
  - `grade_answers.py` grades an answer with `llm` using a JSON schema so
    results include parsed scores
- `data/questions/` – generated question YAML files
- `data/answers/` – model responses to prompts
- `data/results/` – evaluation results
- `data/leaderboard/` – compiled leaderboard data for the web app
- `dev/` – development notes and WIP docs


### Evaluation Workflow (Python)

```bash
pip install -r requirements.txt
```

The benchmark generation and grading scripts live in `./scripts`.
They use `llm` to create questions, produce model answers and grade them.

#### Generating questions

`generate_questions.py` can be run offline to create placeholder questions from `dev/topics.yaml`. Questions are written to `data/questions/`.

#### Running an evaluition

This isa done in 2 parts:

`generate_answers.py` uses the `llm` CLI to fetch a model answer and stores it under `data/answers/<model>/`.

`grade_answers.py` runs the grading prompt with `llm` using a JSON schema so the scores are parsed and written to `data/results`.

#### Running the full pipeline

`run_full_evals.py` ties everything together. It loops over all question files
for the models you specify, generates missing answers, grades them and then
updates the leaderboard.

Example:

```bash
python scripts/run_full_evals.py --models gpt-4.1-nano gpt-4.1-mini
```

Use `--rerun-answer` or `--rerun-grade` to force regeneration.

#### Updating the leaderboard

Results are aggregated into `data/leaderboard` using `aggregate_results.py`.

#### Python tests

```bash
pytest
```

# Licence

This project is licensed under the MIT License.

# Contributing

Contributions are welcome, epecially for new models. Please open a PR.

