# Tauri spike icon resources

These neutral temporary resources are required by `tauri::generate_context!()` for the architecture spike. They are not an accepted product logo or branding asset.

Reproduce from the parent directory with:

```bash
python generate_spike_icons.py icons
```

Expected SHA-256:

```text
b3043d8684afb3e5673517816737a29e5e95fad027201f04a604c11b94c5adc5  icon.png
70fe1e09bfa9206748eecc84f979290a97090aed674fe343615d92471641f05a  icon.ico
```

`icon.png` is required by Linux context generation and `icon.ico` by Windows resource generation even with `--no-bundle`. No `.icns` or production installer branding set is included because those are outside this spike.
