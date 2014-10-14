set nocompatible
filetype off
set rtp+=~/.vim/bundle/vundle/
call vundle#rc()
"----------setting my bundle----------
Bundle "SirVer/ultisnips"
Bundle "hdima/python-syntax"
Bundle "terryma/vim-multiple-cursors"
Bundle "Raimondi/delimitMate"
Bundle "kien/rainbow_parentheses.vim"
Bundle "majutsushi/tagbar"
Bundle "scrooloose/nerdtree"
Bundle "rkulla/pydiction"
Bundle "ervandew/supertab"
filetype plugin indent on
filetype plugin on
filetype indent on
"----------setting Rainbow Parentheses----------
let g:rbpt_colorpairs = [
    \ ['brown',       'RoyalBlue3'],
    \ ['Darkblue',    'SeaGreen3'],
    \ ['darkgray',    'DarkOrchid3'],
    \ ['darkgreen',   'firebrick3'],
    \ ['darkcyan',    'RoyalBlue3'],
    \ ['darkred',     'SeaGreen3'],
    \ ['darkmagenta', 'DarkOrchid3'],
    \ ['brown',       'firebrick3'],
    \ ['gray',        'RoyalBlue3'],
    \ ['black',       'SeaGreen3'],
    \ ['darkmagenta', 'DarkOrchid3'],
    \ ['Darkblue',    'firebrick3'],
    \ ['darkgreen',   'RoyalBlue3'],
    \ ['darkcyan',    'SeaGreen3'],
    \ ['darkred',     'DarkOrchidLoadBraces']
	\ ]
let g:rbpt_loadcmd_toggle = 0
let g:rbpt_max = 16
au VimEnter * RainbowParenthesesToggle
au Syntax * RainbowParenthesesLoadRound
au Syntax * RainbowParenthesesLoadSquare
au Syntax * RainbowParenthesesLoadBraces
"----------setting python-syntax----------
let python_highlight_all = 1
"----------setting vim-multiple-cursors----------
let g:multi_cursor_use_default_mapping=1
let g:multi_cursor_next_key='<C-n>'
let g:multi_cursor_prev_key='<C-p>'
let g:multi_cursor_skip_key='<C-x>'
let g:multi_cursor_quit_key='<Esc>'
highlight multiple_cursors_cursor term=reverse cterm=reverse gui=reverse
highlight link multiple_cursors_visual Visual
"-------------setting tagbar----------------
nmap <F4> :TagbarToggle<CR>
let g:tagbar_type_ruby = {
    \ 'kinds' : [
        \ 'm:modules',
        \ 'c:classes',
        \ 'd:describes',
        \ 'C:contexts',
        \ 'f:methods',
        \ 'F:singleton methods'
    \ ]
\ }
let g:tagbar_type_go = {
    \ 'ctagstype': 'go',
    \ 'kinds' : [
        \'p:package',
        \'f:function',
        \'v:variables',
        \'t:type',
        \'c:const'
    \]
\}
"-------------setting NERDTree----------------
let g:nerdtree_tabs_open_on_console_startup=0
map <F3> :NERDTreeToggle<CR>
imap <F3> <ESC>:NERDTreeToggle<CR>
let NERDTreeDirArrows=0
let NERDTreeShowBookmarks=1
let NERDTreeChDirMode=2
let NERDTreeQuitOnOpen=1
let NERDTreeWinSize=20
let NERDTreeShowHidden=0
"-------------setting pydiction----------------
let g:pydiction_location = '~/.vim/bundle/pydiction/complete-dict'
let g:pydiction_menu_height = 10
"-------------setting indentLine----------------
let g:indentLine_color_gui = '#A4E57E'
"-------------setting taglist----------------
let Tlist_Show_Menu = 1
let Tlist_Show_One_File = 1
let Tlist_Exit_OnlyWindow = 1

"let g:SuperTabContextDefaultCompletionType = "<c-n>"
