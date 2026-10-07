# SKIPscene - Standalone Undertale Cutscene & Dialogue Skip Mod

An Undertale mod that allows you to skip cutscenes and fast-forward dialogue by holding the **'S'** key (or swap it to any key of your choice!).

**100% Standalone - NO UndertaleModTool or third-party tools needed!**
Supports **Xbox Game Pass / Xbox App for PC**, **Steam**, **GOG**, and **DRM-Free** releases.

---

## Features
- **100% Standalone**: No UndertaleModTool, Cheat Engine, or external mods needed.
- **Auto-Detection**: Auto-detects Xbox Game Pass (`C:\XboxGames\Undertale\Content\data.win`) and Steam installations even when run directly from your Downloads folder!
- **Interactive Prompt & Path Argument**: Simply pass the path or drag-and-drop `data.win` onto the script if needed.
- **One-Click Restore**: Easily revert back to your original unmodded game at any time with `--restore`.
- **Configurable Key Binding**: Default key is `S`. Easily swap to `A`, `Z`, `X`, `C`, `Space`, `Shift`, `Ctrl`, or any key!

---

## How to Install & Apply Mod

### Option 1: Run directly from Downloads folder (Recommended)
Open Command Prompt / Terminal in your Downloads folder and run:
```bash
python patch_data_win.py
```
*The script will automatically scan standard Xbox Game Pass and Steam paths (e.g., `C:\XboxGames\Undertale\Content`). If it needs help, it will prompt you to enter or drag-and-drop your `data.win` file!*

### Option 2: Specify your game path directly
```bash
python patch_data_win.py "C:\XboxGames\Undertale\Content\data.win"
```

### Option 3: Copy files into your game folder
Copy `patch_data_win.py` and `skip_key.ini` into your Undertale game directory (e.g. `C:\XboxGames\Undertale\Content\`) and run `python patch_data_win.py`.

---

## How to Restore / Revert Back to Original Game

To remove the mod and get your original unmodded game back at any time:
```bash
python patch_data_win.py --restore
```
*You can also pass your game file path if running from Downloads:*
```bash
python patch_data_win.py "C:\XboxGames\Undertale\Content\data.win" --restore
```

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
