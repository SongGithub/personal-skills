# Interview Preparation Guide

## How to use this

Build answers from your own evidence, kept in the private profile at
`$JOB_SEARCH_HOME/evidence.md`. The examples below are **illustrative** and use
fictional employers: they show the shape of a strong answer, not a script to copy.

## The STAR shape

| Part | What it has to do |
|------|-------------------|
| Situation | One sentence of context — enough to make the stakes legible |
| Task | What you specifically owned. "I led", not "we did" |
| Action | The decisions you made and why. This is the bulk of the answer |
| Result | The measurable outcome, or an honest qualitative one |

Rules that hold regardless of the question:

- Lead with the outcome when the interviewer is time-pressed.
- Never claim a team outcome as solo work, and never hide behind "we".
- When probed, go one level deeper than the headline: what you considered, what you rejected, what broke.
- Keep a number in the Result whenever one exists.

## Illustrative examples

### Reliability — chasing a recurring incident
- **Situation:** A payments platform saw recurring latency incidents during peak hours.
- **Task:** Remove the incidents without simply buying more capacity.
- **Action:** Traced the pattern to CPU throttling caused by limits set by guesswork. Measured real usage, reset requests and limits from data, and added alerting on throttling rather than only on latency.
- **Result:** The incidents stopped recurring, and the same workload ran on less capacity.

### Migration — retiring a painful upgrade
- **Situation:** A critical database was pinned to an extended-support version with a rising support premium.
- **Task:** Move to a supported version with no downtime.
- **Action:** Built a blue/green upgrade path, rehearsed the cutover on a staging copy, and wrote the rollback plan before the forward plan.
- **Result:** Cutover completed with zero downtime; the support premium disappeared.

### Enablement — making the good practice the default
- **Situation:** Security scanning existed but was optional, so it happened late or not at all.
- **Task:** Make the secure path the easy path instead of policing teams.
- **Action:** Wired scanners into the pipeline as gates with actionable output, published fix patterns, and paired with teams on their first failures rather than filing tickets at them.
- **Result:** Checks became routine, and findings were fixed in the pipeline instead of after release.

### Platform — building something teams choose to use
- **Situation:** Product teams each solved deployment differently, duplicating effort.
- **Task:** Provide one platform teams would adopt voluntarily.
- **Action:** Treated internal teams as customers: shipped the first capability for the team with the worst pain, measured adoption rather than output, and iterated on real friction. Added self-service deploys, IaC and observability.
- **Result:** Adoption spread by word of mouth, and onboarding time for a new service dropped.

## Common interview topics (platform / DevOps)

### Technical
- Kubernetes: architecture, networking, RBAC, autoscaling, resource tuning
- Terraform: state management, modules, workspaces, drift
- Cloud networking and identity: VPC design, private connectivity, least privilege
- CI/CD design, and the trade-offs between build platforms
- Incident response and blameless postmortems
- Observability: OpenTelemetry, SLIs and SLOs, alert quality
- Cost optimisation: where spend actually leaks
- Supply chain: secrets handling, scanning, provenance

### Behavioural
- A time you influenced without authority
- How you handle on-call load and burnout on a team
- Prioritising platform work against feature work
- Getting teams to adopt your platform or tooling
- A complex incident, and what changed afterwards

### AI / agentic (differentiator)
- How you use AI in your engineering workflow
- Multi-agent orchestration, and where it breaks down
- Balancing AI automation with security and compliance
- How you verify AI output before it ships
