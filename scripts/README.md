# Python Scripts

This folder contains the automation code for the benchmark.

- `generate_questions.py` – load `dev/topics.yaml` and create question YAML files
- `grade_answers.py` – grade model answers using the OpenAI API
- `make_question_prompt.py` – turn a question YAML into a plain text prompt
- `make_grading_prompt.py` – combine a question, answer, and rubric for judging

Additional scripts can be added here as the project grows.
