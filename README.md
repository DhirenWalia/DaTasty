# DaTasty

## Overview

DaTasty is an AI-enabled data readiness assessment platform built to profile, validate, score, clean, and report on tabular datasets. It supports CSV and Excel inputs and generates a detailed Excel report along with cleaned dataset output.

## Key Features

- Data ingestion from CSV and Excel files
- Dataset profiling and metadata extraction
- Data quality checks for:
  - Completeness (missing values)
  - Uniqueness and duplicate detection
  - Business key duplicate analysis
  - Validity against configurable rules
  - Consistency checks
  - Accuracy and outlier detection
- DTS scoring for AI readiness
- Business recommendations based on quality findings
- Rule-driven data cleaning and transformation
- Excel report generation in `data/output/`
- Optional Streamlit dashboard frontend

## Repository Structure

- `main.py` - CLI entry point for running the analysis pipeline
- `src/engine.py` - Core engine class for end-to-end dataset processing
- `src/ingestion/loader.py` - Data loading utilities for CSV and Excel
- `src/profiling/profiler.py` - Dataset profiling and metadata generation
- `src/quality/` - Data quality modules for completeness, uniqueness, validity, consistency, and accuracy
- `src/scoring/dts_calculator.py` - DTS scoring engine for dataset readiness
- `src/recommendations/advisor.py` - Business recommendation generation
- `src/cleaning/smart_cleaner.py` - Rule-driven cleaning and normalization
- `src/reporting/report_generator.py` - Excel report generation logic
- `dashboard/app.py` - Streamlit dashboard frontend
- `config/rules.json` - Data validation and cleaning rules
- `data/` - Sample input, benchmark data, and generated outputs

## Installation

1. Create or activate a Python virtual environment.

```bash
python -m venv datatsty_env
source datatsty_env/Scripts/activate   # Windows PowerShell
# or
source datatsty_env/bin/activate      # macOS/Linux
```

2. Install requirements.

```bash
pip install -r requirement.txt
```

## Requirements

The project dependencies are listed in `requirement.txt` and include:

- pandas
- numpy
- openpyxl
- sqlalchemy
- streamlit
- plotly
- matplotlib
- seaborn
- scikit-learn
- python-dateutil
- xlsxwriter

## Usage

### CLI Runner

Run the main Python application and provide the path to your dataset when prompted.

```bash
python main.py
```

Example input paths:

- `data/input/customer_data.csv`
- `data/benchmark/DATATSTY_Enterprise_Benchmark_v1.csv`

### Streamlit Dashboard

Launch the dashboard frontend with Streamlit.

```bash
streamlit run dashboard/app.py
```

Or use the deployed app:

https://datasty.streamlit.app/

Upload a CSV or Excel file, then click `Analyze Dataset`.

## Configuration

The `config/rules.json` file defines validation and cleaning rules per column. Sample rule types include:

- `datatype` checks
- required fields
- business key and uniqueness flags
- regex validation patterns
- cleaning pipeline steps such as `trim`, `lower`, `upper`, and `title`
- phone standardization and date formatting

## Output

Generated outputs are written to `data/output/`:

- `DATATSTY_Enterprise_Report.xlsx` — full audit and quality findings report
- `cleaned_dataset.csv` — cleaned dataset after applying rules

## Notes

- The engine currently supports CSV and Excel file formats only.
- The cleaning engine applies rules only for columns defined in `config/rules.json`.
- The DTS score is computed from completeness, uniqueness, validity, consistency, and accuracy dimensions.

## Contributing

To extend the platform, add new quality checks in `src/quality/`, update scoring logic in `src/scoring/dts_calculator.py`, or enhance report generation in `src/reporting/report_generator.py`.
