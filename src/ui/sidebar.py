"""
Sidebar component for the COVID-19 Vaccine Dashboard.
Handles filter controls, theme selection, and PDF export.
"""
import streamlit as st
import pandas as pd
from typing import Tuple, List, Literal

ThemeType = Literal["Dark", "Light"]


def _checkbox_group(df: pd.DataFrame, label: str, column_name: str) -> List[str]:
    """
    Render a checkbox group with Select All functionality.
    
    Args:
        df: DataFrame containing the data.
        label: Display label for the expander.
        column_name: Column name to get unique values from.
        
    Returns:
        List of selected option values.
    """
    options = sorted(df[column_name].unique())
    state_key = f"select_all_state_{column_name}"
    
    with st.expander(label, expanded=False):
        # Initialize session state
        if state_key not in st.session_state:
            st.session_state[state_key] = True

        selected_options: List[str] = []
        
        # Select All Toggle
        if st.checkbox("Select All", value=st.session_state[state_key], key=f"toggle_all_{column_name}"):
            st.session_state[state_key] = True
            selected_options = list(options)
        else:
            st.session_state[state_key] = False
            # Render individual checkboxes
            for opt in options:
                if st.checkbox(str(opt), value=False, key=f"chk_{column_name}_{opt}"):
                    selected_options.append(opt)
                    
    return selected_options


def render_sidebar(df: pd.DataFrame) -> Tuple[List[str], List[str], List[str], ThemeType]:
    """
    Render the sidebar with filters, theme selection, and export options.
    
    Args:
        df: DataFrame containing the vaccine data.
        
    Returns:
        Tuple of (selected_countries, selected_approaches, selected_stages, theme).
    """
    with st.sidebar:
        st.header("Actions")
        
        # Filter Controls
        selected_countries = _checkbox_group(df, "Country", "Country")
        selected_approaches = _checkbox_group(df, "Vaccine Approach", "Approach")
        selected_stages = _checkbox_group(df, "Clinical Stage", "Stage")
        
        st.markdown("---")
        
        # Theme Selection
        st.subheader("Settings")
        theme: ThemeType = st.radio("Theme", ["Dark", "Light"], index=0)
        
        st.markdown("---")
        
        # PDF Export
        if st.button("Print / Save as PDF"):
            st.components.v1.html("<script>window.parent.print()</script>", height=0, width=0)
            
        return selected_countries, selected_approaches, selected_stages, theme
