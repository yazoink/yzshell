-- switch workspace
for i = 1, 9 do
    hl.bind("SUPER + " .. i, hl.dsp.focus({workspace = i}))
end

-- special workspace
hl.bind("SUPER + SHIFT + S", hl.dsp.workspace.toggle_special("special"))