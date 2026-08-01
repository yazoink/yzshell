hl.config({
    input = {
        kb_layout = "us",
        follow_mouse = 1,
        numlock_by_default = true,
        accel_profile = "adaptive",
        scroll_method = "2fg",
        scroll_points = "flat",
        touchpad = {
            disable_while_typing = false,
            scroll_factor = touchpad_scroll_factor
        }
    }
})

hl.device({
    name = "tpps/2-ibm-trackpoint",
    accel_profile = "flat",
    sensitivity = 0.5
})