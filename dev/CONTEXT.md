### Context

Front end is Next.js.

Scripts are Python. Use OpenAI chat completion API for question generation and grading. Offline helpers like `generate_questions.py` and `aggregate_results.py` assist with creating data without API calls.

## dirs in project root

./prompts - YAML prompt templates and rubrics
./scripts - Python scripts for generation, evaluation, grading
./questions - generated question YAML files
./dev - development notes and WIP docs
./answers - model responses to prompts
./results - evaluation results
./leaderboard - compiled leaderboard data for the web app
