"""
Style manager for injecting CSS into Streamlit.
Handles theme-aware CSS generation and injection.
"""
import streamlit as st
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.ui.styles.themes import ThemeColors


def _load_css_file(filename: str) -> str:
    """Load CSS content from a file in the styles directory."""
    styles_dir = Path(__file__).parent
    css_path = styles_dir / filename
    if css_path.exists():
        return css_path.read_text(encoding="utf-8")
    return ""


def _generate_theme_css(theme: "ThemeColors") -> str:
    """Generate theme-specific CSS variables and rules."""
    # Light theme specific overrides for sidebar toggle
    light_toggle_override = ""
    if theme.name == "Light":
        light_toggle_override = f'''
        /* Light Theme: Force sidebar toggle icon visibility */
        [data-testid="collapsedControl"] span,
        [data-testid="stSidebarCollapsedControl"] span,
        button[kind="header"] span {{
            color: {theme.toggle_icon} !important;
        }}
        [data-testid="collapsedControl"]:hover span,
        [data-testid="stSidebarCollapsedControl"]:hover span,
        button[kind="header"]:hover span {{
            color: #ff4b4b !important;
        }}
        [data-testid="collapsedControl"] [class*="st-emotion-cache"],
        [data-testid="stSidebarCollapsedControl"] [class*="st-emotion-cache"],
        button[kind="header"] [class*="st-emotion-cache"] {{
            color: {theme.toggle_icon} !important;
        }}
        [data-testid="collapsedControl"]:hover [class*="st-emotion-cache"],
        [data-testid="stSidebarCollapsedControl"]:hover [class*="st-emotion-cache"],
        button[kind="header"]:hover [class*="st-emotion-cache"] {{
            color: #ff4b4b !important;
        }}
        '''
    
    return f'''
    /* ===== THEME: {theme.name} ===== */
    
    /* Main App Background and Text */
    .stApp {{
        background-color: {theme.bg_color};
        color: {theme.text_color};
    }}
    
    /* Content container padding */
    .block-container {{
        padding-top: 1rem;
        padding-bottom: 1rem;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {theme.sidebar_bg};
    }}
    
    /* Force Text Color in Sidebar */
    [data-testid="stSidebar"] * {{
        color: {theme.sidebar_text_color} !important;
    }}
    
    [data-testid="stSidebar"] label {{
        color: {theme.sidebar_text_color} !important;
    }}

    /* Expanders in Sidebar */
    [data-testid="stSidebar"] details {{
        background-color: transparent !important;
        color: {theme.sidebar_text_color} !important;
        border-color: {theme.border_color};
    }}
    [data-testid="stSidebar"] details > summary {{
        background-color: {theme.sidebar_bg} !important;
        color: {theme.sidebar_text_color} !important;
    }}
    
    /* Sidebar Buttons */
    [data-testid="stSidebar"] button {{
        background-color: {theme.bg_color} !important;
        color: {theme.text_color} !important;
        border: 1px solid {theme.border_color} !important;
    }}
    [data-testid="stSidebar"] button:hover {{
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
    }}
    
    /* Sidebar Dividers */
    [data-testid="stSidebar"] hr {{
        border-color: {theme.border_color} !important;
        background-color: {theme.border_color} !important;
    }}

    
    /* Headers in Main Area */
    h1, h2, h3, .chart-header {{
        color: {theme.header_color} !important;
    }}
    
    .chart-header {{
        font-size: 16px; 
        font-weight: bold;
        margin-bottom: 10px;
    }}

    /* Header transparency */
    header {{
        background-color: transparent !important;
    }}
    
    /* Sidebar Toggle Button */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"],
    button[kind="header"] {{
        background-color: {theme.toggle_bg} !important;
        border: 1px solid {theme.toggle_border} !important;
        color: {theme.toggle_icon} !important;
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
    
    /* Header button icons inherit color */
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
    
    {light_toggle_override}
    
    /* Global override for header icons */
    header [class*="emotion-cache"] {{
        color: {theme.toggle_icon} !important;
    }}
    header:hover [class*="emotion-cache"] {{
        color: {theme.toggle_icon} !important;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    '''


def _get_print_css() -> str:
    """Get print-specific CSS rules."""
    return '''
    /* ===== PRINT STYLES ===== */
    @media print {
        @page {
            size: landscape;
            margin: 1cm;
        }
        
        /* Scale down content to fit 1 page */
        html, body {
            zoom: 75% !important;
            height: 100% !important;
            overflow: hidden !important;
            background-color: #ffffff !important;
            color: #000000 !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        [data-testid="stAppViewContainer"] {
            background-color: #ffffff !important;
        }
        .stApp {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        
        /* Hide non-printable elements */
        [data-testid="stSidebar"] { display: none !important; }
        header { display: none !important; }
        footer { display: none !important; }
        #MainMenu { display: none !important; }
        
        .block-container {
            padding: 1rem !important;
            max-width: 100% !important;
        }
        
        /* Spacing between columns */
        [data-testid="column"] {
            padding: 0 20px !important;
            margin-bottom: 20px !important;
        }
        
        /* Chart separation */
        .stPlotlyChart {
            margin-bottom: 30px !important;
            break-inside: avoid;
        }
        
        /* Force black text */
        p, h1, h2, h3, h4, h5, h6, span, div, label, li, .chart-header {
            color: #000000 !important;
        }
        
        /* Print color accuracy */
        * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        /* Force Plotly text to black */
        .stPlotlyChart text {
            fill: #000000 !important;
        }
    }
    '''


def inject_styles(theme: "ThemeColors") -> None:
    """
    Inject all CSS styles into the Streamlit app.
    
    Args:
        theme: The theme configuration to apply.
    """
    theme_css = _generate_theme_css(theme)
    print_css = _get_print_css()
    
    full_css = f"<style>{theme_css}\n{print_css}</style>"
    st.markdown(full_css, unsafe_allow_html=True)
