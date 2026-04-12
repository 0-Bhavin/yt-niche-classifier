import streamlit as st
import plotly.graph_objects as go

# --- Configuration ---
st.set_page_config(page_title="CPV Dashboard", layout="wide")

# --- Helper Functions ---
def create_speedometer(value, title, max_val=100):
    """Generates a Plotly gauge chart (speedometer)."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 20}},
        gauge={
            'axis': {'range': [None, max_val], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#1f77b4"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, max_val * 0.5], 'color': "#e6f2ff"},
                {'range': [max_val * 0.5, max_val * 0.8], 'color': "#99ccff"},
                {'range': [max_val * 0.8, max_val], 'color': "#3399ff"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_val * 0.9 # Redline at 90%
            }
        }
    ))
    
    # Adjust layout to fit nicely in Streamlit columns
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# --- Dashboard Layout ---

# Top row: Company Name input
company_name = st.text_input("Company Name", placeholder="Enter Company Name Here...")

st.markdown("---") # Visual divider

# Middle row: 3 Columns for the speedometers
col1, col2, col3 = st.columns(3)

# Dummy data for the speedometers (replace with your actual data logic)
cpv_data = {
    "cpv_1": 45,
    "cpv_2": 78,
    "cpv_3": 92
}

# Render the speedometers in their respective columns
with col1:
    st.plotly_chart(create_speedometer(cpv_data["cpv_1"], "CPV Value 1"), use_container_width=True)

with col2:
    st.plotly_chart(create_speedometer(cpv_data["cpv_2"], "CPV Value 2"), use_container_width=True)

with col3:
    st.plotly_chart(create_speedometer(cpv_data["cpv_3"], "CPV Value 3"), use_container_width=True)