#!/bin/bash
set -eou pipefail

/usr/bin/pip3 install --user -r requirements.txt .
cp -v examples/mdpreviewrc $HOME/.mdpreviewrc

echo "Done! Have fun!"