"""
COVID-19 Vaccine Dashboard - Main Application

A Streamlit dashboard for visualizing COVID-19 vaccine candidate data.
Supports Dark and Light themes with PDF export functionality.
"""
import streamlit as st
import sys
import os

# Add the project root to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import Config
from src.services.mock_data import MockDataProvider
from src.services.postgres_data import PostgresDataProvider
from src.ui.sidebar import render_sidebar
from src.ui.components import render_donut_chart, render_bar_chart, render_map, render_sunburst
from src.ui.styles import get_theme, inject_styles


def get_data_provider():
    """Get the appropriate data provider based on configuration."""
    if Config.DATA_SOURCE == "POSTGRES":
        return PostgresDataProvider()
    return MockDataProvider()


def main() -> None:
    """Main application entry point."""
    # --- Page Configuration ---
    st.set_page_config(
        page_title=Config.PAGE_TITLE,
        page_icon=Config.PAGE_ICON,
        layout=Config.LAYOUT,
        initial_sidebar_state="expanded"
    )
    
    # --- Data Loading ---
    provider = get_data_provider()
    
    try:
        df = provider.get_vaccine_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()
    
    # --- Sidebar & Filtering ---
    selected_countries, selected_approaches, selected_stages, theme_name = render_sidebar(df)
    
    filtered_df = df[
        (df["Country"].isin(selected_countries)) &
        (df["Approach"].isin(selected_approaches)) &
        (df["Stage"].isin(selected_stages))
    ]
    
    # --- Apply Theme Styles ---
    theme = get_theme(theme_name)
    inject_styles(theme)
    
    # --- Main Layout ---
    st.title("COVID Vaccine Dashboard")
    st.markdown("`Published` `Not available` `16 days ago`", unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("Overview")
    
    # Row 1: Description + Charts
    row1_col1, row1_col2, row1_col3 = st.columns([1.1, 1.5, 1.3])
    
    with row1_col1:
        st.markdown("""
        ### COVID-19 Vaccine Dashboard
        Everywhere you look, you see negative news about COVID-19. This is to be expected; it's been a brutal year.
        
        *   the sheer volume of attempts to fund the R&D needed
        *   the large number of countries involved
        *   the diversity of vaccine approaches taken
        
        **The Dataset**  
        The dashboard is powered by data maintained by the Milken Institute.
        """)
    
    with row1_col2:
        render_donut_chart(filtered_df, theme_name)
    
    with row1_col3:
        render_bar_chart(filtered_df, theme_name)
    
    # Row 2: Map + Sunburst
    row2_col1, row2_col2 = st.columns([2, 1])
    
    with row2_col1:
        render_map(filtered_df, theme_name)
    
    with row2_col2:
        render_sunburst(filtered_df, theme_name)


if __name__ == "__main__":
    main()
