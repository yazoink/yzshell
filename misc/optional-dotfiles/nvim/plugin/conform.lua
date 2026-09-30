vim.pack.add({ 'https://github.com/stevearc/conform.nvim' })

require("conform").setup({
  formatters_by_ft = {
    lua = { "stylua" },
    python = { "isort", "black" },
    rust = { "rustfmt", lsp_format = "fallback" },
    javascript = { "prettierd", "prettier", stop_after_first = true },
	html = { "prettierd", "prettier", stop_after_first = true },
	css = { "prettierd", "prettier", stop_after_first = true },
	markdown = { "prettierd", "prettier", stop_after_first = true },
	nix = { "alejandra" },
	bash = { "shfmt", "beautysh" },
	sh = { "shfmt", "beautysh" },
	yaml = { "yamllint", "yamlfmt" },
	c = { "uncrustify" },
	rust = { "rustfmt" },
	typst = { "typstyle" },
	php = { "mago", "pretty-php" },
	json = { "fixjson" },
  },
  format_on_save = {
    timeout_ms = 500,
    lsp_format = "fallback",
  },
})