if hl.plugin.hyprexpo ~= nil then
    hl.config({
        plugin = {
            hyprexpo = {
                columns = 3,
                gaps_in = 10,
                gaps_out = 15,
                tile_rounding = 8,
                tile_rounding_power = 4.0,
                bg_col = background,
                active_highlight_col = blue,
                workspace_method = "center current",
                keynav_enable = 1,
                label_enable = 1,
                border_width = 1,
            },
        },
    })
    hl.bind("SUPER + Tab", function()
        hl.plugin.hyprexpo.expo("toggle")
    end)
    hl.plugin.hyprexpo.gesture({
        fingers = 4,
        direction = "up",
        action = "expo",
    })
end