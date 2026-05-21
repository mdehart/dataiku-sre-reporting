# PagerDuty SRE Event Fetcher & Reporting

An automated data pipeline built in Dataiku DSS to extract, tag, and aggregate PagerDuty SRE (Site Reliability Engineering) incident events. This repository tracks the version-controlled recipes, python notebooks, scenarios, and metadata configurations for the project.
graph LR
    %% Palette Configuration
    classDef default fill:#1e1e24,stroke:#4a4a4f,stroke-width:1px,color:#d1d1d6;
    classDef pythonNode fill:#2c3e50,stroke:#34495e,stroke-width:1px,color:#ecf0f1;
    classDef dataNode fill:#204060,stroke:#2980b9,stroke-width:1px,color:#e0f2fe;
    classDef recipeNode fill:#594010,stroke:#d4ac0d,stroke-width:1px,color:#fef9e7;
    classDef mergeNode fill:#5d4037,stroke:#a1887f,stroke-width:1px,color:#efebe9;

    %% Top Pipeline (Low Severity)
    P1([Python script]) :::pythonNode --> D1[support_low_incidents] :::dataNode
    D1 --> R1{{Prepare recipe}} :::recipeNode
    R1 --> D2[support_low_incidents_prepared] :::dataNode

    %% Bottom Pipeline (High Severity)
    P2([Python script]) :::pythonNode --> D3[support_high_incidents] :::dataNode
    D3 --> R2{{Prepare recipe}} :::recipeNode
    R2 --> D4[support_high_incidents_prepared] :::dataNode

    %% Merge & Final Output
    D2 --> M1{{Stack recipe}} :::mergeNode
    D4 --> M1
    M1 --> D5[support_incidents_combined] :::dataNode

    %% Global Background Layout (Styling for markdown viewports)
    style P1 rx:15,ry:15
    style P2 rx:15,ry:15
## Project Overview

This project automates the ingestion and normalization of PagerDuty operational incident data to enable centralized SRE reporting. It separates incidents into discrete severity streams, normalizes the tracking metadata, and combines them into a unified reporting dataset.
<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/e5f6658c-ae57-465f-a2f5-6c6ca2ca4eb5" />
## 🛠️ Data Pipeline Architecture

1. **Ingestion (Python Fetch Scripts)**
   * Utilizes the PagerDuty API endpoint to fetch raw incident log events.
   * Splits incidents based on tracking heuristics into two distinct operational buckets: `support_high_incidents` and `support_low_incidents`.

2. **Data Enrichment & Normalization (Prepare Recipes)**
   * **High Stream:** Processes severe incidents and injects a static tracking tag column: `incident_severity_level = "high"`.
   * **Low Stream:** Processes standard support incidents and injects a matching tracking tag column: `incident_severity_level = "low"`.

3. **Consolidation (Stack Recipe)**
   * Stacks both prepared datasets together into a single master output dataset: `support_incidents_P2OE4T3_PWVQZNH_stacked`.
   * Unifies schemas automatically based on identical columns so the source context (`high` vs `low`) is preserved in a single column without structural separation.

## 🕒 Automation & Orchestration

The pipeline runs completely hands-free via a Dataiku **Time-based Scenario**:
* **Schedule:** Weekly (Every Monday at 2:00 AM)
* **Execution Strategy:** `Build everything upstream` — Triggering the scenario automatically forces the underlying Python scripts to query the fresh week's API logs, run the rows through the visual prepare steps, and refresh the final reporting dataset.

## 🗂️ Repository Structure

This repository reflects the standard version-control export format for a Dataiku project:
* `/recipes/` - JSON schemas and configurations defining the data flow transformations (prepare steps, stack alignments).
* `/scenarios/` - Automated tracking and triggering rules for the weekly refresh jobs.
* `/dashboards/` - Reporting layouts and metrics visualizations for SRE review.
* `/datasets/` - Metadata schemas and connectivity parameters for the input/output tables.
