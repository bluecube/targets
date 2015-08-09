import contextlib
import sys

class Svg:
    def __init__(self, fp = sys.stdout, **extra_args):
        self._fp = fp
        self._tag = "svg"
        self._parameters = {"xmlns": "http://www.w3.org/2000/svg"}
        self._parameters.update(extra_args)
        self._has_content = False

    def write(self, data):
        "Write unescaped data into the current tag."
        if not self._has_content:
            self._fp.write(self._tag_start(self._tag, self._parameters))
            self._fp.write(">")
        self._fp.write(data)
        self._has_content = True

    def tag(self, name, **parameters):
        "Create a new tag with given name and parameters. Return value is a context manager!"
        tag = self.__class__(self)
        tag._tag = name
        tag._parameters = parameters
        return tag

    def unpaired_tag(self, name, **parameters):
        "Directly write an unpaired tag."
        self.write(self._tag_start(name, parameters))
        self.write("/>")

    def _tag_start(self, name, parameters):
        return "<" + name + "".join(" " + self._dashes(str(k)) + '="' + self._escape(str(v)) + '"' for k, v in parameters.items())

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if not self._has_content:
            self._fp.write(self._tag_start(self._tag, self._parameters))
            self._fp.write("/>")
        else:
            self._fp.write("</" + self._tag + ">")

        return False

    @staticmethod
    def _dashes(s):
        return s.replace("_", "-")

    @staticmethod
    def _escape(s):
        escapes = {"&": "&amp;",
                   '"': "&quot;",
                   "'": "&apos;",
                   ">": "&gt;",
                   "<": "&lt;"}

        return "".join(escapes.get(c, c) for c in s)


    # Convenience functions

    def line(self, x1, y1, x2, y2, **extra_parameters):
        self.unpaired_tag("line", x1 = x1, x2 = x2, y1 = y1, y2 = y2, **extra_parameters)

    def circle(self, x, y, r, **extra_parameters):
        self.unpaired_tag("circle", cx = x, cy = y, r = r, **extra_parameters)

    def text(self, text, x, y, **extra_parameters):
        with self.tag("text", x = x, y = y, **extra_parameters) as tag:
            tag.write(self._escape(str(text)))

def mm(n):
    "Format value as number and add 'mm' unit to it"
    return "{:f}mm".format(n)

