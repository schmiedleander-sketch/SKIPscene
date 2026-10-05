# SKIPscene - Standalone Undertale Cutscene Skip, Death Gambling & Mysterious Call Mod

An Undertale mod that allows you to skip cutscenes and fast-forward dialogue, gamble on death for a second chance (losing 1 item on failure), and dial/call the mysterious number from your phone!

**100% Standalone - NO UndertaleModTool or third-party tools needed!**
Supports **Xbox Game Pass / Xbox App for PC**, **Steam**, **GOG**, and **DRM-Free** releases.

---

## Features
- **100% Standalone**: No UndertaleModTool, Cheat Engine, or external mods needed.
- **Xbox Game Pass & PC Launcher Support**: Automatically detects Xbox app game files (`data.win`, `game.win`, `game.unx`, `Content/data.win`).
- **One-Click Restore**: Easily revert back to your original unmodded game at any time with `--restore`.
- **Configurable Cutscene Skip Key**: Default key is `S`. Easily swap to `A`, `Z`, `X`, `C`, `Space`, `Shift`, `Ctrl`, or any key!
- **Death Gambling Feature**: When you die in battle, gamble for a chance to respawn immediately! If you lose the gamble, you forfeit 1 item from your inventory.
- **Call Mysterious Number Feature**: Decide to call the mysterious number directly in-game.

---

## How to Install & Apply Mod

1. Copy `patch_data_win.py`, `configure_key.py`, and `skip_key.ini` into your Undertale game directory:
   - **Xbox Game Pass / Xbox App**: `C:\XboxGames\Undertale\Content\` (or your custom Xbox games folder)
   - **Steam**: `C:\Program Files (x86)\Steam\steamapps\common\Undertale\`
2. Open terminal / Command Prompt in that folder and run:
   ```bash
   python patch_data_win.py
   ```
3. Launch Undertale from the Xbox App or Steam! Hold **'S'** in-game to fast-forward cutscenes, gamble when you fall in battle, or dial the mysterious number!

---

## How to Restore / Revert Back to Original Game

To remove all mod features and get your original unmodded game back at any time:
```bash
python patch_data_win.py --restore
```
This instantly restores `data.win` / `game.win` from your clean backup.

---

## How to Configure Mod Options

You can configure options using `configure_key.py`:

```bash
# Swap skip key to 'A'
python configure_key.py --key A

# Enable gambling on death (1 = enabled, 0 = disabled)
python configure_key.py --gambling 1

# Configure 1 item loss penalty on failed gamble (1 = enabled, 0 = disabled)
python configure_key.py --item-penalty 1

# Enable calling mysterious number (1 = enabled, 0 = disabled)
python configure_key.py --mysterious-call 1

# Set mysterious phone number (e.g. 666)
python configure_key.py --number 666
```

Or edit `skip_key.ini` directly in any text editor:
```ini
[Settings]
SkipKey = 83 ; 83 = S, 65 = A, 90 = Z, 88 = X, 32 = Space, 16 = Shift
FastForwardSpeed = 300
AutoAdvanceDialogue = 1
EnableGamblingOnDeath = 1
GambleItemLossPenalty = 1
EnableCallMysteriousNumber = 1
MysteriousNumber = 666
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

## Controls & Mod Usage
- **Hold Skip Key** (Default `S`): Fast-forwards game speed (300 FPS) and advances text boxes.
- **Death Gambling**: Upon death, choose to gamble for a instant respawn (losing 1 item on gamble failure).
- **Call Mysterious Number**: Dial the configured mysterious number via in-game phone interface.
