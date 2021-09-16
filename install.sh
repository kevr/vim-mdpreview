#!/bin/bash
# This install script installs the project and dependencies
# via systemd pip3 to ./lib. It then creates a ~/.mdpreviewrc
# for the user with paths pointing to this directory.
set -eou pipefail

rm -vf $HOME/.config/systemd/user/mdpreviewd.service

/usr/bin/pip3 install -I --prefix "$(pwd)/lib" -r requirements.txt .

nvim_path="$HOME/.config/nvim/plugged/vim-mdpreview"
pypath="$(find "$nvim_path/lib" -type d -name 'site-packages' | xargs)"

sed -i "s|SCRIPT_PATH|$nvim_path/lib/bin|" \
    $HOME/.config/systemd/user/mdpreviewd.service

cp -vf examples/mdpreviewrc $HOME/.mdpreviewrc
sed -ri "s|^PYTHONPATH=.*$|PYTHONPATH=\"$pypath:$nvim_path\"|" $HOME/.mdpreviewrc
sed -ri "s|^PATH=.*$|PATH=\"$nvim_path/lib/bin:$nvim_path/bin:${PATH}|" \
    $HOME/.mdpreviewrc
sed -ri "s|^MDPREVIEW_PATH=.*$|MDPREVIEW_PATH=\"$nvim_path\"|" $HOME/.mdpreviewrc

systemctl --user daemon-reload

echo "Done! Have fun!"
