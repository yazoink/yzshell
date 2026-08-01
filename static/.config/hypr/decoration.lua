hl.config({
    decoration = {
        rounding = 16,
        rounding_power = 4.0,
        dim_modal = true,
        dim_inactive = true,
        dim_strength = 0.05,
        dim_special = 0.2,
        blur = {
            enabled = false
        },
        shadow = {
            enabled = true,
            range = 20,
            offset = {0, 2},
            render_power = 10,
            color = "rgba(00000020)"
        },
        --animations = { enabled = true },
        blur = { enabled = false }
    }
})