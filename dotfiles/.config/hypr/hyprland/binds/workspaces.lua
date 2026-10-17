-- switch workspace
for i = 1, 9 do
    hl.bind("SUPER + " .. i, hl.dsp.focus({workspace = i}), { description = "Switch to workspace " .. i })
end

-- special workspace
hl.bind("SUPER + SHIFT + S", hl.dsp.workspace.toggle_special("special"), { description = "Move to special workspace" })