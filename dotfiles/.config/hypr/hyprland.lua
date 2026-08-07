# YZSHELL HYPRLAND CONFIG

local status, value = pcall(require, "hyprland.colours")
if status then
    print("successfully loaded 'colours' module, it returned:", value)
else
    print("failed to load 'colours' module, its error message was:", value)
end

local status, value = pcall(require, "hyprland.vars")
if status then
    print("successfully loaded 'vars' module, it returned:", value)
else
    print("failed to load 'vars' module, its error message was:", value)
end

require("hyprland.env")
require("hyprland.monitors")
require("hyprland.input")
require("hyprland.general")
require("hyprland.decoration")
require("hyprland.gestures")
require("hyprland.misc")
require("hyprland.ecosystem")
require("hyprland.binds")
require("hyprland.windowrules")
require("hyprland.autostart")
require("hyprland.animations")
require("hyprland.plugins")