# Examples

This directory contains worked examples of using ORS skills in real workflows.

| File | Use case |
|---|---|
| `claude-code-installation.md` | Install ORS as a Claude Code plugin and load a skill in a chat. |
| `api-integration.md` | Load an ORS skill into the Anthropic API's `system` parameter. |
| `multi-skill-workflow.md` | Chain 3+ ORS skills to complete a multi-step research task. |

## Quick start

The fastest way to use ORS is to clone the repo and point your agent at it:

```bash
git clone https://github.com/pradyumnasagar/open-research-skills.git
cd open-research-skills
claude
```

Then in the chat:

> Use the `bwa-alignment` skill to align these reads to GRCh38.

Claude will read `skills/bioinformatics-sequence/bwa-alignment/SKILL.md` and follow the workflow inside it.

## Plugin install (Claude Code)

```bash
/plugin marketplace add pradyumnasagar/open-research-skills
/plugin install ors-research@pradyumnasagar
/plugin install ors-bioinformatics@pradyumnasagar
/plugin install ors-career-ethics@pradyumnasagar
```

This installs the three plugin groups defined in `.claude-plugin/marketplace.json`.

## Programmatic use (Python)

```python
import pathlib
from anthropic import Anthropic

# Load a skill
skill = pathlib.Path("skills/scientific-writing/manuscript-structure/SKILL.md").read_text()

client = Anthropic()
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=4096,
    system=f"You are a research assistant. Use the following skill:\n\n{skill}",
    messages=[{"role": "user", "content": "Help me structure the methods section of a ChIP-seq paper."}]
)
print(response.content[0].text)
```

## Other agents

| Agent | How to load a skill |
|---|---|
| Cursor | Drop the `skills/` folder into your project; Cursor reads the SKILL.md files as project context. |
| Continue | Add the repo path to your `~/.continue/config.json` under `contextProviders`. |
| Aider | Pass `--read` flags pointing at the SKILL.md files you want. |
| Windsurf | Add the repo as a "rule" in `.windsurf/rules/`. |
| LangChain | Use `DirectoryLoader` on `skills/` and retrieve the relevant SKILL.md as context. |
| OpenAI Assistants | Upload SKILL.md files via the file API and let retrieval pick the right one. |
