import streamlit as st
import sys
import os

# Add the project root to sys.path so we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import Config
from src.services.mock_data import MockDataProvider
from src.services.postgres_data import PostgresDataProvider
from src.ui.sidebar import render_sidebar
from src.ui.components import render_donut_chart, render_bar_chart, render_map, render_sunburst

# --- Page Configuration ---
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout=Config.LAYOUT,
    initial_sidebar_state="expanded"
)

# --- Data Loading ---
@st.cache_resource
def get_data_provider():
    if Config.DATA_SOURCE == "POSTGRES":
        return PostgresDataProvider()
    return MockDataProvider()

provider = get_data_provider()

try:
    df = provider.get_vaccine_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- Sidebar & Filtering ---
# This renders the sidebar widgets and returns values
selected_countries, selected_approaches, selected_stages, theme = render_sidebar(df)

filtered_df = df[
    (df["Country"].isin(selected_countries)) &
    (df["Approach"].isin(selected_approaches)) &
    (df["Stage"].isin(selected_stages))
]

# --- Theming Logic ---
# Dark Theme (Default) vs Light Theme
if theme == "Dark":
    bg_color = "#0e1117"
    text_color = "#ffffff"
    sidebar_bg = "#262730"
    sidebar_text_color = "#ffffff"
    header_color = "#e0e0e0"
    border_color = "#444"
else:
    bg_color = "#ffffff"
    text_color = "#000000"
    sidebar_bg = "#f8f9fa" # Light grey
    # We force black text for visibility on light background
    sidebar_text_color = "#000000" 
    header_color = "#333333"
    border_color = "#dee2e6"

# Inject CSS
st.markdown(f"""
    <style>
        /* Main App Background and Text */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        
        /* content container padding */
        .block-container {{
            padding-top: 1rem;
            padding-bottom: 1rem;
        }}

        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg};
        }}
        
        /* Force Text Color in Sidebar - Broad Selectors for Robustness */
        [data-testid="stSidebar"] * {{
            color: {sidebar_text_color} !important;
        }}
        
        /* Fix specific Streamlit widget styles that might be recalcitrant */
        /* Checkbox & Radio Labels */
        [data-testid="stSidebar"] label {{
            color: {sidebar_text_color} !important;
        }}
        
        /* Fill for Checkboxes/Radios (the box itself) */
        /* We rely on Streamlit's default for the box/circle color usually, 
           but ensuring the text next to it is visible is key. */

        /* Expanders in Sidebar */
        [data-testid="stSidebar"] details {{
            background-color: transparent !important;
            color: {sidebar_text_color} !important;
            border-color: {border_color};
        }}
        [data-testid="stSidebar"] details > summary {{
            background-color: {sidebar_bg} !important;
            color: {sidebar_text_color} !important;
        }}
        
        /* Sidebar Buttons (Print, Apply) */
        [data-testid="stSidebar"] button {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
        }}
        [data-testid="stSidebar"] button:hover {{
            border-color: #ff4b4b !important;
            color: #ff4b4b !important;
        }}
        
        /* Headers in Main Area */
        h1, h2, h3, .chart-header {{
            color: {header_color} !important;
        }}
        
        .chart-header {{
            font-size: 16px; 
            font-weight: bold;
            margin-bottom: 10px;
        }}

        /* Ensure header and all buttons within it are visible */
        header {{
            background-color: transparent !important;
        }}
        
        /* Style sidebar toggle button to match Deploy button (Solid background, clear border) */
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"],
        button[kind="header"] {{
            background-color: { "#ffffff" if theme == "Light" else "#0e1117" } !important;
            border: 1px solid { "rgba(49, 51, 63, 0.2)" if theme == "Light" else "rgba(250, 250, 250, 0.2)" } !important;
            color: { "#31333F" if theme == "Light" else "#fafafa" } !important;
            border-radius: 0.25rem !important;
            padding: 0.25rem !important;
            opacity: 1 !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: border-color 0.2s, color 0.2s !important;
        }}
        
        [data-testid="collapsedControl"]:hover,
        [data-testid="stSidebarCollapsedControl"]:hover,
        button[kind="header"]:hover {{
            border-color: #ff4b4b !important;
            color: #ff4b4b !important;
        }}
        
        /* Ensure SVG icons and text inside header buttons inherit color */
        [data-testid="collapsedControl"] *,
        [data-testid="stSidebarCollapsedControl"] *,
        button[kind="header"] * {{
            color: inherit !important;
            fill: currentColor !important;
            stroke: currentColor !important;
        }}
        
        [data-testid="collapsedControl"]:hover *,
        [data-testid="stSidebarCollapsedControl"]:hover *,
        button[kind="header"]:hover * {{
            color: inherit !important;
            fill: currentColor !important;
            stroke: currentColor !important;
        }}
        
        /* Light Theme ONLY: Force sidebar toggle icon visibility */
        { '''[data-testid="collapsedControl"] span,
        [data-testid="stSidebarCollapsedControl"] span,
        button[kind="header"] span {
            color: #31333F !important;
        }
        [data-testid="collapsedControl"]:hover span,
        [data-testid="stSidebarCollapsedControl"]:hover span,
        button[kind="header"]:hover span {
            color: #ff4b4b !important;
        }
        /* Override dynamically generated Streamlit classes */
        [data-testid="collapsedControl"] [class*="st-emotion-cache"],
        [data-testid="stSidebarCollapsedControl"] [class*="st-emotion-cache"],
        button[kind="header"] [class*="st-emotion-cache"] {
            color: #31333F !important;
        }
        [data-testid="collapsedControl"]:hover [class*="st-emotion-cache"],
        [data-testid="stSidebarCollapsedControl"]:hover [class*="st-emotion-cache"],
        button[kind="header"]:hover [class*="st-emotion-cache"] {
            color: #ff4b4b !important;
        }''' if theme == "Light" else "" }
        
        /* Global override for header icons - force visibility based on theme */
        header [class*="emotion-cache"] {{
            color: { "#31333F" if theme == "Light" else "#fafafa" } !important;
        }}
        header:hover [class*="emotion-cache"] {{
            color: { "#31333F" if theme == "Light" else "#fafafa" } !important;
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Print Styles */
        @media print {{
            @page {{
                size: landscape;
                margin: 1cm;
            }}
            
            /* Scale down content to fit 1 page */
            html, body {{
                zoom: 75% !important;
                height: 100% !important;
                overflow: hidden !important;
                background-color: #ffffff !important;
                color: #000000 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}
            
            [data-testid="stAppViewContainer"] {{
                background-color: #ffffff !important;
            }}
            .stApp {{
                background-color: #ffffff !important;
                color: #000000 !important;
            }}
            
            [data-testid="stSidebar"] {{ display: none !important; }}
            header {{ display: none !important; }}
            footer {{ display: none !important; }}
            #MainMenu {{ display: none !important; }}
            
            .block-container {{
                padding: 1rem !important;
                max-width: 100% !important;
            }}
            
            /* Add spacing between columns to prevent charts touching */
            [data-testid="column"] {{
                padding: 0 20px !important;
                margin-bottom: 20px !important;
            }}
            
            /* Ensure charts have vertical separation too */
            .stPlotlyChart {{
                margin-bottom: 30px !important;
                break-inside: avoid;
            }}
            
            /* Force all text elements to black (except inside Playwright charts which are handled by filter if Dark) */
            p, h1, h2, h3, h4, h5, h6, span, div, label, li, .chart-header {{
                color: #000000 !important;
            }}
            
            /* Clean up background graphics */
            * {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}
            
            /* Force Plotly SVG text to black for ALL themes in print (Visibility on White BG) */
            .stPlotlyChart text {{
                fill: #000000 !important;
            }}
        }}
    </style>
""", unsafe_allow_html=True)


# --- Main Layout ---
st.title("COVID Vaccine Dashboard")
st.markdown("`Published` `Not available` `16 days ago`", unsafe_allow_html=True)

st.markdown("---")
st.subheader("Overview")

# Row 1
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

# Pass 'theme' to charts so they can pick correct Plotly template/colors
with row1_col2:
    render_donut_chart(filtered_df, theme)

with row1_col3:
    render_bar_chart(filtered_df, theme)

# Row 2
row2_col1, row2_col2 = st.columns([2, 1])

with row2_col1:
    render_map(filtered_df, theme)

with row2_col2:
    render_sunburst(filtered_df, theme)
