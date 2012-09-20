syn match TagLine /^>>>[^$\(##\)]*/
highlight TagLine cterm=bold term=bold ctermfg=Cyan

syn region commentreg start=+## + end=+\n+
highlight commentreg ctermfg=DarkGray

syn keyword TodoKeywords        TODO 
highlight TodoKeywords cterm=bold term=bold ctermfg=Yellow

syn keyword FeatureKeywords     NEW IMPROVE IMPROVED FEATURE
highlight FeatureKeywords cterm=bold term=bold ctermfg=Blue

syn keyword DoneKeywords         DONE 
highlight DoneKeywords cterm=bold term=bold ctermfg=LightGreen

syn keyword NodoKeywords        NODO
highlight NodoKeywords cterm=bold term=bold ctermfg=DarkGray

syn keyword BugKeyword         FIXBUG
highlight BugKeyword cterm=bold term=bold ctermfg=Magenta

syn match DoneChar /\(^+\|^ \++\)/
highlight DoneChar cterm=bold term=bold ctermfg=LightGreen

syn match TodoChar /\(^-\|^ \+-\)/
highlight TodoChar cterm=bold term=bold ctermfg=Yellow

syn match NodoChar /\(^x\|^ \+x\)/
highlight NodoChar cterm=bold term=bold ctermfg=DarkGray
