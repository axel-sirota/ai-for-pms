"""
Classical ML Playground — AI for Product Managers
Train models on sample datasets, see metrics and feature importance. No code required.
"""

import gradio as gr
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_absolute_error, mean_squared_error, r2_score,
    confusion_matrix
)
import io
import json

# ── Embedded Sample Datasets ─────────────────────────────────────────────────

def make_churn_dataset():
    np.random.seed(42)
    n = 500
    tenure = np.random.randint(1, 72, n)
    monthly_charges = np.round(np.random.uniform(20, 120, n), 2)
    total_charges = np.round(tenure * monthly_charges * np.random.uniform(0.8, 1.1, n), 2)
    support_calls = np.random.poisson(2, n)
    contract_type = np.random.choice([0, 1, 2], n, p=[0.5, 0.3, 0.2])  # month, 1yr, 2yr
    # Churn logic: short tenure + high charges + many calls + month-to-month
    churn_prob = 1 / (1 + np.exp(-(
        -2 + (-0.03 * tenure) + (0.02 * monthly_charges) +
        (0.3 * support_calls) + (-0.8 * contract_type) +
        np.random.normal(0, 0.5, n)
    )))
    churned = (churn_prob > 0.5).astype(int)
    return pd.DataFrame({
        "tenure_months": tenure,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "support_calls": support_calls,
        "contract_type": contract_type,
        "churned": churned
    })


def make_fraud_dataset():
    np.random.seed(43)
    n = 500
    amount = np.round(np.random.exponential(200, n), 2)
    hour = np.random.randint(0, 24, n)
    distance_from_home = np.round(np.random.exponential(50, n), 1)
    num_transactions_24h = np.random.poisson(5, n)
    is_online = np.random.choice([0, 1], n, p=[0.6, 0.4])
    fraud_prob = 1 / (1 + np.exp(-(
        -4 + (0.003 * amount) + (0.1 * (hour < 5).astype(int)) +
        (0.01 * distance_from_home) + (0.15 * num_transactions_24h) +
        (0.5 * is_online) + np.random.normal(0, 0.5, n)
    )))
    is_fraud = (fraud_prob > 0.5).astype(int)
    return pd.DataFrame({
        "amount": amount,
        "hour_of_day": hour,
        "distance_from_home_km": distance_from_home,
        "transactions_last_24h": num_transactions_24h,
        "is_online": is_online,
        "is_fraud": is_fraud
    })


def make_house_prices_dataset():
    np.random.seed(44)
    n = 500
    sqft = np.random.randint(600, 4000, n)
    bedrooms = np.random.choice([1, 2, 3, 4, 5], n, p=[0.1, 0.25, 0.35, 0.2, 0.1])
    bathrooms = np.clip(bedrooms + np.random.choice([-1, 0, 1], n, p=[0.2, 0.5, 0.3]), 1, 5)
    age_years = np.random.randint(0, 80, n)
    garage = np.random.choice([0, 1, 2], n, p=[0.2, 0.5, 0.3])
    price = np.round(
        50000 + 150 * sqft + 10000 * bedrooms + 15000 * bathrooms -
        500 * age_years + 20000 * garage + np.random.normal(0, 30000, n), -3
    )
    return pd.DataFrame({
        "sqft": sqft,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms.astype(int),
        "age_years": age_years,
        "garage_spaces": garage,
        "price": price.astype(int)
    })


def make_segmentation_dataset():
    np.random.seed(45)
    n = 500
    age = np.random.randint(18, 70, n)
    income = np.round(np.random.lognormal(10.5, 0.6, n), 0).astype(int)
    spend_score = np.clip(np.round(
        30 + 0.3 * (income / 1000) - 0.2 * age + np.random.normal(0, 15, n)
    ), 1, 100).astype(int)
    visits_per_month = np.clip(np.random.poisson(4, n), 0, 20)
    online_ratio = np.round(np.clip(np.random.beta(2, 3, n) + 0.01 * (70 - age), 0, 1), 2)
    # Segment: high_value if income > median AND spend_score > median
    median_income = np.median(income)
    median_spend = np.median(spend_score)
    high_value = ((income > median_income) & (spend_score > median_spend)).astype(int)
    return pd.DataFrame({
        "age": age,
        "annual_income": income,
        "spend_score": spend_score,
        "visits_per_month": visits_per_month,
        "online_purchase_ratio": online_ratio,
        "high_value_customer": high_value
    })


DATASETS = {
    "Customer Churn (Classification)": ("churn", make_churn_dataset, "churned"),
    "Fraud Detection (Classification)": ("fraud", make_fraud_dataset, "is_fraud"),
    "House Prices (Regression)": ("house", make_house_prices_dataset, "price"),
    "Customer Segmentation (Classification)": ("segment", make_segmentation_dataset, "high_value_customer"),
}

# ── Core Training Logic ───────────────────────────────────────────────────────

def load_dataset(dataset_name, uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df, list(df.columns)
    if dataset_name in DATASETS:
        _, gen_fn, target = DATASETS[dataset_name]
        df = gen_fn()
        return df, target
    return None, None


def train_and_evaluate(dataset_name, uploaded_file, target_col, test_size, model_choice):
    try:
        # Load data
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            target = target_col
        elif dataset_name in DATASETS:
            _, gen_fn, target = DATASETS[dataset_name]
            df = gen_fn()
        else:
            return "Select a dataset first.", None, None

        if target not in df.columns:
            return f"Target column '{target}' not found in dataset.", None, None

        # Prepare features
        X = df.drop(columns=[target])
        y = df[target]

        # Encode categorical features
        encoders = {}
        for col in X.select_dtypes(include=["object", "category"]).columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le

        # Detect task type
        is_classification = y.nunique() <= 10 and y.dtype in [np.int64, np.int32, int, np.float64]
        if y.dtype == object:
            le_y = LabelEncoder()
            y = pd.Series(le_y.fit_transform(y))
            is_classification = True

        if not is_classification and y.nunique() <= 10:
            is_classification = True

        # Split
        split = test_size / 100.0
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split, random_state=42)

        # Scale
        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train)
        X_test_s = scaler.transform(X_test)

        # Train models
        results = {}
        models = {}

        if model_choice in ["Both", "Random Forest"]:
            if is_classification:
                rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
            else:
                rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
            rf.fit(X_train, y_train)
            models["Random Forest"] = rf

        if model_choice in ["Both", "Logistic / Linear Regression"]:
            if is_classification:
                lr = LogisticRegression(max_iter=1000, random_state=42)
            else:
                lr = LinearRegression()
            lr.fit(X_train_s, y_train)
            models["Logistic / Linear Regression"] = lr

        # Evaluate
        task_type = "Classification" if is_classification else "Regression"
        metrics_text = f"## Results\n**Task type:** {task_type}\n"
        metrics_text += f"**Training samples:** {len(X_train)} | **Test samples:** {len(X_test)}\n\n"
        metrics_text += "| Model | " + (" | ".join(
            ["Accuracy", "Precision", "Recall", "F1"] if is_classification
            else ["MAE", "RMSE", "R2"]
        )) + " |\n"
        metrics_text += "|" + "---|" * (5 if is_classification else 4) + "\n"

        for name, model in models.items():
            if name == "Logistic / Linear Regression":
                preds = model.predict(X_test_s)
            else:
                preds = model.predict(X_test)

            if is_classification:
                acc = accuracy_score(y_test, preds)
                prec = precision_score(y_test, preds, average="weighted", zero_division=0)
                rec = recall_score(y_test, preds, average="weighted", zero_division=0)
                f1 = f1_score(y_test, preds, average="weighted", zero_division=0)
                metrics_text += f"| **{name}** | {acc:.3f} | {prec:.3f} | {rec:.3f} | {f1:.3f} |\n"
                results[name] = {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1}
            else:
                mae = mean_absolute_error(y_test, preds)
                rmse = np.sqrt(mean_squared_error(y_test, preds))
                r2 = r2_score(y_test, preds)
                metrics_text += f"| **{name}** | ${mae:,.0f} | ${rmse:,.0f} | {r2:.3f} |\n"
                results[name] = {"mae": mae, "rmse": rmse, "r2": r2}

        # Feature importance chart
        fig_importance = None
        if "Random Forest" in models:
            rf_model = models["Random Forest"]
            importances = rf_model.feature_importances_
            feat_names = list(X.columns)
            sorted_idx = np.argsort(importances)
            fig_importance = go.Figure(go.Bar(
                x=importances[sorted_idx],
                y=[feat_names[i] for i in sorted_idx],
                orientation="h",
                marker_color="#3b82f6"
            ))
            fig_importance.update_layout(
                title="Feature Importance (Random Forest)",
                xaxis_title="Importance",
                yaxis_title="Feature",
                height=max(300, len(feat_names) * 40),
                margin=dict(l=20, r=20, t=50, b=30)
            )

        # What-If JSON for state
        feature_info = []
        for col in X.columns:
            feature_info.append({
                "name": col,
                "min": float(X[col].min()),
                "max": float(X[col].max()),
                "mean": float(X[col].mean()),
                "is_int": bool(X[col].dtype in [np.int64, np.int32])
            })

        state = {
            "feature_info": feature_info,
            "is_classification": is_classification,
            "feature_names": list(X.columns),
            "target": target,
        }

        return metrics_text, fig_importance, json.dumps(state)

    except Exception as e:
        return f"Error: {str(e)}", None, None


def get_columns(dataset_name, uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        cols = list(df.columns)
        return gr.update(choices=cols, value=cols[-1])
    if dataset_name in DATASETS:
        _, gen_fn, target = DATASETS[dataset_name]
        df = gen_fn()
        return gr.update(choices=list(df.columns), value=target)
    return gr.update(choices=[], value=None)


def predict_what_if(dataset_name, uploaded_file, model_choice, *feature_values):
    """Make a prediction with user-supplied feature values."""
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            target = df.columns[-1]
        elif dataset_name in DATASETS:
            _, gen_fn, target = DATASETS[dataset_name]
            df = gen_fn()
        else:
            return "Select a dataset first."

        X = df.drop(columns=[target])
        y = df[target]

        is_classification = y.nunique() <= 10
        if y.dtype == object:
            le_y = LabelEncoder()
            y = pd.Series(le_y.fit_transform(y))
            is_classification = True

        for col in X.select_dtypes(include=["object", "category"]).columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))

        # Build input row
        input_vals = list(feature_values[:len(X.columns)])
        if len(input_vals) < len(X.columns):
            return "Not enough feature values provided."

        input_row = pd.DataFrame([input_vals], columns=X.columns)

        # Train model on full data for what-if
        if is_classification:
            model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X, y)
        pred = model.predict(input_row)[0]

        if is_classification:
            proba = model.predict_proba(input_row)[0]
            result = f"## Prediction: **{int(pred)}**\n\n"
            result += "| Class | Probability |\n|---|---|\n"
            for i, p in enumerate(proba):
                bar = "█" * int(p * 20)
                result += f"| {i} | {p:.1%} {bar} |\n"
        else:
            result = f"## Predicted Value: **${pred:,.0f}**\n"

        return result

    except Exception as e:
        return f"Error: {str(e)}"


# ── Gradio UI ─────────────────────────────────────────────────────────────────

with gr.Blocks(title="Classical ML Playground", theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown(
        "# Classical ML Playground\n\n"
        "**PM Decision:** When your team proposes an ML project, use this tool to understand "
        "what they're actually building. You'll see how models learn from data, which features "
        "drive predictions, and what the accuracy numbers really mean.\n\n"
        "Train a model on real-world datasets — no code required. See predictions, metrics, "
        "and **which features matter most**."
    )

    state_json = gr.State("")

    with gr.Tab("1. Choose Data"):
        gr.Markdown("### Select a sample dataset or upload your own CSV")
        dataset_dd = gr.Dropdown(
            choices=list(DATASETS.keys()),
            value="Customer Churn (Classification)",
            label="Sample Dataset"
        )
        upload = gr.File(label="Or upload CSV (optional)", file_types=[".csv"])
        target_dd = gr.Dropdown(label="Target Column (what to predict)", interactive=True)
        dataset_dd.change(get_columns, [dataset_dd, upload], [target_dd])
        upload.change(get_columns, [dataset_dd, upload], [target_dd])

        preview_btn = gr.Button("Preview Data", variant="secondary")
        preview_df = gr.Dataframe(label="Data Preview (first 10 rows)")

        def show_preview(name, file):
            if file is not None:
                df = pd.read_csv(file)
            elif name in DATASETS:
                _, fn, _ = DATASETS[name]
                df = fn()
            else:
                return pd.DataFrame()
            return df.head(10)

        preview_btn.click(show_preview, [dataset_dd, upload], [preview_df])

    with gr.Tab("2. Train & Evaluate"):
        gr.Markdown("### Configure and train your model")
        with gr.Row():
            test_slider = gr.Slider(10, 40, value=20, step=5, label="Test Set Size (%)")
            model_dd = gr.Dropdown(
                choices=["Both", "Random Forest", "Logistic / Linear Regression"],
                value="Both",
                label="Model"
            )
        train_btn = gr.Button("Train Model", variant="primary")
        metrics_out = gr.Markdown(label="Metrics")
        importance_chart = gr.Plot(label="Feature Importance")

        train_btn.click(
            train_and_evaluate,
            [dataset_dd, upload, target_dd, test_slider, model_dd],
            [metrics_out, importance_chart, state_json]
        )

    with gr.Tab("3. What-If Predictor"):
        gr.Markdown(
            "### Change feature values and see the prediction update\n"
            "First train a model in Tab 2, then adjust sliders below."
        )
        # 6 generic sliders (covers all sample datasets)
        sliders = []
        for i in range(6):
            s = gr.Number(label=f"Feature {i+1}", value=0, visible=(i < 6))
            sliders.append(s)

        predict_btn = gr.Button("Predict", variant="primary")
        whatif_out = gr.Markdown()

        def update_sliders(dataset_name, uploaded_file):
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
            elif dataset_name in DATASETS:
                _, fn, target = DATASETS[dataset_name]
                df = fn()
                df = df.drop(columns=[target])
            else:
                return [gr.update()] * 6
            updates = []
            cols = list(df.columns)
            for i in range(6):
                if i < len(cols):
                    col = cols[i]
                    updates.append(gr.update(
                        label=col,
                        value=float(df[col].median()),
                        visible=True
                    ))
                else:
                    updates.append(gr.update(visible=False, value=0))
            return updates

        dataset_dd.change(update_sliders, [dataset_dd, upload], sliders)

        predict_btn.click(
            predict_what_if,
            [dataset_dd, upload, model_dd] + sliders,
            [whatif_out]
        )

    # Load defaults
    demo.load(get_columns, [dataset_dd, upload], [target_dd])
    demo.load(update_sliders, [dataset_dd, upload], sliders)

    gr.Markdown(
        "---\n"
        "**PM Takeaway:** Feature importance shows what drives predictions — ask your team "
        "which features have the biggest impact and whether they make business sense.\n\n"
        "*AI for Product Managers*"
    )


if __name__ == "__main__":
    demo.launch()
