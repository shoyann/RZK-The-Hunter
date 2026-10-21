# Visual evidence boards

Use a board when a side-by-side comparison makes a visual finding easier to
assess, or when the user asks for one. A short location answer does not need a
board. Work within the existing investigation budget; do not search for more
images solely to fill the layout.

The helper assembles inspected local images. It does not search, score similarity,
validate sources, establish geometric alignment or decide that a claim is true.
Apply the investigation's evidence gate before describing a conclusion as verified.
A useful provisional board can also show why a candidate remains uncertain.

## Choose the evidence

- Use the supplied image as the subject and one to four useful reference panels.
  References may be photographs, a map, a plan or a documented crop. A map is
  optional; include it only when it supports the relevant spatial relationship.
- Record each panel's publisher/photographer and source URL, or an explicit local
  source identifier for supplied material. Keep copyright credits when known.
  Reposts of one photograph remain one source lineage.
- Write specific observed matches, such as window divisions or path order.
  Include material mismatches, different viewpoints, image dates when relevant,
  unresolved background objects and other limitations. Do not hide contradictions
  behind a polished layout or invent numeric confidence.
- A building match does not establish the camera position. Leave camera status
  unverified unless actual evidence establishes the position. A building centroid,
  mailing address, guessed marker or visual resemblance alone is insufficient.
- Preserve original files. If a crop, redaction or other transformation is needed,
  save a separate derivative and describe it in the caption with a link to its
  source. Do not use generative reconstruction as evidence. The renderer does not
  redact people, plates or other sensitive content automatically.

## Prepare a spec

Save UTF-8 JSON beside the case images. Paths resolve relative to the spec file;
the helper reads local files only and never fetches a URL. The example below is
a method template, not a finding: replace its filenames, credits and observations
with the case's actual inspected evidence.

```json
{
  "schema_version": 1,
  "title": "Building comparison — provisional finding",
  "subject": {
    "image": "original.jpg",
    "caption": "Supplied photograph",
    "source": "User-supplied original; capture date unknown"
  },
  "references": [
    {
      "image": "reference.jpg",
      "caption": "Published exterior; a different viewpoint",
      "source": "Publisher / photographer — https://example.org/replace-with-source"
    },
    {
      "image": "plan-crop.png",
      "caption": "Crop of site plan; camera position not marked",
      "source": "Plan author — https://example.org/replace-with-plan-source"
    }
  ],
  "matches": [
    "Curved facade and window divisions agree with the reference view."
  ],
  "uncertainties": [
    "The background building has not been independently identified.",
    "No same-viewpoint image or metric camera alignment is available."
  ],
  "camera": {"status": "unverified"}
}
```

`schema_version`, `subject` and `references` are required. Every panel requires
nonempty `image`, `caption` and `source` strings. `title` is optional. `matches`
and `uncertainties` are optional arrays of strings; omit them when no claim has
been made rather than manufacturing a match. Camera status defaults to
`unverified`. Use `{"status":"verified","evidence":"E7: measured pose; case/pose.json"}`
only when that evidence exists and supports the claim. The helper checks that a
supporting note is present, not whether the note is true.

## Render and inspect

```bash
uv run scripts/evidence_board.py case/board.json --out case/evidence.png
```

The script declares Pillow as an optional runtime dependency for `uv run`.
Alternatively install `Pillow>=10.4` in your Python environment and invoke it
with `python`. Other Hunter helpers do not require Pillow.

For Chinese or other text unsupported by the available default fonts, supply a
font with the necessary glyphs:

```bash
uv run scripts/evidence_board.py case/board.json --out case/evidence.png \
  --font /path/to/NotoSansCJK-Regular.ttc
```

The renderer fits images without stretching or cropping them, normalizes EXIF
orientation for display, and puts source credits and limitations on the board.
Long text is wrapped; inputs outside supported limits fail rather than silently
disappearing. Review the actual PNG for readable credits, correct glyphs, source
alignment, panel proportions and visible uncertainties before delivering it.
Shorten prose or choose a suitable font when needed; never remove a material
limitation just to improve the layout.

The output pair is `evidence.png` and `evidence.json`. The sidecar records input
hashes, captions, sources, display transformations and the supplied claim status.
Hashes identify the files used; they do not certify their authenticity. Provenance
records identify the local input paths, so review them before external sharing.
Existing outputs are protected unless `--force` is supplied. Even with `--force`,
the output paths must not overwrite the spec, source images or selected font.

Keep case photographs, downloaded references and generated boards outside the
public skill repository unless their publication has been authorized. Deliver the
board alongside the answer and sources; it does not replace the underlying
evidence record or justify additional precision.
