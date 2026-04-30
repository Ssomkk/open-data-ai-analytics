import os
import json
import pandas as pd
from flask import Flask, render_template, jsonify, send_from_directory

app = Flask(__name__)

# ── Paths ─────────────────────────────────────────────────────────────────────
_HERE    = os.path.dirname(os.path.abspath(__file__))   # .../web
_PROJECT = os.path.dirname(_HERE)                        # project root


def _resolve(env_var: str, local_fallback: str) -> str:
    """Use env var only when the path actually exists; otherwise use local fallback."""
    val = os.environ.get(env_var, "")
    if val and os.path.exists(val):
        return val
    return local_fallback


BASE_DATA    = _resolve("DATA_DIR",    os.path.join(_PROJECT, "data", "raw"))
BASE_REPORT  = _resolve("REPORTS_DIR", os.path.join(_PROJECT, "reports", "lab1"))
FIGURES_DIR  = os.path.join(BASE_REPORT, "figures")

CLEAN_CSV     = os.path.join(BASE_DATA,   "clean_data.csv")
QUALITY_JSON  = os.path.join(BASE_REPORT, "quality_report.json")
RESEARCH_JSON = os.path.join(BASE_REPORT, "research_report.json")

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_clean_data():
    """Load cleaned CSV and return as list-of-dicts."""
    try:
        df = pd.read_csv(CLEAN_CSV)
        return df.head(50).fillna("").to_dict(orient="records"), list(df.columns)
    except Exception as e:
        return [], []


def load_quality_report():
    """Load quality report JSON or derive it from the CSV on-the-fly."""
    if os.path.exists(QUALITY_JSON):
        with open(QUALITY_JSON) as f:
            return json.load(f)

    # Derive on-the-fly from clean_data.csv
    try:
        df = pd.read_csv(CLEAN_CSV)
        report = {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "missing_values": {k: int(v) for k, v in df.isna().sum().items()},
            "duplicates": int(df.duplicated().sum()),
            "dtypes": {k: str(v) for k, v in df.dtypes.items()},
            "missing_total": int(df.isna().sum().sum()),
        }
        return report
    except Exception as e:
        return {"error": str(e)}


def load_research_report():
    """Load research report JSON or derive it from the CSV on-the-fly."""
    if os.path.exists(RESEARCH_JSON):
        with open(RESEARCH_JSON) as f:
            return json.load(f)

    try:
        df = pd.read_csv(CLEAN_CSV)
        numeric = df.select_dtypes(include="number")
        desc = numeric.describe().round(4).to_dict()

        stations = df["station"].value_counts().to_dict() if "station" in df.columns else {}

        # Per-year averages
        yearly = {}
        if "year" in df.columns:
            for col in ["cs_137_emission", "co_60_ emission", "irg"]:
                if col in df.columns:
                    yearly[col] = df.groupby("year")[col].mean().round(4).to_dict()

        report = {
            "describe": desc,
            "stations": stations,
            "yearly_avg": yearly,
        }
        return report
    except Exception as e:
        return {"error": str(e)}


def list_figures():
    """Return sorted list of PNG filenames found in the figures directory."""
    if not os.path.exists(FIGURES_DIR):
        return []
    return sorted(f for f in os.listdir(FIGURES_DIR) if f.endswith(".png"))


# ── Dynamic figure serving (reads directly from FIGURES_DIR) ──────────────────
@app.route("/figures/<path:filename>")
def serve_figure(filename):
    """Serve PNG figures from the reports directory (works locally & in Docker)."""
    return send_from_directory(FIGURES_DIR, filename)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    figures   = list_figures()
    quality   = load_quality_report()
    research  = load_research_report()
    rows, cols = load_clean_data()
    return render_template(
        "index.html",
        figures=figures,
        quality=quality,
        research=research,
        data_rows=rows,
        data_cols=cols,
    )


@app.route("/data")
def data_page():
    rows, cols = load_clean_data()
    return render_template("data.html", data_rows=rows, data_cols=cols)


@app.route("/quality")
def quality_page():
    report = load_quality_report()
    return render_template("quality.html", report=report)


@app.route("/research")
def research_page():
    report = load_research_report()
    return render_template("research.html", report=report)


@app.route("/visualizations")
def visualizations_page():
    figures = list_figures()
    return render_template("visualizations.html", figures=figures)


@app.route("/api/quality")
def api_quality():
    return jsonify(load_quality_report())


@app.route("/api/research")
def api_research():
    return jsonify(load_research_report())


@app.route("/api/figures")
def api_figures():
    return jsonify(list_figures())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
