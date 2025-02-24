import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset (Replace with actual file if needed)
data = {
    "Category": ["Total Cost (Low)", "Total Cost (Medium)", "Total Cost (High)"],
    "UK": [37561920194, 56342880291, 75123840388],
    "US": [224490439085, 336735658627, 448980878170],
    "Both": [262052359279, 393078538918, 524104718558]
}
df_cost = pd.DataFrame(data)

data_per_capita = {
    "Type": ["Absenteeism Base", "Absenteeism Mult", "Absenteeism Total",
              "Presenteeism Base", "Presenteeism Mult", "Presenteeism Total",
              "WEP Base", "WEP Mult", "Stromberg Total WEP"],
    "UK": [4012, 3891, 7903, 3622, 1956, 5577, 13480, 9706, 23186],
    "US": [5038, 4887, 9925, 4548, 2456, 7004, 16928, 12188, 29117],
    "WA": [4891, 4744, 9635, 4415, 2384, 6799, 16434, 11833, 28267]
}
df_per_capita = pd.DataFrame(data_per_capita)

# Set Streamlit Page Config for Dark Mode
st.set_page_config(page_title="PCOS Economic Impact Dashboard", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        .css-1d391kg { background-color: #0e1117 !important; }
        .css-1offfwp { color: white !important; }
    </style>
""", unsafe_allow_html=True)

st.title("PCOS Economic Burden Dashboard")

# Create tabs for different sections
tabs = st.tabs(["Cost Breakdown", "Workforce Productivity"])

with tabs[0]:
    st.subheader("Total Economic Burden by Country")
    cost_level = st.radio("Select Cost Level", ["Low", "Medium", "High"], index=1)
    df_filtered = df_cost[df_cost["Category"].str.contains(cost_level)]
    fig_cost = px.bar(df_filtered, x="Category", y=["UK", "US", "Both"],
                      title="Economic Burden Breakdown", barmode="group",
                      template="plotly_dark")
    st.plotly_chart(fig_cost)

with tabs[1]:
    st.subheader("Workforce Economic Productivity Impact")
    per_capita_selector = st.multiselect("Select Per Capita Type", df_per_capita["Type"].unique(),
                                         default=["Absenteeism Total", "Presenteeism Total", "Stromberg Total WEP"])
    df_per_capita_filtered = df_per_capita[df_per_capita["Type"].isin(per_capita_selector)]
    fig_per_capita = px.bar(df_per_capita_filtered, x="Type", y=["UK", "US", "WA"],
                            title="Workforce Economic Productivity Impact",
                            barmode="group", template="plotly_dark")
    st.plotly_chart(fig_per_capita)

# Display DataTables
st.subheader("Data Overview")
st.write("Economic Burden Data")
st.dataframe(df_cost)
st.write("Workforce Economic Productivity Data")
st.dataframe(df_per_capita)

# Download Button
csv = df_cost.to_csv(index=False)
st.download_button("Download Cost Data", csv, "pcos_cost_data.csv", "text/csv")
