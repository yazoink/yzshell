if hl.plugin.hyprexpo ~= nil then
    hl.config({
        plugin = {
            hyprexpo = {
                columns = 3,
                gaps_in = 10,
                gaps_out = 15,
                tile_rounding = 16,
                tile_rounding_power = 4.0,
                bg_col = background,
                label_color = foreground,
                label_color_default = foreground,
                label_color_hover = foreground,
                label_color_focus = foreground,
                label_color_current = blue,
                workspace_number_color = foreground,
                label_bg_color = background,
                border_color = surface1,
                drag_drop_proxy_color = surface1,
                drag_drop_proxy_active_color = surface1,
                drag_drop_proxy_border_color = surface2,
                drag_drop_proxy_border_width = 1,
                drag_drop_proxy_rounding = 16,
                border_color_current = blue,
                border_color_focus = blue,
                border_color_hover = surface2,
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
        fingers = 3,
        scale = 1.5,
        direction = "up",
        action = "expo",
    })
    hl.plugin.hyprexpo.gesture({
        fingers = 3,
        scale = 1.5,
        direction = "down",
        action = "expo",
    })
end