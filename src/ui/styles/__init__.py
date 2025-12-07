"""Styles package for CSS and theme management."""
from src.ui.styles.themes import get_theme, ThemeColors, ThemeType, DARK_THEME, LIGHT_THEME
from src.ui.styles.style_manager import inject_styles

__all__ = [
    "get_theme",
    "ThemeColors", 
    "ThemeType",
    "DARK_THEME",
    "LIGHT_THEME",
    "inject_styles",
]
