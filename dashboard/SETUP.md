# RAG Evaluation Dashboard — Google Apps Script

## Files
- `Code.gs` — server-side dashboard data + web app entry point
- `Index.html` — dashboard structure
- `Styles.html` — visual design
- `Scripts.html` — charts, insights, dropdown comparison, sorting
- `appsscript.json` — Apps Script manifest

## Deploy
1. Go to script.google.com and create a new Apps Script project.
2. Replace the default `Code.gs` with this project's `Code.gs`.
3. Add three HTML files named exactly:
   - `Index`
   - `Styles`
   - `Scripts`
4. Paste the matching file contents into each.
5. Optional: enable **Show appsscript.json manifest file** in Project Settings and replace it with this manifest.
6. Click **Deploy → New deployment → Web app**.
7. Execute as: **Me**.
8. Choose the access level appropriate for the interview/demo and deploy.

## Updating metrics
All evaluation data is centralized in `DASHBOARD_DATA` at the top of `Code.gs`.
Replace only score values after rerunning `compare.py`; the charts, rankings, deltas, correlation, and insight text recalculate automatically.

## What the dashboard now includes
- KPI cards for the winning configuration
- Horizontal composite leaderboard
- Evaluation Intelligence section with metric-grounded analytical insights
- Exploratory Context Recall ↔ Correctness correlation
- Controlled-experiment impact bar chart
- Three controlled-experiment cards
- Two-dropdown configuration comparator
- Radar chart + metric deltas
- Context-aware comparison insights
- Sortable full evaluation matrix

## Recommended interview flow
1. Start with the KPI row and `final_combined` winner.
2. Use the leaderboard to show the overall ranking.
3. Explain the Evaluation Intelligence findings:
   - coverage beats retrieval purity on this benchmark,
   - chunk size was the strongest isolated lever,
   - top-k exposes the precision/recall trade-off,
   - MPNet did not improve end-to-end quality,
   - faithfulness is saturated and therefore not discriminative here.
4. Use the experiment-impact chart to make the controlled deltas visual.
5. Click an experiment card to load it into the comparator.
6. Finish with the full matrix and limitations.


## Analysis data module

`AnalysisData.gs` contains query-type breakdowns and curated failure-analysis cases. Keep it as a separate Apps Script `.gs` file alongside `Code.gs`.

## v4 fixed layout

The dashboard now uses two top-level tabs:

- **Overview** — KPIs, leaderboard, benchmark insights, controlled experiments, configuration comparator, and full metric matrix.
- **Diagnostics** — query-type performance and curated failure analysis.

The query-type summary uses a responsive card grid rather than a single horizontal strip, so all seven categories wrap cleanly across desktop, tablet, and mobile widths.
