# Installing ORS in Claude Code

This example walks through the most common installation: using ORS as a Claude Code plugin so all 118 skills are available to Claude in your terminal.

## Prerequisites

- Claude Code installed (`npm install -g @anthropic-ai/claude-code` or the equivalent for your OS)
- A terminal in any directory

## Install

```bash
# Step 1: Add the ORS marketplace
/plugin marketplace add pradyumnasagar/open-research-skills

# Step 2: Install the three plugin groups (or pick what you need)
/plugin install ors-research@pradyumnasagar
/plugin install ors-bioinformatics@pradyumnasagar
/plugin install ors-career-ethics@pradyumnasagar

# Step 3: Verify
/plugin list
```

You should see `ors-research`, `ors-bioinformatics`, and `ors-career-ethics` in the installed list.

## Try it out

Start a Claude Code session anywhere on your machine:

```bash
claude
```

In the chat, ask Claude to use a specific ORS skill:

```
> Use the bwa-alignment skill to align reads/sample_R1.fastq.gz to ref/GRCh38.fa
```

Claude reads `skills/bioinformatics-sequence/bwa-alignment/SKILL.md` and follows the workflow there.

## Updating

To pull the latest ORS skills:

```bash
/plugin marketplace update pradyumnasagar/open-research-skills
```

## Uninstalling

```bash
/plugin uninstall ors-research@pradyumnasagar
/plugin uninstall ors-bioinformatics@pradyumnasagar
/plugin uninstall ors-career-ethics@pradyumnasagar
/plugin marketplace remove pradyumnasagar/open-research-skills
```

## Troubleshooting

**"Marketplace not found"** — Check your internet connection and that you're running a recent version of Claude Code. The marketplace command was added in a 2025 release.

**"Skill not loading"** — Some agents cache skill metadata. Restart Claude Code or use `/plugin refresh`.

**"Permission denied" when installing** — Claude Code installs to `~/.claude/plugins/`. If that path is read-only, check the directory permissions.
