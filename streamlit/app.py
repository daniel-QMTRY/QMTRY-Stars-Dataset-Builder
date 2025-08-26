import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="QMTRY • Stars Dataset Demo", layout="wide")

st.title("⭐ QMTRY — Stars Dataset Builder (Demo)")
st.caption("Synthetic demo — PDC & SUPD outputs")

member_fp = Path("output_demo/measure_member_results.csv")
rollup_fp = Path("output_demo/measure_contract_rollup.csv")

if not member_fp.exists():
    st.warning("Run the build first: `python scripts/build_stars_dataset.py`")
else:
    m = pd.read_csv(member_fp)
    r = pd.read_csv(rollup_fp)
    st.subheader("Contract Rollup")
    st.dataframe(r, use_container_width=True)

    st.subheader("Member-level PDC (Diabetes vs Statin)")
    fig = px.scatter(m, x="pdc_diabetes", y="pdc_statin", color="supd_flag",
                     hover_data=["member_id","contract_id"])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("SUPD status by member")
    st.dataframe(m[["member_id","supd_flag","pdc_diabetes","pdc_statin"]])
