# Research Lines Update Summary

## Overview
Successfully updated `data/research_lines.json` with publication data from `data/papers.json`.

## What Was Added

For each research line, the following information was added when researchers with publications were found:

### 1. Publication Statistics
- **total_papers**: Total number of papers from all researchers in the line
- **total_citations**: Total citations from all researchers in the line
- **h_index_max**: Maximum h-index among researchers in the line
- **average_papers_per_researcher**: Average papers per researcher
- **average_citations_per_researcher**: Average citations per researcher
- **researchers_count**: Number of researchers with publications

### 2. Researchers Publications
For each researcher with publications:
- Name and Scholar profile information
- Research interests
- Publication statistics (total papers, citations, h-index, i10-index)
- Top 5 most cited papers with full details

## Results

- **Total research lines**: 125
- **Research lines with publications**: 40
- **Researchers matched**: 8

### Top Research Lines by Publications

1. **Ciência de Dados**: 100 papers, 2,020 citations (5 researchers)
2. **Inteligência Computacional**: 100 papers, 1,772 citations (5 researchers)
3. **Inteligência Artificial**: 60 papers, 1,872 citations (3 researchers)
4. **Engenharia de Software**: 60 papers, 1,378 citations (3 researchers)

### Researchers Matched

1. **Paulo Sérgio Dos Santos Júnior** - 20 papers, 409 citations
2. **Rodrigo Fernandes Calhau** - 20 papers, 218 citations
3. **Fabiano Borges Ruy** - 20 papers, 751 citations
4. **Mateus Conrad Barcellos Da Costa** - 20 papers, 70 citations
5. **Hilario Oliveira** - 20 papers, 480 citations
6. **Daniel Cruz Cavalieri** - 20 papers, 273 citations
7. **Francisco de Assis Boldt** - 20 papers, 712 citations
8. **Sérgio Nery Simões** - 20 papers, 269 citations

## Metadata Updates

- Added `last_updated` timestamp
- Added `papers_data_generated_at` reference to source data

## Example Structure

```json
{
  "name": "Inteligência Artificial",
  "publication_statistics": {
    "total_papers": 60,
    "total_citations": 1872,
    "h_index_max": 14,
    "average_papers_per_researcher": 20.0,
    "average_citations_per_researcher": 624.0,
    "researchers_count": 3
  },
  "researchers_publications": [
    {
      "name": "Fabiano Borges Ruy",
      "scholar_id": "StrLqxIAAAAJ",
      "scholar_url": "https://scholar.google.com/citations?user=StrLqxIAAAAJ",
      "interests": ["Software Engineering", "Software Processes", ...],
      "total_papers": 20,
      "total_citations": 751,
      "h_index": {"all_time": "14", "since_2020": "8"},
      "i10_index": {"all_time": "16", "since_2020": "7"},
      "top_5_papers": [...]
    }
  ]
}
```

## Files Modified

- `data/research_lines.json` - Updated with publication data

## Files Created

- `update_research_lines.py` - Python script for updating research lines
- `RESEARCH_LINES_UPDATE_SUMMARY.md` - This summary document
