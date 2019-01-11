from flask import Markup
from os import remove, path, name as osName
from lesscpy import compile as C
from  hashlib import md5
# Fixing file not found for py2
from sys import version_info
if version_info.major == 2:
    FileNotFoundError = IOError


class lessc(object):
    def __init__(
        self, app=None, minify=True,
        spaces=True, tabs=False, inTag=True
    ):
        """
        A Flask extension to add lesscpy support to the template, and
        recompile less file if changed.

        @param: app Flask app instance to be passed (default:None).
        @param: minify To minify the css output (default:True).
        @param: spaces To minify spaces in css (default:True).
        @param: tabs To minify tabs in css (default:True).
        @param: inTag To return css file link in html tag (default:True).
        """
        self.app = app
        self.minify = minify
        self.spaces = spaces
        self.tabs = tabs
        self.inTag = inTag
        self.STORAGE = {}  # where compiled less files stored
        if self.app is None:
            raise(AttributeError("lessc(app=) requires Flask app instance"))
        for arg in [
            ['minify', minify],
            ['spaces', spaces],
            ['tabs', tabs]
        ]:
            if not isinstance(arg[1], bool):
                raise(TypeError("lessc(" + arg[0] + "=) requires"
                " True or False"))
        self.injectThem()

    def injectThem(self):
        """ injecting cssify into the template as cssify """
        @self.app.context_processor
        def inject_vars():
            return dict(cssify=self.cssify)

    def cssify(self, less=None):
        splitter = '\\' if osName == 'nt' else '/'
        if less is None:
            raise(AttributeError(
                'lessc.cssify() requires less file link'))

        lessPath = splitter.join([self.app.static_folder, less])
        if path.isfile(path.abspath(lessPath)):
            if less in self.STORAGE.keys():
                return self.returnLink(self.STORAGE[less])
            else:
                splittedPath = less.split(splitter)
                cssName = splittedPath[-1].split('.')[0] + '.css'
                splittedPath[-1] = cssName
                cssRelPath = splitter.join(splittedPath)
                cssPath = splitter.join([self.app.static_folder, cssRelPath])
                with open(cssPath, 'w+') as file:
                    file.write(C(
                        path.abspath(lessPath),
                        xminify=self.minify,
                        spaces=self.spaces,
                        tabs=self.tabs))
                self.STORAGE[less] = cssRelPath
                return self.returnLink(cssRelPath)
        else:
            raise(FileNotFoundError(
                'lessc.cssify(css=) cannot find the css file'))

    def returnLink(self, css_path):
        """ to return html ready link if needed """
        if self.inTag:
            return Markup(
                '<link rel="stylesheet" href="/%s"></link>' % css_path
            )
        else:
            return '/' + css_path

