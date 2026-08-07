vim.pack.add({ 'https://github.com/nvim-treesitter/nvim-treesitter' })

vim.api.nvim_create_autocmd('PackChanged', { callback = function(ev)
  local name, kind = ev.data.spec.name, ev.data.kind
  if name == 'nvim-treesitter' and kind == 'update' then
    if not ev.data.active then vim.cmd.packadd('nvim-treesitter') end
    vim.cmd('TSUpdate')
  end
end })

require('nvim-treesitter').setup({
  ensure_installed = {
    'rust',
    'javascript',
    'zig',
    'bash',
    'latex',
    'c',
    'comment',
    'css',
    'desktop',
    'diff',
    'git_config',
    'gitignore',
    'git_rebase',
    'gitattributes',
    'gitcommit',
    'go',
    'html',
    'hyprlang',
    'json',
    'kdl',
    'lua',
    'luap',
    'nix',
    'php',
    'php_only',
    'python',
    'query',
    'regex',
    'scss',
    'ssh_config',
    'toml',
    'typst',
    'vim',
    'vimdoc',
    'xml',
    'xresources',
    'yaml',
    'yuck',
    'zsh',
    'jq',
    'markdown',
    'markdown_inline',
  },
  sync_install = true,
  auto_install = true,
  highlight = { enable = true },
  indent = { enable = true },
  incremental_selection = { enable = true },
})