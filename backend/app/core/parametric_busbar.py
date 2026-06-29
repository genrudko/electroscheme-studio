from __future__ import annotations

from app.schemas.parametric_symbols import (
    BusbarPreviewRequest,
    ParametricBaySlot,
    ParametricSymbolPreview,
    ParametricTerminal,
)


def _fmt(value: float) -> str:
    if abs(value) < 1e-9:
        value = 0.0
    return f"{value:.6g}"


def _voltage_css_var() -> str:
    return "var(--voltage-color, currentColor)"


def _equipment_kinds_for_bus_slot() -> list[str]:
    return [
        "circuit_breaker",
        "disconnector",
        "earthing_switch",
        "voltage_transformer",
        "surge_arrester",
        "line_feeder",
        "transformer_feeder",
        "section_coupler",
    ]


def _make_slot(
    *,
    terminal: ParametricTerminal,
    bus_x: float,
    bus_y: float,
    bay_depth: float,
) -> ParametricBaySlot:
    if terminal.side == "top":
        anchor_x = terminal.x
        anchor_y = terminal.y - bay_depth
        direction = "up"
        side = "top"
    elif terminal.side == "bottom":
        anchor_x = terminal.x
        anchor_y = terminal.y + bay_depth
        direction = "down"
        side = "bottom"
    elif terminal.side == "left":
        anchor_x = terminal.x - bay_depth
        anchor_y = terminal.y
        direction = "left"
        side = "left"
    else:
        anchor_x = terminal.x + bay_depth
        anchor_y = terminal.y
        direction = "right"
        side = "right"

    index = terminal.index or 0
    return ParametricBaySlot(
        id=f"bay_slot_{terminal.side}_{index}",
        terminal_id=terminal.id,
        index=index,
        side=side,
        bus_x=bus_x,
        bus_y=bus_y,
        terminal_x=terminal.x,
        terminal_y=terminal.y,
        equipment_anchor_x=anchor_x,
        equipment_anchor_y=anchor_y,
        preferred_routing_direction=direction,
        allowed_equipment_kinds=_equipment_kinds_for_bus_slot(),
    )


def _horizontal_terminals(params: BusbarPreviewRequest) -> tuple[list[ParametricTerminal], list[ParametricBaySlot], str, dict[str, float]]:
    margin = params.margin
    y = margin + params.lead_length + (params.bay_depth if params.connection_side in {"top", "both"} else 0)
    length = params.length
    top_extra = params.bay_depth if params.connection_side in {"top", "both"} else 0
    bottom_extra = params.bay_depth if params.connection_side in {"bottom", "both"} else 0
    height = margin * 2 + params.lead_length * 2 + top_extra + bottom_extra
    width = length + margin * 2

    terminals: list[ParametricTerminal] = [
        ParametricTerminal(id="left_end", x=margin, y=y, role="busbar_end", side="left"),
        ParametricTerminal(id="right_end", x=margin + length, y=y, role="busbar_end", side="right"),
    ]
    bay_slots: list[ParametricBaySlot] = []

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
                terminal = ParametricTerminal(
                    id=f"tap_top_{index + 1}",
                    x=x,
                    y=y2,
                    role="parameterized_connection",
                    side="top",
                    index=index + 1,
                )
                terminals.append(terminal)
                bay_slots.append(_make_slot(terminal=terminal, bus_x=x, bus_y=y, bay_depth=params.bay_depth))
                elements.append(
                    f'<line x1="{_fmt(x)}" y1="{_fmt(y)}" x2="{_fmt(x)}" y2="{_fmt(y2)}" '
                    f'stroke="{_voltage_css_var()}" stroke-width="1.5" vector-effect="non-scaling-stroke" />'
                )
            if params.connection_side in {"bottom", "both"}:
                y2 = y + params.lead_length
                terminal = ParametricTerminal(
                    id=f"tap_bottom_{index + 1}",
                    x=x,
                    y=y2,
                    role="parameterized_connection",
                    side="bottom",
                    index=index + 1,
                )
                terminals.append(terminal)
                bay_slots.append(_make_slot(terminal=terminal, bus_x=x, bus_y=y, bay_depth=params.bay_depth))
                elements.append(
                    f'<line x1="{_fmt(x)}" y1="{_fmt(y)}" x2="{_fmt(x)}" y2="{_fmt(y2)}" '
                    f'stroke="{_voltage_css_var()}" stroke-width="1.5" vector-effect="non-scaling-stroke" />'
                )

    for slot in bay_slots:
        elements.append(
            f'<circle cx="{_fmt(slot.equipment_anchor_x)}" cy="{_fmt(slot.equipment_anchor_y)}" r="3" '
            'fill="none" stroke="var(--slot-color, #2563eb)" stroke-width="1" vector-effect="non-scaling-stroke" />'
        )

    view_box = {"x": 0.0, "y": 0.0, "width": width, "height": height}
    return terminals, bay_slots, "\n".join(elements), view_box


def _vertical_terminals(params: BusbarPreviewRequest) -> tuple[list[ParametricTerminal], list[ParametricBaySlot], str, dict[str, float]]:
    margin = params.margin
    x = margin + params.lead_length + (params.bay_depth if params.connection_side in {"top", "both"} else 0)
    length = params.length
    left_extra = params.bay_depth if params.connection_side in {"top", "both"} else 0
    right_extra = params.bay_depth if params.connection_side in {"bottom", "both"} else 0
    width = margin * 2 + params.lead_length * 2 + left_extra + right_extra
    height = length + margin * 2

    terminals: list[ParametricTerminal] = [
        ParametricTerminal(id="top_end", x=x, y=margin, role="busbar_end", side="top"),
        ParametricTerminal(id="bottom_end", x=x, y=margin + length, role="busbar_end", side="bottom"),
    ]
    bay_slots: list[ParametricBaySlot] = []

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
                terminal = ParametricTerminal(
                    id=f"tap_left_{index + 1}",
                    x=x2,
                    y=y,
                    role="parameterized_connection",
                    side="left",
                    index=index + 1,
                )
                terminals.append(terminal)
                bay_slots.append(_make_slot(terminal=terminal, bus_x=x, bus_y=y, bay_depth=params.bay_depth))
                elements.append(
                    f'<line x1="{_fmt(x)}" y1="{_fmt(y)}" x2="{_fmt(x2)}" y2="{_fmt(y)}" '
                    f'stroke="{_voltage_css_var()}" stroke-width="1.5" vector-effect="non-scaling-stroke" />'
                )
            if params.connection_side in {"bottom", "both"}:
                x2 = x + params.lead_length
                terminal = ParametricTerminal(
                    id=f"tap_right_{index + 1}",
                    x=x2,
                    y=y,
                    role="parameterized_connection",
                    side="right",
                    index=index + 1,
                )
                terminals.append(terminal)
                bay_slots.append(_make_slot(terminal=terminal, bus_x=x, bus_y=y, bay_depth=params.bay_depth))
                elements.append(
                    f'<line x1="{_fmt(x)}" y1="{_fmt(y)}" x2="{_fmt(x2)}" y2="{_fmt(y)}" '
                    f'stroke="{_voltage_css_var()}" stroke-width="1.5" vector-effect="non-scaling-stroke" />'
                )

    for slot in bay_slots:
        elements.append(
            f'<circle cx="{_fmt(slot.equipment_anchor_x)}" cy="{_fmt(slot.equipment_anchor_y)}" r="3" '
            'fill="none" stroke="var(--slot-color, #2563eb)" stroke-width="1" vector-effect="non-scaling-stroke" />'
        )

    view_box = {"x": 0.0, "y": 0.0, "width": width, "height": height}
    return terminals, bay_slots, "\n".join(elements), view_box


def generate_busbar_preview(params: BusbarPreviewRequest) -> ParametricSymbolPreview:
    if params.orientation == "vertical":
        terminals, bay_slots, svg_fragment, view_box = _vertical_terminals(params)
    else:
        terminals, bay_slots, svg_fragment, view_box = _horizontal_terminals(params)

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
            "bay_slots": True,
        },
        "busbar": {
            "connection_count": params.connection_count,
            "connection_side": params.connection_side,
            "orientation": params.orientation,
            "length": params.length,
            "stroke_width_multiplier": params.stroke_width,
            "bay_depth": params.bay_depth,
            "bay_slot_count": len(bay_slots),
        },
        "auto_scheme_generation": {
            "role": "bus_section",
            "can_host_bays": True,
            "slot_model": "generated_even_spacing",
            "terminal_generation": "even_spacing",
            "bay_slot_count": len(bay_slots),
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
        bay_slots=bay_slots,
        parameters=params,
        capabilities=capabilities,
    )