# Loading ORS skills into the Anthropic API

This example shows how to load a single ORS skill (or several) into the `system` parameter of the Anthropic API.

## Python (Anthropic SDK)

```python
import pathlib
from anthropic import Anthropic

# Load a skill from disk
skill_text = pathlib.Path("skills/scientific-writing/manuscript-structure/SKILL.md").read_text()

# Strip the frontmatter — only the body is useful in the system prompt
body = skill_text.split("---", 2)[2].strip()

client = Anthropic()
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=4096,
    system=f"""You are a research assistant. Apply the following skill to every user request:

<skill>
{body}
</skill>

When the user asks you to do something the skill covers, follow its workflow.
When the user asks something outside the skill, answer normally but mention the skill is loaded in case they want to switch tasks.""",
    messages=[{"role": "user", "content": "Help me structure the methods section of a ChIP-seq paper."}]
)

print(response.content[0].text)
```

## Multi-skill routing

When you have many skills and don't want to pay the token cost of loading them all, use the frontmatter descriptions for routing:

```python
import pathlib
import frontmatter  # pip install python-frontmatter

# Load only frontmatter for routing
def load_skill_descriptions(skills_dir: pathlib.Path) -> str:
    out = []
    for md in sorted(skills_dir.rglob("SKILL.md")):
        fm = frontmatter.load(md)
        rel = md.relative_to(skills_dir.parent)
        out.append(f"- {fm['name']} ({rel.parent}): {fm['description']}")
    return "\n".join(out)

# Build a routing prompt
routing_prompt = f"""You have access to the following ORS skills. When the user asks a question,
identify which skill(s) apply and load their full text from disk.

Available skills:
{load_skill_descriptions(pathlib.Path('skills'))}

Format your response as:
SKILL: <skill-name>
REASON: <why this skill applies>
"""

# First call — let the model pick the skill
router_response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=512,
    system=routing_prompt,
    messages=[{"role": "user", "content": "Align these reads to GRCh38"}]
)
chosen_skill = parse_skill_name(router_response.content[0].text)

# Second call — load the chosen skill
skill = pathlib.Path(f"skills/{chosen_skill}/SKILL.md").read_text()
# ... use as in the single-skill example above
```

## TypeScript / Node.js (Anthropic SDK)

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { readFile } from "fs/promises";
import { join } from "path";

const skill = await readFile(
  join("skills/scientific-writing/manuscript-structure/SKILL.md"),
  "utf-8"
);
const body = skill.split("---")[2].trim();

const client = new Anthropic();
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 4096,
  system: `Apply this skill to every request:\n\n${body}`,
  messages: [{ role: "user", content: "Help me write an R01 specific aims page." }],
});

console.log(response.content[0].text);
```

## Bedrock (AWS)

```python
import boto3
import json
import pathlib

skill_body = pathlib.Path("skills/research-grants/nih-r01-specific-aims/SKILL.md").read_text().split("---", 2)[2].strip()

client = boto3.client("bedrock-runtime")
response = client.invoke_model(
    modelId="anthropic.claude-opus-4-8-20260601",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "system": f"Apply this skill:\n\n{skill_body}",
        "messages": [{"role": "user", "content": "Write the specific aims for my R01 on T-cell exhaustion."}]
    })
)
print(json.loads(response["body"].read()))
```

## Vertex AI (Google Cloud)

```python
import vertexai
from vertexai.generative_models import GenerativeModel
import pathlib

vertexai.init(project="my-project", location="us-central1")
model = GenerativeModel("claude-opus-4-8@20260601")

skill_body = pathlib.Path("skills/research-grants/nsf-standard-grant/SKILL.md").read_text().split("---", 2)[2].strip()
response = model.generate_content(
    f"Apply this skill:\n\n{skill_body}\n\nUser question: draft the project summary for my NSF proposal on quantum sensors.",
)
print(response.text)
```

## Notes

- The Anthropic API supports up to ~200K tokens of system prompt context on Claude Opus 4.8. ORS skills are small (~5–15 KB each), so you can fit 10–20 in one call if needed.
- Skills compose well. You can concatenate the bodies of related skills (e.g., `literature-research/systematic-review` + `scientific-writing/manuscript-structure` + `peer-review/manuscript-review`).
- The `name` field is the routing key. The `description` field is the routing signal.
- If you load a skill as a system prompt, you do **not** need to mention the skill in the user message — the agent already has it loaded.
