# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Enhanced data pipeline automation
- Real-time data monitoring dashboard
- Predictive analytics for radiation trends
- Multi-language support (Ukrainian, English, Russian)

## [0.1.0] - 2026-03-05

### Added
- Initial project structure with comprehensive documentation
- Data loading pipeline (`src/data_load.py`) for downloading public datasets from data.gov.ua
- Automated data quality analysis notebook (`notebooks/data_quality_analysis.ipynb`)
- Data research and exploration notebook (`notebooks/data_research.ipynb`)
- Data visualization notebook (`notebooks/data_visualization.ipynb`)
- Raw data files:
  - `nuclear_safety_q4_2025.xlsx` - Q4 2025 nuclear safety measurements
  - `pasport-naboru-danikh.xlsx` - Data collection passport/metadata
  - `clean_data.csv` - Processed and cleaned dataset
- Report visualizations:
  - Average IRG index by nuclear power station
  - Average IRG measurements by station
  - Co-60 emission dynamics by year
  - Cs-137 emission dynamics by year
  - Correlation matrix analysis
  - Data distribution analysis
  - Overall emission dynamics trends
  - Nuclear power stations overview
- Project README with problem statement and research questions
- Analysis focused on three key areas:
  1. Trends in Cs-137 and Co-60 emissions over recent years
  2. Comparative analysis of radiation background across different NPPs
  3. Permitted vs actual emission levels assessment

### Features
- Automated data ingestion from Ukraine's open data portal (data.gov.ua)
- Quality assurance checks for data consistency
- Exploratory data analysis capabilities
- Statistical visualization and reporting
- Support for monitoring ecological and radiation conditions around nuclear power plants (NPPs)

### Technical Stack
- Python 3.x
- Pandas for data manipulation
- Jupyter Notebooks for analysis and documentation
- Excel/CSV data formats
- Git version control

## Project Information

**Project Name:** Аналіз відкритих даних: Екологічна та радіаційна обстановка в зоні АЕС  
(Open Data AI Analytics)

**Data Source:** [Ukraine's Open Data Portal - Ecological and Radiation Conditions](https://data.gov.ua/dataset/4a9d3d56-bd95-4c3e-97e7-1cdc7bcbd445)

**Purpose:** Create a simple pipeline for analyzing and monitoring ecological conditions around nuclear power plants using open government data.
