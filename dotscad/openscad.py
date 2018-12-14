import os, sys
import platform
import tempfile
import subprocess
import re


class OpenSCAD(object):

    __slots__ = ("path", "_debug", "_source")

    def __init__(self, path, debug=False):
        self.path = path
        self._debug = bool(debug)
        self._load()

    def debug(self, message=None):
        if self._debug:
            if message is not None:
                print(message, file=sys.stderr)
        return self._debug

    def render(self):
        """
        Render the source code.  With this base class, that just means returning the unmodified source.
        :return:str
        """
        return self._source

    def version(self):
        cmd = [self.cmd(), "--version"]
        # Note: version comes on stderr
        out = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, universal_newlines=True
        )
        match = re.match(r"^\s*OpenSCAD version (\d{4})\.(\d\d)\.(\d\d)\s*$", out)
        return (match[1], match[2], match[3]) if match else ()

    def render_stl(self, dest, overwrite=False):
        # Get path to the parent directory of the file we're working with so
        # openscad can find includes, etc.
        dirname = os.path.dirname(os.path.abspath(self.path))

        # Make sure the output has the proper suffix
        if not dest.lower().endswith(".stl"):
            dest += ".stl"

        # @todo decide if we want this...
        # Destinations are relative to the source path
        # if not os.path.isabs(dest):
        #    path = os.path.join(dirname,dest)

        # Don't overwrite
        if os.path.exists(dest) and not overwrite:
            self.debug("Skipping.  Destination file {0} exists.".format(dest))
            return False

        if self.debug():
            tmp_scad_path = os.path.join(dirname, dest + ".DEBUG.scad")
            # @todo print warning to stderr if tmp_scad_path exists
            tmp_scad = open(tmp_scad_path, "w")
            tmp_scad.write(str.encode(self.render()))
            tmp_scad.close()
        else:
            # When not debugging, we'll want a temp file that cleans up after itself
            tmp_scad = tempfile.NamedTemporaryFile(suffix=".scad", dir=dirname)
            tmp_scad.write(str.encode(self.render()))
            tmp_scad.flush()
            tmp_scad_path = tmp_scad.name

        cmd = [
            self.cmd(),
            "-o",
            dest,
            #'--render', # latest version of openscad doesn't want this [CSA]
            tmp_scad_path,
        ]
        self.debug(" ".join(cmd))
        subprocess.call(cmd, cwd=dirname)
        return True

    def cmd(self):
        """ Returns the appropriate command for the current OS """
        if os.getenv("OPENSCAD_PATH"):
            return os.getenv("OPENSCAD_PATH")
        if platform.system() == "Darwin":
            return "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
        if platform.system() == "Windows":
            # TODO: Windows path may not be accurate everywhere.
            # TODO: Figure out how to load from registry?
            return '"C:/Program Files/OpenSCAD/openscad"'
        # Default to linux-friendly CLI program name
        return "openscad"

    def _load(self):
        with open(self.path) as file:
            self._source = file.read()

    def __str__(self):
        return self.render()

