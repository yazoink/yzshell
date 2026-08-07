vim.pack.add({ 'https://github.com/nvim-mini/mini.nvim' })

require('mini.basics').setup()

require('mini.extra').setup()

require('mini.pick').setup()
vim.keymap.set('n', '<leader>ff', MiniPick.builtin.files, { desc = 'Pick files' })

require('mini.files').setup({
    mappings = {
        go_in = '<Enter>',
        go_out = '<BS>',
        mark_set = ' ',
        reset = 'R',
        trim_left   = '<',
        trim_right  = '>',
    }
})
 local minifiles_toggle = function(...)
    if MiniFiles.close() == nil then MiniFiles.open(...) end
  end
vim.keymap.set('n', '<leader>e', minifiles_toggle, { desc = 'Open file explorer' })

require('mini.trailspace').setup()
vim.keymap.set('n', '<leader>tr', MiniTrailspace.trim, { desc = 'Trim all trailing whitespace' })
vim.keymap.set('n', '<leader>tl', MiniTrailspace.trim_last_lines, { desc = 'Trim all trailing empty lines' })

--require('mini.animate').setup()

local hipatterns = require('mini.hipatterns')
hipatterns.setup({
    highlighters = {
        -- Highlight standalone 'FIXME', 'HACK', 'TODO', 'NOTE'
        fixme = { pattern = '%f[%w]()FIXME()%f[%W]', group = 'MiniHipatternsFixme' },
        hack  = { pattern = '%f[%w]()HACK()%f[%W]',  group = 'MiniHipatternsHack'  },
        todo  = { pattern = '%f[%w]()TODO()%f[%W]',  group = 'MiniHipatternsTodo'  },
        note  = { pattern = '%f[%w]()NOTE()%f[%W]',  group = 'MiniHipatternsNote'  },

        -- Highlight hex color strings (`#rrggbb`) using that color
        hex_color = hipatterns.gen_highlighter.hex_color(),
    },
})

require('mini.indentscope').setup()

require('mini.notify').setup()

require('mini.icons').setup({ style = 'glyph' })

require('mini.statusline').setup({use_icons = false})

require('mini.tabline').setup()

require('mini.surround').setup()

require('mini.pairs').setup()

require('mini.comment').setup({
    mappings = {
        comment = 'gc',
        comment_line = 'gcc',
        comment_visual = 'gc',
        textobject = 'gc',
    }
})

local gen_loader = require('mini.snippets').gen_loader
require('mini.snippets').setup({
  snippets = {
    -- Load custom file with global snippets first (adjust for Windows)
    gen_loader.from_file('~/.config/nvim/snippets/global.json'),

    -- Load snippets based on current language by reading files from
    -- "snippets/" subdirectories from 'runtimepath' directories.
    gen_loader.from_lang(),
  },
})

require('mini.completion').setup()