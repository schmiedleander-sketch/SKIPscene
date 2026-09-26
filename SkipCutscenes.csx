// Undertale Cutscene & Dialogue Skip Script for UndertaleModTool
// Allows skipping cutscenes and fast-forwarding text by holding 'S' or any customized key.

using System;
using System.Text;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using UndertaleModLib;
using UndertaleModLib.Models;

EnsureDataLoaded();

// Key Mapping Dictionary
Dictionary<string, int> keyMap = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase)
{
    {"S", 83}, {"A", 65}, {"B", 66}, {"C", 67}, {"D", 68}, {"E", 69}, {"F", 70},
    {"G", 71}, {"H", 72}, {"I", 73}, {"J", 74}, {"K", 75}, {"L", 76}, {"M", 77},
    {"N", 78}, {"O", 79}, {"P", 80}, {"Q", 81}, {"R", 82}, {"T", 84}, {"U", 85},
    {"V", 86}, {"W", 87}, {"X", 88}, {"Y", 89}, {"Z", 90},
    {"SPACE", 32}, {"SHIFT", 16}, {"CTRL", 17}, {"ALT", 18}, {"TAB", 9},
    {"0", 48}, {"1", 49}, {"2", 50}, {"3", 51}, {"4", 52},
    {"5", 53}, {"6", 54}, {"7", 55}, {"8", 56}, {"9", 57}
};

int skipKeyCode = 83; // Default 'S' key
int fastForwardSpeed = 300; // Room speed multiplier
bool autoAdvanceDialogue = true;

// Prompt user or read configuration
string iniPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "skip_key.ini");
if (!File.Exists(iniPath))
{
    string exeDir = Path.GetDirectoryName(Data.FilePath ?? "");
    if (!string.IsNullOrEmpty(exeDir))
        iniPath = Path.Combine(exeDir, "skip_key.ini");
}

if (File.Exists(iniPath))
{
    foreach (var line in File.ReadAllLines(iniPath))
    {
        string trimmed = line.Trim();
        if (trimmed.StartsWith(";") || trimmed.StartsWith("#") || !trimmed.Contains("="))
            continue;
        var parts = trimmed.Split(new char[] { '=' }, 2);
        string key = parts[0].Trim();
        string val = parts[1].Split(';')[0].Trim();

        if (key.Equals("SkipKey", StringComparison.OrdinalIgnoreCase))
        {
            if (int.TryParse(val, out int code))
            {
                skipKeyCode = code;
            }
            else if (keyMap.ContainsKey(val))
            {
                skipKeyCode = keyMap[val];
            }
        }
        else if (key.Equals("FastForwardSpeed", StringComparison.OrdinalIgnoreCase))
        {
            if (int.TryParse(val, out int speed))
                fastForwardSpeed = speed;
        }
        else if (key.Equals("AutoAdvanceDialogue", StringComparison.OrdinalIgnoreCase))
        {
            if (int.TryParse(val, out int autoAdv))
                autoAdvanceDialogue = (autoAdv != 0);
        }
    }
}

ScriptMessage($"Applying Cutscene Skip Mod...\nSkip Key Code: {skipKeyCode} ('{(char)(skipKeyCode >= 65 && skipKeyCode <= 90 ? skipKeyCode : '?')}')\nFast-Forward Speed: {fastForwardSpeed}");

// Code to inject into Step Event
string skipGML = $@"
// CUTSCENE & DIALOGUE SKIPPER
var skip_key = {skipKeyCode};
var is_skipping = keyboard_check(skip_key);

if (is_skipping) {{
    room_speed = {fastForwardSpeed};

    // Fast forward dialogue text box if present
    if (instance_exists(obj_writer)) {{
        with (obj_writer) {{
            if (variable_instance_exists(id, ""stringpos"") && variable_instance_exists(id, ""originalstring"")) {{
                stringpos = string_length(originalstring);
            }}
        }}
    }}

    // Advance dialogue
    if ({(autoAdvanceDialogue ? 1 : 0)}) {{
        keyboard_key_press(ord(""Z""));
        keyboard_key_release(ord(""Z""));
    }}
}} else {{
    if (room_speed > 30) {{
        room_speed = 30;
    }}
}}
";

// Inject into obj_time step event or obj_mainchara
UndertaleGameObject objTime = Data.GameObjects.ByName("obj_time");
if (objTime != null)
{
    UndertaleGameObject.Event stepEvent = objTime.Events[1].FirstOrDefault(e => e.EventSubtype == 0); // Step
    if (stepEvent == null)
    {
        stepEvent = new UndertaleGameObject.Event() { EventSubtype = 0 };
        objTime.Events[1].Add(stepEvent);
    }

    UndertaleCode code = stepEvent.Actions.Count > 0 ? stepEvent.Actions[0].CodeId : null;
    if (code != null)
    {
        string existingCode = code.GMLCode ?? "";
        if (!existingCode.Contains("CUTSCENE & DIALOGUE SKIPPER"))
        {
            code.ReplaceGML(existingCode + "\n\n" + skipGML, Data);
        }
    }
    else
    {
        UndertaleCode newCode = new UndertaleCode();
        newCode.Name = Data.Strings.MakeUnused("gml_Object_obj_time_Step_0");
        newCode.ReplaceGML(skipGML, Data);
        Data.Code.Add(newCode);

        UndertaleGameObject.EventAction action = new UndertaleGameObject.EventAction();
        action.CodeId = newCode;
        stepEvent.Actions.Add(action);
    }
}

ScriptMessage("Cutscene Skip Mod successfully applied! Save your data.win file to complete setup.");
