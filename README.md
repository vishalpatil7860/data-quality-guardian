# Data Quality Guardian

A lightweight, open-source data quality monitoring tool for data engineers. Run configurable checks against your databases, track trends over time, and get alerted when data quality drops.

## Features

- **Completeness** — detect nulls and missing values
- **Uniqueness** — find duplicates and violated unique constraints
- **Freshness** — monitor how recently data was updated
- **Volume** — track row counts and detect unexpected drops
- **Schema Drift** — detect column additions, removals, or type changes
- **Referential Integrity** — check foreign key relationships
- **Custom SQL** — write your own arbitrary checks
- **Trend Tracking** — check results stored in SQLite for historical analysis
- **Dashboard** — Streamlit web UI for visualizing trends
- **CLI** — run checks, view history, generate reports
- **Reports** — console, JSON, and Markdown output

## Quick Start

```bash
pip install -r requirements.txt
cp examples/example_config.yaml dq_config.yaml
# Edit dq_config.yaml with your database connection
python -m dqguardian.cli run
python -m dqguardian.cli dashboard
```

## Requirements

- Python 3.10+
- SQLAlchemy, PyYAML, Click, Rich, Streamlit, Plotly, Pandas

All dependencies are free and open-source.