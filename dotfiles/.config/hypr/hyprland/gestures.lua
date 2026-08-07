hl.config({
    gestures = {
        workspace_swipe_touch = true,
        workspace_swipe_forever = true,
        workspace_swipe_direction_lock = false,
        workspace_swipe_create_new = true
    }
})

hl.gesture({
    fingers = 3,
    direction = "horizontal",
    action = "workspace"
})