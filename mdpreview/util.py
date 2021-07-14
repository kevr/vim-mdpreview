import os

home = os.environ.get("HOME")
share = os.environ.get("MDPREVIEW_PATH",
                       os.path.join(home, ".local", "share", "mdpreview"))
