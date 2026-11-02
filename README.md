# M4B Splitter

Split an M4B audiobook into separate MP3 files, one per chapter. Chapter titles are used for output filenames when available.

## Requirements

- Python 3
- FFmpeg, with `ffmpeg` and `ffprobe` available on your `PATH`

## Usage

Run the script and provide the audiobook path when prompted:

```powershell
python m4b_splitter.py
```

Or pass the path directly:

```powershell
python m4b_splitter.py "path\to\audiobook.m4b"
```

The MP3 chapters are saved in a `<audiobook>_chapters` folder beside the input file. In VS Code, you can also run `m4b_splitter.py` with **Run and Debug** and enter the path when prompted.
