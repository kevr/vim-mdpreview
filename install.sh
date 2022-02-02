#!/bin/bash
# This install script installs the project and dependencies
# via systemd pip3 to ./lib. It then creates a ~/.mdpreviewrc
# for the user with paths pointing to this directory.
CONF="$HOME/.mdpreviewrc"
SERVICE="$HOME/.config/systemd/user/mdpreviewd.service"

exists() {
    if ! type $1 >/dev/null 2>&1; then
        return 1
    fi
    return 0
}

dependency_missing() {
    echo "error: unable to locate dependent executable $1"
    exit 1
}

if ! exists git; then
    dependency_missing git
elif ! exists pip; then
    dependency_missing pip
elif ! exists systemctl; then
    dependency_missing systemctl
fi

# Cleanup previous config/service files.
rm -vf $CONF $SERVICE

# Fetch git tags.
git fetch --tags

# Install python package
dir="$(realpath $(dirname $0))"
libdir="${dir}/lib"
pip install -I --prefix "$libdir" -r requirements.txt .
pypath="$(find "$libdir" -type d -name 'site-packages' | xargs)"

# Install config
install -m644 "${dir}/examples/mdpreviewrc" $CONF
sed -i "s|%PATH%|${libdir}/bin:${dir}/bin:${PATH}|g" $CONF
sed -i "s|%PYTHONPATH%|${pypath}:${dir}|g" $CONF
sed -i "s|%MDPREVIEW_PATH%|${dir}|g" $CONF

# Install mdpreviewd.service
install -Dm644 "${dir}/systemd/mdpreviewd.service" $SERVICE
sed -i "s|%SCRIPT_PATH%|${dir}/bin|" $SERVICE

systemctl --user daemon-reload
systemctl --user restart mdpreviewd.service

echo "Done!"
echo -n "To begin using vim-mdpreview, execute :MarkdownPreview while editing "
echo "a markdown file, then hot reload the preview by saving markdown files."
