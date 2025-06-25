# CEO Bench

**CEO Bench** is an open research benchmark evaluating how well large language models handle executive leadership tasks. It generates realistic management questions, collects model answers and scores them with an automatic rubric to produce a leaderboard.

## Running Evaluations

1. Install Python requirements and the `llm` command line tool.
   ```bash
   pip install -r requirements.txt
   ```
2. Run the full pipeline for one or more models. Missing answers will be generated, graded and then aggregated into the leaderboard CSV.
   ```bash
   python scripts/run_full_evals.py --models gpt-4.1-nano gpt-4.1-mini --grading-model gpt-4.1-mini
   ```
   Add `--sample 0.25` to evaluate on a random subset of questions (default is `1`).

You can also run the steps individually:

- `generate_answers.py` – fetch an answer for a single question.
- `grade_answer.py` – score an answer with the grading model.
- `aggregate_results.py` – build `data/leaderboard/leaderboard.csv` from graded answer JSON files.
- `check_model.py` – send a quick "Hello" prompt to verify a model works.

Data produced by the pipeline lives under the `data/` directory in `questions/`, `answers/`, `graded_answers/` and `leaderboard/`.

## Groq Setup

To evaluate Groq models you need the optional plugin and an API key:

```bash
llm install llm-groq
export LLM_GROQ_KEY=YOUR_KEY
```

Run `llm groq refresh` to fetch the list of available models. The pipeline can
then be run with `--models groq/gemma2-9b-it`.

## OpenRouter Setup

Evaluating models via OpenRouter requires the `llm-openrouter` plugin and an API
key:

```bash
llm install llm-openrouter
export OPENROUTER_KEY=YOUR_KEY
```

Free models such as `openrouter/meta-llama/llama-3.2-3b-instruct:free` and
`openrouter/meta-llama/llama-3.2-1b-instruct:free` are limited to 50 requests per
day. Add credits to increase this quota if you need to run larger samples.

## Evaluation Questions

The benchmark covers a range of executive topics:

- **Strategic Thinking**
- **Operational Excellence**
- **Leadership & Communication**
- **Financial Acumen**
- **Risk & Ethics**
- **Innovation & Growth**

`generate_questions.py` creates YAML question files for these topics based on `data/topics.yaml`. If a specific prompt looks wrong you can rerun just that one with `regenerate_question.py`.

## Grading

Answers are scored automatically using the rubric attached to each question. `grade_answer.py` builds a grading prompt from the question and answer files and calls `llm` to produce structured JSON. The JSON contains scores for each rubric dimension plus an overall score.

## Leaderboard

`aggregate_results.py` collects all scoring JSON into `data/leaderboard/leaderboard.csv`. This CSV powers the website and lets you compare models at a glance.

## Project Structure

```
app/          Next.js front-end
scripts/      Python evaluation scripts
templates/    Prompt templates for question and grading generation
data/         Generated YAML, answers, graded answers and leaderboard CSV
tests/        Pytest unit tests
dev/          Development notes and WIP documents
```

`ROADMAP.md` tracks ongoing implementation tasks.

Run the Python tests with:

```bash
pytest
```
Run lint checks:
```bash
flake8 scripts/ tests/
```
Run the JS tests with:
```bash
npm test
```

## Next.js Web Site

The `app/` directory contains a small Next.js project that displays the leaderboard and describes the benchmark. To work on the web interface locally:

```bash
npm install
npm run dev
npm run lint
npm run build
```
The site is deployed via Vercel and is updated whenever the `main` branch changes.

## License

This project is released under the MIT License.

## Contributing

Contributions are welcome! Please check `ROADMAP.md` for current plans and open a pull request for improvements or new evaluation scripts.
