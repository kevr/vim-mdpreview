# vim-mdpreview

A vim plugin which allows users to hot reload previews of markdown
in a browser as they save markdown files in vim.

## VIM Commands

- `:MarkdownPreview`
    - Open the markdown preview in `$BROWSER`.

`:MarkdownPreview` requires that the `mdpreviewd` service is
running. See [Installation](#installation) for details.

## Dependencies

These dependencies must be installed globally in the Python
installation used to run the server.

<table>
<tr><th>Dependencies</th><th>Integrations</th></tr>
<tr><td>

| Python / PIP Package   |
|------------------------|
| fastapi                |
| aiofiles               |
| websockets             |
| uvicorn                |
| asgiref                |
| uvloop                 |
| httptools              |

</td><td>

| Project                                                                    |
|----------------------------------------------------------------------------|
| [github-markdown-css](https://github.com/sindresorhus/github-markdown-css) |
| [marked](https://github.com/markedjs/marked)                               |

</td></tr>
</table>

On `Ubuntu`, on can install deps via:

    $ sudo apt-get -y install python3-aiofiles python3-pip \ 
        python3-websockets python3-uvloop python3-httptools
    $ sudo /usr/bin/pip3 install fastapi

## Installation

To install `vim-mdpreview`, you must install the `mdpreview` Python
package through `setup.py`.

    $ sudo python3 setup.py install --install-scripts=/usr/local/bin

This will install the `mdpreview` package along with resources and
the `mdpreviewd.service` systemd unit.

Change `MD_USER` to the user who uses vim:

    $ SERVICE=/etc/systemd/system/mdpreviewd.service
    $ sudo sed -i 's;MD_USER=kevr;MD_USER=<your_user>;' $SERVICE

Reload the service if needed and start it.

    $ sudo systemctl daemon-reload mdpreviewd
    $ sudo systemctl start mdpreviewd

Put the ftplugin script in your `~/.vim`:

    $ mkdir -p ~/.vim/after/ftplugin
    $ cp .vim/after/ftplugin/markdown.vim ~/.vim/after/ftplugin/
