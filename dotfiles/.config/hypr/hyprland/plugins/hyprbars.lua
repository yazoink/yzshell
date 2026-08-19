if hl.plugin.hyprbars ~= nil then
	hl.config({
		plugin = {
			hyprbars = {
				bar_title_enabled = true,
				bar_height = 40,
				bar_text_font = "Sans",
				bar_text_weight = "bold",
				bar_text_size = 14,
				bar_text_align = "center",
				bar_precedence_over_border = true,
				bar_padding = 13,
				bar_button_padding = 8,
				bar_buttons_alignment = "left",
				bar_part_of_window = true,
				on_double_click = "hyprctl dispatch fullscreen 1",
				bar_color = background,
				col = {
					text = foreground,
				},
			},
		},
	})

	hl.window_rule({
		name = "BAR INACTIVE",
		match = {
			focus = false,
		},
		["hyprbars:title_color"] = surface4,
	})

	hl.plugin.hyprbars.add_button({
		bg_color = window_button1,
		fg_color = window_button1,
		size = 16,
		icon = "",
		action = "hyprctl dispatch 'hl.dsp.window.close()'",
	})

	hl.plugin.hyprbars.add_button({
		bg_color = window_button2,
		fg_color = window_button2,
		size = 16,
		icon = "",
		--action = "hyprctl dispatch 'hl.dsp.window.move({workspace=\"special:special\", follow=false})'",
		action = "hyprctl dispatch 'hl.dsp.window.float({action=\"toggle\"})'",
	})

	hl.plugin.hyprbars.add_button({
		bg_color = window_button3,
		fg_color = window_button3,
		size = 16,
		icon = "",
		action = "hyprctl dispatch 'hl.dsp.window.fullscreen({action=\"toggle\"})'",
	})
end
