import streamlit as st
import pandas as pd

def render_sidebar(df: pd.DataFrame):
    with st.sidebar:
        st.header("Actions")
        
        # --- Helper for Checkbox Group ---
        def checkbox_group(label, column_name):
            options = sorted(df[column_name].unique())
            
            with st.expander(label, expanded=False):
                if f"select_all_state_{column_name}" not in st.session_state:
                     st.session_state[f"select_all_state_{column_name}"] = True

                selected_options = []
                # Select All Toggle
                if st.checkbox("Select All", value=st.session_state[f"select_all_state_{column_name}"], key=f"toggle_all_{column_name}"):
                    st.session_state[f"select_all_state_{column_name}"] = True
                    selected_options = options # Return all
                else:
                    st.session_state[f"select_all_state_{column_name}"] = False
                    # Render individual
                    for opt in options:
                        if st.checkbox(opt, value=False, key=f"chk_{column_name}_{opt}"):
                            selected_options.append(opt)
                            
            return selected_options

        # --- Filters ---
        selected_countries = checkbox_group("Country", "Country")
        selected_approaches = checkbox_group("Vaccine Approach", "Approach")
        selected_stages = checkbox_group("Clinical Stage", "Stage")
        
        st.markdown("---")
        
        # --- Theme & Export ---
        st.subheader("Settings")
        theme = st.radio("Theme", ["Dark", "Light"], index=0)
        
        st.markdown("---")
        if st.button("Print / Save as PDF"):
            # Use window.parent.print() to print the main page, not the iframe
            st.components.v1.html("<script>window.parent.print()</script>", height=0, width=0)
            
        return selected_countries, selected_approaches, selected_stages, theme
