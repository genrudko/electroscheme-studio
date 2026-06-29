from __future__ import annotations

import html
from dataclasses import dataclass

from app.schemas.parametric_symbols import (
    BusbarPreviewRequest,
    ParametricBaySlot,
    ParametricSymbolPreview,
    ParametricTerminal,
)


@dataclass
class _BarGeometry:
    bar_x: float
    bar_y: float
    bar_w: float
    bar_h: float
    center_x: float
    center_y: float
    view_w: float
    view_h: float
    label_anchor_x: float
    label_anchor_y: float
    label_rotation: int = 0


def _fmt(value: float) -> str:
    if abs(value) < 1e-9:
        value = 0.0
    return f"{value:.6g}"


def _bar_fill() -> str:
    return "var(--busbar-color, #6d0ad6)"


def _slot_stroke() -> str:
    return "var(--slot-stroke, #ffffff)"


def _label_color() -> str:
    return "var(--label-color, #111111)"


def _number_text(params: BusbarPreviewRequest, label_number: int | None) -> str:
    if not params.bay_numbering_enabled or label_number is None:
        return ""
    if params.bay_numbering_style == "prefix_number":
        return f"{params.bay_numbering_prefix}{label_number}"
    return f"{label_number}"


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


def _spacing(params: BusbarPreviewRequest) -> float:
    return params.connection_spacing if params.connection_spacing is not None else 48.0


def _required_slot_length(params: BusbarPreviewRequest) -> float:
    if params.connection_count <= 0:
        return max(params.length, params.end_slot_offset * 2.0)
    if params.connection_count == 1:
        return max(params.end_slot_offset * 2.0, params.slot_diameter + params.end_slot_offset * 2.0)
    return params.end_slot_offset * 2.0 + _spacing(params) * (params.connection_count - 1)


def _compute_length(params: BusbarPreviewRequest) -> float:
    required = _required_slot_length(params)
    if params.fit_length_to_slots:
        return required
    return max(params.length, required)


def _auto_bus_label_position(params: BusbarPreviewRequest, geom: _BarGeometry) -> tuple[float, float, int]:
    pos = params.bus_label_position
    gap = params.bus_label_gap
    if params.orientation == "horizontal":
        if pos == "auto":
            pos = "right"
        if pos == "left":
            return geom.bar_x - gap, geom.center_y, 0
        if pos == "top":
            return geom.center_x, geom.bar_y - gap, 0
        if pos == "bottom":
            return geom.center_x, geom.bar_y + geom.bar_h + gap, 0
        return geom.bar_x + geom.bar_w + gap, geom.center_y, 0

    if pos == "auto":
        pos = "top"
    if pos == "left":
        return geom.bar_x - gap, geom.center_y, -90
    if pos == "right":
        return geom.bar_x + geom.bar_w + gap, geom.center_y, 90
    if pos == "bottom":
        return geom.center_x, geom.bar_y + geom.bar_h + gap, 0
    return geom.center_x, geom.bar_y - gap, -90


def _bus_label_position(params: BusbarPreviewRequest, geom: _BarGeometry) -> tuple[float, float, int]:
    x, y, rotation = _auto_bus_label_position(params, geom)
    x += params.bus_label_offset_x
    y += params.bus_label_offset_y
    if params.bus_label_rotation_mode == "manual":
        rotation = params.bus_label_rotation_deg
    return x, y, rotation


def _horizontal_geometry(params: BusbarPreviewRequest) -> _BarGeometry:
    label_top_zone = params.bay_label_offset + 30.0 if params.bay_numbering_enabled else 0.0
    label_bottom_zone = (
        params.bay_label_offset + 30.0
        if params.bay_numbering_enabled and params.connection_side == "both" and params.bay_label_both_side_separate_rows
        else 0.0
    )
    top_slot_zone = params.bay_depth if params.connection_side in {"top", "both"} else 0.0
    bottom_slot_zone = params.bay_depth if params.connection_side in {"bottom", "both"} else 0.0
    length = _compute_length(params)

    bar_x = params.margin
    bar_y = params.margin + label_top_zone + top_slot_zone + 8.0
    bar_w = length
    bar_h = params.thickness_mm
    center_y = bar_y + bar_h / 2.0

    temp_geom = _BarGeometry(
        bar_x=bar_x,
        bar_y=bar_y,
        bar_w=bar_w,
        bar_h=bar_h,
        center_x=bar_x + bar_w / 2.0,
        center_y=center_y,
        view_w=0.0,
        view_h=0.0,
        label_anchor_x=0.0,
        label_anchor_y=0.0,
    )
    label_x, label_y, rotation = _bus_label_position(params, temp_geom)

    view_w = max(bar_x + bar_w + params.margin + 220.0, label_x + 220.0)
    view_h = max(bar_y + bar_h + bottom_slot_zone + label_bottom_zone + params.margin + 20.0, label_y + 80.0)

    return _BarGeometry(
        bar_x=bar_x,
        bar_y=bar_y,
        bar_w=bar_w,
        bar_h=bar_h,
        center_x=bar_x + bar_w / 2.0,
        center_y=center_y,
        view_w=view_w,
        view_h=view_h,
        label_anchor_x=label_x,
        label_anchor_y=label_y,
        label_rotation=rotation,
    )


def _vertical_geometry(params: BusbarPreviewRequest) -> _BarGeometry:
    label_left_zone = params.bay_label_offset + 30.0 if params.bay_numbering_enabled else 0.0
    left_slot_zone = params.bay_depth if params.connection_side in {"top", "both"} else 0.0
    right_slot_zone = params.bay_depth if params.connection_side in {"bottom", "both"} else 0.0
    length = _compute_length(params)

    bar_x = params.margin + label_left_zone + left_slot_zone + 12.0
    bar_y = params.margin + 44.0
    bar_w = params.thickness_mm
    bar_h = length
    center_x = bar_x + bar_w / 2.0

    temp_geom = _BarGeometry(
        bar_x=bar_x,
        bar_y=bar_y,
        bar_w=bar_w,
        bar_h=bar_h,
        center_x=center_x,
        center_y=bar_y + bar_h / 2.0,
        view_w=0.0,
        view_h=0.0,
        label_anchor_x=0.0,
        label_anchor_y=0.0,
    )
    label_x, label_y, rotation = _bus_label_position(params, temp_geom)

    view_w = max(bar_x + bar_w + right_slot_zone + params.margin + 220.0, label_x + 160.0)
    view_h = max(bar_y + bar_h + params.margin + 60.0, label_y + 120.0)

    return _BarGeometry(
        bar_x=bar_x,
        bar_y=bar_y,
        bar_w=bar_w,
        bar_h=bar_h,
        center_x=center_x,
        center_y=bar_y + bar_h / 2.0,
        view_w=view_w,
        view_h=view_h,
        label_anchor_x=label_x,
        label_anchor_y=label_y,
        label_rotation=rotation,
    )


def _slot_positions_horizontal(params: BusbarPreviewRequest, geom: _BarGeometry) -> list[float]:
    if params.connection_count <= 0:
        return []
    if params.connection_count == 1:
        return [geom.bar_x + geom.bar_w / 2.0]
    spacing = _spacing(params)
    return [geom.bar_x + params.end_slot_offset + i * spacing for i in range(params.connection_count)]


def _slot_positions_vertical(params: BusbarPreviewRequest, geom: _BarGeometry) -> list[float]:
    if params.connection_count <= 0:
        return []
    if params.connection_count == 1:
        return [geom.bar_y + geom.bar_h / 2.0]
    spacing = _spacing(params)
    return [geom.bar_y + params.end_slot_offset + i * spacing for i in range(params.connection_count)]


def _bay_label_position(params: BusbarPreviewRequest, geom: _BarGeometry, slot_side: str, bus_x: float, bus_y: float) -> tuple[float | None, float | None]:
    if not params.bay_numbering_enabled:
        return None, None

    if params.orientation == "horizontal":
        if params.connection_side == "both" and params.bay_label_both_side_separate_rows and slot_side == "bottom":
            return bus_x, geom.bar_y + geom.bar_h + params.bay_label_offset
        return bus_x, geom.bar_y - params.bay_label_offset

    if params.connection_side == "both" and params.bay_label_both_side_separate_rows and slot_side == "right":
        return geom.bar_x + geom.bar_w + params.bay_label_offset, bus_y
    return geom.bar_x - params.bay_label_offset, bus_y


def _make_slot(
    *,
    params: BusbarPreviewRequest,
    terminal_id: str,
    slot_side: str,
    index: int,
    bus_x: float,
    bus_y: float,
    label_number: int | None,
    geom: _BarGeometry,
) -> ParametricBaySlot:
    if slot_side == "top":
        equipment_anchor_x = bus_x
        equipment_anchor_y = geom.bar_y - params.bay_depth
        direction = "up"
    elif slot_side == "bottom":
        equipment_anchor_x = bus_x
        equipment_anchor_y = geom.bar_y + geom.bar_h + params.bay_depth
        direction = "down"
    elif slot_side == "left":
        equipment_anchor_x = geom.bar_x - params.bay_depth
        equipment_anchor_y = bus_y
        direction = "left"
    else:
        equipment_anchor_x = geom.bar_x + geom.bar_w + params.bay_depth
        equipment_anchor_y = bus_y
        direction = "right"

    label_x, label_y = _bay_label_position(params, geom, slot_side, bus_x, bus_y)

    return ParametricBaySlot(
        id=f"bay_slot_{slot_side}_{index}",
        terminal_id=terminal_id,
        index=index,
        side=slot_side,
        bus_x=bus_x,
        bus_y=bus_y,
        terminal_x=bus_x,
        terminal_y=bus_y,
        equipment_anchor_x=equipment_anchor_x,
        equipment_anchor_y=equipment_anchor_y,
        preferred_routing_direction=direction,
        label_number=label_number,
        label=_number_text(params, label_number),
        label_x=label_x,
        label_y=label_y,
        allowed_equipment_kinds=_equipment_kinds_for_bus_slot(),
    )


def _render_busbar_rect(elements: list[str], geom: _BarGeometry) -> None:
    elements.append(
        f'<rect x="{_fmt(geom.bar_x)}" y="{_fmt(geom.bar_y)}" '
        f'width="{_fmt(geom.bar_w)}" height="{_fmt(geom.bar_h)}" '
        f'fill="{_bar_fill()}" stroke="{_bar_fill()}" stroke-width="1" rx="0" />'
    )


def _render_bus_label(elements: list[str], params: BusbarPreviewRequest, geom: _BarGeometry) -> None:
    if not params.bus_label:
        return

    label = html.escape(params.bus_label)
    x = geom.label_anchor_x
    y = geom.label_anchor_y
    rotation = geom.label_rotation

    elements.append(
        f'<text x="{_fmt(x)}" y="{_fmt(y)}" '
        f'transform="rotate({rotation} {_fmt(x)} {_fmt(y)})" '
        'font-family="Arial, sans-serif" font-size="16" dominant-baseline="middle" '
        'data-role="bus-label" data-draggable="true" '
        f'data-offset-x="{_fmt(params.bus_label_offset_x)}" '
        f'data-offset-y="{_fmt(params.bus_label_offset_y)}" '
        f'data-rotation="{rotation}" '
        f'fill="{_label_color()}">{label}</text>'
    )


def _render_slot_marker(elements: list[str], params: BusbarPreviewRequest, slot: ParametricBaySlot) -> None:
    elements.append(
        f'<circle cx="{_fmt(slot.bus_x)}" cy="{_fmt(slot.bus_y)}" r="{_fmt(params.slot_diameter / 2.0)}" '
        f'fill="none" stroke="{_slot_stroke()}" stroke-width="1.4" />'
    )
    if slot.label and slot.label_x is not None and slot.label_y is not None:
        label = html.escape(slot.label)
        elements.append(
            f'<text x="{_fmt(slot.label_x)}" y="{_fmt(slot.label_y)}" '
            'font-family="Arial, sans-serif" font-size="14" text-anchor="middle" dominant-baseline="middle" '
            f'fill="{_label_color()}">{label}</text>'
        )


def _horizontal_preview(params: BusbarPreviewRequest) -> tuple[list[ParametricTerminal], list[ParametricBaySlot], str, dict[str, float]]:
    geom = _horizontal_geometry(params)
    terminals: list[ParametricTerminal] = [
        ParametricTerminal(id="left_end", x=geom.bar_x, y=geom.center_y, role="busbar_end", side="left"),
        ParametricTerminal(id="right_end", x=geom.bar_x + geom.bar_w, y=geom.center_y, role="busbar_end", side="right"),
    ]
    bay_slots: list[ParametricBaySlot] = []
    elements: list[str] = []

    _render_busbar_rect(elements, geom)

    next_label = params.bay_numbering_start
    for idx, x in enumerate(_slot_positions_horizontal(params, geom), start=1):
        if params.connection_side in {"top", "both"}:
            terminal = ParametricTerminal(id=f"tap_top_{idx}", x=x, y=geom.center_y, role="parameterized_connection", side="top", index=idx)
            terminals.append(terminal)
            slot = _make_slot(params=params, terminal_id=terminal.id, slot_side="top", index=idx, bus_x=x, bus_y=geom.center_y, label_number=next_label if params.bay_numbering_enabled else None, geom=geom)
            bay_slots.append(slot)
            next_label += params.bay_numbering_step

        if params.connection_side in {"bottom", "both"}:
            terminal = ParametricTerminal(id=f"tap_bottom_{idx}", x=x, y=geom.center_y, role="parameterized_connection", side="bottom", index=idx)
            terminals.append(terminal)
            slot = _make_slot(params=params, terminal_id=terminal.id, slot_side="bottom", index=idx, bus_x=x, bus_y=geom.center_y, label_number=next_label if params.bay_numbering_enabled else None, geom=geom)
            bay_slots.append(slot)
            next_label += params.bay_numbering_step

    for slot in bay_slots:
        _render_slot_marker(elements, params, slot)

    _render_bus_label(elements, params, geom)

    view_box = {"x": 0.0, "y": 0.0, "width": geom.view_w, "height": geom.view_h}
    return terminals, bay_slots, "\n".join(elements), view_box


def _vertical_preview(params: BusbarPreviewRequest) -> tuple[list[ParametricTerminal], list[ParametricBaySlot], str, dict[str, float]]:
    geom = _vertical_geometry(params)
    terminals: list[ParametricTerminal] = [
        ParametricTerminal(id="top_end", x=geom.center_x, y=geom.bar_y, role="busbar_end", side="top"),
        ParametricTerminal(id="bottom_end", x=geom.center_x, y=geom.bar_y + geom.bar_h, role="busbar_end", side="bottom"),
    ]
    bay_slots: list[ParametricBaySlot] = []
    elements: list[str] = []

    _render_busbar_rect(elements, geom)

    next_label = params.bay_numbering_start
    for idx, y in enumerate(_slot_positions_vertical(params, geom), start=1):
        if params.connection_side in {"top", "both"}:
            terminal = ParametricTerminal(id=f"tap_left_{idx}", x=geom.center_x, y=y, role="parameterized_connection", side="left", index=idx)
            terminals.append(terminal)
            slot = _make_slot(params=params, terminal_id=terminal.id, slot_side="left", index=idx, bus_x=geom.center_x, bus_y=y, label_number=next_label if params.bay_numbering_enabled else None, geom=geom)
            bay_slots.append(slot)
            next_label += params.bay_numbering_step

        if params.connection_side in {"bottom", "both"}:
            terminal = ParametricTerminal(id=f"tap_right_{idx}", x=geom.center_x, y=y, role="parameterized_connection", side="right", index=idx)
            terminals.append(terminal)
            slot = _make_slot(params=params, terminal_id=terminal.id, slot_side="right", index=idx, bus_x=geom.center_x, bus_y=y, label_number=next_label if params.bay_numbering_enabled else None, geom=geom)
            bay_slots.append(slot)
            next_label += params.bay_numbering_step

    for slot in bay_slots:
        _render_slot_marker(elements, params, slot)

    _render_bus_label(elements, params, geom)

    view_box = {"x": 0.0, "y": 0.0, "width": geom.view_w, "height": geom.view_h}
    return terminals, bay_slots, "\n".join(elements), view_box


def generate_busbar_preview(params: BusbarPreviewRequest) -> ParametricSymbolPreview:
    if params.orientation == "vertical":
        terminals, bay_slots, svg_fragment, view_box = _vertical_preview(params)
    else:
        terminals, bay_slots, svg_fragment, view_box = _horizontal_preview(params)

    computed_length = _compute_length(params)

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
            "connection_spacing_configurable": True,
            "end_slot_offset_configurable": True,
            "fit_length_to_slots": params.fit_length_to_slots,
            "internal_slot_markers": True,
            "bay_slots": True,
            "bay_slot_numbering": params.bay_numbering_enabled,
            "side_aware_label_rows": True,
            "draggable_bus_label": True,
            "bus_label_rotation": True,
            "bus_label": bool(params.bus_label),
        },
        "busbar": {
            "connection_count": params.connection_count,
            "connection_side": params.connection_side,
            "orientation": params.orientation,
            "length": computed_length,
            "fit_length_to_slots": params.fit_length_to_slots,
            "end_slot_offset": params.end_slot_offset,
            "thickness_mm": params.thickness_mm,
            "connection_spacing": params.connection_spacing,
            "slot_diameter": params.slot_diameter,
            "bay_depth": params.bay_depth,
            "bay_slot_count": len(bay_slots),
            "bay_numbering_enabled": params.bay_numbering_enabled,
            "bay_label_both_side_separate_rows": params.bay_label_both_side_separate_rows,
            "bay_numbering_style": params.bay_numbering_style,
            "bay_numbering_prefix": params.bay_numbering_prefix,
            "bay_numbering_start": params.bay_numbering_start,
            "bay_numbering_step": params.bay_numbering_step,
            "bus_label": params.bus_label,
            "bus_label_position": params.bus_label_position,
            "bus_label_gap": params.bus_label_gap,
            "bus_label_offset_x": params.bus_label_offset_x,
            "bus_label_offset_y": params.bus_label_offset_y,
            "bus_label_rotation_mode": params.bus_label_rotation_mode,
            "bus_label_rotation_deg": params.bus_label_rotation_deg,
            "voltage_kv": params.voltage_kv,
        },
        "auto_scheme_generation": {
            "role": "bus_section",
            "can_host_bays": True,
            "slot_model": "edge_offset_plus_spacing",
            "terminal_generation": "edge_offset_spacing",
            "bay_slot_count": len(bay_slots),
            "bay_labels": [slot.label for slot in bay_slots if slot.label],
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