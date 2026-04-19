#!/usr/bin/env python3
"""
Streamlit entry point for OCR Receipt Scanner - Deployment Version.
This version is optimized for Streamlit Share with minimal dependencies.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io
import json
import sqlite3
from datetime import datetime, date
import tempfile
import os
import sys
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="OCR Receipt Scanner",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🧾 OCR Receipt Scanner")
st.markdown("""
Upload receipt images or PDFs to extract and analyze spending data.
This demo version shows the UI/UX without full OCR processing.
""")

# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'processed_receipts' not in st.session_state:
    st.session_state.processed_receipts = []

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Upload & Scan", "Dashboard", "Analytics", "Settings"]
)

# Sample data for demo
sample_receipts = [
    {
        "id": 1,
        "store": "Walmart",
        "total": 168.52,
        "date": "2026-04-19",
        "time": "12:41 PM",
        "items": 12,
        "category": "Groceries"
    },
    {
        "id": 2,
        "store": "Target",
        "total": 89.75,
        "date": "2026-04-18",
        "time": "3:15 PM",
        "items": 8,
        "category": "Household"
    },
    {
        "id": 3,
        "store": "Costco",
        "total": 245.30,
        "date": "2026-04-17",
        "time": "10:30 AM",
        "items": 15,
        "category": "Bulk"
    }
]

if page == "Upload & Scan":
    st.header("📤 Upload & Scan Receipts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("File Upload")
        uploaded_files = st.file_uploader(
            "Choose receipt images or PDFs",
            type=["jpg", "jpeg", "png", "pdf"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            st.success(f"Uploaded {len(uploaded_files)} file(s)")
            
            for file in uploaded_files:
                st.write(f"• {file.name} ({file.size:,} bytes)")
    
    with col2:
        st.subheader("Camera Capture")
        st.info("Camera capture requires browser permissions")
        use_camera = st.checkbox("Use camera")
        
        if use_camera:
            camera_input = st.camera_input("Take a photo of your receipt")
            if camera_input:
                st.success("Photo captured!")
                st.image(camera_input, caption="Captured Receipt", use_column_width=True)
    
    if st.button("Process Receipts", type="primary"):
        with st.spinner("Processing receipts..."):
            # Simulate processing
            import time
            time.sleep(2)
            
            # Add sample data
            for receipt in sample_receipts:
                st.session_state.processed_receipts.append(receipt)
            
            st.success(f"Processed {len(sample_receipts)} sample receipts!")
            
            # Show sample output
            st.subheader("Sample Output")
            df = pd.DataFrame(sample_receipts)
            st.dataframe(df, use_container_width=True)

elif page == "Dashboard":
    st.header("📊 Dashboard")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Receipts", len(sample_receipts))
    
    with col2:
        total_spent = sum(r["total"] for r in sample_receipts)
        st.metric("Total Spent", f"${total_spent:,.2f}")
    
    with col3:
        avg_spent = total_spent / len(sample_receipts) if sample_receipts else 0
        st.metric("Average Receipt", f"${avg_spent:,.2f}")
    
    with col4:
        total_items = sum(r["items"] for r in sample_receipts)
        st.metric("Total Items", total_items)
    
    # Recent receipts
    st.subheader("Recent Receipts")
    df_recent = pd.DataFrame(sample_receipts)
    st.dataframe(
        df_recent[["store", "total", "date", "items", "category"]],
        use_container_width=True
    )
    
    # Spending by store
    st.subheader("Spending by Store")
    store_totals = df_recent.groupby("store")["total"].sum().reset_index()
    fig_store = px.bar(
        store_totals,
        x="store",
        y="total",
        title="Total Spending by Store",
        color="store"
    )
    st.plotly_chart(fig_store, use_container_width=True)

elif page == "Analytics":
    st.header("📈 Analytics")
    
    # Time series
    st.subheader("Spending Over Time")
    df_time = pd.DataFrame(sample_receipts)
    df_time["date"] = pd.to_datetime(df_time["date"])
    df_time = df_time.sort_values("date")
    
    fig_time = px.line(
        df_time,
        x="date",
        y="total",
        title="Daily Spending",
        markers=True
    )
    st.plotly_chart(fig_time, use_container_width=True)
    
    # Category breakdown
    st.subheader("Spending by Category")
    category_totals = df_time.groupby("category")["total"].sum().reset_index()
    fig_pie = px.pie(
        category_totals,
        values="total",
        names="category",
        title="Spending Distribution by Category"
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Export options
    st.subheader("Export Data")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export as CSV"):
            csv = df_time.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="receipts_export.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Export as Excel"):
            # Create Excel file in memory
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_time.to_excel(writer, sheet_name='Receipts', index=False)
            st.download_button(
                label="Download Excel",
                data=output.getvalue(),
                file_name="receipts_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col3:
        if st.button("Export as JSON"):
            json_data = df_time.to_json(orient="records", indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="receipts_export.json",
                mime="application/json"
            )

else:  # Settings
    st.header("⚙️ Settings")
    
    st.subheader("Application Settings")
    
    # OCR Engine selection
    engine = st.selectbox(
        "OCR Engine (Demo)",
        ["EasyOCR (Recommended)", "Tesseract", "Cloud API"],
        index=0
    )
    
    # Language selection
    languages = st.multiselect(
        "Languages",
        ["English", "Spanish", "French", "German", "Chinese"],
        default=["English"]
    )
    
    # Processing options
    col1, col2 = st.columns(2)
    
    with col1:
        enable_preprocessing = st.checkbox("Enable Image Preprocessing", value=True)
        enable_validation = st.checkbox("Enable Data Validation", value=True)
    
    with col2:
        auto_categorize = st.checkbox("Auto-categorize Items", value=True)
        save_to_db = st.checkbox("Save to Database", value=True)
    
    # Database management
    st.subheader("Database Management")
    
    if st.button("Clear All Data", type="secondary"):
        st.session_state.processed_receipts = []
        st.session_state.uploaded_files = []
        st.success("All data cleared!")
    
    if st.button("Load Sample Data", type="primary"):
        st.session_state.processed_receipts = sample_receipts
        st.success("Sample data loaded!")

# Footer
st.markdown("---")
st.markdown("""
**OCR Receipt Scanner** • Demo Version • Built with Streamlit
""")

if __name__ == "__main__":
    pass