# SKIPscene - Standalone Undertale Cutscene & Dialogue Skip Mod

An Undertale mod that allows you to skip cutscenes and fast-forward dialogue by holding the **'S'** key (or swap it to any key of your choice!).

## Features
- **Standalone Patcher**: Patch `data.win` directly using `patch_data_win.py` without needing UndertaleModTool or any third-party tools.
- **UndertaleModTool Support**: Also includes `SkipCutscenes.csx` for users who prefer using UndertaleModTool.
- **Configurable Key Binding**: Default key is `S`. Easily swap to `A`, `Z`, `X`, `C`, `Space`, `Shift`, `Ctrl`, or any custom key!
- **Fast-Forward Game Speed**: Fast-forwards cutscenes at 300 FPS while held down.

---

## Quick Start (Standalone - No UndertaleModTool Needed!)

1. Place `patch_data_win.py` and `skip_key.ini` in your Undertale folder (where `data.win` and `UNDERTALE.exe` are located).
2. Run the patcher in terminal / command prompt:
   ```bash
   python patch_data_win.py
   ```
3. Launch Undertale! Hold **'S'** (or your swapped key) to skip cutscenes and text.

---

## How to Swap / Change the Skip Key

You can change or swap the skip key at any time:

### Method 1: Use `configure_key.py` (Recommended)
Swap keys with a single command:
```bash
# Swap skip key to 'A'
python configure_key.py --key A

# Swap skip key to 'Space'
python configure_key.py --key Space

# Swap skip key to 'Z'
python configure_key.py --key Z
```

### Method 2: Edit `skip_key.ini`
Open `skip_key.ini` in any text editor and change `SkipKey`:
```ini
[Settings]
SkipKey = 83 ; 83 = S, 65 = A, 90 = Z, 88 = X, 32 = Space, 16 = Shift
FastForwardSpeed = 300
AutoAdvanceDialogue = 1
```

---

## Key Codes Reference Table

| Key | Key Name | KeyCode Value |
|---|---|---|
| `S` (Default) | Key S | `83` |
| `A` | Key A | `65` |
| `B` | Key B | `66` |
| `C` | Key C | `67` |
| `D` | Key D | `68` |
| `X` | Key X | `88` |
| `Z` | Key Z | `90` |
| `Space` | Spacebar | `32` |
| `Shift` | Shift Key | `16` |
| `Ctrl` | Ctrl Key | `17` |
| `Alt` | Alt Key | `18` |

---

## Controls
- **Hold Skip Key** (Default `S`): Fast-forwards game speed (300 FPS) and auto-advances dialogue text.
- **Release Skip Key**: Returns game speed to normal (30 FPS).
