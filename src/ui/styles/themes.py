"""
Theme configuration for the COVID Vaccine Dashboard.
Centralized color and styling definitions for Dark and Light themes.
"""
from dataclasses import dataclass
from typing import Literal

ThemeType = Literal["Dark", "Light"]


@dataclass(frozen=True)
class ThemeColors:
    """Immutable theme color configuration."""
    name: str
    bg_color: str
    text_color: str
    sidebar_bg: str
    sidebar_text_color: str
    header_color: str
    border_color: str
    # Chart-specific
    grid_color: str
    land_color: str
    coastline_color: str
    # Sidebar toggle button
    toggle_bg: str
    toggle_border: str
    toggle_icon: str


# Theme definitions
DARK_THEME = ThemeColors(
    name="Dark",
    bg_color="#0e1117",
    text_color="#ffffff",
    sidebar_bg="#262730",
    sidebar_text_color="#ffffff",
    header_color="#e0e0e0",
    border_color="#444",
    grid_color="#444",
    land_color="#262730",
    coastline_color="#444",
    toggle_bg="#0e1117",
    toggle_border="rgba(250, 250, 250, 0.2)",
    toggle_icon="#fafafa",
)

LIGHT_THEME = ThemeColors(
    name="Light",
    bg_color="#ffffff",
    text_color="#000000",
    sidebar_bg="#f8f9fa",
    sidebar_text_color="#000000",
    header_color="#333333",
    border_color="#dee2e6",
    grid_color="#cccccc",
    land_color="#f0f2f6",
    coastline_color="#ccc",
    toggle_bg="#ffffff",
    toggle_border="rgba(49, 51, 63, 0.2)",
    toggle_icon="#31333F",
)


def get_theme(theme_name: ThemeType) -> ThemeColors:
    """Get theme configuration by name."""
    return DARK_THEME if theme_name == "Dark" else LIGHT_THEME
