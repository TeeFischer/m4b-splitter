
import subprocess
import json
import os
import shutil
import sys

def split_audiobook(filename):
    if not os.path.isfile(filename):
        print("File not found:", filename)
        return

    missing_tools = [
        tool for tool in ("ffprobe", "ffmpeg")
        if shutil.which(tool) is None
    ]
    if missing_tools:
        print(
            "Required FFmpeg tools not found: "
            + ", ".join(missing_tools)
            + ". Install FFmpeg, add its bin folder to PATH, "
            + "and restart VS Code. (I installed on Windows in PowerShell"
            + " 'winget install --id Gyan.FFmpeg.Shared -e')"
        )
        return

    # Read chapter information
    result = subprocess.run(
        [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_chapters", filename
        ],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("ffprobe could not read the audiobook:")
        print(result.stderr.strip())
        return

    data = json.loads(result.stdout)
    chapters = data.get("chapters", [])

    if not chapters:
        print("No chapters found in this audiobook!")
        return

    output_dir = os.path.splitext(filename)[0] + "_chapters"
    os.makedirs(output_dir, exist_ok=True)

    print(f"Found {len(chapters)} chapters.")

    for i, chapter in enumerate(chapters):
        start = float(chapter["start_time"])
        end = float(chapter["end_time"])

        title = chapter.get("tags", {}).get(
            "title", f"Chapter {i+1}"
        )

        safe_title = "".join(
            c for c in title
            if c.isalnum() or c in " -_"
        ).strip()

        if not safe_title:
            safe_title = f"Chapter {i+1}"

        output = os.path.join(
            output_dir,
            f"{i+1:03d} - {safe_title}.mp3"
        )

        print(f"Creating: {output}")

        result = subprocess.run([
            "ffmpeg", "-y",
            "-ss", str(start),
            "-i", filename,
            "-t", str(end - start),
            "-map", "0:a:0",
            "-vn",
            "-codec:a", "libmp3lame",
            "-q:a", "2",
            output
        ], stdout=subprocess.DEVNULL,
           stderr=subprocess.PIPE,
           text=True)
        if result.returncode != 0:
            print(f"ffmpeg failed to create {output}:")
            print(result.stderr.strip())
            return

    print("\nDone! Chapters saved in:", output_dir)


if __name__ == "__main__":
    print("=== M4B Audiobook Splitter ===\n")
    filepath = (
        sys.argv[1]
        if len(sys.argv) > 1
        else input("Enter the full path to your M4B file:\n").strip().strip('"')
    )

    split_audiobook(filepath)

    if len(sys.argv) == 1:
        input("\nPress Enter to exit...")
