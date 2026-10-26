# science-programme-ops

Tools and documents for running the science side of a hyperspectral Earth-observation company: getting
papers and talks cleared for publication, and finding research partners. Written with Pixxel's Science
Programme in mind; the data and the analysis are public.

## What's here

| Folder | What it is |
|---|---|
| `landscape/` | `landscape.py` pulls every paper since 2021 with an Indian author and "hyperspectral" in the title or abstract from OpenAlex (2,938 papers), and writes `landscape.md`: the most active institutions, which satellites they use, and who already works with spaceborne hyperspectral data. |
| `partnerships/` | `proposal.md`: three partnerships drawn from that data, with the reasons and the limits. `pipeline.md`: the stages from first contact to a joint paper. |
| `process/` | `publication-review.md`: a review process for papers, posters and talks, with roles, a confidentiality checklist and times for each stage. |
| `tracker/` | `pubtrack.py`: checks a CSV of submissions against the process rules and shows what will miss its deadline. Standard library only. |

## Run it

```bash
cd landscape && python3 landscape.py          # ~15 requests to OpenAlex, cached in landscape/cache/
cd tracker && python3 pubtrack.py check submissions_example.csv
cd tracker && python3 pubtrack.py status submissions_example.csv --today 2026-10-28
cd tracker && python3 -m unittest discover -s tests
```

OpenAlex now gives requests without an API key a small shared daily budget. One run of `landscape.py`
fits easily; for repeated runs set `OPENALEX_API_KEY` (free from openalex.org).

## Notes on the data

- Counts are OpenAlex records, so they carry its coverage gaps and affiliation errors. The point is the
  ranking and the pattern, not the exact numbers.
- Sensor names are matched as whole words in titles and abstracts. "PRISMA" is also a reporting guideline
  for systematic reviews and "EMIT" is also a verb, so those two get a stricter check.
- `tracker/submissions_example.csv` is invented example data.
