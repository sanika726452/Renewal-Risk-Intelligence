# Renewal Risk Intelligence

A Python-based renewal risk intelligence prototype for BizOps teams. The project ingests account, usage, ticket, NPS, CSM note, and changelog signals, builds a unified account-level customer 360 view, scores renewal risk, and generates plain-English explanations plus recommended actions.

## What the solution does

- Ingests all provided source datasets from the raw folder
- Cleans and normalizes the account, support, usage, and NPS records
- Engineers product-health and customer-health features
- Uses an LLM call through OpenRouter/OpenAI-compatible APIs for note analysis when an API key is available
- Falls back to a deterministic heuristic analysis when the key is not configured so the demo remains runnable
- Produces a ranked renewal report and a Streamlit dashboard for exploration

## Architecture

- `main.py` runs the full batch pipeline and writes outputs to the `outputs/` folder
- `src/services/` handles data loading, cleaning, merging, and parsing
- `src/scoring/risk_engine.py` calculates renewal risk bands and confidence
- `src/reporting/report_generator.py` converts raw signals into concise, customer-facing explanations
- `src/analysis/llm_analyzer.py` + `src/services/llm_service.py` perform note-level AI analysis
- `app.py` provides a simple interactive Streamlit demo

## Run locally

1. Create or activate the project virtual environment.
2. Install dependencies:

   `pip install -r requirements.txt`

3. Optionally set an LLM key in `.env`:

   `OPENROUTER_API_KEY=<your-key>`

4. Run the batch pipeline:

   `python main.py`

5. Launch the demo UI:

   `streamlit run app.py`

## Notable analysis choices

- The changelog is treated as a migration-risk signal, not just a historical artifact. The parser surfaces deprecated SDKs and migration pressure, which helps explain renewal risk that would be invisible from purely tabular usage data.
- The CSM notes are noisy, so the current pipeline uses regex-based account extraction and a robust fallback analysis path. This keeps the workflow stable even in low-token or no-LLM settings.
- The non-obvious insight is that customers still bound to legacy SDK patterns are often at elevated risk even when their current NPS is moderate. The changelog + usage + support signal combination makes that pattern much clearer.

## Tradeoffs and production improvements

- Right now, the project favors a transparent, explainable scoring model over a highly exotic model architecture.
- The LLM path is intentionally lightweight and robust: if the external API is unavailable, the system still produces a usable result from keyword heuristics.
- For production, I would add:
  - a dedicated entity-resolution step for account-name matching
  - model versioning and prompt version tracking
  - a real observability layer for API failures and fallback rates
  - a stricter governance process for LLM output validation and auditability
  - a scheduled pipeline with persistent data-quality checks

## Deliverable summary

The repository now includes:

- an end-to-end Python pipeline
- a Streamlit dashboard demo
- generated outputs in `outputs/`
- a README with the approach and run instructions
