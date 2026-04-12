import streamlit as st
import math
from pdf_generator import generate_cpv_report
# --- NEW IMPORT ---
from cpv.cpv_calculator import calculate_niche_metrics 

# --- Configuration & CSS ---
# (Keep your existing st.set_page_config and CSS block here)

# --- Updated Helper Function ---
def create_card(title, value):
    """Generates a modern HTML/SVG card with a circular progress indicator."""
    radius = 40
    circumference = 2 * math.pi * radius
    
    # Since CPV values are often small (e.g., 0.5 to 15.0), 
    # we'll scale the visual ring logic so it looks good in the demo.
    # Let's cap the visual "progress" at 20 INR for a full circle.
    visual_percent = min((value / 20) * 100, 100)
    offset = circumference - (visual_percent / 100) * circumference
    
    # Color logic: Green is cheap (good), Red is expensive
    color = "#10B981" if value < 2 else "#F59E0B" if value < 7 else "#EF4444"
    
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
                <h3 style="margin: 0; font-size: 18px;">₹{value:.2f}</h3>
            </div>
        </div>
    </div>
    """
    return html

# --- DATA INTEGRATION ---
# Fetch real data from your SQLite DB
raw_metrics = calculate_niche_metrics()

# Map the DB results to the format your UI/PDF expects
# The calculator returns: niche, avg_cpv, total_views, total_spend, video_count
cpv_data = [
    {
        "title": m["niche"], 
        "value": m["avg_cpv"],
        "views": m["total_views"],
        "count": m["video_count"]
    } 
    for m in raw_metrics
]

# --- Dashboard Layout ---
col_title, col_btn = st.columns([0.8, 0.2])
with col_title:
    st.title("YouTube Niche Analysis") # Updated for your project
    st.subheader("Cost Per View (CPV) Efficiency")

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    # Generate PDF using the real data
    pdf_bytes = generate_cpv_report(cpv_data)
    
    st.download_button(
        label="📄 Download Report",
        data=pdf_bytes,
        file_name="Niche_CPV_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

st.markdown("<hr style='margin-top: 0;'>", unsafe_allow_html=True)

# Grid Layout logic (remains the same as your code)
cols_per_row = 4
for i in range(0, len(cpv_data), cols_per_row):
    cols = st.columns(cols_per_row, gap="medium")
    for j, col in enumerate(cols):
        if i + j < len(cpv_data):
            item = cpv_data[i + j]
            with col:
                # Display the card with the Niche Name and Avg CPV
                st.markdown(create_card(item["title"], item["value"]), unsafe_allow_html=True)
                # Optional: Small caption for views
                st.caption(f"Total Views: {item['views']:,}")