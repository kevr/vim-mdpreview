#!/bin/bash
# This install script installs the project and dependencies
# via systemd pip3 to ./lib. It then creates a ~/.mdpreviewrc
# for the user with paths pointing to this directory.
set -eou pipefail

/usr/bin/pip3 install -I --prefix "$(pwd)/lib" -r requirements.txt .

sed -i "s|SCRIPT_PATH|$(pwd)/lib/bin|" \
    $HOME/.config/systemd/user/mdpreviewd.service

pypath="$(find $(pwd)/lib -type d -name 'site-packages' | xargs)"
cp -vf examples/mdpreviewrc $HOME/.mdpreviewrc
sed -ri "s|^PYTHONPATH=.*$|PYTHONPATH=\"$pypath:$(pwd)\"|" $HOME/.mdpreviewrc
sed -ri "s|^PATH=.*$|PATH=\"$(pwd)/lib/bin:$(pwd)/bin:\${PATH}\"|" \
    $HOME/.mdpreviewrc
sed -ri "s|^MDPREVIEW_PATH=.*$|MDPREVIEW_PATH=\"$(pwd)\"|" $HOME/.mdpreviewrc

systemctl --user daemon-reload

echo "Done! Have fun!"
