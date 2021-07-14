#!/bin/bash
set -eou pipefail

/usr/bin/pip3 install -I --user -r requirements.txt .

sed -i "s|SCRIPT_PATH|$(pwd)/bin|" \
    $HOME/.config/systemd/user/mdpreviewd.service

cp -vf examples/mdpreviewrc $HOME/.mdpreviewrc
sed -ri "s|^PYTHONPATH=.*$|PYTHONPATH=\"$(pwd)\"|" $HOME/.mdpreviewrc
sed -ri "s|^PATH=.*$|PATH=\"$(pwd)/bin:\${PATH}\"|" $HOME/.mdpreviewrc
sed -ri "s|^MDPREVIEW_PATH=.*$|MDPREVIEW_PATH=\"$(pwd)\"|" $HOME/.mdpreviewrc

echo "Done! Have fun!"
