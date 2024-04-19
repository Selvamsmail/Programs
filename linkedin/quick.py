import json
import os

# Path to your VSCode settings.json file
settings_file_path = os.path.expanduser("C:/Users/PM/AppData/Roaming/Code/User/settings.json")

# Replace the above path with the appropriate location for your OS.
# Common locations are:
# Windows: C:\Users\YourUserName\AppData\Roaming\Code\User\settings.json
# macOS: ~/Library/Application Support/Code/User/settings.json
# Linux: ~/.config/Code/User/settings.json

# Load existing settings
with open(settings_file_path, "r") as file:
    settings_data = json.load(file)

# Update settings for better performance
settings_data["update.channel"] = "none"  # Disable automatic updates
settings_data["telemetry.enableTelemetry"] = False  # Disable telemetry data
settings_data["telemetry.enableCrashReporter"] = False  # Disable crash reporter
settings_data["editor.wordWrap"] = "off"  # Disable word wrapping
settings_data["editor.minimap.enabled"] = False  # Disable minimap
settings_data["python.languageServer"] = "Jedi"  # Use Jedi language server for Python
settings_data["editor.quickSuggestionsDelay"] = 100  # Set IntelliSense delay to 100ms
settings_data["files.autoSave"] = "off"  # Disable auto-save

# Save updated settings
with open(settings_file_path, "w") as file:
    json.dump(settings_data, file, indent=4)

print("VSCode settings have been updated for improved performance.")
