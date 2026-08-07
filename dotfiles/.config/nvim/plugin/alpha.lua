vim.pack.add({ 'https://github.com/goolord/alpha-nvim' })
vim.pack.add({'https://github.com/nvim-lua/plenary.nvim'}) 

require('alpha').setup(require'alpha.themes.dashboard'.config)