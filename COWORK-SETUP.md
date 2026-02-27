# Cowork Mode Setup

How to use this repo with VS Code's Claude Code extension (Cowork mode).

## What Is Cowork?

Cowork is a way to run Claude Code inside VS Code instead of the terminal. You get the same Claude Code capabilities (file reading, web search, code execution) but in a sidebar panel next to your editor. It is part of the Claude Code VS Code extension.

The practical difference is minimal. Same agents, same workflow, same outputs. You just get a nicer split-view where you can see files and Claude's work side by side.

## Prerequisites

1. **VS Code** installed
2. **Claude Code CLI** installed (`claude` command works in your terminal)
3. **Claude Code VS Code extension** installed from the VS Code marketplace (search "Claude Code")

If you can run `claude --version` in your terminal and get a response, you are good to go.

## Getting Started

1. Open this repo folder in VS Code
2. Open the Claude Code panel from the sidebar (look for the Claude icon)
3. Start a new session

That is it. You are now running Claude Code with full access to the repo files.

## Running Agents

The workflow is the same as terminal usage:

1. Open the agent file you want to run (e.g., `_agents/job-search/interactive.md`)
2. Copy the entire contents of the file
3. Paste it into the Claude Code panel
4. Follow the prompts (fill in job URL, company name, etc.)

### Agent Options

| Agent | File | When to Use |
|-------|------|-------------|
| Interactive | `_agents/job-search/interactive.md` | First time, Q&A format |
| Single Job | `_agents/job-search/main.md` | Power users, one job |
| Batch | `_agents/job-search/batch.md` | Multiple jobs at once |
| Multi-Job | `_agents/job-search/multi-job.md` | Compare roles at same company |

## Tips

- **Project context loads automatically.** The `.claude/CLAUDE.md` file gives Claude context about the repo structure, so it knows where agents, templates, and config files live.
- **You can edit files while Claude works.** The split-view lets you tweak your user profile or templates while an agent runs.
- **Same outputs.** Everything saves to the same configured output path whether you run from terminal or Cowork.
- **Model selection still applies.** See `MODEL-GUIDE.md` for which models work best for different tasks.

## Differences from Terminal

Honestly, not much. The main differences:

- Sidebar UX instead of a full terminal window
- You can see file changes in real time in the editor
- Easier to copy/paste between files and the Claude panel
- Same underlying Claude Code engine, same tools, same permissions

If you are comfortable with terminal Claude Code, Cowork is just a convenience layer. If you prefer GUIs, Cowork is the way to go.
