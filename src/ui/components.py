import streamlit as st
import plotly.express as px
import pandas as pd

def render_donut_chart(df: pd.DataFrame, theme: str = "Dark"):
    st.markdown('<div class="chart-header">Vaccine Candidates per Phase</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("No data")
        return
        
    phase_counts = df.groupby("Stage")["Candidates"].sum().reset_index()
    fig = px.pie(
        phase_counts, 
        values="Candidates", 
        names="Stage", 
        hole=0.6,
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    
    bg_color = 'rgba(0,0,0,0)'
    template = "plotly_dark" if theme == "Dark" else "plotly_white"
    font_color = "white" if theme == "Dark" else "black"
    
    fig.update_traces(textfont_color=font_color)
    fig.update_layout(
        template=template,
        showlegend=False, 
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(color=font_color)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_bar_chart(df: pd.DataFrame, theme: str = "Dark"):
    st.markdown('<div class="chart-header">Vaccine Candidates per Phase</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("No data")
        return

    bar_data = df.groupby("Stage")["Candidates"].sum().reset_index().sort_values("Candidates", ascending=False)
    fig = px.bar(
        bar_data, 
        x="Stage", 
        y="Candidates",
        color_discrete_sequence=['#00CC96']
    )
    
    bg_color = 'rgba(0,0,0,0)'
    template = "plotly_dark" if theme == "Dark" else "plotly_white"
    font_color = "white" if theme == "Dark" else "black"
    # In light mode, we might want a visible grid
    grid_color = '#444' if theme == "Dark" else '#cccccc'
    
    fig.update_traces(
        textfont_color=font_color, 
        marker_line_width=0
    )
    fig.update_layout(
        template=template,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(color=font_color),
        xaxis=dict(
            showgrid=False, 
            tickfont=dict(color=font_color),
            title_font=dict(color=font_color)
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor=grid_color, 
            tickfont=dict(color=font_color),
            title_font=dict(color=font_color)
        )
    )
    st.plotly_chart(fig, use_container_width=True)

def render_map(df: pd.DataFrame, theme: str = "Dark"):
    st.markdown('<div class="chart-header">Map of Vaccine Candidates</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("No data")
        return

    map_data = df.groupby("Country")["Candidates"].sum().reset_index()
    fig = px.choropleth(
        map_data,
        locations="Country",
        locationmode="country names",
        color="Candidates",
        color_continuous_scale="Oranges", 
        projection="natural earth"
    )
    
    bg_color = 'rgba(0,0,0,0)'
    template = "plotly_dark" if theme == "Dark" else "plotly_white"
    land_color = '#262730' if theme == "Dark" else '#f0f2f6'
    font_color = "white" if theme == "Dark" else "black"
    
    fig.update_layout(
        template=template,
        margin=dict(t=0, b=0, l=0, r=0),
        geo=dict(
            bgcolor=bg_color,
            showlakes=False,
            showocean=False,
            landcolor=land_color,
            coastlinecolor='#444' if theme == "Dark" else '#ccc'
        ),
        paper_bgcolor=bg_color,
        font=dict(color=font_color),
        coloraxis_colorbar=dict(
            orientation='h',
            yanchor="top", 
            y=-0.05, 
            xanchor="center", 
            x=0.5,
            tickfont=dict(color=font_color),
            title=dict(font=dict(color=font_color))
        )
    )
    st.plotly_chart(fig, use_container_width=True)

def render_sunburst(df: pd.DataFrame, theme: str = "Dark"):
    st.markdown('<div class="chart-header">Sunburst of Country & Clinical Stages</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("No data")
        return

    fig = px.sunburst(
        df,
        path=['Country', 'Stage'],
        values='Candidates',
        color='Country',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    bg_color = 'rgba(0,0,0,0)'
    template = "plotly_dark" if theme == "Dark" else "plotly_white"
    font_color = "white" if theme == "Dark" else "black"
    
    # Ensure text inside sunburst is visible
    # Ideally, if segments are dark, text is white. If segments are light, text is black.
    # Since we are using "Pastel" data, segments are light. So we prefer black or dark text.
    # However in Dark mode we might want white? Let's check.
    # Actually, uniformity helps.
    
    fig.update_traces(insidetextfont=dict(color=font_color))
    
    fig.update_layout(
        template=template,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor=bg_color,
        font=dict(color=font_color)
    )
    st.plotly_chart(fig, use_container_width=True)
