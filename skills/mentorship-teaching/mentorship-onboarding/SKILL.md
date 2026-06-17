---

name: mentorship-onboarding
description: "Establishes effective mentor-mentee relationships through structured onboarding using the Entering Mentoring curriculum (CIMER, UW-Madison), defining expectations, communication cadences, and feedback norms. Use when initiating a new mentoring relationship, transitioning between mentors, or formalizing an informal mentorship."
license: MIT
---
<!-- metadata:
  category: mentorship-teaching
  oversight: medium
  version: 1.0.0
  author: Pradyumna Jayaram
  tags: [mentorship-teaching, research]
  difficulty: intermediate
-->

## Version Compatibility

Reference frameworks and tools cited: CIMER Entering Mentoring (2024 revision), AAAS MyIDP, NSF PAPPG 24-1.

The frameworks referenced here are stable. If implementing within a specific institution, adapt communication templates to local norms and compliance requirements. Mentors in NIH-funded labs should reference specific broadening requirements applicable to their award type.

# Mentorship Onboarding

## Hard rules

1. **No fabricated citations.** Every cited work must resolve to a verifiable
2. **No claim without provenance.** Every quantitative or factual claim
3. **No silent failure.** Every script invocation, API call, or tool use must declare its exit status and what to do on non-zero. A skill that silently swallows errors is a violation.

## When to use

Load this skill when the user asks a question that matches its declared
trigger conditions (see the frontmatter `description` for the most common
ones). Do not load it for questions outside its scope — defer to the
appropriate ORS skill instead.

## When NOT to use

Do not load this skill if the question is in a sibling skill's domain
(see `## Cross-references`), if the user explicitly asks for a different
tool, or if the task is outside the skill's declared category.

## When to Use This Skill

| Scenario | Why this skill is needed |
|-----------|--------------------------|
| New mentor-mentee relationship | Establishes framework before expectations diverge |
| First-time mentor | Provides evidence-based structure, reduces anxiety |
| Transitioning to new mentor | Re-sets expectations, avoids carryover assumptions |
| Lab rotation completion | Formalizes lessons learned, prepares for next phase |
| Multi-mentor arrangement | Aligns expectations across mentors |

## The CIMER Onboarding Framework

The Entering Mentoring curriculum identifies five key areas that must be addressed in the first meetings:

1. **Establishing expectations** — What does each party expect from the relationship?
2. **Assessing current skills and knowledge** — Where is the mentee starting?
3. **Defining communication norms** — How, when, and how often will you communicate?
4. **Creating a development plan** — What specific goals will guide the mentorship period?
5. **Establishing feedback norms** — How will you give and receive feedback?

### Expectation Alignment Template

The most common source of mentorship breakdown is misaligned expectations. Address these dimensions explicitly:

| Dimension | Mentor Expectation | Mentee Expectation |
|-----------|---------------------|---------------------|
| Meeting frequency | Weekly / biweekly / monthly | Same |
| Meeting format | In-person / Zoom / hybrid | Same |
| Email/chat response time | Within 24-48 hours | Same |
| Feedback delivery | Immediate / scheduled | Same |
| Project ownership | Mentor leads / mentee leads | Same |
| Authorship expectations | % contribution to justify co-authorship | Same |
| Working hours | Core hours / flexible / as needed | Same |
| Time-off policy | Request advance / inform | Same |
"
**Activity:** In the first meeting, each party independently填写上面的表格，然后对比讨论。这避免了"以为对方知道"的假设。

### Initial Skills Assessment

Use a structured self-assessment to identify mentee's starting point:

**Research Skills Inventory:**

- Literature search and synthesis
- Experimental design
- Technical lab skills
- Data analysis (statistics, coding)
- Scientific writing
- Grant writing (for advanced mentees)
- Lab management and mentorship (for senior mentees)

**Example conversation starter:**
"Before we set goals, I'd like to understand where you are in each of these areas. On a scale of 1-5 for each: Where would you rate yourself, and what's one area where you'd most like to grow?"

## Communication Norms Agreement

Explicitly define communication norms in writing:

```
MENTORSHIP COMMUNICATION AGREEMENT

Meeting Schedule: [Day] [time] every [week/biweek/month]
Format: [in-person / Zoom / hybrid]
Pre-meeting: Mentee sends agenda by [day/time]
Post-meeting: Mentor returns written feedback by [day/time]

Email/Chat:
- Urgent (实验安全): [response time]
- General questions: [response time]
- Scheduling: [response time]

Feedback:
- Positive feedback: [immediate / weekly]
- Constructive feedback: [in meetings / scheduled 1:1]
- Written annual review: [yes/no]

Documentation:
- Meeting notes: [who maintains]
- IDP updates: [frequency]
```

## Onboarding Meeting Sequence

### Meeting 1: Introduction and Expectation Alignment (60-90 minutes)

**Before meeting:**
- Mentee completes self-assessment
- Both parties review AAAS MyIDP initial assessment

**Agenda:**
1. Personal introductions (background, research interests)
2. Mentor research program overview
3. Mentee goals and motivations
4. Expectations discussion using template above
5. Communication norms agreement
6. Schedule next meeting

**Deliverable:** Signed communication agreement

### Meeting 2: Skills Assessment and Initial Planning (45-60 minutes)

**Agenda:**
1. Review self-assessment results
2. Identify priority growth areas
3. Discuss lab norms and culture
4. Assign initial project or reading
5. Set first IDP draft goals

**Deliverable:** Initial IDP draft with 3-month milestones

### Meeting 3: Plan Finalization and Launch (30-45 minutes)

**Agenda:**
1. Review and finalize IDP
2. Establish feedback schedule
3. Introduce key lab members
4. Resource allocation确认

**Deliverable:** Finalized 6-month IDP, feedback schedule

## Common Onboarding Pitfalls

| Pitfall | Why it matters | Prevention |
|--------|--------------|-------------|
| No written agreement | Verbal understandings are forgotten | Sign communication agreement |
| Assuming mentee knows lab culture | Cultural norms vary; explicitness prevents conflict | Provide written lab manual |
| Inconsistent meeting schedule | Relationship stalls without accountability | Calendar recurring meetings |
| Only discussing实验 | Broader development neglected | Include career and skill goals in IDP |
| Mentor not providing feedback structure | Mentee unsure how to improve | Use CIMER feedback framework |
| No documentation | Institutional knowledge lost | Maintain meeting notes |

## Feedback Framework: The CIMER Model

Effective feedback is specific, timely, and balanced. Use this structure:

**Behavior:** "When you [specific action]..."
**Impact:** "It [positive/neutral/negative effect]..."
**Suggestion:** "In the future, consider [alternative]..."

**Example:**
"当你在实验前检查protocols时，你的实验成功率和可重复性显著提高。建议继续保持这个习惯，也尝试在开始前向团队成员简要解释你的实验设计。"

## References

- CIMER Entering Mentoring Curriculum: https://cimer.wisc.edu/
- NSF PAPPG Chapter V (Mentoring): https://www.nsf.gov/bfa/dias/policy/pappg/
- NIH BEST Programs: https://www.nih.gov/best-programs
- AAAS MyIDP: https://myidp.sciencecareers.org/
- CAST UDL Guidelines: https://udlguidelines.cast.org/

## Related Skills

- mentorship-teaching/ors-mentorship-goal-setting - Setting research and career goals using IDP framework
- mentorship-teaching/ors-teaching-course-design - Designing formal research training curriculum
- mentorship-teaching/ors-teaching-syllabus - Creating course syllabi with learning outcomes

## Cross-references

Other skills in this category:

- mentorship-goal-setting
- teaching-course-design
- teaching-syllabus

## Changelog

- **1.1.0** (migration) — Bulk-migrated to v0.4.0 schema: canonical
  metadata block, base Hard rules, Cross-references. Body content
  unchanged; author should review and fill in any domain-specific
  extensions to the Hard rules.
- **1.0.0** — Initial release.

