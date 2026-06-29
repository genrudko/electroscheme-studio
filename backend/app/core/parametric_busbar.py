from __future__ import annotations

from app.schemas.parametric_symbols import (
    BusbarPreviewRequest,
    ParametricSymbolPreview,
    ParametricTerminal,
)


def _fmt(value: float) -> str:
    if abs(value) < 1e-9:
        value = 0.0
    return f"{value:.6g}"


def _voltage_css_var() -> str:
    return "var(--voltage-color, currentColor)"


def _horizontal_terminals(params: BusbarPreviewRequest) -> tuple[list[ParametricTerminal], str, dict[str, float]]:
    margin = params.margin
    y = margin + params.lead_length
    length = params.length
    height = margin * 2 + params.lead_length * 2
    width = length + margin * 2

    terminals: list[ParametricTerminal] = [
        ParametricTerminal(id="left_end", x=margin, y=y, role="busbar_end", side="left"),
        ParametricTerminal(id="right_end", x=margin + length, y=y, role="busbar_end", side="right"),
    ]

    elements = [
        (
            f'<line x1="{_fmt(margin)}" y1="{_fmt(y)}" '
            f'x2="{_fmt(margin + length)}" y2="{_fmt(y)}" '
            f'stroke="{_voltage_css_var()}" stroke-width="{_fmt(params.stroke_width)}" '
            'stroke-linecap="round" vector-effect="non-scaling-stroke" />'
        )
    ]

    if params.connection_count > 0:
        step = length / (params.connection_count + 1)
        for index in range(params.connection_count):
            x = margin + step * (index + 1)
            if params.connection_side in {"top", "both"}:
                y2 = y - params.lead_length
                terminals.append(
                    ParametricTerminal(
                        id=f"tap_top_{index + 1}",
                        x=x,
                        y=y2,
                        role="parameterized_connection",
                        side="top",
                        index=index + 1,
                    )
                )
                elements.append(
                    f'<line x1="{_fmt(x)}" y1="{_fmt(y)}" x2="{_fmt(x)}" y2="{_fmt(y2)}" '
                    f'stroke="{_voltage_css_var()}" stroke-width="1.5" vector-effect="non-scaling-stroke" />'
                )
            if params.connection_side in {"bottom", "both"}:
                y2 = y + params.lead_length
                terminals.append(
                    ParametricTerminal(
                        id=f"tap_bottom_{index + 1}",
                        x=x,
                        y=y2,
                        role="parameterized_connection",
                        side="bottom",
                        index=index + 1,
                    )
                )
                elements.append(
                    f'<line x1="{_fmt(x)}" y1="{_fmt(y)}" x2="{_fmt(x)}" y2="{_fmt(y2)}" '
                    f'stroke="{_voltage_css_var()}" stroke-width="1.5" vector-effect="non-scaling-stroke" />'
                )

    view_box = {"x": 0.0, "y": 0.0, "width": width, "height": height}
    return terminals, "\n".join(elements), view_box


def _vertical_terminals(params: BusbarPreviewRequest) -> tuple[list[ParametricTerminal], str, dict[str, float]]:
    margin = params.margin
    x = margin + params.lead_length
    length = params.length
    width = margin * 2 + params.lead_length * 2
    height = length + margin * 2

    terminals: list[ParametricTerminal] = [
        ParametricTerminal(id="top_end", x=x, y=margin, role="busbar_end", side="top"),
        ParametricTerminal(id="bottom_end", x=x, y=margin + length, role="busbar_end", side="bottom"),
    ]

    elements = [
        (
            f'<line x1="{_fmt(x)}" y1="{_fmt(margin)}" '
            f'x2="{_fmt(x)}" y2="{_fmt(margin + length)}" '
            f'stroke="{_voltage_css_var()}" stroke-width="{_fmt(params.stroke_width)}" '
            'stroke-linecap="round" vector-effect="non-scaling-stroke" />'
        )
    ]

    if params.connection_count > 0:
        step = length / (params.connection_count + 1)
        for index in range(params.connection_count):
            y = margin + step * (index + 1)
            if params.connection_side in {"top", "both"}:
                x2 = x - params.lead_length
                terminals.append(
                    ParametricTerminal(
                        id=f"tap_left_{index + 1}",
                        x=x2,
                        y=y,
                        role="parameterized_connection",
                        side="left",
                        index=index + 1,
                    )
                )
                elements.append(
                    f'<line x1="{_fmt(x)}" y1="{_fmt(y)}" x2="{_fmt(x2)}" y2="{_fmt(y)}" '
                    f'stroke="{_voltage_css_var()}" stroke-width="1.5" vector-effect="non-scaling-stroke" />'
                )
            if params.connection_side in {"bottom", "both"}:
                x2 = x + params.lead_length
                terminals.append(
                    ParametricTerminal(
                        id=f"tap_right_{index + 1}",
                        x=x2,
                        y=y,
                        role="parameterized_connection",
                        side="right",
                        index=index + 1,
                    )
                )
                elements.append(
                    f'<line x1="{_fmt(x)}" y1="{_fmt(y)}" x2="{_fmt(x2)}" y2="{_fmt(y)}" '
                    f'stroke="{_voltage_css_var()}" stroke-width="1.5" vector-effect="non-scaling-stroke" />'
                )

    view_box = {"x": 0.0, "y": 0.0, "width": width, "height": height}
    return terminals, "\n".join(elements), view_box


def generate_busbar_preview(params: BusbarPreviewRequest) -> ParametricSymbolPreview:
    if params.orientation == "vertical":
        terminals, svg_fragment, view_box = _vertical_terminals(params)
    else:
        terminals, svg_fragment, view_box = _horizontal_terminals(params)

    capabilities = {
        "feature_flags": {
            "parametric": True,
            "busbar": True,
            "colorizable_by_voltage_class": True,
            "rotatable": True,
            "stretchable": True,
            "snap_anchors_required": True,
            "auto_layout_eligible": True,
            "connection_count_configurable": True,
        },
        "busbar": {
            "connection_count": params.connection_count,
            "connection_side": params.connection_side,
            "orientation": params.orientation,
            "length": params.length,
            "stroke_width_multiplier": params.stroke_width,
        },
        "auto_scheme_generation": {
            "role": "bus_section",
            "can_host_bays": True,
            "terminal_generation": "even_spacing",
        },
    }

    return ParametricSymbolPreview(
        id=params.id,
        name_ru=params.name_ru,
        kind="busbar",
        viewBox=view_box,
        svg_fragment=svg_fragment,
        terminals=terminals,
        snap_anchors=terminals,
        parameters=params,
        capabilities=capabilities,
    )