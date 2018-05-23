from flask import Markup
from os import remove, path, name as osName
from lesscpy import compile as C
from  hashlib import md5
# Fixing file not found for py2
from sys import version_info
if version_info.major == 2:
    FileNotFoundError = IOError


class lessc(object):
    def __init__(self, app=None, minify=True, spaces=True, tabs=False, inTag=True):
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
        self.hash = None
        self.path = None
        if self.app is None:
            raise(AttributeError("lessc(app=) requires Flask app instance"))
        for arg in [
            ['minify', minify],
            ['spaces', spaces],
            ['tabs', tabs]]:
            if not isinstance(arg[1], bool):
                raise(TypeError("lessc(" + arg[0] + "=) requires True or False"))
        self.injectThem()


    def injectThem(self):
        """ injecting cssify into the template as cssify """
        @self.app.context_processor
        def inject_vars():
            return dict(cssify=self.cssify)


    def cssify(self, css=None):
        splitter = '\\' if osName == 'nt' else '/'
        if css is None:
            raise(AttributeError(
                'lessc.cssify() requires less file link'))
        elif path.isfile(path.abspath(css)):
            if self.hash == self.getHash(path.abspath(css)):
                return self.returnLink()
            else:
                splittedPath = css.split(splitter)
                cssName = splittedPath[len(splittedPath) - 1].split('.')[0]
                splittedPath[len(splittedPath) - 1] = cssName + '.css'
                self.path = splitter.join(splittedPath)
                self.hash = self.getHash(path.abspath(css))
                if path.isfile(self.path):
                    remove(self.path)
                with open(self.path, 'w+') as file:
                    file.write(C(
                        path.abspath(css),
                        minify=self.minify,
                        spaces=self.spaces,
                        tabs=self.tabs
                    ))
                return self.returnLink()
        else:
            raise(FileNotFoundError('lessc.cssify(css=) cannot find the css file'))


    def getHash(self, file):
        """ to get md5 hash of css file to make sure not changed """
        hashing = md5()
        with open(file, 'r') as rFile:
            por = rFile.read()
            hashing.update(por)
        return hashing.hexdigest()


    def returnLink(self):
        if self.inTag:
            return Markup(
                '<link rel="stylesheet" href="%s"></link>' % self.path
            )
        else:
            return self.path