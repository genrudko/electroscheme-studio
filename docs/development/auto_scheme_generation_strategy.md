# Automatic scheme generation strategy

## Product goal

Automatic scheme generation from an equipment list is a killer feature and must be treated as a first-class design goal.

The system should eventually support:

```text
equipment list / topology model
→ bay/feeder layout
→ symbol placement
→ busbar generation
→ terminal graph
→ orthogonal routing
→ labels
→ validation
→ editable scheme
```

## Non-negotiable requirement

Generated schemes must remain editable.

Automatic generation must not create a dead static picture.

Each generated object must retain:

- equipment ID;
- symbol ID;
- terminals;
- snap anchors;
- voltage class;
- state;
- bay/section relation;
- source metadata;
- editable parameters.

## Minimum input model

The first practical model can be simple:

```json
{
  "station": "Example substation",
  "voltage_levels": [
    {
      "voltage_class": "110kv",
      "switchgear": "ОРУ-110 кВ",
      "busbars": ["1С-110", "2С-110"],
      "bays": [
        {
          "id": "bay_1",
          "name": "ВЛ 110 кВ Example",
          "equipment": [
            { "kind": "disconnector", "name": "ЛР" },
            { "kind": "circuit_breaker", "name": "В" },
            { "kind": "current_transformer", "name": "ТТ" }
          ]
        }
      ]
    }
  ]
}
```

## Layout principles

Initial auto-layout should be deterministic and conservative.

Rules:

1. Place voltage levels in separate bands.
2. Generate busbars first.
3. Generate bays in declared order.
4. Place primary switching devices along bay axis.
5. Create terminals and connection graph before drawing wires.
6. Use orthogonal routing.
7. Minimize crossings.
8. Preserve editability.

## Symbol requirements for auto-generation

A symbol can participate in auto-generation only if it has:

```text
kind
terminals
snap anchors
voltage color policy
rotation policy
default dimensions
layout role
```

For busbars, additionally:

```text
connection_count
connection_spacing
length
generated terminal positions
```

For switching devices, additionally:

```text
state variants
normal state
operational states
```

## Future generator stages

### Stage 1

Generate a simple single-bus section with several bays.

### Stage 2

Generate two bus systems with sectionalizing/coupler equipment.

### Stage 3

Generate transformer bays and voltage-level relations.

### Stage 4

Generate full substation single-line diagrams from station profile.

### Stage 5

Generate object-specific schemes from imported plant topology data.