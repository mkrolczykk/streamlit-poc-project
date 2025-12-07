"""
Chart components for the COVID-19 Vaccine Dashboard.
Provides Plotly-based visualizations with theme support.
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from typing import Literal

ThemeType = Literal["Dark", "Light"]


def _get_chart_config(theme: ThemeType) -> dict:
    """
    Get common chart configuration based on theme.
    
    Args:
        theme: The current theme name.
        
    Returns:
        Dictionary with common chart configuration values.
    """
    is_dark = theme == "Dark"
    return {
        "bg_color": "rgba(0,0,0,0)",
        "template": "plotly_dark" if is_dark else "plotly_white",
        "font_color": "white" if is_dark else "black",
        "grid_color": "#444" if is_dark else "#cccccc",
        "land_color": "#262730" if is_dark else "#f0f2f6",
        "coastline_color": "#444" if is_dark else "#ccc",
    }


def render_donut_chart(df: pd.DataFrame, theme: ThemeType = "Dark") -> None:
    """
    Render a donut chart showing vaccine candidates per phase.
    
    Args:
        df: DataFrame with vaccine data containing 'Stage' and 'Candidates' columns.
        theme: The current theme ('Dark' or 'Light').
    """
    st.markdown('<div class="chart-header">Vaccine Candidates per Phase</div>', unsafe_allow_html=True)
    
    if df.empty:
        st.info("No data available")
        return
    
    config = _get_chart_config(theme)
    phase_counts = df.groupby("Stage")["Candidates"].sum().reset_index()
    
    fig = px.pie(
        phase_counts, 
        values="Candidates", 
        names="Stage", 
        hole=0.6,
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    
    fig.update_traces(textfont_color=config["font_color"])
    fig.update_layout(
        template=config["template"],
        showlegend=False, 
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor=config["bg_color"],
        plot_bgcolor=config["bg_color"],
        font=dict(color=config["font_color"])
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_bar_chart(df: pd.DataFrame, theme: ThemeType = "Dark") -> None:
    """
    Render a bar chart showing vaccine candidates per phase.
    
    Args:
        df: DataFrame with vaccine data containing 'Stage' and 'Candidates' columns.
        theme: The current theme ('Dark' or 'Light').
    """
    st.markdown('<div class="chart-header">Vaccine Candidates per Phase</div>', unsafe_allow_html=True)
    
    if df.empty:
        st.info("No data available")
        return
    
    config = _get_chart_config(theme)
    bar_data = df.groupby("Stage")["Candidates"].sum().reset_index().sort_values("Candidates", ascending=False)
    
    fig = px.bar(
        bar_data, 
        x="Stage", 
        y="Candidates",
        color_discrete_sequence=["#00CC96"]
    )
    
    fig.update_traces(textfont_color=config["font_color"], marker_line_width=0)
    fig.update_layout(
        template=config["template"],
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor=config["bg_color"],
        plot_bgcolor=config["bg_color"],
        font=dict(color=config["font_color"]),
        xaxis=dict(
            showgrid=False, 
            tickfont=dict(color=config["font_color"]),
            title_font=dict(color=config["font_color"])
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor=config["grid_color"], 
            tickfont=dict(color=config["font_color"]),
            title_font=dict(color=config["font_color"])
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_map(df: pd.DataFrame, theme: ThemeType = "Dark") -> None:
    """
    Render a choropleth map showing vaccine candidates by country.
    
    Args:
        df: DataFrame with vaccine data containing 'Country' and 'Candidates' columns.
        theme: The current theme ('Dark' or 'Light').
    """
    st.markdown('<div class="chart-header">Map of Vaccine Candidates</div>', unsafe_allow_html=True)
    
    if df.empty:
        st.info("No data available")
        return
    
    config = _get_chart_config(theme)
    map_data = df.groupby("Country")["Candidates"].sum().reset_index()
    
    fig = px.choropleth(
        map_data,
        locations="Country",
        locationmode="country names",
        color="Candidates",
        color_continuous_scale="Oranges", 
        projection="natural earth"
    )
    
    fig.update_layout(
        template=config["template"],
        margin=dict(t=0, b=0, l=0, r=0),
        geo=dict(
            bgcolor=config["bg_color"],
            showlakes=False,
            showocean=False,
            landcolor=config["land_color"],
            coastlinecolor=config["coastline_color"]
        ),
        paper_bgcolor=config["bg_color"],
        font=dict(color=config["font_color"]),
        coloraxis_colorbar=dict(
            orientation="h",
            yanchor="top", 
            y=-0.05, 
            xanchor="center", 
            x=0.5,
            tickfont=dict(color=config["font_color"]),
            title=dict(font=dict(color=config["font_color"]))
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_sunburst(df: pd.DataFrame, theme: ThemeType = "Dark") -> None:
    """
    Render a sunburst chart showing country and clinical stages hierarchy.
    
    Args:
        df: DataFrame with vaccine data containing 'Country', 'Stage', and 'Candidates' columns.
        theme: The current theme ('Dark' or 'Light').
    """
    st.markdown('<div class="chart-header">Sunburst of Country & Clinical Stages</div>', unsafe_allow_html=True)
    
    if df.empty:
        st.info("No data available")
        return
    
    config = _get_chart_config(theme)
    
    fig = px.sunburst(
        df,
        path=["Country", "Stage"],
        values="Candidates",
        color="Country",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(insidetextfont=dict(color=config["font_color"]))
    fig.update_layout(
        template=config["template"],
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor=config["bg_color"],
        font=dict(color=config["font_color"])
    )
    
    st.plotly_chart(fig, use_container_width=True)
