---

name: teaching-course-design
description: "Designs research training courses using Wiggins and McTighe's Backward Design framework, Bloom's Taxonomy (revised) for cognitive scaffolding, and Universal Design for Learning (UDL) principles for accessibility. Use when designing new courses, redesigning existing curricula, creating research training modules, or building learning progressions."
license: MIT
---




<!-- metadata:
category: mentorship-teaching
version: 1.0.0
author: Pradyumna Jayaram
tags:
  - mentorship-teaching
  - research
difficulty: intermediate
-->

## Version Compatibility

Reference frameworks: Backward Design (Wiggins & McTighe 2005), Bloom's Taxonomy Revised (Anderson & Krathwohl 2001), UDL 3.0 (CAST 2024).

The frameworks are stable. Adapt templates to your institution's course approval format and discipline-specific learning outcomes. Bloom's levels and Backward Design stages are durable; institutional templates change.

# Course Design for Research Training

Effective research training courses—whether semester-long graduate courses, multi-day workshops, or structured rotation curricula—do not start with content. They start with the desired learning outcomes. This skill applies Wiggins and McTighe's Backward Design to research training, scaffolding learning progressions with Bloom's Taxonomy and ensuring accessibility through Universal Design for Learning (UDL).

For syllabus-level course structure and policies, see `mentorship-teaching/ors-teaching-syllabus`. For individual mentee development planning, see `mentorship-teaching/ors-mentorship-goal-setting`.

## When to Use This Skill

| Scenario | Application |
|-----------|-------------|
| New graduate course development | Full backward design from outcomes |
| Workshop design | Compressed backward design |
| Lab rotation curriculum | Module-level design |
| Redesigning existing course | Revise outcomes and assessments |
| Training grant program design | Multi-component curriculum design |
| Online asynchronous training | Modular backward design |

## The Backward Design Framework
"
Wiggins and McTighe's backward design reverses traditional planning. Instead of "What topics should I cover?", start with "What should students be able to do?"

### Stage 1: Identify Desired Results

What should students know, understand, and be able to do? This is the **end-of-course destination**.

**Three categories of learning goals (drawn from Understanding by Design):**

1. **Enduring understandings** — Big ideas that transfer beyond the course
2. **Essential questions** — Recurring questions that organize inquiry
3. **Core knowledge and skills** — Discrete content and procedures

**Example for a graduate R programming course:**

- **Enduring understanding:** "Data analysis is iterative hypothesis refinement, not one-shot analysis"
- **Essential question:** "What are the assumptions underlying this analysis, and when do they fail?"
- **Core skills:** Data import, transformation, visualization, statistical modeling, reproducible workflows

### Stage 2: Determine Acceptable Evidence

How will we know students have achieved the desired results? This is the **assessment plan** before lesson planning.

**Assessment types in research training:**

| Type | Purpose | Examples |
|------|---------|----------|
| Formative | Monitor learning during instruction | Weekly problem sets, code reviews, peer feedback |
| Summative | Evaluate learning at end of unit/module | Project reports, final exam, capstone |
| Performance-based | Assess real-world capability | Code reproducible analysis, present at journal club, mentor a junior |
| Self-assessment | Build metacognition | Weekly reflection, skills self-audit |

**Principle:** Assessments must align with outcomes. If "communicate scientific findings" is a goal, there must be assessed presentations, not just multiple-choice questions.

### Stage 3: Plan Learning Experiences and Instruction

Only now do you design the lessons, activities, and materials. This is where Bloom's Taxonomy guides the cognitive level of activities.

**Backward Design Sequence:**

```
Stage 1: Outcomes (What should students be able to do?)
   ↓
Stage 2: Assessments (How will we know they can?)
   ↓
Stage 3: Instruction (What experiences build toward this?)
```

## Bloom's Taxonomy for Cognitive Scaffolding

Use Bloom's revised levels to ensure activities progress from foundational to higher-order thinking:

| Level | Cognitive demand | Example activity |
|-------|------------------|------------------|
| Remember | Recall facts, terms, concepts | Vocabulary quiz, definitional matching |
| Understand | Explain ideas, interpret | Summarize paper, explain concept to peer |
| Apply | Use information in new situations | Implement method on new dataset, troubleshoot code |
| Analyze | Draw connections, identify patterns | Compare methods, diagnose analytical choice |
| Evaluate | Justify a stance, critique | Peer-review draft manuscript, evaluate statistical approach |
| Create | Produce original work | Design experiment, synthesize review, develop new method |

**Scaffolding principle:** Begin course with Remember/Understand activities, build to Apply/Analyze, end with Evaluate/Create. Avoid spending entire course at lower levels.

## Universal Design for Learning (UDL)

UDL provides a research-based framework for designing learning experiences accessible to all students. The CAST UDL framework organizes around three networks:

### Multiple Means of Engagement (the "why" of learning)

- Provide options for recruiting interest (varied examples, choice in projects)
- Sustain effort and persistence (chunked goals, progress monitoring)
- Support self-regulation (self-assessment, reflection prompts)

**In research training:**
- Allow choice of dataset for analysis projects
- Connect work to real research questions
- Provide clear milestones rather than open-ended deadlines

### Multiple Means of Representation (the "what" of learning)

- Provide options for perception (video, text, audio)
- Provide options for language and symbols (define jargon, use multiple notations)
- Provide options for comprehension (worked examples, concept maps, summaries)

**In research training:**
- Provide both code and prose explanations of methods
- Use multiple example datasets
- Define statistical terms and avoid disciplinary jargon

### Multiple Means of Action and Expression (the "how" of learning)

- Provide options for physical action (lab accommodations, software flexibility)
- Provide options for expression (oral, written, code, video)
- Provide options for executive function (project management tools, templates)

**In research training:**
- Accept oral, written, or video project reports
- Provide project planning templates
- Allow varied software stacks (R or Python)

## Course Design Template

```
COURSE DESIGN DOCUMENT

Course: [Title]
Level: [Undergraduate/Graduate/Postdoc/Professional]
Duration: [Semester/Workshop/Module]
Prerequisites: [Required prior knowledge/skills]

== STAGE 1: DESIRED RESULTS ==

Enduring Understandings (3-5 big ideas):
1. [...]
2. [...]
3. [...]

Essential Questions (3-5):
1. [...]
2. [...]
3. [...]

Core Knowledge/Skills:
- [...]
- [...]
- [...]

== STAGE 2: ASSESSMENT EVIDENCE ==

Performance Tasks:
- [Major authentic assessment, e.g., capstone project]

Other Evidence:
- Weekly [formative assessment]
- Mid-term [summative]
- Final [summative]
- Self-assessment [frequency]

Alignment Check:
- Outcome 1 assessed by [...]
- Outcome 2 assessed by [...]

== STAGE 3: LEARNING PLAN ==

Unit 1: [Title] (Bloom level: [Remember/Understand])
- Outcomes: [...]
- Activities: [...]
- Assessment: [...]

Unit 2: [Title] (Bloom level: [Apply])
[...]

[Continue units with increasing Bloom level]

== UDL CONSIDERATIONS ==
Engagement: [Specific UDL choices]
Representation: [Specific UDL choices]
Action/Expression: [Specific UDL choices]
```

## Module Design for Workshops

For shorter training (e.g., 2-day workshops, week-long bootcamps), use compressed backward design:

**Day-by-day module structure:**

| Day | Bloom level | Activity types | Culminating task |
|-----|-------------|----------------|------------------|
| Day 1 AM | Remember, Understand | Lectures, demos, vocabulary | Recall exercise |
| Day 1 PM | Apply | Hands-on practice, pair programming | Apply to provided data |
| Day 2 AM | Analyze, Evaluate | Case studies, critique exercises | Compare/contrast reports |
| Day 2 PM | Create | Capstone, integration project | Public presentation |

**Compressed outcomes template:**

```
By the end of this workshop, participants will be able to:
1. [Apply-level outcome]
2. [Analyze-level outcome]
3. [Create-level outcome]
```

## Lab Rotation Curriculum Design

Lab rotations require module-level design that integrates with the broader IDP framework:

**Module structure for a 10-week rotation:**

| Week | Focus | Bloom level | Mentee deliverable |
|------|-------|-------------|-------------------|
| 1-2 | Onboarding, reading, methods intro | Remember/Understand | Literature summary |
| 3-4 | Apply methods to assigned problem | Apply | Initial results |
| 5-6 | Analyze and troubleshoot | Analyze | Analysis report |
| 7-8 | Design follow-up experiment | Create | Experimental plan |
| 9-10 | Communicate and document | Evaluate | Rotation presentation |

**Key principle:** Each module should produce a concrete artifact. Documentation is the evidence of learning.

## Common Course Design Pitfalls

| Pitfall | Why it fails | Prevention |
|---------|--------------|------------|
| Content coverage dominates | Outcome alignment lost | Use backward design, outcome-first |
| Assessments all at Remember | Lower-order learning persists | Build to Evaluate/Create |
| One mode of engagement | Excludes diverse learners | Apply UDL multiple means |
| No formative assessment | Can't adjust mid-course | Build weekly check-ins |
| Assessments misaligned | Measure wrong things | Map each outcome to assessment |
| Bloom levels flat | No cognitive growth | Sequence activities up hierarchy |
| Skills taught in isolation | Poor transfer to research | Use authentic research tasks |

## References

- Wiggins & McTighe (2005), *Understanding by Design* (2nd ed.)
- Anderson & Krathwohl (2001), *A Taxonomy for Learning, Teaching, and Assessing*
- CAST UDL Guidelines 3.0: https://udlguidelines.cast.org/
- CIMER Entering Mentoring: https://cimer.wisc.edu/
- AAAS MyIDP: https://myidp.sciencecareers.org/

## Related Skills

- mentorship-teaching/ors-teaching-syllabus - Translating course design into syllabus
- mentorship-teaching/ors-mentorship-goal-setting - Individual mentee development planning
- mentorship-teaching/ors-mentorship-onboarding - Mentor-mentee relationship setup