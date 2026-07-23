<img width="1368" height="289" alt="Screenshot 2026-07-23 at 1 16 17 AM" src="https://github.com/user-attachments/assets/1acc5d7e-95b9-4ff0-9bea-58984ca489d7" />

Data Observability Sample App

A minimal, self-contained example of building and deploying a data-quality dashboard as a Databricks App. Built to walk through the full loop — simulated data → Streamlit dashboard → GitHub → Databricks Apps deployment via Git — using nothing but a free Databricks workspace and a GitHub repo.

What this is

This app simulates 30 days of data-quality metrics (Completeness, Timeliness, Uniqueness, and an Overall Health score) across 6 example tables, then visualizes them in a Streamlit dashboard with:

Top-line KPI tiles for the latest day
A trend chart you can switch between metrics
A sortable snapshot table of the latest score per table

It's meant as a teaching example for anyone learning how Databricks Apps works end-to-end — not a production data quality tool.

Project structure
data-observability-sample/
├── app.py                   # Streamlit dashboard
├── app.yaml                 # Tells Databricks Apps how to run the app
├── requirements.txt         # Python dependencies
├── generate_sample_data.py  # Script that generates the simulated dataset
└── data/
    └── dq_metrics.csv       # Generated sample data (30 days x 6 tables)
Run it locally
bash
git clone https://github.com/<your-username>/data-observability-sample.git
cd data-observability-sample
pip install -r requirements.txt
streamlit run app.py

Regenerate the sample dataset at any time with:

bash
python generate_sample_data.py
Deploy to Databricks Apps (via Git)

This app is set up to deploy straight from a GitHub repo — no manual file uploads needed.

Fork or clone this repo to your own GitHub account.
In your Databricks workspace, go to Compute → Apps → + Create app → Create a custom app.
In the Configure Git step, enter your repo URL (https://github.com/<your-username>/data-observability-sample) and select GitHub as the provider.
Set the Git reference to main.
If your repo is private, add a Git credential (GitHub personal access token with repo scope) via Configure Git credential on the app overview page.
(Optional) Enable Auto deploy on push events so every git push redeploys the app automatically.
Click Create app, then Deploy.

Databricks will pull the repo, read app.yaml, install requirements.txt, and start the Streamlit app. Once status shows Running, open the app URL to see the dashboard live.

Adapting this for real data

Swap out data/dq_metrics.csv for a live query — for example, point app.py at a Databricks SQL warehouse or a Delta table using the Databricks SDK instead of pandas.read_csv. The dashboard layout and charts will work unchanged as long as the resulting DataFrame keeps the same column names.

License

Feel free to fork, adapt, and reuse for your own learning or internal demos.
