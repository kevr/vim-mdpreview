" Setup a write hook to update our /tmp/mdpreview.md which
" our server listens for changes on.
autocmd BufWritePost * :call system( "cp " . expand("%") . " /tmp/mdpreview.md")
command MarkdownPreview call system("bash -c '$BROWSER http://localhost:13337'")

