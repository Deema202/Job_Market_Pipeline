# Job Market ETL Pipeline

An end-to-end Data Engineering ETL (Extract, Transform, Load) pipeline built with Python, SQLAlchemy, and SQLite. The pipeline extracts real-time technology job market data from the **Adzuna API**, cleans and imputes missing metrics, and loads the structured data into a **Star Schema** relational database for analytical querying.

---

## 🏗️ Architecture & Data Model

The pipeline transforms raw JSON data from the Adzuna API into a **Star Schema** to optimize analytical performance and reporting.

### Star Schema Design
* **Fact Table:**
  * `fact_jobs`: Contains metrics (salary_min, salary_max, salary_avg) and foreign keys referencing dimension tables.
* **Dimension Tables:**
  * `dim_company`: Company names and attributes.
  * `dim_location`: Geographic attributes (location name, country, region, coordinates).
  * `dim_category`: Job categories and tags.
  * `dim_contract`: Employment types (e.g., permanent, contract).
  * `dim_date`: Date attributes (full date, year, month, day) derived from job posting timestamps.

---

## 📁 Repository Structure

```text
├── database.py         # SQLAlchemy ORM models (Star Schema definition)
├── extract.py          # Extraction module (fetches data from Adzuna API)
├── transform.py        # Transformation module (cleaning & salary imputation)
├── load.py             # Loading module (populates dimensions and fact table)
├── main.py             # Main pipeline orchestrator script
├── sample_response.json# Sample API raw data backup
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation