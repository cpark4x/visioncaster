# Archive

This directory contains learning artifacts - tools that were built to explore ideas but aren't production-ready.

## ProblemSpace v1

**What it was:** A problem validation tool that required humans to provide evidence and metrics.

**Why archived:** User testing revealed it solved the wrong problem. People want AI to do research and discovery, not just format their existing knowledge.

**Key learnings:**
- ✅ Amplifier pattern works great for multi-stage pipelines
- ✅ State management and resumability work well
- ✅ Architecture was sound
- ❌ Wrong workflow: asked humans for evidence they didn't have
- ❌ AI did too little, human did too much
- 💡 Insight: "People are lazy - AI should research and validate on its own"

**What we built instead:** ProblemExplorer - an AI-research-first tool where AI discovers evidence, proposes metrics, and humans just validate.

**Date archived:** 2025-10-28
