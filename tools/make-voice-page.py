#!/usr/bin/env python3
"""Build mcp-course-voice.html: the course page pointed at the cloned track.

    python tools/make-voice-page.py                    # audio-qwen -> mcp-course-voice.html
    python tools/make-voice-page.py --audio audio-clone --out mcp-course-chatterbox.html

Reads mcp-course.html, swaps the audio manifest for one built from the real
durations of the mp3s in the chosen directory, and writes a second page.
The Kokoro page is never modified: both tracks stay playable side by side,
which is the only way to compare them honestly.

Durations come from the files rather than from stamps.json, so the page
cannot drift from what is actually on disk.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEGIN = "/* AUDIO-MANIFEST:BEGIN"
END = "AUDIO-MANIFEST:END */"


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audio", default="audio-qwen",
                    help="Directory holding the chapter mp3s. Default audio-qwen.")
    ap.add_argument("--out", default="mcp-course-voice.html")
    ap.add_argument("--voice", default="Anuj (Qwen3-TTS 0.6B clone)",
                    help="Shown in the player credit line.")
    ap.add_argument("--engine", default="Qwen3-TTS 0.6B",
                    help="Replaces 'Kokoro-82M' in the credit line.")
    args = ap.parse_args()

    try:
        import soundfile as sf
    except ImportError:
        sys.exit("Needs soundfile:  pip install soundfile")

    src = ROOT / "mcp-course.html"
    dst = ROOT / args.out
    audio = ROOT / args.audio

    if not src.exists():
        sys.exit("Missing %s" % src)
    if dst.resolve() == src.resolve():
        sys.exit("Refusing to overwrite %s -- that is the Kokoro page." % src.name)
    if not audio.is_dir():
        sys.exit("Missing %s" % audio)

    html = src.read_text(encoding="utf-8")
    if BEGIN not in html or END not in html:
        sys.exit("Manifest markers not found in %s" % src.name)

    tracks = {f.stem: round(sf.info(str(f)).duration, 1)
              for f in sorted(audio.glob("ch*.mp3"))}
    if not tracks:
        sys.exit("No ch*.mp3 files in %s" % audio)

    entries = ",\n".join('    %s: { f: "%s.mp3", d: %.1f }' % (c, c, d)
                         for c, d in sorted(tracks.items()))
    block = (BEGIN + " · clone track · regenerate with tools/make-voice-page.py */\n"
             "var AUDIO = {\n"
             '  dir: "%s/",\n'
             '  voice: "%s",\n'
             "  tracks: {\n%s\n  }\n};\n/* " % (args.audio, args.voice, entries) + END)

    start, end = html.index(BEGIN), html.index(END) + len(END)
    out = html[:start] + block + html[end:]

    old_credit = '"Narrated offline with Kokoro-82M"'
    if out.count(old_credit) == 1:
        out = out.replace(old_credit, '"Narrated offline with %s"' % args.engine, 1)
    else:
        print("! credit line not found; the page will still say Kokoro-82M")

    m = re.search(r"<title>(.*?)</title>", out, re.S)
    if m and "voice" not in m.group(1).lower():
        out = out.replace(m.group(0), "<title>%s (my voice)</title>"
                          % m.group(1).strip(), 1)

    dst.write_text(out, encoding="utf-8")
    missing = [c for c in tracks if not (audio / (c + ".mp3")).exists()]
    print("wrote %s" % dst.name)
    print("  %d chapters, %.1f min, from %s/" % (len(tracks),
                                                 sum(tracks.values()) / 60, args.audio))
    if missing:
        print("  ! missing files: %s" % ", ".join(missing))
    print("  %s untouched" % src.name)


if __name__ == "__main__":
    main()
