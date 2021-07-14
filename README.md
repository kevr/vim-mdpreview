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
| jinja2                 |

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

With `vim-plug`, users do not need to do anything else. Just
`:PlugInstall`, open a markdown file, run `:MarkdownPreview`
and continue on to live previewing your vim markdown writes.

### Otherwise

Run `install.sh` to automate a bunch of environment variable
configuration after installing pip to the local directory.

It'll also install a systemd service to `$HOME/.config/systemd/user`
which vim starts up for hot reload communication.

    $ ./install.sh

Last but not least, put the ftplugin script in your `~/.vim`:

    $ mkdir -p ~/.vim/after/ftplugin
    $ cp after/ftplugin/markdown.vim ~/.vim/after/ftplugin/

Now, opening a markdown file in vim will launch the `mdpreviewd`
service and writing one will update the preview.

## Configuration

There's just one configuration located at
[example/mdpreviewrc](example/mdpreviewrc) which contains specific `PATH`
and `PORT` environment variables used by the `mdpreviewd` systemd service.

Before the service can successfully start,
[example/mdpreviewrc](example/mdpreviewrc) must be located at
`$HOME/.mdpreviewrc`.


**NOTE:** It is suggested that this configuration file is not changed
other than the `PORT` variable. Installation through `vim-plug` and
other means set the path information up for you.

## License

This project operates under the [MIT](LICENSE) Public License.

## Authors

| Name         | Email          |
|--------------|----------------|
| Kevin Morris | kevr@0cost.org |
