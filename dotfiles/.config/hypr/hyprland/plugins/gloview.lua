if hl.plugin.gloview ~= nil then
	hl.config({
		plugin = {
			gloview = {
				anchor = "top",
				backdrop_color = "rgba(00000020)",
				gap = 8,
				padding = 8,
				padding_top = 8,
				padding_bottom = 58,
				blur = 1,
				strip_height = 150,
				strip_margin = 8,
				strip_gap = 8,
				strip_card_round = 8,
				preview_round = 16,
				strip_band_color = background,
				strip_card_color = surface1,
				strip_active_color = surface2,
				strip_active_border = blue,
				strip_active_border_size = 2,
				strip_hover_border = surface3,
				strip_hover_border_size = 1,
				strip_plus_color = surface3,
				preview_bg = surface2,
				shadow_color = "rgba(00000020)",
				hover_border = "rgba(00000000)",
				hover_border_size = 1,
				select_border = "rgba(00000000)",
				select_border_size = 1,
				show_special = 1,
				show_special = 0,
				hide_top_layers = 0,
				hide_overlay_layers = 0,
				above_namespaces = "waybar",
				dynamic_workspaces = 1,
				show_empty = 0,
				show_all_workspaces = 0,
				show_workspace_labels = 0,
				show_window_labels = 0,
			},
		},
	})
	hl.bind("SUPER + Tab", hl.plugin.gloview.toggle)
	hl.bind("SUPER + SHIFT + Tab", hl.plugin.gloview.desktop)
	hl.bind("SUPER + CTRL + Tab", hl.plugin.gloview.allworkspaces)
end
