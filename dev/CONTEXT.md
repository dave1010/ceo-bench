### Context

Front end is Next.js.

Scripts are Python. Use OpenAI chat completion API for question generation and grading. Offline helpers like `generate_questions.py` and `aggregate_results.py` assist with creating data without API calls.

## dirs in project root

./templates - prompt templates and rubrics
./scripts - Python scripts for generation, evaluation, grading
    - generate_answers.py calls `llm` to produce an answer for a question
    - grade_answers.py grades an answer using `llm` with a JSON schema so results include parsed scores
./data/questions - generated question YAML files
./dev - development notes and WIP docs
./data/answers - model responses to prompts
./data/results - evaluation results
./data/leaderboard - compiled leaderboard data for the web app
