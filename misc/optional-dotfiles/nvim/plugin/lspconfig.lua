vim.pack.add({'https://github.com/neovim/nvim-lspconfig'})

vim.lsp.enable({
    'basics_ls',
    'nil_ls',
    'basedpyright',
    'phpactor',
    'phptools',
    'bashls',
    'clangd',
    'cssls',
    'html',
    'htmx',
    'intelephense',
    'jsonls',
    'markdown_oxide',
    'qmlls',
    'stylua',
    'typst_lsp',
    "ts_ls",
    "rust_analyzer"
})

--vim.lsp.config('module', {x = y})