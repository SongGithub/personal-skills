---
name: job-application-assistant
description: >
  Assistant for job applications: evaluating job postings, tailoring CVs, writing cover letters,
  and preparing for interviews. Triggers on keywords like: job posting, job application, CV,
  cover letter, resume, interview prep, job fit, career, application, apply, SEEK
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, Edit, Write, AskUserQuestion
---

# Job Application Assistant

Before evaluating a role or tailoring a CV, read the sibling [`job-search-quality` skill](../job-search-quality/SKILL.md). Its current salary and title configuration and evidence gates take precedence over older preferences in this skill or memory.

---

## Workflow

When the user provides a job posting (URL or text), follow this workflow:

### Step 0: Strategic Context Check
Before any role evaluation, recall the career-first-principles framework from memory.
- Run the **6-question Decision Filter** from `references/04-job-evaluation.md` as the primary gate
- Re-read the **steering sentence**: *"Am I moving toward being the person who builds the leverage on the next rising curve in a place that treats engineering as an investment — or toward executing known answers in a place that treats me as a cost?"*
- Context: read the candidate's financial runway and risk appetite from the private profile (`$JOB_SEARCH_HOME/profile.md`). If runway is comfortable, optimise for **direction over speed**
- Phase 1 goal: Become the rare "builds AND influences at the AI frontier"

### Step 1: Research & Evaluate Fit
- Fetch the job posting content (use WebFetch for URLs)
- Analyze the posting for required competencies, keywords, and priorities
- Research the company (website, LinkedIn, mission, recent news)
- Score the posting against the candidate's profile using the framework in `references/04-job-evaluation.md` — include both the **First-Principles filter** and the **weighted scoring dimensions**
- Present the evaluation table and verdict
- Suggest whether the candidate should call the employer before applying (see `references/04-job-evaluation.md` for guidance)
- Ask the user if they want to proceed with an application

### Step 2: Tailor CV
- Read the most relevant existing CV variant from `cv/` as a starting point
- Follow the guidelines in `references/05-cv-templates.md`
- Create `cv/main_<company>.tex` with tailored content
- Adjust: profile statement, skills section, experience bullet emphasis, section order

### Step 3: Write Cover Letter
- Follow the writing style rules in `references/03-writing-style.md` (critical: no em-dashes, no cliches)
- Follow the template structure in `references/06-cover-letter-templates.md`
- Create `cover_letters/cover_<company>_<role>.tex`
- Ensure the letter connects specific experience to the role requirements

### Step 4: Interview Preparation
- Follow the framework in `references/07-interview-prep.md`
- Prepare STAR-format answers for likely questions
- Identify role-specific talking points
- Draft questions the candidate should ask the interviewer

---

## Reference Files

| File | Purpose |
|------|---------|
| `$JOB_SEARCH_HOME/profile.md` | Private — candidate profile: education, experience, skills |
| `$JOB_SEARCH_HOME/targets.md` | Private — working style, ideal environments, exclusions |
| `references/03-writing-style.md` | Tone, structure, do's and don'ts |
| `references/04-job-evaluation.md` | Scoring framework for job fit |
| `references/05-cv-templates.md` | LaTeX CV structure and tailoring rules |
| `references/06-cover-letter-templates.md` | LaTeX cover letter structure and tailoring rules |
| `references/07-interview-prep.md` | STAR examples, tough questions, roleplay guidelines |

---

## Quick Commands

The user may also ask for individual steps without the full workflow:
- "Evaluate this job posting" - Step 1 only
- "Write a CV for [company]" - Step 2 only
- "Write a cover letter for [role] at [company]" - Step 3 only
- "Help me prepare for an interview at [company]" - Step 4 only
- "What jobs should I look for?" - Career strategy discussion using profile + evaluation framework
