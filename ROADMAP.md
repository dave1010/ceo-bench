## CEO Bench Implementation Roadmap

(this file should be edited as progress is made. also update /dev/CONTEXT.md with anything useful for future developers)

TODO: everything not already marked DONE below

### Phase 1: Research & Planning

* DONE pick about 5-10 topics and a some subtopics each (./dev/topic-ideas.md has early draft)
* DONE topics structured in dev/topics.yaml for easy iteration
* DONE compile sample prompts and rubrics.
* DONE created repo skeleton (prompts/, scripts/, etc) for future work
* DONE manually test a tiny vs big LLM on a few prompts.
* tweak scoring
* estimate human performance on these tasks.
* update readme with findings and progress (ongoing)
* draft Prompt Templates, Rubric Specs, Evaluation Pipeline, Analysis & Reporting.

### Phase 2: Proof of Concept Scripts for Querstion Generation & Evaluation

* DONE generate prompts (with few shot examples) and script to loop through topics and subtopics and generate YAML questions (prototype)
* DONE Python script to generate N questions per topic/subtopic (placeholder logic)
* integrate LLM API to create real questions
* Filtering: remove duplicates, low-quality via heuristics.
* should have 200+ questions across all topics
* DONE YAML files in ./questions/{incremental-id}-{topic}-{subtiopic}-{title}.yaml
* DONE include in yaml: topic, subtopic, title, question, rubric


### phase 3 Run evals with models

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
