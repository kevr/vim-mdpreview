" Setup a write hook to update our /tmp/mdpreview.md which
" our server listens for changes on.
if !get(g:, 'mdpreview_port')
    " By default, we use port 13337.
    let g:mdpreview_port = "13337"
endif

" Start the user mdpreviewd service.
call system("systemctl --user is-active mdpreviewd")
if v:shell_error != 0
    call system("systemctl --user start mdpreviewd")
endif

if v:shell_error != 0
    echo "Unable to start mpdreviewd.service."
    echo "See `journalctl -u mpdreviewd -e` for logs."
endif

function! UpdatePreview()
    let l:content = join(getline(1, '$'), "\n")

    " Update content.
    call writefile(split(get(l:, "content"), "\n", 1),
        \ glob("/tmp/mdpreview.md"), "b")
endfunction

" After writing a file, copy it to /tmp/mdpreview.md.
" This is then detected by mdpreviewd and triggers a websocket
" load via Javascript on the rendered markdown page.
autocmd BufWritePost *.md :call UpdatePreview()

" Spawn a preview browser tab using $BROWSER.
" g:mdpreview_port configures the port used (default: '13337').
command MarkdownPreview call system(
    \ "bash -c '$BROWSER http://localhost:" . get(g:, 'mdpreview_port') . " >/dev/null 2>&1 &'")
