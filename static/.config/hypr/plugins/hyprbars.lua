hl.config({
    plugin = {
        hyprbars = {
            bar_title_enabled = true,
            bar_height = 38,
            bar_text_font = "Sans",
            bar_text_weight = "bold",
            bar_text_size = 15,
            bar_text_align = "center",
            bar_precedence_over_border = true,
            bar_padding = 12,
            bar_button_padding = 8,
            bar_buttons_alignment = "left",
            bar_part_of_window = true,
            on_double_click = "hyprctl dispatch fullscreen 1",
            bar_color = background,
            col = {
                text = foreground
            }
        }
    }
})

hl.window_rule({  
  name="BAR INACTIVE",  
    match = {  
    focus = false  
  },  
  ["hyprbars:title_color"] = surface4
})

hl.plugin.hyprbars.add_button({
    bg_color = red,
    fg_color = red,
    size = 16,
    icon = "",
    action = "hyprctl dispatch killactive",
})

hl.plugin.hyprbars.add_button({
    bg_color = yellow,
    fg_color = yellow,
    size = 16,
    icon = "",
    action = "hyprctl dispatch movetoworkspacesilent special",
})

hl.plugin.hyprbars.add_button({
    bg_color = green,
    fg_color = green,
    size = 16,
    icon = "",
    action = "hyprctl dispatch fullscreen 1",
})