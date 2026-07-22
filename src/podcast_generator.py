# -*- coding: utf-8 -*-
"""
Dual-Host Podcast Audio Generator
==================================

Converts a Markdown dialogue script into a dual-host podcast MP3 using
Microsoft Edge-TTS neural voices.

Voice configuration:
  - Host A (male): zh-CN-YunxiNeural
  - Host B (female): zh-CN-XiaoxiaoNeural

Features:
  - Async edge-tts generation with concurrency control
  - Per-segment caching (resume on failure)
  - Natural pauses between sentences and sections
  - No system ffmpeg required (uses imageio-ffmpeg bundled binary)

Usage:
    python podcast_generator.py -i script.md -o podcast.mp3

Script format (Markdown):
    ## Section Title

    **Host A:** Hello and welcome...

    **Host B:** Today we'll talk about...

    ---

    **A:** The next point is...
    **B:** Really? Tell me more.
"""
import argparse
import asyncio
import os
import re
import sys
import wave
import subprocess

import edge_tts
import imageio_ffmpeg

# ---------- Voice Configuration ----------
VOICE_A = "zh-CN-YunxiNeural"    # Host A (male)
VOICE_B = "zh-CN-XiaoxiaoNeural"  # Host B (female)
RATE_A = "-3%"                    # Speech rate adjustment for Host A
RATE_B = "-1%"                    # Speech rate adjustment for Host B

# ---------- Pause Configuration ----------
PAUSE_SEC = 0.38      # Pause between consecutive sentences (seconds)
SEG_PAUSE_SEC = 0.65   # Pause when switching sections (seconds)

# ---------- FFmpeg ----------
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def parse_script(path):
    """Parse a Markdown dialogue script into a list of (speaker, text, section) tuples.

    Supported formats:
      - **Host A:** text
      - **A:** text
      - **A：** text  (fullwidth colon)
    """
    dialogues = []
    # Matches: **Host A:** text  /  **A:** text  /  **A：** text
    pattern = re.compile(
        r'^\*\*(?:Host\s*|主播\s*)?([AB])(?:[：:])?\*\*\s*[：:]?\s*(.+)$'
    )
    section = 0
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.strip().startswith('## ') or line.strip() == '---':
                section += 1
            m = pattern.match(line)
            if m and m.group(2).strip():
                dialogues.append((m.group(1), m.group(2).strip(), section))
    return dialogues


async def synthesize_one(text, voice, rate, out_path):
    """Generate a single audio segment using edge-tts."""
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(out_path)


async def generate_all(dialogues, cache_dir):
    """Generate all TTS segments with caching and retry logic."""
    sem = asyncio.Semaphore(4)  # Limit concurrent requests
    total = len(dialogues)

    for i, (speaker, text, _) in enumerate(dialogues):
        out = os.path.join(cache_dir, f"seg_{i:03d}.mp3")

        # Skip if already cached and valid
        if os.path.exists(out) and os.path.getsize(out) > 100:
            print(f"  [{i+1}/{total}] Host {speaker} (cached) ok  {text[:24]}...",
                  flush=True)
            continue

        voice = VOICE_A if speaker == 'A' else VOICE_B
        rate = RATE_A if speaker == 'A' else RATE_B

        async with sem:
            success = False
            for attempt in range(3):
                try:
                    await synthesize_one(text, voice, rate, out)
                    success = True
                    break
                except Exception as e:
                    print(f"  Retry {attempt+1}/3: segment {i} "
                          f"[Host {speaker}] - {e}", flush=True)
                    await asyncio.sleep(2)

            if not success:
                raise RuntimeError(
                    f"Segment {i} failed after 3 retries: {text[:30]}"
                )

        print(f"  [{i+1}/{total}] Host {speaker} ok  {text[:24]}...",
              flush=True)


def merge_audio(dialogues, cache_dir, out_wav, out_mp3):
    """Merge all TTS segments into a single WAV (with pauses), then export MP3."""
    total = len(dialogues)

    # Step 1: Convert each MP3 segment to WAV (24kHz mono 16-bit)
    print("\nConverting segments to WAV...", flush=True)
    for i in range(total):
        mp3 = os.path.join(cache_dir, f"seg_{i:03d}.mp3")
        wav = os.path.join(cache_dir, f"seg_{i:03d}.wav")

        if os.path.exists(wav) and os.path.getsize(wav) > 100:
            continue

        subprocess.run(
            [FFMPEG, "-y", "-i", mp3,
             "-ar", "24000", "-ac", "1",
             "-acodec", "pcm_s16le", wav],
            check=True, capture_output=True
        )
        print(f"  [{i+1}/{total}] ok", flush=True)

    # Step 2: Concatenate WAV segments with natural pauses
    print("\nConcatenating audio with pauses...", flush=True)
    with wave.open(out_wav, 'wb') as out:
        params_set = False
        prev_section = -1
        sampwidth = framerate = None

        for i in range(total):
            wav_path = os.path.join(cache_dir, f"seg_{i:03d}.wav")
            with wave.open(wav_path, 'rb') as w:
                if not params_set:
                    p = w.getparams()
                    out.setparams(p)
                    sampwidth = p.sampwidth
                    framerate = p.framerate
                    params_set = True

                # Insert pause before this segment (except the first)
                if i > 0:
                    pause = (SEG_PAUSE_SEC
                             if dialogues[i][2] != prev_section
                             else PAUSE_SEC)
                    silence = b'\x00' * int(sampwidth * framerate * pause)
                    out.writeframes(silence)

                out.writeframes(w.readframes(w.getnframes()))
                prev_section = dialogues[i][2]

    # Step 3: Export to MP3 (192kbps)
    print("\nExporting MP3 (192kbps)...", flush=True)
    subprocess.run(
        [FFMPEG, "-y", "-i", out_wav, "-b:a", "192k", out_mp3],
        check=True, capture_output=True
    )


def main():
    parser = argparse.ArgumentParser(
        description="Dual-Host Podcast Audio Generator (edge-tts)"
    )
    parser.add_argument(
        "-i", "--input", required=True,
        help="Input Markdown script (with **Host A:** / **Host B:** format)"
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Output MP3 file path"
    )
    parser.add_argument(
        "--cache", default=None,
        help="TTS cache directory (default: auto-generated from output name)"
    )
    args = parser.parse_args()

    script_path = os.path.abspath(args.input)
    out_mp3 = os.path.abspath(args.output)
    out_wav = out_mp3.rsplit('.', 1)[0] + ".wav"

    # Determine cache directory
    if args.cache:
        cache_dir = os.path.abspath(args.cache)
    else:
        base = os.path.splitext(os.path.basename(out_mp3))[0]
        cache_dir = os.path.join(
            os.path.dirname(out_mp3), f"_tts_cache_{base}"
        )
    os.makedirs(cache_dir, exist_ok=True)

    if not os.path.exists(script_path):
        print(f"Error: Script not found: {script_path}", flush=True)
        sys.exit(1)

    # Parse script
    print(f"Parsing script: {script_path}", flush=True)
    dialogues = parse_script(script_path)

    a_count = sum(1 for d in dialogues if d[0] == 'A')
    b_count = sum(1 for d in dialogues if d[0] == 'B')
    print(f"Total: {len(dialogues)} segments | "
          f"Host A (male): {a_count} | Host B (female): {b_count}",
          flush=True)

    if not dialogues:
        print("Error: No dialogue found. Use **Host A:** or **A:** format.",
              flush=True)
        sys.exit(3)

    print(f"Cache directory: {cache_dir}", flush=True)

    # Generate TTS
    print("\nGenerating speech with edge-tts...", flush=True)
    try:
        asyncio.run(generate_all(dialogues, cache_dir))
    except Exception as e:
        print(f"\nGeneration failed: {e}", flush=True)
        sys.exit(2)

    # Merge audio
    merge_audio(dialogues, cache_dir, out_wav, out_mp3)

    # Report results
    size_mb = os.path.getsize(out_mp3) / (1024 * 1024)
    with wave.open(out_wav, 'rb') as w:
        duration = w.getnframes() / w.getframerate()
    minutes, seconds = int(duration // 60), int(duration % 60)

    print(f"\n=== Generation Complete ===", flush=True)
    print(f"  File:     {out_mp3}", flush=True)
    print(f"  Duration: {minutes}m {seconds}s", flush=True)
    print(f"  Size:     {size_mb:.1f} MB", flush=True)
    print(f"  Codec:    MP3 192kbps", flush=True)


if __name__ == "__main__":
    main()
