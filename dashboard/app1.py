import streamlit as st
import random
import math
from pathlib import Path
from pdf_generator import generate_cpv_report
# --- Configuration ---
st.set_page_config(page_title="CPV Dashboard", layout="wide")

# --- Custom CSS for "JS-like" elements with shadows ---
# We use CSS to handle hover effects, box-shadows, and smooth transitions
st.markdown("""
    <style>
    .metric-card {
        background-color: var(--background-color);
        border-radius: 12px;
        padding: 24px 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid rgba(128,128,128,0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .circle-bg {
        fill: none;
        stroke: rgba(128,128,128,0.15);
        stroke-width: 8;
    }
    .circle-progress {
        fill: none;
        stroke-width: 8;
        stroke-linecap: round;
        transition: stroke-dashoffset 1s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

# --- Helper Function for the Progress Ring ---
def create_card(title, value):
    """Generates a modern HTML/SVG card with a circular progress indicator."""
    radius = 40
    circumference = 2 * math.pi * radius
    # Calculate how much of the stroke to hide based on the value
    offset = circumference - (value / 100) * circumference
    
    # Dynamic coloring based on value
    # Dynamic coloring: Lower is Green (<40), Mid is Yellow (40-74), High is Red (>=75)
    color = "#EF4444" if value >= 75 else "#F59E0B" if value >= 40 else "#10B981"
    
    html = f"""
    <div class="metric-card">
        <h4 style="margin-top: 0; margin-bottom: 15px; opacity: 0.8; font-weight: 500;">{title}</h4>
        <div style="position: relative; width: 100px; height: 100px; margin: 0 auto;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle class="circle-bg" cx="50" cy="50" r="{radius}" />
                <circle class="circle-progress" cx="50" cy="50" r="{radius}" stroke="{color}" 
                        stroke-dasharray="{circumference}" stroke-dashoffset="{offset}" 
                        transform="rotate(-90 50 50)" />
            </svg>
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                <h3 style="margin: 0; font-size: 22px;">{value}</h3>
            </div>
        </div>
    </div>
    """
    return html

# --- Dashboard Layout ---
# Generate dummy data for 20 elements (moved UP so the PDF can read it)
cpv_data = [{"title": f"CPV Value {i+1}", "value": random.randint(15, 100)} for i in range(20)]
# Sort the data dynamically in descending order
cpv_data = sorted(cpv_data, key=lambda x: x["value"], reverse=False)

# 1. Company Name and Download/Upload Button Header
col_title, col_upload, col_btn = st.columns([0.6, 0.2, 0.2])
with col_title:
    st.title("Acme Corporation")
with col_upload:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CSV File Uploader
    uploaded_file = st.file_uploader(
        "Upload CSV",
        type="csv",
        label_visibility="collapsed",
        key="csv_uploader"
    )
    
    if uploaded_file is not None:
        # Save to db folder
        db_path = Path(__file__).parent.parent / "db" / uploaded_file.name
        with open(db_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✓ Saved: {uploaded_file.name}")

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate the actual PDF bytes using our new function
    pdf_bytes = generate_cpv_report(cpv_data)
    
    st.download_button(
        label="📄 Download Report",
        data=pdf_bytes,
        file_name="Acme_Strategic_Expansion.pdf",
        mime="application/pdf",
        use_container_width=True
    )

st.markdown("<hr style='margin-top: 0;'>", unsafe_allow_html=True)

# 2 & 3 & 4. Repeatable 4-column layout
cols_per_row = 4

# Loop through the data and group it into rows of 4
for i in range(0, len(cpv_data), cols_per_row):
    # Create 4 columns with standard spacing
    cols = st.columns(cols_per_row, gap="medium")
    
    # Populate each column in the current row
    for j, col in enumerate(cols):
        # Ensure we don't go out of bounds if the array length isn't perfectly divisible by 4
        if i + j < len(cpv_data):
            item = cpv_data[i + j]
            with col:
                st.markdown(create_card(item["title"], item["value"]), unsafe_allow_html=True)