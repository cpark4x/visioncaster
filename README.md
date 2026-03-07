# VisionCaster

**Validate the problem before you build the solution.**

A PM toolkit for AI-powered problem validation. Give it a problem statement, it does the research, surfaces what's actually known, and generates a structured, evidence-backed problem brief — before you commit to building anything.

Built in October 2025. MVP works end-to-end. Paused — may become part of a larger PM specialist toolkit.

---

## The core tool: ProblemExplorer

Most teams commit to building something before they've truly validated the problem. ProblemExplorer flips that — AI does the research first, so you're working from evidence, not assumptions.

```bash
make problemexplorer PROBLEM="Managing AI-first teams is challenging"
```

What it does:
1. Takes your problem statement
2. Generates research queries automatically
3. Executes searches and synthesizes findings
4. Validates evidence quality
5. Outputs a structured, research-backed problem statement document

**Why this matters for PMs:** A problem statement you can defend — with sources, evidence dimensions, and quality validation — is worth 10 built-on-assumptions ones.

---

## What's inside

| Tool | Status | Description |
|---|---|---|
| **ProblemExplorer** | ✅ MVP complete | AI-research-first problem validation |
| **ProblemSpace v1** | 📦 Archived | First attempt — solved the wrong problem |

**On ProblemSpace v1:** The first version asked users to provide evidence and had AI format it. User testing revealed the flaw immediately — people haven't done the research yet, that's the whole point. *"People are lazy — AI should do the work."* That insight became ProblemExplorer. ProblemSpace v1 is kept as a learning artifact.

---

## Setup

**Prerequisites:** Python 3.9+, Amplifier ([github.com/microsoft/amplifier](https://github.com/microsoft/amplifier))

```bash
git clone https://github.com/cpark4x/visioncaster
cd visioncaster
pip install -e amplifier/.
```

**Note:** ProblemExplorer MVP uses mock search data. Production use requires a real web search integration (SerpAPI or similar).

---

## Key learnings from building this

1. **MVP = working end-to-end** — mock data is fine, complete workflow matters
2. **Test the assumption, not the polish** — v1 looked good and solved the wrong problem entirely
3. **User insight beats architecture** — one round of testing revealed more than weeks of design
4. **Code for structure, AI for intelligence** — reliable pipeline + intelligent AI > trying to make AI reliable

---

## Status

Working MVP. Paused. Will return when integrating into a broader PM specialist toolkit — likely alongside Outcomist and canvas-specialists research pipeline.

---

## Built by

**Chris Park** — Senior PM, Microsoft Office of the CTO, AI Incubation group.
Engineering degree from Waterloo. 17 years shipping product.

[LinkedIn](https://www.linkedin.com/in/chrispark1/) · [GitHub](https://github.com/cpark4x)
