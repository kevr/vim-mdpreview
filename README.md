# vim-mdpreview

A vim plugin which allows users to hot reload previews of markdown
in a browser as they save markdown files in vim.

## VIM Commands

- `:MarkdownPreview`
    - Open the markdown preview in `$BROWSER`.

`:MarkdownPreview` requires that the `mdpreviewd` service is
running. See [Installation](#installation) for details.

## Dependencies

All dependencies are public and available via `pip`.

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

## Installation

### With `vim-plug`

    Plug 'kevr/vim-mdpreview', { 'do': './install.sh' }

<small>**NOTE:** The `vim-plug` method installs `mdpreview` packages
and binaries to `$HOME/.local`</small>

### With `pip`

To install `vim-mdpreview`, you must install the `mdpreview` Python
package through `setup.py` or via `pip[3]` (including dependencies).

    $ /usr/bin/pip3 install --user -r requirements.txt .

<small>**Note:** Pay attention to use your system `python3` binary to
avoid any virtualenv issues.</small>

Last but not least, put the ftplugin script in your `~/.vim`:

    $ mkdir -p ~/.vim/after/ftplugin
    $ cp after/ftplugin/markdown.vim ~/.vim/after/ftplugin/

Now, opening a markdown file in vim will launch the `mdpreviewd`
service and writing one will update the preview.

## License

This project operates under the [MIT](LICENSE) Public License.

## Authors

| Name         | Email          |
|--------------|----------------|
| Kevin Morris | kevr@0cost.org |
