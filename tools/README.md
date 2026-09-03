# Narration pipeline

Spoken-word narration for `mcp-course.html`, rendered locally with free,
open-source tools. No API key, no account, no cloud service, no telemetry.
Once the model files are downloaded, the whole thing runs offline.

| Piece | What it is | Licence |
|---|---|---|
| [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) | The voice. An 82M-parameter TTS model — small enough for CPU, good enough not to sound like a screen reader. | Apache-2.0 |
| [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) | Runs the model through onnxruntime, so there's no PyTorch install. | MIT |
| [espeak-ng](https://github.com/espeak-ng/espeak-ng) | Grapheme-to-phoneme. Ships inside `espeakng-loader`, so there's nothing to install system-wide. | GPL-3.0 (used as a data/phonemiser dependency) |
| [libsndfile](https://libsndfile.github.io/libsndfile/) via `soundfile` | Writes the MP3s directly — no ffmpeg needed. | LGPL-2.1 |

## Layout

```
narration/    18 plain-text scripts, one per chapter  <- edit these
tools/        this pipeline
models/       Kokoro weights (~350 MB, gitignored, re-downloadable)
audio/        chNN.mp3, what the page actually plays
samples/      short auditions for picking a voice and a speed
```

## First run

```sh
python -m venv .venv
.venv\Scripts\activate            # Windows;  source .venv/bin/activate elsewhere
pip install -r tools/requirements.txt
python tools/generate-audio.py --fetch-model
python tools/generate-audio.py
```

The full render is about 45 minutes of CPU for about 50 minutes of audio,
roughly real time. It only has to happen once — reruns skip any chapter whose
script hasn't changed.

## Why this runs on the CPU

`--device` accepts `cpu` (default), `dml`, `cuda` or `auto`, but on this
machine CPU is the only one that works, and it's worth writing down why so the
experiment isn't repeated.

**DirectML fails outright.** `onnxruntime-directml` 1.24.4 installs fine and
reports `DmlExecutionProvider`, but the first inference dies:

```
RUNTIME_EXCEPTION : Non-zero status code returned while running ConvTranspose
node. Name:'/encoder/F0.1/pool/ConvTranspose' ... 80070057 The parameter is incorrect.
```

The DML provider *claims* that node and then fails on it, so onnxruntime never
falls back to CPU for it and the whole session dies. This is not a "slower than
CPU" outcome — nothing renders at all.

**CUDA needs a driver update first.** Current `onnxruntime-gpu` wants CUDA 12,
which needs an NVIDIA driver of roughly 527 or newer. The driver here is
462.30, which caps at CUDA 11.2. The GTX 1650 is Turing and is still supported
by current drivers, so updating is possible — and then `--device cuda` is worth
a try. Until then it will exit with a clear message rather than silently
spending an hour on the CPU.

For reference, the CPU baseline measured on this machine:

```
CPU  ch09: 11 paragraphs, 118.4s audio in 125.2s  ->  0.95x realtime
```

Roughly real time, so the full course costs about as long to render as it does
to listen to. Note that RAM matters more than cores here: with 8.5 GB total,
per-chapter times swing between 70s and 165s depending on what else is open,
which is also why there's no `--jobs` flag. Parallel workers would each need
their own ~500 MB copy of the model.

## Editing the narration

The scripts in `narration/` are the source of truth, and they're deliberately
plain text: one chapter per file, blank line between paragraphs. Each blank
line becomes a real pause in the audio, so paragraph breaks are pacing, not
just formatting.

Change a sentence, then:

```sh
python tools/generate-audio.py --only 09
```

Only chapter 09 re-renders (about 90 seconds), and the new duration is patched
back into `mcp-course.html` automatically.

These are *spoken* adaptations, not the page's prose read aloud. Tables, JSON
frames and code don't survive being read out, so the narration points at the
interactive panels instead of reciting them, and carries the argument in a
register meant for the ear: shorter sentences, more signposting, the
occasional aside. If a line sounds wrong, fix the wording in `narration/` —
don't reach for the pronunciation table in `generate-audio.py` unless it's
genuinely an acronym problem.

Two conventions worth knowing when you edit:

- **Write for the ear, not the eye.** `M×N` becomes "M by N", `tools/list`
  becomes "the tools list request", `400 Bad Request` becomes "four hundred,
  bad request". The scripts already do this throughout.
- **Spell initialisms with dots** — `C.L.I.`, `I.A.M.`, `R.F.C.` — and the
  pipeline says them letter by letter. It also knows that the final dot is
  both part of the acronym *and* a full stop when a new sentence follows, so
  "…single sign-on, I.A.M. A wrapper is lossy" keeps its pause. Undotted
  `MCP`, `API`, `JSON`, `HTTP` and friends are handled by name.

## Choosing a voice

`samples/` has the same passage in every credible English voice, at three
speeds, and in several blends. Listen, then re-render with your pick:

```sh
python tools/generate-audio.py --voice bm_george --force
python tools/generate-audio.py --list-voices          # 50+ others
```

### Blending

Kokoro voices are style vectors, so they average — and the average is a
perfectly good voice. `--voice` takes a blend spec:

```sh
--voice "bm_george+bm_fable"          # even mix
--voice "bm_george*0.65+bm_fable*0.35"  # weighted; weights are normalised
--voice "bf_emma*0.6+af_heart*0.4"    # borrow a better-trained voice's quality
```

This is worth knowing because of an awkward fact about the voice set: the two
best-trained voices in Kokoro (`af_heart`, `af_bella`) are American, while the
best British one only reaches a B−. A blend lets you keep the accent that
matches the document's spelling without giving up the quality.

A blend's phonemisation language follows its components — all-`b*` voices get
`en-gb`, anything else `en-us`. Override with `--lang` if you disagree.

The default is **`bf_emma`** at **speed 0.9** — British, to match the
document's spelling ("standardises", "optimisation", "flavours"), and slowed
a little because Kokoro's default pace lands near 195 words per minute, which
is brisk for teaching material. 0.9 puts it around 170. Listeners can speed it
back up in the player.

Voices starting `b` are British and `a` American; the script picks `en-gb` or
`en-us` phonemisation to match.

## How it reaches the page

`generate-audio.py` writes the durations into `mcp-course.html` between these
markers:

```js
/* AUDIO-MANIFEST:BEGIN ... */
var AUDIO = { dir: "audio/", voice: "bf_emma", tracks: { ch00: {...} } };
/* AUDIO-MANIFEST:END */
```

They're inlined rather than fetched, because the page is meant to work when
opened straight off disk — `fetch()` on a `file://` URL is blocked, but
`<audio src>` is not.

The player then injects itself only after one track has actually loaded. So
`mcp-course.html` on its own, with no `audio/` folder next to it, is still the
same self-contained single file it was before: no broken play buttons, no
console errors, nothing to explain.

## Shipping it

`audio/` is about 20 MB and worth committing — it's the deliverable. `models/`
is not; it's a 350 MB build dependency, and `--fetch-model` gets it back.
