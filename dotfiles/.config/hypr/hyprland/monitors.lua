hl.monitor({
	output = "",
	mode = "preferred",
	position = "auto",
	scale = "auto",
})

hl.monitor({
	output = "desc:Dell Inc. DELL U2715H 6VY7R72K01YS",
	mode = "highres",
	position = "auto",
	scale = 1.33,
	--scale = 1.6,
})

hl.monitor({
	output = "desc:BOE 0x0868",
	mode = "highres",
	position = "auto",
	scale = 1.33,
})

hl.config({
	xwayland = {
		force_zero_scaling = true,
	},
})
