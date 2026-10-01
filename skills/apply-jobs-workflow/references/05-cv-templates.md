# CV Templates and Tailoring Guide

## Structure
1. **Header** — Name, tagline (role-specific), contact info
2. **Summary** — 2-3 sentences tailored to the specific role and company
3. **Core Skills** — 12-15 skills as tags, reorder by relevance to target role
4. **Experience** — Reverse chronological, most recent first
5. **Education** — Master's + Bachelor's

## Tailoring Rules

### For Each Application
1. Pull top 5-7 keywords from the job description
2. Ensure those keywords appear in summary and relevant experience bullets
3. Reorder skill tags so the most relevant 6-8 appear first
4. If the role emphasises something specific (e.g. security, cost, AI), lead with related bullets in each role
5. Remove or shorten bullets irrelevant to the target role

### Example: Platform Engineer role
- Lead with: Kubernetes platform experience, self-service tooling, IaC at scale
- De-emphasise: Security tooling details (Checkmarx twistlock specifics), legacy API decommissioning

### Example: DevOps / SRE role
- Lead with: Reliability engineering, incident response, observability, on-call automation
- De-emphasise: AI agent orchestration (keep but shorter), cloud cost specifics

### Example: DevSecOps / AppSec role
- Lead with: Security gate integration, Checkmarx/SonarQube/Twistlock, security alert automation
- De-emphasise: Kubernetes performance tuning, cost optimisation

## Output Formats
- HTML + CSS (print-friendly, ATS-compatible)
- LaTeX → PDF (for human-reviewed applications via lualatex)
- DOCX (for direct upload to Workday, Lever, Greenhouse etc.)

## ATS Tips
- Use standard section headings (Summary, Experience, Education — not random titles)
- No tables, columns, or graphics — flat text parses best
- Save as .docx for systems that parse XML layouts; .pdf for human review
- Avoid acronyms on first use — spell out "Site Reliability Engineering (SRE)" then use acronym
