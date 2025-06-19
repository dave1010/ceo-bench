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

### Python Workflow

The benchmark generation and grading scripts live in `./scripts`.
They use the OpenAI API to create questions, produce model answers and grade them.
Results are written to `./answers`, `./results` and aggregated into `./leaderboard` using `aggregate_results.py`.
`generate_questions.py` can be run offline to create placeholder questions from `dev/topics.yaml`.
`generate_answers.py` uses the `llm` CLI to fetch a model answer and stores it under `./answers/<model>/`.
`grade_answers.py` runs the grading prompt with `llm` and writes the result JSON into `./results`.

## Repo Layout

See `dev/CONTEXT.md` for details. Key directories are:

- `prompts/` – prompt templates and rubrics
- `questions/` – generated question YAML files
- `scripts/` – Python automation scripts
- `answers/` – model answers
- `results/` – grading outputs
- `leaderboard/` – processed leaderboard data
- `dev/` – development notes

**Deploy**

Deployed on Vercel; push to `main` to update.
