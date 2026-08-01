# YZSHELL HYPRLAND CONFIG

local status, value = pcall(require, "generated")
if status then
    print("successfully loaded 'colours' module, it returned:", value)
else
    print("failed to load 'colours' module, its error message was:", value)
end

require("env")
require("monitors")
require("input")
require("general")
require("decoration")
require("gestures")
require("misc")
require("binds")
require("windowrules")
require("autostart")
require("plugins")