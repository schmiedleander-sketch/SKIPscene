# SKIPscene - Standalone Undertale Cutscene & Dialogue Skip Mod

An Undertale mod that allows you to skip cutscenes and fast-forward dialogue by holding the **'S'** key (or swap it to any key of your choice!).

**100% Standalone - NO UndertaleModTool or third-party tools needed!**
Supports **Xbox Game Pass / Xbox App for PC**, **Steam**, **GOG**, and **DRM-Free** releases.

---

## Features
- **100% Standalone**: No UndertaleModTool, Cheat Engine, or external mods needed.
- **Xbox Game Pass & PC Launcher Support**: Automatically detects Xbox app game files (`data.win`, `game.win`, `game.unx`, `Content/data.win`).
- **One-Click Restore**: Easily revert back to your original unmodded game at any time with `--restore`.
- **Configurable Key Binding**: Default key is `S`. Easily swap to `A`, `Z`, `X`, `C`, `Space`, `Shift`, `Ctrl`, or any key!

---

## How to Install & Apply Mod

1. Copy `patch_data_win.py`, `configure_key.py`, and `skip_key.ini` into your Undertale game directory:
   - **Xbox Game Pass / Xbox App**: `C:\XboxGames\Undertale\Content\` (or your custom Xbox games folder)
   - **Steam**: `C:\Program Files (steamapps\common\Undertale\`
2. Open terminal / Command Prompt in that folder and run:
   ```bash
   python patch_data_win.py
   ```
3. Launch Undertale from the Xbox App or Steam! Hold **'S'** in-game to fast-forward cutscenes and dialogue.

---

## How to Restore / Revert Back to Original Game

To remove the mod and get your original unmodded game back at any time:
```bash
python patch_data_win.py --restore
```
This instantly restores `data.win` / `game.win` from your clean backup.

---

## How to Swap / Change the Skip Key

Default skip key is **'S'**. You can swap to any key using `configure_key.py`:

```bash
# Swap skip key to 'A'
python configure_key.py --key A

# Swap skip key to 'Space'
python configure_key.py --key Space

# Swap skip key to 'Z'
python configure_key.py --key Z
```

Or edit `skip_key.ini` directly in any text editor:
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
- **Hold Skip Key** (Default `S`): Fast-forwards game speed (300 FPS) and advances text boxes.
- **Release Skip Key**: Returns game speed to normal (30 FPS).
