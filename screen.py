import threading, time, base64, sys

ver = sys.version_info.major
if ver==2:
    import StringIO as io
elif ver==3:
    import io


class Screen():
    def __init__(self):
        self.screenbuf = ""
        self.password = ""

    def update(self, frame_data):
        """Receive a base64-encoded JPEG frame from the sharer."""
        self.screenbuf = frame_data

    def gen(self):
        s = ''
        if ver==2:
            s = self.screenbuf
        elif ver==3:
            s = self.screenbuf if isinstance(self.screenbuf, str) else self.screenbuf.decode() if self.screenbuf else ''
        return s

screenlive = Screen()
