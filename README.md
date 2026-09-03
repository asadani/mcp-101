# MCP 101

An interactive tutorial on the Model Context Protocol. Eighteen chapters on
one page, with the protocol's moving parts as things you step through rather
than diagrams you look at.

**▶ [Start the tutorial](https://tech.anujsadani.in/mcp-101/)**

No build, no install, no server. One HTML file that also runs from `file://`
if you clone it. You can read it, listen to it, or both.

---

## What makes it interactive

The hard part of MCP is not the vocabulary. It is that six things are talking
at once, and prose makes you hold all six in your head. So the page lets you
drive them instead:

- **A wire tap on the full lifecycle.** Step through a single question, from
  cold start to answer, and watch the actual JSON-RPC frames appear as they
  are sent. You can see exactly which steps are MCP and which are the LLM API
  doing its own job.
- **Three lanes: host, model, server.** Every step highlights who is acting.
  This is where most MCP confusion dissolves, because the model never runs
  anything.
- **The M×N problem, as a dial.** Move the number of models and the number of
  tools, watch the integration count grow, then watch what a protocol does to
  it.
- **Transport comparison.** stdio against HTTP, side by side, with what each
  implies for ports, auth and deployment.
- **An authorization walkthrough.** The OAuth flow as discrete steps rather
  than a sequence diagram you skim.
- **Runnable server code**, in tabs, for the chapter where you build one.
- **A self-check** at the end, which tells you which chapter to revisit.

## Chapters

| | | |
|---|---|---|
| 00 | A brain in a jar | Why a model alone cannot do anything |
| 01 | Client and server | The two words, used precisely |
| 02 | API, then REST | What we already had |
| 03 | Why REST alone doesn't help a model | The gap MCP fills |
| 04 | Tool use | What the model actually emits |
| 05 | The M×N problem | The reason a protocol exists |
| 06 | Host, client, server | The three roles, kept straight |
| 07 | The primitives | Tools, resources, prompts |
| 08 | Transports | stdio and HTTP |
| 09 | The full lifecycle | One question, end to end |
| 10 | REST vs MCP | When each is the right answer |
| 11 | Security | The attacks specific to this |
| 12 | Designing servers people can use | Tool design as interface design |
| 13 | Authorization | OAuth, and who holds the token |
| 14 | Build one | A working server |
| 15 | Debugging and testing | Inspecting the wire |
| 16 | AWS in practice | What this looks like deployed |
| 17 | Check yourself | Eighteen questions |

About two hours of reading, or under an hour if you listen.

---

## Two narrations, your pick

Every chapter is narrated, with the player built into the page. Pick whichever
you prefer:

| | | |
|---|---|---|
| **[Default](https://tech.anujsadani.in/mcp-101/)** | my own voice | 50 min |
| **[Alternative](https://tech.anujsadani.in/mcp-101/kokoro.html)** | a synthetic voice | 45 min |

The two pages link to each other, so you can switch at any point. Both are
rendered offline and served from this repo. Nothing streams from anywhere and
no account is involved.

---

## Repo layout

```
index.html            the tutorial, default narration
kokoro.html           the same tutorial, synthetic narration
narration/            the scripts, one .txt per chapter
audio-qwen/           the default narration
audio-kokoro/         the synthetic narration
tools/generate-audio.py   re-renders narration/ to mp3s
```

Editing a chapter means editing its `.txt` in `narration/` and re-running the
render. Only chapters whose text changed are redone, and the page manifest is
rewritten with the new durations so the player never drifts from the files.

```bash
pip install -r tools/requirements.txt
python tools/generate-audio.py --fetch-model   # once
python tools/generate-audio.py                 # re-render
```

## Licence

MIT. The narration models are Apache 2.0.
