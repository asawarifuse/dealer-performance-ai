import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

df = pd.read_csv('dealer_kpi_with_anomalies.csv')
df_dealers = pd.read_csv('dealer_master.csv')
df['month'] = pd.to_datetime(df['month'])
df = df.merge(df_dealers[['dealer_id', 'city', 'region', 'dealer_type']], on='dealer_id', how='left')

genai.configure(api_key="AIzaSyD8Ab8RN6L8gNbPnc_IZVBhDXkRY-teFrTaVo8OepZRR66IjT2Pbw")
gemini_model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="Dealer Performance AI", layout="wide")
st.title("Dealer Performance Intelligence System")
st.caption("AI-Powered Analytics | 500 Dealers | 11 KPIs")

page = st.sidebar.radio("Go to", ["Executive Summary", "Dealer Deep Dive", "Dealer Comparison", "Anomaly Center", "AI Assistant"])

latest = df[df['month'] == df['month'].max()]
total_sales = df['monthly_sales'].sum()
total_dealers = df_dealers['dealer_id'].nunique()
avg_score = round(df['composite_score'].mean(), 1)
anomaly_count = len(df[df['anomaly'] == -1])
anomaly_pct = round(anomaly_count / len(df) * 100, 1)

if page == "Executive Summary":
    st.header("Executive Summary")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Sales", f"{total_sales:,}")
    c2.metric("Total Dealers", total_dealers)
    c3.metric("Avg Score", avg_score)
    c4.metric("Anomalies", anomaly_count)
    c5.metric("Anomaly %", f"{anomaly_pct}%")
    col1, col2 = st.columns(2)
    with col1:
        sales_trend = df.groupby('month')['monthly_sales'].sum().reset_index()
        fig = px.line(sales_trend, x='month', y='monthly_sales', title="Sales Trend")
        fig.update_traces(line_color='#1B3A5C')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        region_score = df.groupby('region')['composite_score'].mean().reset_index()
        fig = px.bar(region_score, x='region', y='composite_score', title="Avg Score by Region", color='region')
        st.plotly_chart(fig, use_container_width=True)
    col3, col4 = st.columns(2)
    with col3:
        city_sales = df.groupby('city')['monthly_sales'].sum().reset_index()
        fig = px.scatter_geo(city_sales, locations='city', locationmode='country names', size='monthly_sales', title="Sales by City", projection='natural earth')
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        bottom10 = latest.nsmallest(10, 'composite_score')[['dealer_id', 'city', 'composite_score']]
        st.subheader("Bottom 10 Dealers")
        st.dataframe(bottom10, use_container_width=True)

elif page == "Dealer Deep Dive":
    st.header("Dealer Deep Dive")
    selected = st.selectbox("Select Dealer", df_dealers['dealer_id'].unique())
    dealer_data = df[df['dealer_id'] == selected]
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Model CR", round(dealer_data['model_wise_cr'].mean(), 1))
    c2.metric("Advisor CR", round(dealer_data['sales_advisor_cr'].mean(), 1))
    c3.metric("Market Share", round(dealer_data['market_share'].mean(), 1))
    c4.metric("SSI", round(dealer_data['ssi'].mean(), 1))
    c5.metric("CSAT", round(dealer_data['csat'].mean(), 1))
    c6.metric("CPTV", round(dealer_data['cptv'].mean(), 1))
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(dealer_data, x='month', y='composite_score', title="Score Trend", color_discrete_sequence=['#1B3A5C'])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.line(dealer_data, x='month', y='monthly_sales', title="Sales Trend", color_discrete_sequence=['#27AE60'])
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("Monthly Breakdown")
    st.dataframe(dealer_data[['month', 'composite_score', 'monthly_sales', 'cptv', 'tat_complaint_resolution']].sort_values('month', ascending=False), use_container_width=True)

elif page == "Dealer Comparison":
    st.header("Dealer Comparison")
    region_filter = st.selectbox("Filter by Region", ["All"] + list(df_dealers['region'].unique()))
    if region_filter != "All":
        filtered = df[df['region'] == region_filter]
        filtered_dealers = df_dealers[df_dealers['region'] == region_filter]
    else:
        filtered, filtered_dealers = df, df_dealers
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Dealers", filtered_dealers['dealer_id'].nunique())
    c2.metric("Avg Score", round(filtered['composite_score'].mean(), 1))
    c3.metric("Best Score", round(filtered['composite_score'].max(), 1))
    c4.metric("Worst Score", round(filtered['composite_score'].min(), 1))
    col1, col2 = st.columns(2)
    with col1:
        ds = filtered.groupby('dealer_id').agg({'composite_score': 'mean', 'monthly_sales': 'sum'}).reset_index()
        fig = px.scatter(ds, x='monthly_sales', y='composite_score', hover_name='dealer_id', title="Score vs Sales")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        ranking = filtered.groupby('dealer_id')['composite_score'].mean().reset_index().sort_values('composite_score')
        st.subheader("Dealer Ranking")
        st.dataframe(ranking, use_container_width=True)

elif page == "Anomaly Center":
    st.header("Anomaly Center")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Anomalies", anomaly_count)
    c2.metric("Anomaly %", f"{anomaly_pct}%")
    c3.metric("Dealers Flagged", df[df['anomaly'] == -1]['dealer_id'].nunique())
    c4.metric("Avg Score (Normal)", round(df[df['anomaly'] == 1]['composite_score'].mean(), 1))
    c5.metric("Avg Score (Anomaly)", round(df[df['anomaly'] == -1]['composite_score'].mean(), 1))
    col1, col2 = st.columns(2)
    with col1:
        at = df.groupby(['month', 'anomaly_label']).size().reset_index(name='count')
        fig = px.bar(at, x='month', y='count', color='anomaly_label', title="Anomalies by Month", color_discrete_map={'Normal': '#27AE60', 'Anomaly': '#E74C3C'})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        ar = df[df['anomaly'] == -1].groupby('region').size().reset_index(name='count')
        fig = px.pie(ar, names='region', values='count', title="Anomalies by Region")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("Flagged Dealers (Last 3 Months)")
    last3 = df['month'].max() - pd.DateOffset(months=3)
    flagged = df[(df['anomaly'] == -1) & (df['month'] >= last3)][['month', 'dealer_id', 'city', 'region', 'composite_score']].sort_values('composite_score')
    st.dataframe(flagged, use_container_width=True)

elif page == "AI Assistant":
    st.header("Dashboard Speaker")
    st.markdown("Ask any question about dealer performance.")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    user_input = st.chat_input("e.g., Which dealers are underperforming?")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    ctx = f"Dealers: {total_dealers}. Sales: {total_sales}. Avg Score: {avg_score}. Anomalies: {anomaly_count} ({anomaly_pct}%). KPIs: model_wise_cr, sales_advisor_cr, market_share, SSI, CSAT, monthly_sales, booking_pipeline, accessories_per_car, CPTV, TAT."
                    prompt = f"You are a dealer performance analyst. {ctx}\nUser: {user_input}\nAnswer concisely."
                    response = gemini_model.generate_content(prompt)
                    reply = response.text
                except:
                    reply = "AI unavailable. Check dashboard tabs for insights."
                st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
