
import streamlit as st
import pandas as pd
import json
import urllib.request

from data.generator import generate_opportunities

st.set_page_config(
    page_title="SalesPulse AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 SalesPulse AI")
st.subheader("Intelligent Sales Forecasting & Pipeline Risk Management")

opportunities = generate_opportunities()


def call_api(endpoint, data):
    api_request = urllib.request.Request(
        f"http://127.0.0.1:8000/{endpoint}",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(api_request) as response:
        return json.loads(response.read().decode("utf-8"))


def get_api(endpoint):
    api_request = urllib.request.Request(
        f"http://127.0.0.1:8000/{endpoint}",
        method="GET"
    )

    with urllib.request.urlopen(api_request) as response:
        return json.loads(response.read().decode("utf-8"))


try:
    forecast_result = call_api("forecast", opportunities)
    risk_result = call_api("risks", opportunities)

    forecast = forecast_result["forecast"]
    risks = risk_result["risky_opportunities"]

    # Dashboard Metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Opportunities", len(opportunities))
    col2.metric("Total Pipeline", f"₹{forecast['total_pipeline']:,.0f}")
    col3.metric("Expected Revenue", f"₹{forecast['expected_revenue']:,.0f}")
    col4.metric(
        "High Risk Deals",
        sum(1 for deal in risks if deal["risk_level"] == "High")
    )

    # Sales Forecast Scenarios
    st.divider()
    st.subheader("Sales Forecast Scenarios")

    scenario_data = pd.DataFrame({
        "Scenario": ["Worst Case", "Expected Revenue", "Best Case"],
        "Revenue": [
            forecast["worst_case"],
            forecast["expected_revenue"],
            forecast["best_case"]
        ]
    })

    st.bar_chart(scenario_data.set_index("Scenario"))

    # What-If Scenario Simulator
    st.divider()
    st.subheader("🎯 What-If Scenario Simulator")

    probability_change = st.slider(
        "Adjust open-deal win probabilities (percentage points)",
        min_value=-20,
        max_value=20,
        value=0,
        step=5
    )

    adjusted_expected_revenue = 0

    for deal in opportunities:
        adjusted_probability = deal["probability"]

        if deal["stage"] != "Closed Won":
            adjusted_probability = max(
                0,
                min(100, adjusted_probability + probability_change)
            )

        adjusted_expected_revenue += (
            deal["amount"] * adjusted_probability / 100
        )

    col1, col2 = st.columns(2)

    col1.metric(
        "Baseline Expected Revenue",
        f"₹{forecast['expected_revenue']:,.0f}"
    )

    difference = adjusted_expected_revenue - forecast["expected_revenue"]

    col2.metric(
        "Scenario Expected Revenue",
        f"₹{adjusted_expected_revenue:,.0f}",
        delta=f"₹{difference:+,.0f}"
    )

    # Sales Opportunities
    st.divider()
    st.subheader("Sales Opportunities")

    selected_stage = st.selectbox(
        "Filter by Stage",
        [
            "All", "Prospecting", "Qualification",
            "Proposal", "Negotiation", "Closed Won"
        ]
    )

    if selected_stage == "All":
        filtered_opportunities = opportunities
    else:
        filtered_opportunities = [
            deal for deal in opportunities
            if deal["stage"] == selected_stage
        ]

    st.dataframe(
        pd.DataFrame(filtered_opportunities),
        use_container_width=True
    )

    csv_data = pd.DataFrame(filtered_opportunities).to_csv(index=False)

    st.download_button(
        label="Download Opportunities CSV",
        data=csv_data,
        file_name="sales_opportunities.csv",
        mime="text/csv"
    )

    # Opportunity Ageing Analysis
    st.divider()
    st.subheader("⏳ Opportunity Ageing Analysis")

    ageing_30 = sum(1 for deal in opportunities if deal["days_open"] >= 30)
    ageing_60 = sum(1 for deal in opportunities if deal["days_open"] >= 60)
    ageing_90 = sum(1 for deal in opportunities if deal["days_open"] >= 90)

    col1, col2, col3 = st.columns(3)

    col1.metric("Open 30+ Days", ageing_30)
    col2.metric("Open 60+ Days", ageing_60)
    col3.metric("Open 90+ Days", ageing_90)

    delayed_deals = [
        deal for deal in opportunities
        if deal["days_open"] >= 60
    ]

    if delayed_deals:
        st.write("**Opportunities open for 60 days or more**")
        st.dataframe(pd.DataFrame(delayed_deals), use_container_width=True)
    else:
        st.success("No opportunities open for 60 days or more.")

    # Forecast History and Save Button
    st.divider()
    st.subheader("📜 Forecast History")

    if st.button("💾 Save Current Forecast"):
        try:
            save_result = call_api("forecast-history", opportunities)
            st.success("Forecast saved successfully!")
        except Exception as error:
            st.error(f"Could not save forecast: {error}")

    history_result = get_api("forecast-history")
    history = history_result["history"]

    if history:
        history_df = pd.DataFrame(history)
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("No previous forecasts available.")

    # Rep & Territory Performance Analysis
    st.divider()
    st.subheader("👥 Rep & Territory Performance Analysis")

    performance_df = pd.DataFrame(opportunities)

    rep_performance = performance_df.groupby("sales_rep").agg(
        total_opportunities=("name", "count"),
        total_pipeline=("amount", "sum"),
        expected_revenue=(
            "amount",
            lambda values: (
                values * performance_df.loc[values.index, "probability"] / 100
            ).sum()
        )
    ).reset_index()

    territory_performance = performance_df.groupby("territory").agg(
        total_opportunities=("name", "count"),
        total_pipeline=("amount", "sum")
    ).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Sales Representative Performance**")
        st.dataframe(rep_performance, use_container_width=True)
        st.bar_chart(
            rep_performance.set_index("sales_rep")["expected_revenue"]
        )

    with col2:
        st.write("**Territory Performance**")
        st.dataframe(territory_performance, use_container_width=True)
        st.bar_chart(
            territory_performance.set_index("territory")["total_pipeline"]
        )

    # Risk Detection
    st.divider()
    st.subheader("⚠️ Pipeline Risk Detection")

    if risks:
        st.dataframe(pd.DataFrame(risks), use_container_width=True)
    else:
        st.success("No risky opportunities detected.")

except Exception as error:
    st.error(f"Could not connect to the backend: {error}")
    st.info("Make sure the FastAPI server is running.")
