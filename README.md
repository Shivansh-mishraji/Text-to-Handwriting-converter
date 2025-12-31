Text-to-Handwriting Converter

Usage

- Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

- Convert a text string to handwriting PNG:

```powershell
python file.py --text "Hello world" --output out.png
```

- Convert a text file to handwriting PNG:

```powershell
python file.py --input-file notes.txt --output notes.png
```

Notes

- The script uses `pywhatkit.text_to_handwriting` where available for realistic handwriting. If `pywhatkit` is missing or fails, it falls back to a PIL-based renderer that uses system fonts and per-character jitter to emulate handwriting.
- On Windows, installing a handwriting font (e.g., "Segoe Script", "Bradley Hand") and passing `--font PATH_TO_TTF` improves realism.
