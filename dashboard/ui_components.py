"""
ui_components.py
Official shadcn/ui design system for Railway Fault Diagnosis & Predictive Maintenance Dashboard.
Supports pristine White Theme (Light Mode) and Zinc Dark Theme.
Implements shadcn/ui Card anatomy, Badges, Tabs, Lucide SVG icons, Alert boxes, Progress bars,
and minimalist modern dashboard typography.
"""

import streamlit as st
import html
import re

# ============================================================
# LUCIDE SVG ICONS (Clean 16px/20px geometric stroke icons)
# ============================================================

def icon_svg(name, size=16, color="currentColor", stroke_width=2):
    """Returns minimalist Lucide stroke SVG icons."""
    icons = {
        "activity": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
        "zap": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        "thermometer": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>',
        "radio": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="2"/><path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48-.01a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14"/></svg>',
        "gauge": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/></svg>',
        "train": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="16" x="4" y="3" rx="2"/><path d="M4 11h16"/><path d="M12 3v8"/><path d="m8 19-2 3"/><path d="m18 22-2-3"/><circle cx="8" cy="15" r="1"/><circle cx="16" cy="15" r="1"/></svg>',
        "alert_triangle": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        "alert_circle": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
        "check_circle": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
        "sparkles": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/></svg>',
        "cpu": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
        "database": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/></svg>',
        "wrench": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
        "layers": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
        "shield": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        "compass": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>',
        "clock": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "search": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
        "check": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
        "sun": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>',
        "moon": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
    }
    return icons.get(name, "")


def inject_custom_css(theme="light"):
    """
    Injects shadcn/ui White Theme (Light Mode) or Zinc Dark Theme CSS.
    Default: theme="light" (Pure White Theme).
    """
    is_light = (theme == "light")

    if is_light:
        bg_app = "#ffffff"
        fg_main = "#09090b"
        bg_card = "#ffffff"
        bg_card_muted = "#f8fafc"
        border_color = "#e4e4e7"
        muted_text = "#71717a"
        sidebar_bg = "#fafafa"
        primary_btn_bg = "#18181b"
        primary_btn_fg = "#ffffff"
        primary_btn_hover = "#27272a"
        tab_list_bg = "#f4f4f5"
        tab_active_bg = "#ffffff"
        tab_active_shadow = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
        card_shadow = "0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px -1px rgba(0, 0, 0, 0.04)"
        alert_normal_bg = "#f0fdf4"
        alert_normal_border = "#bbf7d0"
        alert_warning_bg = "#fffbeb"
        alert_warning_border = "#fde68a"
        alert_critical_bg = "#fef2f2"
        alert_critical_border = "#fecaca"
        badge_sec_bg = "#f4f4f5"
        badge_sec_fg = "#18181b"
        progress_track = "#f4f4f5"
    else:
        bg_app = "#09090b"
        fg_main = "#fafafa"
        bg_card = "#09090b"
        bg_card_muted = "#18181b"
        border_color = "#27272a"
        muted_text = "#a1a1aa"
        sidebar_bg = "#09090b"
        primary_btn_bg = "#fafafa"
        primary_btn_fg = "#18181b"
        primary_btn_hover = "#e4e4e7"
        tab_list_bg = "#18181b"
        tab_active_bg = "#09090b"
        tab_active_shadow = "0 1px 2px 0 rgba(0, 0, 0, 0.2)"
        card_shadow = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
        alert_normal_bg = "linear-gradient(135deg, rgba(34, 197, 94, 0.05) 0%, #09090b 100%)"
        alert_normal_border = "rgba(34, 197, 94, 0.25)"
        alert_warning_bg = "linear-gradient(135deg, rgba(245, 158, 11, 0.06) 0%, #09090b 100%)"
        alert_warning_border = "rgba(245, 158, 11, 0.3)"
        alert_critical_bg = "linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, #09090b 100%)"
        alert_critical_border = "rgba(239, 68, 68, 0.35)"
        badge_sec_bg = "#27272a"
        badge_sec_fg = "#fafafa"
        progress_track = "#27272a"

    st.markdown(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

    <style>
        /* Base App Canvas */
        .stApp {{
            background-color: {bg_app} !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            color: {fg_main} !important;
            letter-spacing: -0.01em;
        }}

        [data-testid="stHeader"] {{
            background: {bg_app} !important;
            border-bottom: 1px solid {border_color} !important;
        }}

        /* Main Container */
        .block-container {{
            max-width: 1480px !important;
            padding-top: 1.75rem !important;
            padding-bottom: 4rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            border-right: 1px solid {border_color} !important;
        }}

        [data-testid="stSidebar"] hr {{
            border-color: {border_color} !important;
            margin: 1rem 0 !important;
        }}

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
        [data-testid="stSidebar"] label {{
            color: {fg_main} !important;
        }}

        [data-testid="stSidebar"] .shadcn-card {{
            background-color: {'#ffffff' if is_light else '#18181b'} !important;
            border: 1px solid {border_color} !important;
            box-shadow: {card_shadow} !important;
        }}

        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Inter', sans-serif !important;
            color: {fg_main} !important;
            font-weight: 600 !important;
            letter-spacing: -0.025em !important;
        }}

        p, span, label {{
            font-family: 'Inter', sans-serif !important;
            color: {fg_main};
        }}

        /* ============================================================
           SHADCN/UI CARD COMPONENT (.shadcn-card)
           ============================================================ */
        .shadcn-card {{
            background-color: {bg_card};
            border: 1px solid {border_color};
            border-radius: 0.75rem; /* rounded-xl */
            padding: 1.5rem;
            box-shadow: {card_shadow};
            transition: border-color 0.15s ease, box-shadow 0.15s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .shadcn-card:hover {{
            border-color: {'#a1a1aa' if is_light else '#3f3f46'};
        }}

        .shadcn-metric-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }}

        .shadcn-metric-title {{
            font-size: 0.875rem;
            font-weight: 500;
            color: {muted_text};
            letter-spacing: -0.01em;
            margin: 0;
        }}

        .shadcn-metric-value {{
            font-size: 1.75rem;
            font-weight: 700;
            color: {fg_main};
            letter-spacing: -0.03em;
            line-height: 1.15;
            margin: 0.25rem 0 0.35rem 0;
            font-feature-settings: "cv02", "cv03", "cv04", "cv11";
        }}

        .shadcn-metric-desc {{
            font-size: 0.75rem;
            color: {muted_text};
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}

        /* ============================================================
           SHADCN/UI BADGES (.shadcn-badge)
           ============================================================ */
        .shadcn-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            border-radius: 9999px;
            padding: 0.125rem 0.625rem;
            font-size: 0.75rem;
            font-weight: 600;
            line-height: 1rem;
            transition: background-color 0.15s ease;
            white-space: nowrap;
        }}

        .badge-secondary {{
            background-color: {badge_sec_bg};
            color: {badge_sec_fg};
            border: 1px solid {border_color};
        }}

        .badge-outline {{
            background-color: transparent;
            color: {fg_main};
            border: 1px solid {border_color};
        }}

        .badge-default {{
            background-color: {primary_btn_bg};
            color: {primary_btn_fg};
        }}

        .badge-success {{
            background-color: {'#ecfdf5' if is_light else 'rgba(34, 197, 94, 0.1)'};
            color: {'#15803d' if is_light else '#4ade80'};
            border: 1px solid {'#bbf7d0' if is_light else 'rgba(34, 197, 94, 0.2)'};
        }}

        .badge-warning {{
            background-color: {'#fffbeb' if is_light else 'rgba(245, 158, 11, 0.1)'};
            color: {'#b45309' if is_light else '#fbbf24'};
            border: 1px solid {'#fde68a' if is_light else 'rgba(245, 158, 11, 0.2)'};
        }}

        .badge-destructive {{
            background-color: {'#fef2f2' if is_light else 'rgba(239, 68, 68, 0.1)'};
            color: {'#b91c1c' if is_light else '#f87171'};
            border: 1px solid {'#fecaca' if is_light else 'rgba(239, 68, 68, 0.2)'};
        }}

        /* ============================================================
           SHADCN/UI HEADER / PAGE TITLE BAR
           ============================================================ */
        .shadcn-header-container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 1.5rem;
            margin-bottom: 1.75rem;
            border-bottom: 1px solid {border_color};
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .shadcn-header-title {{
            font-size: 1.875rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            color: {fg_main};
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.625rem;
        }}

        .shadcn-header-subtitle {{
            font-size: 0.875rem;
            color: {muted_text};
            margin: 0.35rem 0 0 0;
            font-weight: 400;
        }}

        .shadcn-header-actions {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        /* ============================================================
           SHADCN/UI SECTION HEADERS
           ============================================================ */
        .shadcn-section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 2.25rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
        }}

        .shadcn-section-title {{
            font-size: 1.125rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: {fg_main};
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .shadcn-section-desc {{
            font-size: 0.875rem;
            color: {muted_text};
            margin: 0.25rem 0 0 0;
        }}

        /* ============================================================
           SHADCN/UI ALERT BOX
           ============================================================ */
        .shadcn-alert {{
            position: relative;
            width: 100%;
            border-radius: 0.5rem;
            border: 1px solid {border_color};
            padding: 1rem 1.25rem;
            background-color: {bg_card};
            margin-bottom: 1.25rem;
        }}

        .alert-normal {{
            border-color: {alert_normal_border};
            background: {alert_normal_bg};
        }}

        .alert-warning {{
            border-color: {alert_warning_border};
            background: {alert_warning_bg};
        }}

        .alert-critical {{
            border-color: {alert_critical_border};
            background: {alert_critical_bg};
        }}

        .shadcn-alert-title {{
            font-size: 0.875rem;
            font-weight: 600;
            color: {fg_main};
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.375rem;
        }}

        .shadcn-alert-desc {{
            font-size: 0.875rem;
            color: {'#4b5563' if is_light else '#a1a1aa'};
            line-height: 1.5;
            margin: 0;
        }}

        /* ============================================================
           SHADCN/UI PROGRESS BAR
           ============================================================ */
        .shadcn-progress-track {{
            position: relative;
            height: 0.5rem;
            width: 100%;
            overflow: hidden;
            border-radius: 9999px;
            background-color: {progress_track};
            margin: 0.75rem 0 1rem 0;
        }}

        .shadcn-progress-fill {{
            height: 100%;
            border-radius: 9999px;
            transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        /* ============================================================
           SHADCN/UI BUTTONS
           ============================================================ */
        div.stButton > button {{
            background-color: {primary_btn_bg} !important;
            color: {primary_btn_fg} !important;
            border: 1px solid {primary_btn_bg} !important;
            border-radius: 0.375rem !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            padding: 0.5rem 1rem !important;
            height: 2.25rem !important;
            transition: all 0.15s ease !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        }}

        div.stButton > button:hover {{
            background-color: {primary_btn_hover} !important;
            border-color: {primary_btn_hover} !important;
            color: {primary_btn_fg} !important;
            transform: none !important;
        }}

        /* ============================================================
           SHADCN/UI TABS (Radix UI Segmented Track)
           ============================================================ */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {tab_list_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 0.5rem !important;
            padding: 0.25rem !important;
            gap: 0.25rem !important;
            height: 2.5rem !important;
        }}

        .stTabs [data-baseweb="tab"] {{
            background-color: transparent !important;
            border-radius: 0.375rem !important;
            color: {muted_text} !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            padding: 0.35rem 0.85rem !important;
            height: 2rem !important;
            border: none !important;
            transition: all 0.15s ease !important;
        }}

        .stTabs [data-baseweb="tab"]:hover {{
            color: {fg_main} !important;
        }}

        .stTabs [aria-selected="true"] {{
            background-color: {tab_active_bg} !important;
            color: {fg_main} !important;
            border: 1px solid {border_color} !important;
            box-shadow: {tab_active_shadow} !important;
        }}

        /* ============================================================
           STREAMLIT FORM CONTROLS (shadcn Input & Select)
           ============================================================ */
        div[data-baseweb="select"] > div {{
            background-color: {bg_card} !important;
            border: 1px solid {border_color} !important;
            color: {fg_main} !important;
            border-radius: 0.375rem !important;
            font-size: 0.875rem !important;
            height: 2.25rem !important;
        }}

        div[data-baseweb="select"] > div:hover {{
            border-color: {'#71717a' if is_light else '#3f3f46'} !important;
        }}

        div[data-baseweb="popover"] {{
            background-color: {bg_card} !important;
            border: 1px solid {border_color} !important;
            border-radius: 0.5rem !important;
        }}

        /* Radio Pill Group */
        div[data-testid="stRadio"] > div {{
            background-color: {tab_list_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 0.5rem !important;
            padding: 0.35rem 0.5rem !important;
        }}

        div[data-testid="stRadio"] label p,
        div[data-testid="stRadio"] label span {{
            color: {fg_main} !important;
            font-size: 0.8125rem !important;
            font-weight: 500 !important;
        }}

        /* Expanders */
        [data-testid="stExpander"] {{
            background-color: {bg_card} !important;
            border: 1px solid {border_color} !important;
            border-radius: 0.5rem !important;
            box-shadow: {card_shadow} !important;
        }}

        [data-testid="stExpander"] summary {{
            color: {fg_main} !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
        }}

        /* Dataframe Table */
        [data-testid="stDataFrame"] {{
            border: 1px solid {border_color} !important;
            border-radius: 0.5rem !important;
            overflow: hidden !important;
        }}

        /* Pipeline Visualizer Track */
        .shadcn-pipeline-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(135px, 1fr));
            gap: 0.75rem;
            margin: 1.25rem 0;
        }}

        .shadcn-pipeline-node {{
            background-color: {bg_card};
            border: 1px solid {border_color};
            border-radius: 0.5rem;
            padding: 1rem 0.75rem;
            text-align: center;
            transition: border-color 0.15s ease, background-color 0.15s ease;
            position: relative;
        }}

        .shadcn-pipeline-node:hover {{
            border-color: {'#71717a' if is_light else '#52525b'};
            background-color: {bg_card_muted};
        }}

        .pipeline-step-num {{
            font-size: 0.6875rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            color: {muted_text};
            margin-bottom: 0.375rem;
        }}

        .pipeline-step-title {{
            font-size: 0.8125rem;
            font-weight: 600;
            color: {fg_main};
            margin-bottom: 0.25rem;
        }}

        .pipeline-step-proto {{
            font-size: 0.6875rem;
            color: {muted_text};
            font-family: 'JetBrains Mono', monospace;
        }}

        /* Footer */
        .shadcn-footer {{
            border-top: 1px solid {border_color};
            padding: 2rem 0 1rem 0;
            margin-top: 3rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: {muted_text};
            font-size: 0.8125rem;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .shadcn-footer a {{
            color: {fg_main};
            text-decoration: underline;
            text-underline-offset: 4px;
        }}
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# 1. SHADCN/UI TOP HEADER COMPONENT
# ============================================================

def render_header(train_id_display="TRAIN #1", is_online=True, last_sync=None):
    """
    Renders the official shadcn/ui Dashboard Top Header:
    Clean breadcrumbs / brand on left, status badges and active unit on right.
    """
    sync_text = f"• Synced at {last_sync}" if last_sync else ""
    
    st.markdown(f"""
    <div class="shadcn-header-container">
        <div>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                <span class="shadcn-badge badge-outline" style="font-family: 'JetBrains Mono', monospace;">
                    {icon_svg('train', size=13)} Railway SCADA
                </span>
                <span style="opacity: 0.4; font-size: 0.75rem;">/</span>
                <span style="font-size: 0.75rem; opacity: 0.75;">Predictive Maintenance</span>
            </div>
            <h1 class="shadcn-header-title">
                Railway Intelligence
            </h1>
            <p class="shadcn-header-subtitle">
                Real-time condition monitoring, multi-sensor telemetry & AI-assisted fault diagnosis {sync_text}
            </p>
        </div>
        <div class="shadcn-header-actions">
            <span class="shadcn-badge badge-success">
                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background-color: #22c55e; margin-right: 4px;"></span>
                System Online
            </span>
            <span class="shadcn-badge badge-secondary" style="font-family: 'JetBrains Mono', monospace;">
                {icon_svg('activity', size=13)}
                {html.escape(str(train_id_display))}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 2. SHADCN/UI METRIC CARD (Hero KPI Widget)
# ============================================================

def metric_card(title, value, unit="", icon_name="zap", status="normal", subtitle=None):
    """
    Renders an authentic shadcn/ui Card with Metric KPI layout:
    - CardHeader: title on left, muted Lucide SVG icon on right
    - CardContent: bold primary value with unit, muted description/delta on bottom
    """
    icon_map = {
        "speed": "zap",
        "temp": "thermometer",
        "vib": "radio",
        "brake": "gauge",
        "default": "activity"
    }
    key_icon = icon_map.get(icon_name, icon_name)
    svg_markup = icon_svg(key_icon, size=16, color="#71717a")

    status_color_map = {
        "normal": "#10b981",
        "warning": "#f59e0b",
        "critical": "#ef4444",
        "info": "#3b82f6"
    }
    dot_color = status_color_map.get(status, "#71717a")
    sub_text = subtitle if subtitle else "Normal Operating Threshold"

    st.markdown(f"""
    <div class="shadcn-card">
        <div class="shadcn-metric-header">
            <span class="shadcn-metric-title">{html.escape(title)}</span>
            <span>{svg_markup}</span>
        </div>
        <div>
            <div class="shadcn-metric-value">
                {html.escape(str(value))}
                <span style="font-size: 0.875rem; font-weight: 500; opacity: 0.7; margin-left: 2px;">{html.escape(unit)}</span>
            </div>
            <p class="shadcn-metric-desc">
                <span style="color: {dot_color}; font-size: 10px;">●</span>
                <span>{html.escape(sub_text)}</span>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 3. SHADCN/UI SECTION HEADER
# ============================================================

def section_header(title, subtitle=None, icon_name=None, badge=None):
    """Renders a standard shadcn/ui section header with optional badge."""
    icon_markup = icon_svg(icon_name, size=18, color="#71717a") if icon_name else ""
    badge_html = f'<span class="shadcn-badge badge-outline">{html.escape(badge)}</span>' if badge else ""
    desc_html = f'<p class="shadcn-section-desc">{html.escape(subtitle)}</p>' if subtitle else ""

    st.markdown(f"""
    <div class="shadcn-section-header">
        <div>
            <h2 class="shadcn-section-title">
                {icon_markup}
                <span>{html.escape(title)}</span>
            </h2>
            {desc_html}
        </div>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 4. SHADCN/UI INFO CARD (Grid Box)
# ============================================================

def info_card(title, value, subtitle=None, icon_name="activity"):
    """Renders a clean shadcn/ui Card for metadata (Train, Region, Age, Operations)."""
    svg_markup = icon_svg(icon_name, size=15, color="#71717a")
    sub_html = f'<div style="font-size: 0.75rem; opacity: 0.65; margin-top: 0.25rem;">{html.escape(subtitle)}</div>' if subtitle else ""

    st.markdown(f"""
    <div class="shadcn-card" style="padding: 1.125rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.375rem;">
            <span style="font-size: 0.75rem; font-weight: 500; opacity: 0.7; text-transform: uppercase; letter-spacing: 0.05em;">
                {html.escape(title)}
            </span>
            <span>{svg_markup}</span>
        </div>
        <div style="font-size: 1.125rem; font-weight: 600; letter-spacing: -0.02em;">
            {html.escape(str(value))}
        </div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 5. SHADCN/UI STATUS BADGE HELPER
# ============================================================

def status_badge(text, variant="secondary", icon=None):
    """
    Renders a shadcn/ui badge.
    variant: 'default' | 'secondary' | 'outline' | 'success' | 'warning' | 'destructive'
    """
    variant_class = f"badge-{variant}" if variant in ["secondary", "outline", "default", "success", "warning", "destructive"] else "badge-secondary"
    icon_html = f"{icon_svg(icon, size=12)} " if icon else ""
    st.markdown(f'<span class="shadcn-badge {variant_class}">{icon_html}{html.escape(str(text))}</span>', unsafe_allow_html=True)


# ============================================================
# 6. SHADCN/UI FAULT ALERT CARD
# ============================================================

def fault_status_card(status, detected_faults=None, dataset_failure=None):
    """
    Renders the Fault Detection Card following shadcn/ui Alert conventions:
    - Normal -> Subtle green tint & check_circle
    - Warning -> Subtle amber tint & alert_triangle
    - Critical -> Subtle destructive red tint & alert_circle
    """
    status_upper = (status or "NORMAL").upper()
    detected_faults = detected_faults or []

    if status_upper == "CRITICAL":
        alert_class = "alert-critical"
        badge_variant = "badge-destructive"
        svg_icon = icon_svg("alert_circle", size=18, color="#ef4444")
        title_text = "Critical Fault Alert"
        desc_text = "Multiple sensor parameters have breached safe operational envelopes. Urgent engineering service order generated."
    elif status_upper == "WARNING":
        alert_class = "alert-warning"
        badge_variant = "badge-warning"
        svg_icon = icon_svg("alert_triangle", size=18, color="#f59e0b")
        title_text = "Warning — Anomaly Detected"
        desc_text = "Subsystem sensor readings indicate elevated wear or thermal dissipation. Depot inspection recommended."
    else:
        alert_class = "alert-normal"
        badge_variant = "badge-success"
        svg_icon = icon_svg("check_circle", size=18, color="#10b981")
        title_text = "All Parameters Nominal"
        desc_text = "All monitored train telemetry channels are within standard design limits. No abnormal condition detected."

    # Fault badges
    if detected_faults:
        chips_html = "".join([
            f'<span class="shadcn-badge {badge_variant}" style="margin: 2px 4px 2px 0;">⚠ {html.escape(f)}</span>'
            for f in detected_faults
        ])
    else:
        chips_html = '<span style="font-size: 0.8125rem; font-weight: 500; opacity: 0.85;">✓ No active faults logged for current telemetry cycle.</span>'

    # Ground-truth failure
    if dataset_failure and str(dataset_failure).lower() != "nan" and str(dataset_failure).strip():
        dataset_html = f"""
        <div style="margin-top: 0.875rem; padding-top: 0.75rem; border-top: 1px solid rgba(128,128,128,0.2); font-size: 0.75rem; opacity: 0.8;">
            Dataset Ground-Truth Failure: <strong style="color: #ef4444;">{html.escape(str(dataset_failure))}</strong>
        </div>
        """
    else:
        dataset_html = ""

    st.markdown(f"""
    <div class="shadcn-alert {alert_class}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.5rem;">
            <div class="shadcn-alert-title">
                {svg_icon}
                <span>{title_text}</span>
            </div>
            <span class="shadcn-badge {badge_variant}">
                {status_upper}
            </span>
        </div>
        <p class="shadcn-alert-desc">
            {desc_text}
        </p>
        <div style="margin-top: 0.875rem;">
            <div style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7; margin-bottom: 0.375rem;">
                Identified Fault Conditions:
            </div>
            <div>
                {chips_html}
            </div>
        </div>
        {dataset_html}
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 7. SHADCN/UI RISK ASSESSMENT & SENSOR HEALTH
# ============================================================

def risk_assessment_card(risk_level, detected_risk_score, dataset_risk_score=None, sensor_health=None, severity=None):
    """
    Renders Risk Assessment using shadcn Card + Progress bar components.
    """
    risk_level_upper = (risk_level or "LOW").upper()

    if risk_level_upper == "HIGH" or risk_level_upper == "CRITICAL":
        fill_color = "#ef4444"
        badge_variant = "badge-destructive"
    elif risk_level_upper == "MEDIUM":
        fill_color = "#f59e0b"
        badge_variant = "badge-warning"
    else:
        fill_color = "#10b981"
        badge_variant = "badge-success"

    try:
        score_val = float(detected_risk_score)
    except:
        score_val = 15.0
    clamped_score = max(0.0, min(100.0, score_val))

    try:
        health_val = float(sensor_health) if sensor_health is not None else (100.0 - clamped_score)
    except:
        health_val = 88.0
    clamped_health = max(0.0, min(100.0, health_val))

    dataset_score_str = f"{float(dataset_risk_score):.1f}" if dataset_risk_score is not None and not str(dataset_risk_score).lower() == "nan" else "N/A"
    severity_str = str(severity) if severity is not None and not str(severity).lower() == "nan" else "Nominal"

    st.markdown(f"""
    <div class="shadcn-card" style="padding: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.8125rem; font-weight: 500; opacity: 0.75;">
                Aggregate Fleet Risk Score
            </span>
            <span class="shadcn-badge {badge_variant}">
                {risk_level_upper} RISK
            </span>
        </div>
        <div class="shadcn-progress-track">
            <div class="shadcn-progress-fill" style="width: {clamped_score}%; background-color: {fill_color};"></div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin-top: 0.25rem;">
            <div class="shadcn-card" style="padding: 0.625rem; text-align: center; border-radius: 0.375rem;">
                <div style="font-size: 0.6875rem; opacity: 0.7; text-transform: uppercase;">Detected</div>
                <div style="font-size: 1rem; font-weight: 700; font-family: 'JetBrains Mono', monospace;">
                    {clamped_score:.1f}
                </div>
            </div>
            <div class="shadcn-card" style="padding: 0.625rem; text-align: center; border-radius: 0.375rem;">
                <div style="font-size: 0.6875rem; opacity: 0.7; text-transform: uppercase;">Dataset</div>
                <div style="font-size: 1rem; font-weight: 700; font-family: 'JetBrains Mono', monospace;">
                    {dataset_score_str}
                </div>
            </div>
            <div class="shadcn-card" style="padding: 0.625rem; text-align: center; border-radius: 0.375rem;">
                <div style="font-size: 0.6875rem; opacity: 0.7; text-transform: uppercase;">Health Index</div>
                <div style="font-size: 1rem; font-weight: 700; color: #10b981; font-family: 'JetBrains Mono', monospace;">
                    {clamped_health:.1f}%
                </div>
            </div>
            <div class="shadcn-card" style="padding: 0.625rem; text-align: center; border-radius: 0.375rem;">
                <div style="font-size: 0.6875rem; opacity: 0.7; text-transform: uppercase;">Severity</div>
                <div style="font-size: 0.875rem; font-weight: 600; color: #f59e0b; margin-top: 2px;">
                    {html.escape(severity_str)}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Alias risk_card to risk_assessment_card
risk_card = risk_assessment_card


# ============================================================
# 8. SHADCN/UI AI DIAGNOSIS CARDS
# ============================================================

def ai_card(title, content, icon_name="sparkles", variant="secondary"):
    """
    Renders individual AI Railway Diagnosis cards styled as shadcn/ui Cards:
    CardHeader with title and icon, CardContent with clean prose.
    """
    svg_markup = icon_svg(icon_name, size=16, color="#71717a")
    clean_content = content.strip() if content else "No advisory generated."
    clean_content = re.sub(r'^\*+\s*', '', clean_content)

    st.markdown(f"""
    <div class="shadcn-card" style="padding: 1.25rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
            <div style="font-size: 0.8125rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; letter-spacing: -0.01em;">
                {svg_markup}
                <span>{html.escape(title)}</span>
            </div>
            <span class="shadcn-badge badge-outline" style="font-size: 0.6875rem;">AI Advisory</span>
        </div>
        <div style="font-size: 0.875rem; line-height: 1.6; font-weight: 400; opacity: 0.9;">
            {html.escape(clean_content).replace(chr(10), '<br>')}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 9. SHADCN/UI SYSTEM ARCHITECTURE PIPELINE
# ============================================================

def pipeline_diagram():
    """
    Renders the system pipeline as a grid of minimal shadcn/ui cards.
    """
    steps = [
        ("01", "zap", "Sensor Sim", "IoT Ingestion"),
        ("02", "radio", "MQTT Broker", "Port 1883"),
        ("03", "cpu", "Stream Engine", "Python Consumer"),
        ("04", "alert_triangle", "Rule Engine", "Fault Detector"),
        ("05", "database", "PostgreSQL", "Relational Store"),
        ("06", "layers", "RAG Engine", "LangChain + FAISS"),
        ("07", "cpu", "Ollama LLM", "Llama 3.2"),
        ("08", "sparkles", "AI Diagnosis", "Root Cause Directives"),
        ("09", "train", "SCADA UI", "Streamlit Dashboard")
    ]

    cards_html = ""
    for num, icon_key, title, proto in steps:
        svg_code = icon_svg(icon_key, size=18, color="#71717a")
        cards_html += f"""
        <div class="shadcn-pipeline-node">
            <div class="pipeline-step-num">{num}</div>
            <div style="margin: 0.35rem 0;">{svg_code}</div>
            <div class="pipeline-step-title">{title}</div>
            <div class="pipeline-step-proto">{proto}</div>
        </div>
        """

    st.markdown(f"""
    <div class="shadcn-pipeline-grid">
        {cards_html}
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 10. SHADCN/UI AI OUTPUT PARSER
# ============================================================

def parse_ai_diagnosis(raw_text):
    """
    Parses Ollama output into 4 structured sections:
    - diagnosis
    - possible_causes
    - recommended_action
    - safety_recommendation
    """
    sections = {
        "diagnosis": "",
        "possible_causes": "",
        "recommended_action": "",
        "safety_recommendation": ""
    }
    if not raw_text or not isinstance(raw_text, str):
        return sections

    text = raw_text.strip()

    pattern = re.compile(
        r'(?:\d+[\.\)]\s*|\*\*|\#+\s*)?(Diagnosis|Possible Causes?|Recommended Actions?|Safety Advice|Safety Recommendations?)(?:\*\*|\#+)?[:\s]*',
        re.IGNORECASE
    )

    parts = pattern.split(text)
    if len(parts) >= 3:
        for i in range(1, len(parts), 2):
            header = parts[i].strip().lower()
            content = parts[i+1].strip() if i+1 < len(parts) else ""
            content = re.sub(r'^\*+\s*', '', content)
            content = re.sub(r'^\#+\s*', '', content)
            if "diagnosis" in header:
                sections["diagnosis"] = content
            elif "cause" in header:
                sections["possible_causes"] = content
            elif "action" in header:
                sections["recommended_action"] = content
            elif "safety" in header or "advice" in header:
                sections["safety_recommendation"] = content

    if not sections["diagnosis"]:
        sections["diagnosis"] = text

    return sections


# ============================================================
# 11. SHADCN/UI FOOTER
# ============================================================

def scada_footer():
    """Renders the clean shadcn/ui footer."""
    st.markdown("""
    <div class="shadcn-footer">
        <div>
            Built with <strong>Python</strong>, <strong>Streamlit</strong>, <strong>PostgreSQL</strong>, <strong>MQTT</strong>, <strong>LangChain FAISS</strong> & <strong>Ollama Llama-3.2</strong>.
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;">
            Designed with <a href="https://github.com/shadcn-ui/ui" target="_blank">shadcn/ui</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
