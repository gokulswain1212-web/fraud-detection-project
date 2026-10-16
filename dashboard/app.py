import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
from pathlib import Path
import sys

# Add parent directory to path to import backend modules
sys.path.append(str(Path(__file__).parent.parent))

from backend.features import engineer_transaction, to_model_frame, PRE_APPROVAL_FEATURES, POST_PROCESSING_FEATURES

# Page configuration
st.set_page_config(
    page_title="FraudGuard AI Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: #1e293b;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Load Models ----------
@st.cache_resource
def load_models():
    """Load the trained fraud detection models"""
    base_dir = Path(__file__).parent.parent
    model_dir = base_dir / "models" / "production"

    pre_model_path = model_dir / "fraud_preapproval_model.pkl"
    post_model_path = model_dir / "fraud_postprocessing_model.pkl"

    pre_model = None
    post_model = None

    if pre_model_path.exists():
        pre_model = joblib.load(pre_model_path)
        st.success("✅ Pre-approval model loaded")

    if post_model_path.exists():
        post_model = joblib.load(post_model_path)
        st.success("✅ Post-processing model loaded")

    return pre_model, post_model

pre_model, post_model = load_models()

# ---------- Header ----------
st.markdown('<h1 class="main-header">🛡️ FraudGuard AI Analytics Dashboard</h1>', unsafe_allow_html=True)
st.markdown("Real-time fraud detection analytics and monitoring")

st.divider()

# ---------- Sidebar ----------
st.sidebar.header("⚙️ Dashboard Controls")

# Navigation
page = st.sidebar.radio(
    "Select Page",
    ["📊 Overview", "🔍 Live Prediction", "📈 Model Performance", "📋 Transaction Data"]
)

# ---------- Overview Page ----------
if page == "📊 Overview":
    st.header("📊 Dashboard Overview")

    # Sample transaction statistics (replace with real data if available)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Model Accuracy", "99.99%", "Post-processing")
    with col2:
        st.metric("Response Time", "< 100ms", "Real-time")
    with col3:
        st.metric("Features", "12", "Post-processing")
    with col4:
        st.metric("Models", "2", "Pre + Post")

    st.divider()

    # Model comparison
    st.subheader("🤖 Model Performance Comparison")

    colA, colB = st.columns(2)

    with colA:
        st.markdown("### Pre-Approval Model")
        st.info("**Accuracy:** 99.92%")
        st.info("**Fraud Precision:** 77.79%")
        st.info("**Fraud Recall:** 54.35%")
        st.info("**Features:** 6")
        st.info("**Use Case:** Real-time screening")

    with colB:
        st.markdown("### Post-Processing Model")
        st.success("**Accuracy:** 99.99%")
        st.success("**Fraud Precision:** 100%")
        st.success("**Fraud Recall:** 99.33%")
        st.success("**Features:** 12")
        st.success("**Use Case:** Enhanced analysis")

    st.divider()

    # Feature information
    st.subheader("🔍 Features Used by Models")

    tab1, tab2 = st.tabs(["Pre-Approval Features", "Post-Processing Features"])

    with tab1:
        st.write("**Pre-Approval Model (6 features):**")
        for feature in PRE_APPROVAL_FEATURES:
            st.write(f"- {feature}")

    with tab2:
        st.write("**Post-Processing Model (12 features):**")
        for feature in POST_PROCESSING_FEATURES:
            st.write(f"- {feature}")

# ---------- Live Prediction Page ----------
elif page == "🔍 Live Prediction":
    st.header("🔍 Live Transaction Analysis")

    if pre_model is None and post_model is None:
        st.error("❌ No models loaded. Please ensure model files exist in models/production/")
        st.stop()

    # Transaction input form
    st.subheader("Enter Transaction Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        transaction_type = st.selectbox(
            "Transaction Type",
            ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]
        )
        step = st.number_input("Step", min_value=0, value=1)
        amount = st.number_input("Amount ($)", min_value=0.0, value=9839.64)

    with col2:
        old_balance_org = st.number_input("Sender Old Balance ($)", min_value=0.0, value=170136.0)
        old_balance_dest = st.number_input("Receiver Old Balance ($)", min_value=0.0, value=0.0)

    with col3:
        new_balance_org = st.number_input("Sender New Balance ($)", min_value=0.0, value=160296.36)
        new_balance_dest = st.number_input("Receiver New Balance ($)", min_value=0.0, value=0.0)

    # Analyze button
    if st.button("🔍 Analyze Transaction", type="primary", use_container_width=True):
        with st.spinner("Analyzing transaction..."):
            # Prepare transaction data
            transaction_data = {
                "Step": step,
                "Type": transaction_type,
                "Amount": amount,
                "Oldbalanceorg": old_balance_org,
                "Oldbalancedest": old_balance_dest,
            }

            # Add optional fields if provided
            if new_balance_org > 0 or new_balance_dest > 0:
                transaction_data["Newbalanceorig"] = new_balance_org
                transaction_data["Newbalancedest"] = new_balance_dest

            # Determine which model to use
            has_new_balances = "Newbalanceorig" in transaction_data and "Newbalancedest" in transaction_data

            if has_new_balances and post_model is not None:
                # Use post-processing model
                features = POST_PROCESSING_FEATURES
                model = post_model
                model_name = "Post-Processing"
            elif pre_model is not None:
                # Use pre-approval model
                features = PRE_APPROVAL_FEATURES
                model = pre_model
                model_name = "Pre-Approval"
            else:
                st.error("❌ No suitable model available")
                st.stop()

            # Engineer features
            try:
                engineered = engineer_transaction(transaction_data)
                frame = to_model_frame(engineered, features)

                # Make prediction
                prediction = int(model.predict(frame)[0])

                # Get probability
                probability = None
                if hasattr(model, "predict_proba"):
                    probability = float(model.predict_proba(frame)[0][1])

                # Display results
                st.divider()
                st.subheader("🎯 Analysis Results")

                result_col1, result_col2 = st.columns(2)

                with result_col1:
                    if prediction == 1:
                        st.error("🚨 **POTENTIAL FRAUD DETECTED**")
                    else:
                        st.success("✅ **LEGITIMATE TRANSACTION**")

                with result_col2:
                    if probability is not None:
                        prob_pct = probability * 100
                        st.metric("Fraud Probability", f"{prob_pct:.2f}%")

                st.divider()

                # Model information
                st.info(f"**Model Used:** {model_name}")
                st.info(f"**Features Analyzed:** {len(features)}")

                # Features used
                with st.expander("View Features Analyzed"):
                    for feature in features:
                        st.write(f"- {feature}")

                # Warning
                st.warning("⚠️ **Disclaimer:** This is a model prediction, not a confirmed fraud finding. Always verify with additional checks before taking action.")

            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")

# ---------- Model Performance Page ----------
elif page == "📈 Model Performance":
    st.header("📈 Model Performance Metrics")

    # Load performance reports if available
    base_dir = Path(__file__).parent.parent
    reports_dir = base_dir / "mlops" / "monitoring" / "reports"

    pre_report_path = reports_dir / "fraud_preapproval_report.csv"
    post_report_path = reports_dir / "fraud_postprocessing_report.csv"

    tab1, tab2 = st.tabs(["Pre-Approval Model", "Post-Processing Model"])

    with tab1:
        st.subheader("Pre-Approval Model Performance")

        if pre_report_path.exists():
            df_pre = pd.read_csv(pre_report_path)
            st.dataframe(df_pre, use_container_width=True)

            # Create visualization
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Accuracy", f"{df_pre['accuracy'].values[0]:.4f}")
                st.metric("Fraud Precision", f"{df_pre['fraud_precision'].values[0]:.4f}")

            with col2:
                st.metric("Fraud Recall", f"{df_pre['fraud_recall'].values[0]:.4f}")
                st.metric("Fraud F1-Score", f"{df_pre['fraud_f1'].values[0]:.4f}")
        else:
            st.warning("Performance report not found. Run model evaluation to generate reports.")

    with tab2:
        st.subheader("Post-Processing Model Performance")

        if post_report_path.exists():
            df_post = pd.read_csv(post_report_path)
            st.dataframe(df_post, use_container_width=True)

            # Create visualization
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Accuracy", f"{df_post['accuracy'].values[0]:.4f}")
                st.metric("Fraud Precision", f"{df_post['fraud_precision'].values[0]:.4f}")

            with col2:
                st.metric("Fraud Recall", f"{df_post['fraud_recall'].values[0]:.4f}")
                st.metric("Fraud F1-Score", f"{df_post['fraud_f1'].values[0]:.4f}")
        else:
            st.warning("Performance report not found. Run model evaluation to generate reports.")

    st.divider()

    # Data drift report
    st.subheader("📊 Data Drift Monitoring")

    drift_report_path = reports_dir / "data_drift_report.csv"

    if drift_report_path.exists():
        df_drift = pd.read_csv(drift_report_path)
        st.dataframe(df_drift, use_container_width=True)

        # Highlight significant drift
        significant_drift = df_drift[df_drift['Significant Difference'] == True]
        if not significant_drift.empty:
            st.warning(f"⚠️ **Significant data drift detected in {len(significant_drift)} feature(s):")
            for _, row in significant_drift.iterrows():
                st.write(f"- {row['Feature']}: KS Statistic = {row['KS Statistic']:.4f}")
        else:
            st.success("✅ No significant data drift detected")
    else:
        st.warning("Data drift report not found.")

# ---------- Transaction Data Page ----------
elif page == "📋 Transaction Data":
    st.header("📋 Transaction Data Reference")

    st.info("💡 This section shows sample transaction data for reference. In production, this would connect to your database.")

    # Generate sample data for demonstration
    @st.cache_data
    def generate_sample_data():
        np.random.seed(42)
        n = 100
        df = pd.DataFrame({
            "Step": np.random.randint(0, 744, n),
            "Type": np.random.choice(["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"], n),
            "Amount": np.random.exponential(1000, n).round(2),
            "Oldbalanceorg": np.random.exponential(5000, n).round(2),
            "Oldbalancedest": np.random.exponential(3000, n).round(2),
            "Newbalanceorig": np.random.exponential(4000, n).round(2),
            "Newbalancedest": np.random.exponential(3500, n).round(2),
        })
        return df

    sample_df = generate_sample_data()

    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        type_filter = st.multiselect("Filter by Transaction Type", df["Type"].unique())
    with col2:
        amount_filter = st.slider("Minimum Amount", 0.0, 10000.0, 0.0)

    filtered_df = sample_df.copy()
    if type_filter:
        filtered_df = filtered_df[filtered_df["Type"].isin(type_filter)]
    if amount_filter > 0:
        filtered_df = filtered_df[filtered_df["Amount"] >= amount_filter]

    st.dataframe(filtered_df, use_container_width=True)

    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Sample Data",
        data=csv,
        file_name="sample_transactions.csv",
        mime="text/csv"
    )

# ---------- Footer ----------
st.divider()
st.markdown("""
<div style='text-align: center; color: #64748b;'>
    <p>FraudGuard AI Dashboard | Powered by Machine Learning</p>
    <p>⚠️ This is for demonstration purposes. Always verify predictions with additional checks.</p>
</div>
""", unsafe_allow_html=True)
