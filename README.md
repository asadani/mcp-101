# MCP 101

An interactive tutorial on the Model Context Protocol. Eighteen chapters on
one page, with the protocol's moving parts as things you step through rather
than diagrams you look at.

**▶ [Start the tutorial](https://tech.anujsadani.in/mcp-101/)**

No build, no install, no server. One HTML file that also runs from `file://`
if you clone it.

---

## What makes it interactive

The hard part of MCP is not the vocabulary. It is that six things are talking
at once, and prose makes you hold all six in your head. So the page lets you
drive them instead:

- **A wire tap on the full lifecycle.** Step through a single question, from
  cold start to answer, and watch the actual JSON-RPC frames appear as they
  are sent. The tap fills up as you go, so you can see exactly which steps are
  MCP and which are the LLM API doing its own job.
- **Three lanes: host, model, server.** Every step highlights who is acting.
  This is where most MCP confusion dissolves, because the model never runs
  anything.
- **The M×N problem, as a dial.** Move the number of models and the number of
  tools, and watch the integration count grow, then watch what a protocol does
  to it.
- **Transport comparison.** stdio against HTTP, side by side, with what each
  one actually implies for ports, auth and deployment.
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
| 11 | Security | The attacks that are specific to this |
| 12 | Designing servers people can use | Tool design as interface design |
| 13 | Authorization | OAuth, and who holds the token |
| 14 | Build one | A working server |
| 15 | Debugging and testing | Inspecting the wire |
| 16 | AWS in practice | What this looks like deployed |
| 17 | Check yourself | Eighteen questions |

About two hours of reading, or 45 minutes if you listen.

---

## Listening

The whole course is narrated, and the player is built into the page. There are
two recordings of it:

- **[index.html](https://tech.anujsadani.in/mcp-101/)** — narrated by Kokoro-82M, 45.5 minutes
- **[my-voice.html](https://tech.anujsadani.in/mcp-101/my-voice.html)** — the same course in a clone of my own voice, 50.3 minutes

Both are rendered offline from the scripts in `narration/`. Nothing is
streamed from anywhere and no account is involved.

---

## Layout

```
index.html            the tutorial
my-voice.html         the same tutorial, narrated in my voice
narration/            the source scripts, one .txt per chapter
audio-kokoro/         the shipped narration
audio-qwen/           the cloned-voice narration
audio-chatterbox/     one chapter from an earlier attempt, kept for comparison
tools/
  generate-audio.py   renders narration/ to mp3s
  make-voice-page.py  builds the clone-voice page from the tutorial
voice/
  passage.txt         the passage read aloud to make a voice reference
  reference-short.txt its transcript
```

### Re-rendering the narration

```bash
pip install -r tools/requirements.txt
python tools/generate-audio.py --fetch-model      # 354 MB, once
python tools/generate-audio.py                    # writes audio-kokoro/
```

Only chapters whose script changed are re-rendered. The cache key covers the
text, voice, speed and engine, so changing any of them invalidates exactly
what it should. Editing a chapter and re-running takes about a minute.

`voice/*.wav` is not in this repo, on purpose: a clean recording of a voice is
precisely what someone needs to clone it. The passage and transcript are text
and are tracked, so anyone can reproduce the pipeline with a reference of
their own.

The narration pipeline was generalised into
[narrate-your-writing](https://github.com/asadani/narrate-your-writing), which
does this for any directory of text and needs no MCP course to be useful.

---

## Licence

MIT. The narration models are Apache 2.0.

Cloning a voice that is not yours, without consent, is not a grey area.
