hl.bind("SUPER + Q", hl.dsp.window.close(), { description = "Close active window" })
hl.bind("SUPER + CTRL + Q", hl.dsp.window.kill(), { description = "Kill active window" })
hl.bind("SUPER + X", hl.dsp.window.pin({ action = "toggle" }), { description = "Pin active window" })
hl.bind("SUPER + F", hl.dsp.window.float({ action = "toggle" }), { description = "Float active window" })
hl.bind("SUPER + M", hl.dsp.window.fullscreen({ mode = "maximized", action = "toggle" }), { description = "Maximise active window" })
hl.bind("SUPER + SHIFT + M", hl.dsp.window.fullscreen({ mode = "fullscreen", action = "toggle" }), { description = "Fullscreen active window" })

-- move window to workspace
for i = 1, 9 do
    hl.bind("SUPER + SHIFT + " .. i, hl.dsp.window.move({workspace = i}), { description = "Switch to workspace " .. i })
end

-- move window to special workspace
hl.bind(
    "SUPER + CTRL + up",
    hl.dsp.window.move({ workspace = "special:special", follow = false }, { description = "Move to special workspace" })
)

-- focus in direction
hl.bind("SUPER + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind("SUPER + mouse:274", hl.dsp.window.drag(), { mouse = true })
hl.bind("SUPER + mouse:273", hl.dsp.window.resize(), { mouse = true })
--#/# bind = SUPER + ←/↑/→/↓,, -- Focus in direction
for i = 1, 4 do
    local arrowkey = { "Left", "Right", "Up", "Down" }
    local focusdir = { "l", "r", "u", "d" }
    hl.bind("SUPER + " .. arrowkey[i], hl.dsp.focus({ direction = focusdir[i] }), { description = "Focus in direction " .. focusdir[i] })
end

-- move in direction
for i = 1, 4 do
    local arrowkey = { "Left", "Right", "Up", "Down" }
    local focusdir = { "l", "r", "u", "d" }
    hl.bind("SUPER + SHIFT + " .. arrowkey[i], hl.dsp.window.move({ direction = focusdir[i] }))
end

-- split ratio
hl.bind("SUPER + Minus", hl.dsp.layout("splitratio -0.1"), { repeating = true, description = "Decrease split ratio" })
hl.bind("SUPER + Equal", hl.dsp.layout("splitratio +0.1"), { repeating = true, description = "Increase split ratio" })

hl.bind("SUPER + K", hl.dsp.layout("swapsplit"), { description = "Swap split" })