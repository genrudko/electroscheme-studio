#!/usr/bin/env python3
"""Secondary equipment and auxiliary symbols — ГОСТ-compliant definitions.

Instruments, machines, passive components, reactors, bus bars,
terminals, earthing, enclosures, batteries, cables, cable accessories,
lightning protection, contacts, signaling, protection devices.
"""
from __future__ import annotations

from _build_library import (
    SW, SC, _sym, _term, _mk_svg,
    svg_instrument, svg_machine, svg_generator_excited,
    svg_resistor, svg_rheostat, svg_var_resistor,
    svg_capacitor, svg_electrolytic_capacitor, svg_inductor,
    svg_reactor, svg_shunt_reactor,
    svg_bus, svg_bus_tap, svg_bus_node,
    svg_terminal, svg_terminal_board,
    svg_ground, svg_frame_ground, svg_antenna_ground,
    svg_enclosure, svg_switchgear_cell, svg_withdrawable_element,
    svg_battery, svg_battery_cell, svg_accumulator,
    svg_cable, svg_cable_pair, svg_cable_shielded,
    svg_cable_joint, svg_cable_terminal,
    svg_cable_gland, svg_cable_duct,
    svg_lightning_arrester, svg_earthing_device, svg_opn_sl,
    svg_no_contact_closed, svg_no_contact_open,
    svg_nc_contact_closed, svg_nc_contact_open,
    svg_changeover_closed, svg_changeover_open,
    svg_relay_coil, svg_contactor_coil,
    _no_contact_states, _nc_contact_states, _changeover_states,
)


def build_instruments() -> list[dict]:
    """Measuring instruments — ГОСТ 2.729-68."""
    t = _term
    items: list[dict] = []
    specs = [
        ("ammeter", "Ammeter PA", "A"),
        ("voltmeter", "Voltmeter PV", "V"),
        ("wattmeter", "Wattmeter PW", "W"),
        ("varmeter", "Varmeter PVAR", "VAR"),
        ("frequency_meter", "Frequency meter PF", "Hz"),
        ("power_factor_meter", "Power factor meter PCos", "cos"),
        ("ohmmeter", "Ohmmeter PO", "Ohm"),
        ("energy_meter", "Energy meter E", "Wh"),
    ]
    for sid, name, letter in specs:
        items.append(_sym(
            sid, sid, name, "instruments",
            "ГОСТ 2.729-68", "fig.1",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_instrument(letter),
            letter=letter,
        ))
    return items


def build_machines() -> list[dict]:
    """Electrical machines — ГОСТ 2.722-68."""
    t = _term
    return [
        _sym(
            "synchronous_gen", "synchronous_gen",
            "Synchronous generator GS",
            "machines",
            "ГОСТ 2.722-68", "fig.1",
            "0 0 80 80", 80, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_generator_excited("G"),
            letter="GS",
        ),
        _sym(
            "synchronous_motor", "synchronous_motor",
            "Synchronous motor MS",
            "machines",
            "ГОСТ 2.722-68", "fig.1",
            "0 0 80 80", 80, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_machine("M"),
            letter="MS",
        ),
        _sym(
            "asynchronous_motor", "asynchronous_motor",
            "Asynchronous (induction) motor MI",
            "machines",
            "ГОСТ 2.722-68", "fig.1",
            "0 0 80 80", 80, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_machine("M"),
            letter="MI",
        ),
        _sym(
            "dc_generator", "dc_generator",
            "DC generator GD",
            "machines",
            "ГОСТ 2.722-68", "fig.1",
            "0 0 80 80", 80, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_generator_excited("G"),
            letter="GD",
        ),
        _sym(
            "dc_motor", "dc_motor",
            "DC motor MD",
            "machines",
            "ГОСТ 2.722-68", "fig.1",
            "0 0 80 80", 80, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_machine("M"),
            letter="MD",
        ),
        _sym(
            "universal_motor", "universal_motor",
            "Universal motor MU",
            "machines",
            "ГОСТ 2.722-68", "fig.1",
            "0 0 80 80", 80, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_machine("M"),
            letter="MU",
        ),
        _sym(
            "special_machine", "special_machine",
            "Special electrical machine",
            "machines",
            "ГОСТ 2.722-68", "fig.1",
            "0 0 80 80", 80, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_machine("X"),
            letter="X",
        ),
        _sym(
            "servo_motor", "servo_motor",
            "Servo motor",
            "machines",
            "ГОСТ 2.722-68", "fig.1",
            "0 0 80 80", 80, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_machine("SM"),
            letter="SM",
        ),
    ]


def build_passive() -> list[dict]:
    """Passive components — ГОСТ 2.728-74."""
    t = _term
    return [
        _sym(
            "resistor", "resistor",
            "Resistor R",
            "passive",
            "ГОСТ 2.728-74", "fig.1",
            "0 0 100 40", 100, 40,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_resistor(),
            letter="R",
        ),
        _sym(
            "rheostat", "rheostat",
            "Rheostat R",
            "passive",
            "ГОСТ 2.728-74", "fig.1",
            "0 0 100 50", 100, 50,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_rheostat(),
            letter="R",
        ),
        _sym(
            "var_resistor", "var_resistor",
            "Variable resistor R",
            "passive",
            "ГОСТ 2.728-74", "fig.1",
            "0 0 100 50", 100, 50,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_var_resistor(),
            letter="R",
        ),
        _sym(
            "capacitor", "capacitor",
            "Capacitor C",
            "passive",
            "ГОСТ 2.728-74", "fig.2",
            "0 0 100 50", 100, 50,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_capacitor(),
            letter="C",
        ),
        _sym(
            "electrolytic_capacitor", "electrolytic_capacitor",
            "Electrolytic capacitor C",
            "passive",
            "ГОСТ 2.728-74", "fig.2",
            "0 0 100 55", 100, 55,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_electrolytic_capacitor(),
            letter="C",
        ),
        _sym(
            "inductor", "inductor",
            "Inductor (coil) L",
            "passive",
            "ГОСТ 2.723-68", "fig.3",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_inductor(),
            letter="L",
        ),
    ]


def build_reactor() -> list[dict]:
    """Shunt reactors — ГОСТ 2.723-68."""
    t = _term
    return [
        _sym(
            "shunt_reactor", "shunt_reactor",
            "Shunt reactor L",
            "reactor",
            "ГОСТ 2.723-68", "fig.3",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_reactor(),
            letter="L",
        ),
        _sym(
            "filter_reactor", "filter_reactor",
            "Filter reactor L",
            "reactor",
            "ГОСТ 2.723-68", "fig.3",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_reactor(),
            letter="L",
        ),
    ]


def build_bus_line() -> list[dict]:
    """Bus bars and connection lines — ГОСТ 2.702-2011."""
    t = _term
    return [
        _sym(
            "bus_bar", "bus_bar",
            "Bus bar (main bus)",
            "bus_line",
            "ГОСТ 2.702-2011", "fig.2",
            "0 0 100 20", 100, 20,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_bus(),
        ),
        _sym(
            "bus_tap", "bus_tap",
            "Bus tap / branch",
            "bus_line",
            "ГОСТ 2.702-2011", "fig.2",
            "0 0 60 60", 60, 60,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_bus_tap(),
        ),
        _sym(
            "bus_node", "bus_node",
            "Bus node / junction",
            "bus_line",
            "ГОСТ 2.702-2011", "fig.2",
            "0 0 40 40", 40, 40,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_bus_node(),
        ),
        _sym(
            "power_line", "power_line",
            "Power line (overhead)",
            "bus_line",
            "ГОСТ 2.702-2011", "fig.2",
            "0 0 100 20", 100, 20,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_bus(),
        ),
    ]


def build_terminals() -> list[dict]:
    """Terminals and connectors — ГОСТ 2.721-74."""
    t = _term
    return [
        _sym(
            "terminal", "terminal",
            "Terminal / binding post",
            "terminals",
            "ГОСТ 2.721-74", "fig.6",
            "0 0 30 30", 30, 30,
            [t("t1", 50, 100)],
            svg_terminal(),
        ),
        _sym(
            "terminal_board", "terminal_board",
            "Terminal board",
            "terminals",
            "ГОСТ 2.721-74", "fig.6",
            "0 0 100 30", 100, 30,
            [t("t1", 10, 50), t("t2", 90, 50)],
            svg_terminal_board(),
        ),
    ]


def build_ground() -> list[dict]:
    """Earthing symbols — ГОСТ 2.756-76."""
    t = _term
    return [
        _sym(
            "ground", "ground",
            "Protective earth PE",
            "ground",
            "ГОСТ 2.756-76", "fig.1",
            "0 0 40 50", 40, 50,
            [t("t1", 50, 0)],
            svg_ground(),
        ),
        _sym(
            "frame_ground", "frame_ground",
            "Frame / chassis ground",
            "ground",
            "ГОСТ 2.756-76", "fig.1",
            "0 0 40 50", 40, 50,
            [t("t1", 50, 0)],
            svg_frame_ground(),
        ),
        _sym(
            "signal_ground", "signal_ground",
            "Signal / reference ground",
            "ground",
            "ГОСТ 2.756-76", "fig.1",
            "0 0 40 55", 40, 55,
            [t("t1", 50, 0)],
            svg_antenna_ground(),
        ),
        _sym(
            "earthing_device", "earthing_device",
            "Earthing device",
            "ground",
            "ГОСТ 2.756-76", "fig.1",
            "0 0 60 80", 60, 80,
            [t("t1", 50, 0)],
            svg_earthing_device(),
        ),
    ]


def build_enclosure() -> list[dict]:
    """Enclosures, switchgear cells — ГОСТ 2.721-74."""
    t = _term
    return [
        _sym(
            "enclosure_general", "enclosure_general",
            "General enclosure / cubicle",
            "enclosure",
            "ГОСТ 2.721-74", "fig.12",
            "0 0 100 80", 100, 80,
            [],
            svg_enclosure(),
        ),
        _sym(
            "switchgear_cell", "switchgear_cell",
            "Switchgear cell (KRU)",
            "enclosure",
            "ГОСТ 2.721-74", "fig.12",
            "0 0 100 120", 100, 120,
            [],
            svg_switchgear_cell(),
        ),
        _sym(
            "withdrawable_cell", "withdrawable_cell",
            "Withdrawable (truck-type) cell",
            "enclosure",
            "ГОСТ 2.721-74", "fig.12",
            "0 0 100 80", 100, 80,
            [],
            svg_withdrawable_element(),
        ),
    ]


def build_battery() -> list[dict]:
    """Batteries and power supplies — ГОСТ 2.721-74."""
    t = _term
    return [
        _sym(
            "battery", "battery",
            "Battery (multiple cells) GB",
            "battery",
            "ГОСТ 2.721-74", "fig.8",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_battery(),
            letter="GB",
        ),
        _sym(
            "battery_cell", "battery_cell",
            "Single battery cell GB",
            "battery",
            "ГОСТ 2.721-74", "fig.8",
            "0 0 60 60", 60, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_battery_cell(),
            letter="GB",
        ),
        _sym(
            "accumulator", "accumulator",
            "Accumulator (rechargeable) GBA",
            "battery",
            "ГОСТ 2.721-74", "fig.8",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_accumulator(),
            letter="GBA",
        ),
    ]


def build_cable() -> list[dict]:
    """Cables and wiring — ГОСТ 2.721-74."""
    t = _term
    return [
        _sym(
            "cable_1phase", "cable_1phase",
            "Single-phase cable",
            "cable",
            "ГОСТ 2.721-74", "fig.10",
            "0 0 100 40", 100, 40,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_cable(),
        ),
        _sym(
            "cable_pair", "cable_pair",
            "Cable pair",
            "cable",
            "ГОСТ 2.721-74", "fig.10",
            "0 0 100 40", 100, 40,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_cable_pair(),
        ),
        _sym(
            "cable_3phase", "cable_3phase",
            "Three-phase cable",
            "cable",
            "ГОСТ 2.721-74", "fig.10",
            "0 0 100 40", 100, 40,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_cable(),
        ),
        _sym(
            "cable_shielded", "cable_shielded",
            "Shielded cable",
            "cable",
            "ГОСТ 2.721-74", "fig.10",
            "0 0 100 50", 100, 50,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_cable_shielded(),
        ),
        _sym(
            "cable_joint", "cable_joint",
            "Cable joint / splice",
            "cable",
            "ГОСТ 2.721-74", "fig.10",
            "0 0 100 40", 100, 40,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_cable_joint(),
        ),
    ]


def build_cable_accessories() -> list[dict]:
    """Cable accessories — ГОСТ 2.721-74."""
    t = _term
    return [
        _sym(
            "cable_gland", "cable_gland",
            "Cable gland",
            "cable_accessories",
            "ГОСТ 2.721-74", "fig.10",
            "0 0 50 40", 50, 40,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_cable_gland(),
        ),
        _sym(
            "cable_duct", "cable_duct",
            "Cable duct / tray",
            "cable_accessories",
            "ГОСТ 2.721-74", "fig.10",
            "0 0 100 40", 100, 40,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_cable_duct(),
        ),
    ]


def build_lightning() -> list[dict]:
    """Lightning and earthing protection."""
    t = _term
    return [
        _sym(
            "lightning_rod", "lightning_rod",
            "Lightning rod / air terminal",
            "lightning",
            "ГОСТ 2.742-68", "fig.7",
            "0 0 100 80", 100, 80,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_lightning_arrester(),
        ),
        _sym(
            "lightning_arrester", "lightning_arrester",
            "Lightning arrester",
            "lightning",
            "ГОСТ 2.742-68", "fig.7",
            "0 0 100 80", 100, 80,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_lightning_arrester(),
        ),
        _sym(
            "earthing_conductor", "earthing_conductor",
            "Earthing conductor",
            "lightning",
            "ГОСТ 2.756-76", "fig.1",
            "0 0 60 80", 60, 80,
            [t("t1", 50, 0)],
            svg_earthing_device(),
        ),
    ]


def build_contact_types() -> list[dict]:
    """Contact types — ГОСТ 2.759-82 / ГОСТ 2.755-87."""
    t = _term
    return [
        _sym(
            "no_contact", "no_contact",
            "Normally open (NO) contact",
            "contact_types",
            "ГОСТ 2.759-82", "fig.1",
            "0 0 80 60", 80, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_no_contact_open(),
            interactive=True, def_state="open",
            states=_no_contact_states(),
        ),
        _sym(
            "nc_contact", "nc_contact",
            "Normally closed (NC) contact",
            "contact_types",
            "ГОСТ 2.759-82", "fig.1",
            "0 0 80 60", 80, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_nc_contact_closed(),
            interactive=True, def_state="closed",
            states=_nc_contact_states(),
        ),
        _sym(
            "changeover_contact", "changeover_contact",
            "Changeover (CO) contact",
            "contact_types",
            "ГОСТ 2.759-82", "fig.1",
            "0 0 80 80", 80, 80,
            [t("t1", 0, 50), t("t2", 100, 30), t("t3", 100, 70)],
            svg_changeover_open(),
            interactive=True, def_state="pos1",
            states=_changeover_states(),
        ),
        _sym(
            "relay_coil", "relay_coil",
            "Relay coil / electromagnetic drive",
            "contact_types",
            "ГОСТ 2.759-82", "fig.5",
            "0 0 40 80", 40, 80,
            [t("t1", 50, 0), t("t2", 50, 100)],
            svg_relay_coil(),
        ),
    ]


def build_signaling() -> list[dict]:
    """Signaling devices — ГОСТ 2.727-68."""
    t = _term
    return [
        _sym(
            "indicator_lamp", "indicator_lamp",
            "Indicator lamp H",
            "signaling",
            "ГОСТ 2.727-68", "fig.1",
            "0 0 80 60", 80, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_instrument("H", vb="0 0 80 60", y=30, r=12),
            letter="H",
        ),
        _sym(
            "alarm_lamp", "alarm_lamp",
            "Alarm lamp H",
            "signaling",
            "ГОСТ 2.727-68", "fig.1",
            "0 0 80 60", 80, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_instrument("H", vb="0 0 80 60", y=30, r=12),
            letter="H",
        ),
        _sym(
            "buzzer", "buzzer",
            "Buzzer / audible alarm",
            "signaling",
            "ГОСТ 2.727-68", "fig.1",
            "0 0 80 60", 80, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_instrument("BZ", vb="0 0 80 60", y=30, r=12),
            letter="BZ",
        ),
        _sym(
            "bell", "bell",
            "Electric bell",
            "signaling",
            "ГОСТ 2.727-68", "fig.1",
            "0 0 80 60", 80, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_instrument("BL", vb="0 0 80 60", y=30, r=12),
            letter="BL",
        ),
        _sym(
            "horn", "horn",
            "Electric horn / siren",
            "signaling",
            "ГОСТ 2.727-68", "fig.1",
            "0 0 80 60", 80, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_instrument("HN", vb="0 0 80 60", y=30, r=12),
            letter="HN",
        ),
    ]


def build_protection_devices() -> list[dict]:
    """Protection devices — ГОСТ 2.728-74."""
    t = _term
    return [
        _sym(
            "surge_protector", "surge_protector",
            "Surge protector / SPD",
            "protection_devices",
            "ГОСТ 2.742-68", "fig.7",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_opn_sl(),
            letter="FV",
        ),
        _sym(
            "overvoltage_protector", "overvoltage_protector",
            "Overvoltage protector",
            "protection_devices",
            "ГОСТ 2.742-68", "fig.7",
            "0 0 100 60", 100, 60,
            [t("t1", 0, 50), t("t2", 100, 50)],
            svg_opn_sl(),
            letter="FV",
        ),
    ]


def build_secondary_symbols() -> list[dict]:
    return (
        build_instruments()
        + build_machines()
        + build_passive()
        + build_reactor()
        + build_bus_line()
        + build_terminals()
        + build_ground()
        + build_enclosure()
        + build_battery()
        + build_cable()
        + build_cable_accessories()
        + build_lightning()
        + build_contact_types()
        + build_signaling()
        + build_protection_devices()
    )
