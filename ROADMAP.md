## CEO Bench Implementation Roadmap

(this file should be edited as progress is made. see README for project context and directory structure)

TODO: everything not already marked DONE below

### Phase 1: Research & Planning

* DONE pick about 5-10 topics and a some subtopics each (./data/topics.yaml)
* DONE compile sample questions and rubrics. (/questions)
* DONE created repo skeleton (prompts/, scripts/, etc) for future work
* DONE set up `llm` and confirm it gets back real LLM responses (`llm --model gpt-4.1-nano --system "You are a helpful assistant" "What is the capital of France?"`)
* DONE send a test question to gpt-4.1-mini and save the answer in /answers - maybe we need to tweak the files in /prompts.
* DONE send a test answer to gpt-4.1-mini and save the grading in /results
* DONE get it working with scripts (make_question_prompt.py and then get python to call `llm`). see `/dev/test-run.txt` for a sample run.

### Phase 2: Proof of Concept Scripts for Querstion Generation & Evaluation

* DONE YAML files in ./questions/{incremental-id}-{topic}-{subtiopic}-{title}.yaml
* DONE include in yaml: topic, subtopic, title, question, rubric
* DONE generate prompts (with few shot examples) and script to loop through topics and subtopics and generate YAML questions (prototype)
* DONE Python script to generate N questions per topic/subtopic (placeholder logic)
* DONE make the grading use a schema (see /dev/llm-schemas.txt) and parse grading_text
* DONE run 3 or 4 test questions through the pipeline to confirm everything works end-to-end
* DONE test gpt-4.1-mini vs gpt-4.1-nano vs gpt-4.1 on a few prompts.
* DONE update readme with findings and progress

### Phase 2.5 scaling up question generation

* DONE create real questions using the /data/topics.yaml file and getting the LLM to generate them (expand generate_questions.py and refactor). this should loop through each topic and subtopic and ask the LLM to generate a question and rubric (just the first subtopic for now). we need to ensure questions are diverse in each subtopic - we can give the LLM the titles of any exisiting questions in the subtopic and ask it to be diverse. will need a new prompt template. we'll need to get this right with just 1 subtopic first, generating 10 questions. the script shold use the next available incremental ID for the question file name.
* manually review the generated questions and rubrics
* continue for all subtopics, then all topics
* Filtering: remove duplicates, low-quality via heuristics.
* should have 200+ questions across all topics

### phase 3 un evals with models

* DONE refactor all scripts, restructure directories
* write scripts to batch the processes
* write script to generate answers with models, save results
* write script to grade answers with judge LLM, save results
* iterate to improve prompts and scoring
* update readme

### phase 4 Leaderboard

* DONE write script to turn results into leaderboard data
* make leaderboard display in Next.js app, updating on deploy
* make fancy chart, inckuding human baseline range

### phase 5 Analysis / evaluation of findings / interpretation

* Significance tests between models (t‑test or nonparametric).
* Correlation of rubric dims.
* write some words


### Phase 6: Paper / publish

* Abstract, Intro, Related Work, Methodology, Results, Discussion, Conclusion.
* Methodology: prompt design, eval pipeline, scoring.
* Results: tables, figures.
* GitHub repo, MIT license, instructions.
* share
