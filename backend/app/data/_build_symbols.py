#!/usr/bin/env python3
"""Primary equipment symbols — ГОСТ-compliant definitions.

Circuit breakers, disconnectors, grounding switches, contactors,
manual switches, fuses, arresters/OPN, transformers, CT/VT,
relay protection devices.
"""
from __future__ import annotations

from _build_library import (
    SW, SC,
    _cb, _ds, _sym, _term, _mk_svg,
    svg_cb_sl_closed, svg_cb_sl_open,
    svg_ds_sl_closed, svg_ds_sl_open,
    svg_grounding_sl, svg_grounding_sl_open,
    svg_contactor_coil,
    svg_fuse_sl, svg_fuse_holders_sl,
    svg_spark_gap_sl, svg_opn_sl, svg_surge_capacitor_sl,
    svg_xfmr_2w, svg_xfmr_3w, svg_xfmr_2w_delta_wye, svg_xfmr_autotransformer,
    svg_ct_sl, svg_ct_normal,
    svg_vt_sl, svg_vt_normal,
    svg_reactor, svg_shunt_reactor,
    svg_relay_overcurrent, svg_relay_diff, svg_relay_distance,
    svg_relay_earth_fault, svg_relay_thermal, svg_relay_pressure,
    svg_relay_overload, svg_relay_buchholz, svg_relay_gas,
    _cb_states, _ds_states,
)


def build_switching() -> list[dict]:
    """Circuit breakers (QF) — ГОСТ 2.755-87."""
    t = _term
    return [
        _cb("cb_vacuum", "Vacuum circuit breaker QF",
            "switching"),
        _cb("cb_sf6", "SF6 circuit breaker QF",
            "switching"),
        _cb("cb_air", "Air circuit breaker QF",
            "switching"),
        _cb("cb_oil", "Oil circuit breaker QF",
            "switching"),
        _cb("cb_moulded", "Moulded-case circuit breaker (MCCB) QF",
            "switching"),
        _cb("cb_miniature", "Miniature circuit breaker (MCB) QF",
            "switching"),
        _cb("cb_magnetic", "Magnetic contactor-circuit breaker QF",
            "switching"),

        # Normal-mode (expandable) circuit breakers
        _sym(
            "cb_vacuum_n", "cb_vacuum_n",
            "Vacuum circuit breaker QF (normal)",
            "switching",
            "ГОСТ 2.755-87", "fig.1",
            "0 0 80 60", 80, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_cb_sl_closed(vb="0 0 80 60", y=30, bx=26, bw=20, bh=16),
            letter="QF",
            interactive=True, def_state="closed",
            states=_cb_states(),
        ),
    ]


def build_disconnector() -> list[dict]:
    """Disconnectors (QS) — ГОСТ 2.755-87."""
    t = _term
    return [
        _ds("ds_horizontal", "Horizontal disconnector QS",
            "disconnector"),
        _ds("ds_vertical", "Vertical disconnector QS",
            "disconnector"),
        _ds("ds_center", "Center-break disconnector QS",
            "disconnector"),
        _ds("ds_double", "Double-break disconnector QS",
            "disconnector"),

        # Grounding switch (ZN)
        _sym(
            "grounding_switch", "grounding_switch",
            "Grounding switch ZN",
            "disconnector",
            "ГОСТ 2.755-87", "fig.3",
            "0 0 100 80", 100, 80,
            [t("t1", 0, 25)],
            svg_grounding_sl(),
            letter="ZN",
            interactive=True, def_state="closed",
            states=[
                {"id": "closed", "name": "Closed", "alternate_svg": svg_grounding_sl()},
                {"id": "open", "name": "Open", "alternate_svg": svg_grounding_sl_open()},
            ],
        ),

        # Disconnector with grounding knife
        _sym(
            "ds_with_grounding", "ds_with_grounding",
            "Disconnector QS with grounding knife",
            "disconnector",
            "ГОСТ 2.755-87", "fig.2-3",
            "0 0 100 100", 100, 100,
            [t("t1", 0, 30), t("t2", 100, 30)],
            svg_ds_sl_closed(vb="0 0 100 60", y=30),
            letter="QS",
        ),
    ]


def build_contactor() -> list[dict]:
    """Contactors and starters (KM) — ГОСТ 2.759-82."""
    t = _term
    return [
        _sym(
            "contactor_ac", "contactor_ac",
            "AC contactor KM",
            "contactor",
            "ГОСТ 2.759-82", "fig.5",
            "0 0 40 80", 40, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_contactor_coil(),
            letter="KM",
        ),
        _sym(
            "contactor_dc", "contactor_dc",
            "DC contactor KM",
            "contactor",
            "ГОСТ 2.759-82", "fig.5",
            "0 0 40 80", 40, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_contactor_coil(),
            letter="KM",
        ),
    ]


def build_switch() -> list[dict]:
    """Manual switches — ГОСТ 2.755-87."""
    return [
        _sym(
            "switch_load", "switch_load",
            "Load-break switch Q",
            "switch",
            "ГОСТ 2.755-87", "fig.1",
            "0 0 100 60", 100, 60,
            [_term("t1", 0, 50), _term("t2", 100, 50)],
            svg_ds_sl_closed(),
            letter="Q",
            interactive=True, def_state="closed",
            states=_ds_states(),
        ),
        _sym(
            "switch_isolating", "switch_isolating",
            "Isolating switch Q",
            "switch",
            "ГОСТ 2.755-87", "fig.1",
            "0 0 100 60", 100, 60,
            [_term("t1", 0, 50), _term("t2", 100, 50)],
            svg_ds_sl_closed(),
            letter="Q",
            interactive=True, def_state="closed",
            states=_ds_states(),
        ),
    ]


def build_fuse() -> list[dict]:
    """Fuses (FU) — ГОСТ 2.728-74."""
    t = _term
    return [
        _sym(
            "fuse_limiting", "fuse_limiting",
            "Limiting fuse FU",
            "fuse",
            "ГОСТ 2.728-74", "fig.9",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_fuse_sl(),
            letter="FU",
        ),
        _sym(
            "fuse_protective", "fuse_protective",
            "Protective fuse FU",
            "fuse",
            "ГОСТ 2.728-74", "fig.9",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_fuse_sl(),
            letter="FU",
        ),
        _sym(
            "fuse_holders", "fuse_holders",
            "Fuse with holders FU",
            "fuse",
            "ГОСТ 2.728-74", "fig.9",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_fuse_holders_sl(),
            letter="FU",
        ),
    ]


def build_arrester() -> list[dict]:
    """Arresters and OPN — ГОСТ 2.742-68."""
    t = _term
    return [
        _sym(
            "spark_gap", "spark_gap",
            "Spark gap FV",
            "arrester",
            "ГОСТ 2.742-68", "fig.7",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_spark_gap_sl(),
            letter="FV",
        ),
        _sym(
            "opn", "opn",
            "Surge arrester (OPN) FV",
            "arrester",
            "ГОСТ 2.742-68", "fig.7",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_opn_sl(),
            letter="FV",
        ),
        _sym(
            "surge_capacitor", "surge_capacitor",
            "Surge capacitor FV",
            "arrester",
            "ГОСТ 2.742-68", "fig.7",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_surge_capacitor_sl(),
            letter="FV",
        ),
    ]


def build_transformer() -> list[dict]:
    """Transformers — ГОСТ 2.723-68."""
    t = _term
    return [
        _sym(
            "xfmr_2w", "xfmr_2w",
            "Two-winding transformer T",
            "transformer",
            "ГОСТ 2.723-68", "fig.4",
            "0 0 100 100", 80, 100,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_xfmr_2w(),
            letter="T",
            props={"primary_voltage": "", "secondary_voltage": ""},
        ),
        _sym(
            "xfmr_3w", "xfmr_3w",
            "Three-winding transformer T",
            "transformer",
            "ГОСТ 2.723-68", "fig.4",
            "0 0 100 120", 80, 120,
            [t("t1", 50, 0), t("t2", 50, 100), t("t3", 80, 50)],
            svg_xfmr_3w(),
            letter="T",
        ),
        _sym(
            "xfmr_delta_wye", "xfmr_delta_wye",
            "Transformer Dy11 T",
            "transformer",
            "ГОСТ 2.723-68", "fig.4",
            "0 0 100 110", 80, 110,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_xfmr_2w_delta_wye(),
            letter="T",
            props={"connection_group": "Dyn11"},
        ),
        _sym(
            "autotransformer", "autotransformer",
            "Autotransformer TA",
            "transformer",
            "ГОСТ 2.723-68", "fig.4",
            "0 0 100 110", 80, 110,
            [t("t1", 30, 0), t("t2", 70, 100)],
            svg_xfmr_autotransformer(),
            letter="TA",
        ),
    ]


def build_ct_vt() -> list[dict]:
    """Instrument transformers — ГОСТ 2.723-68."""
    t = _term
    return [
        _sym(
            "ct_wound", "ct_wound",
            "Wound-type current transformer TA",
            "ct_vt",
            "ГОСТ 2.723-68", "fig.5",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_ct_sl(),
            letter="TA",
        ),
        _sym(
            "ct_bar", "ct_bar",
            "Bar-type current transformer TA",
            "ct_vt",
            "ГОСТ 2.723-68", "fig.5",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_ct_sl(),
            letter="TA",
        ),
        _sym(
            "ct_normal", "ct_normal",
            "Current transformer (normal diagram) TA",
            "ct_vt",
            "ГОСТ 2.723-68", "fig.5",
            "0 0 80 60", 80, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_ct_normal(),
            letter="TA",
        ),
        _sym(
            "vt_inductive", "vt_inductive",
            "Inductive voltage transformer TV",
            "ct_vt",
            "ГОСТ 2.723-68", "fig.5",
            "0 0 100 80", 100, 80,
            [t("t1", 0, 25), t("t2", 100, 25)],
            svg_vt_sl(),
            letter="TV",
        ),
        _sym(
            "vt_normal", "vt_normal",
            "Voltage transformer (normal diagram) TV",
            "ct_vt",
            "ГОСТ 2.723-68", "fig.5",
            "0 0 60 80", 60, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_vt_normal(),
            letter="TV",
        ),
    ]


def build_relay() -> list[dict]:
    """Relay protection devices — ГОСТ 2.759-82."""
    t = _term
    return [
        _sym(
            "r_overcurrent", "r_overcurrent",
            "Overcurrent relay 50/51",
            "relay",
            "ГОСТ 2.759-82", "fig.5",
            "0 0 40 80", 40, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_relay_overcurrent(),
            letter="50/51",
        ),
        _sym(
            "r_diff", "r_diff",
            "Differential relay 87",
            "relay",
            "ГОСТ 2.759-82", "fig.5",
            "0 0 40 80", 40, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_relay_diff(),
            letter="87",
        ),
        _sym(
            "r_distance", "r_distance",
            "Distance relay 21",
            "relay",
            "ГОСТ 2.759-82", "fig.5",
            "0 0 40 80", 40, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_relay_distance(),
            letter="21",
        ),
        _sym(
            "r_earth_fault", "r_earth_fault",
            "Earth-fault relay 51N",
            "relay",
            "ГОСТ 2.759-82", "fig.5",
            "0 0 40 80", 40, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_relay_earth_fault(),
            letter="51N",
        ),
        _sym(
            "r_thermal", "r_thermal",
            "Thermal relay 49",
            "relay",
            "ГОСТ 2.759-82", "fig.5",
            "0 0 40 80", 40, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_relay_thermal(),
            letter="49",
        ),
        _sym(
            "r_pressure", "r_pressure",
            "Pressure relay 63",
            "relay",
            "ГОСТ 2.759-82", "fig.5",
            "0 0 40 80", 40, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_relay_pressure(),
            letter="63",
        ),
        _sym(
            "r_overload", "r_overload",
            "Overload relay 49",
            "relay",
            "ГОСТ 2.759-82", "fig.5",
            "0 0 40 80", 40, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_relay_overload(),
            letter="49",
        ),
        _sym(
            "r_buchholz", "r_buchholz",
            "Buchholz relay 71",
            "relay",
            "ГОСТ 2.759-82", "fig.5",
            "0 0 40 80", 40, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_relay_buchholz(),
            letter="71",
        ),
        _sym(
            "r_gas", "r_gas",
            "Gas relay 71",
            "relay",
            "ГОСТ 2.759-82", "fig.5",
            "0 0 40 80", 40, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_relay_gas(),
            letter="71",
        ),
    ]


def build_primary_symbols() -> list[dict]:
    return (
        build_switching()
        + build_disconnector()
        + build_contactor()
        + build_switch()
        + build_fuse()
        + build_arrester()
        + build_transformer()
        + build_ct_vt()
        + build_relay()
    )
