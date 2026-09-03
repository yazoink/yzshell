-- performance mode on fullscreen
hl.on("window.fullscreen", function()
	local game_mode = (hl.get_config("animations.enabled") == false)

	if game_mode then
		hl.exec_cmd("hyprctl reload")
		return
	end

	hl.exec_cmd("hyprctl reload")
	hl.config({
		general = {
			gaps_in = 0,
			gaps_out = 0, -- Disable gaps
			border_size = 0,
		},
		animations = {
			enabled = false, -- Disable animations
			borderangle = { enabled = false },
		},
		-- Disable blur, shadow and window rounding
		decoration = {
			shadow = { enabled = false },
			blur = { enabled = false },
			rounding = 0,
			active_opacity = 1,
			inactive_opacity = 1,
			fullscreen_opacity = 1,
		},
	})
end)

-- reset submap on reload
hl.on("config.reloaded", function()
	hl.dsp.submap("reset")
end)
