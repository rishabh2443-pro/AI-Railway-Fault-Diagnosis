"""
dashboard package initialization
Exposes ui_components helper functions for seamless imports.
"""

from dashboard.ui_components import (
    inject_custom_css,
    render_header,
    metric_card,
    section_header,
    info_card,
    status_badge,
    fault_status_card,
    risk_assessment_card,
    risk_card,
    ai_card,
    pipeline_diagram,
    scada_footer,
    parse_ai_diagnosis,
    icon_svg
)

__all__ = [
    "inject_custom_css",
    "render_header",
    "metric_card",
    "section_header",
    "info_card",
    "status_badge",
    "fault_status_card",
    "risk_assessment_card",
    "risk_card",
    "ai_card",
    "pipeline_diagram",
    "scada_footer",
    "parse_ai_diagnosis",
    "icon_svg"
]
