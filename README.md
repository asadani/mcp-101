# mcp-101

A short course on the Model Context Protocol, written to be read on one page
and listened to in two voices.

- **`mcp-course.html`** — the course, narrated by Kokoro-82M. 18 chapters, 45.5 minutes.
- **`mcp-course-voice.html`** — the same course, narrated by a clone of my own voice. 50.3 minutes.

Both pages open straight off disk. The audio manifest is inlined rather than
fetched, so `file://` works with no server.

---

## Layout

```
narration/            the source scripts, one .txt per chapter
tools/
  generate-audio.py   renders narration/ to mp3s, three engines
  make-voice-page.py  builds the clone-voice page from the Kokoro one
audio-kokoro/         the shipped track (Kokoro-82M, bm_george+bm_fable)
audio-qwen/           the clone track (Qwen3-TTS 0.6B)
audio-chatterbox/     one chapter from an earlier attempt, kept for comparison
voice/
  passage.txt         the passage read aloud to make the reference
  reference-short.txt its transcript
mcp-course.html       the page, pointed at audio-kokoro/
mcp-course-voice.html the page, pointed at audio-qwen/
```

**`voice/*.wav` is not in this repo, on purpose.** `reference-short.wav` is a
clean 4.5-second recording of my voice, which is precisely what someone needs
to clone it. The passage and the transcript are text and are tracked, so the
pipeline is reproducible by anyone who records their own reference.

---

## Rendering

```bash
pip install -r tools/requirements.txt
python tools/generate-audio.py --fetch-model      # 354 MB, once

python tools/generate-audio.py                                  # kokoro
python tools/generate-audio.py --engine qwen --device cuda      # your voice
```

Only chapters whose text has changed are re-rendered. The cache key covers the
script, the voice, the speed and the engine, so changing any of them
invalidates exactly what it should.

### The three engines, measured on a GTX 1650 (4 GB) with 8.5 GB of system RAM

| Engine | Params | Real-time factor | Full 45-minute course |
|---|---|---|---|
| Kokoro-82M, CPU | 82M | 0.53× | 24 min |
| Kokoro-82M, CUDA | 82M | 0.12× | 6 min |
| Qwen3-TTS 0.6B, CUDA | 0.6B | 2.7× | ~3 h |
| Chatterbox 0.5B, CUDA | 0.5B | 16.8× | 12.7 h |

Real-time factor is seconds of compute per second of audio. Lower is better.
Chatterbox is in the table because it was tried first and is the reason the
others are worth measuring: its weights left 0.79 GB of headroom on a 4 GB
card, so it paged constantly and eventually tripped the display driver's
watchdog mid-run.

---

## Things worth knowing before changing anything

**The clone engines cannot write into `audio-kokoro/`.** The script refuses,
because that directory holds the finished course and a bad `--out-dir` should
not be able to destroy it.

**Acronyms are handled per engine.** Kokoro's espeak frontend needs `MCP`
spelled `em see pee`; Qwen's neural frontend says it correctly on its own and
gets worse if you feed it the phonetic version. Hence `--acronyms` /
`--no-acronyms`, defaulted per engine.

**The pauses matter more than any model setting.** `GAP_PARAGRAPH = 0.55` and
`GAP_OPENING = 0.85` do more for listenability than anything else here.
Silence is concatenated, not synthesised, so it is exact.

**A short voice reference beats a long one.** 4.5 seconds rendered at 4.6×
real time and 2.68 GB peak; 85 seconds of the same voice ran at 9.7× and then
stalled. The reference sits in the model's context for the whole generation.

**The clone runs about 10% longer.** 45.5 minutes of Kokoro became 50.3
minutes cloned. Nothing is truncated; it just speaks at a human pace.

---

## Related

The pipeline was generalised into
[narrate-your-writing](https://github.com/asadani/narrate-your-writing), which
narrates any directory of text files and needs no MCP course to be useful.
The write-ups are at
[Narrating your writing with Kokoro](https://tech.anujsadani.in/narrate-writing-kokoro/),
[Cloning your own voice with Qwen3-TTS](https://tech.anujsadani.in/clone-your-voice-qwen3-tts/),
and [Reviving a six-year-old GPU for small models](https://tech.anujsadani.in/revive-old-gpu-small-models/).

## Licence

MIT for the code. Kokoro-82M and Qwen3-TTS are Apache 2.0.

Cloning a voice that is not yours, without consent, is not a grey area.
