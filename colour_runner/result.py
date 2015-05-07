from unittest import result
from unittest.util import strclass

from blessings import Terminal
try:
    # Python 2
    text_type = unicode
except NameError:
    # Python 3
    text_type = str


class ColourTextTestResult(result.TestResult):
    """
    A test result class that prints colour formatted text results to a stream.

    Based on https://github.com/python/cpython/blob/3.3/Lib/unittest/runner.py
    """
    separator1 = '=' * 70
    separator2 = '-' * 70
    indent = ' ' * 4

    _terminal = Terminal()

    colour_defaults = {
        "default": "white",
        "error": "red",
        "success": "green",
        "fail": "yellow",
        "skip": "yellow",
        "expected": "green",
        "unexpected": "red",
        "test_title": "blue",
        "test_name": "white"
    }

    _test_class = None

    def __init__(self, stream, descriptions, verbosity):
        super(ColourTextTestResult, self).__init__(stream, descriptions,
                                                   verbosity)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

        self.colours = {
            None: self.fetchColour(self.colour_defaults["default"]),
            'error': self.fetchColour("bold", self.colour_defaults["error"]),
            'expected': self.fetchColour("italic",
                                         self.colour_defaults["expected"]),
            'fail': self.fetchColour("bold", self.colour_defaults["fail"]),
            'skip': self.fetchColour("italic", self.colour_defaults["skip"]),
            'success': self.fetchColour(self.colour_defaults["success"]),
            'test_title': self.fetchColour("underline", "bold",
                                           self.colour_defaults["test_title"]),
            'test_name': self.fetchColour(self.colour_defaults["test_name"]),
            'unexpected': self.fetchColour("italic",
                                           self.colour_defaults["unexpected"]),
        }

    def fetchColour(self, *args):
        return getattr(self._terminal, "_".join(args), text_type)

    def getShortDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return self.indent + doc_first_line
        return self.indent + test._testMethodName

    def getLongDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        return str(test)

    def getClassDescription(self, test):
        test_class = test.__class__
        doc = test_class.__doc__
        if self.descriptions and doc:
            return doc.split('\n')[0].strip()
        return strclass(test_class)

    def startTest(self, test):
        super(ColourTextTestResult, self).startTest(test)
        if self.showAll:
            if self._test_class != test.__class__:
                self._test_class = test.__class__
                title = self.getClassDescription(test)
                self.stream.writeln(self.colours['test_title'](title))
            self.stream.write(self.colours['test_name'](
                self.getShortDescription(test))
            )
            self.stream.write(' ... ')
            self.stream.flush()

    def printResult(self, short, extended, colour_key=None):
        colour = self.colours[colour_key]
        if self.showAll:
            self.stream.writeln(colour(extended))
        elif self.dots:
            self.stream.write(colour(short))
            self.stream.flush()

    def addSuccess(self, test):
        super(ColourTextTestResult, self).addSuccess(test)
        self.printResult('.', 'ok', 'success')

    def addError(self, test, err):
        super(ColourTextTestResult, self).addError(test, err)
        self.printResult('E', 'ERROR', 'error')

    def addFailure(self, test, err):
        super(ColourTextTestResult, self).addFailure(test, err)
        self.printResult('F', 'FAIL', 'fail')

    def addSkip(self, test, reason):
        super(ColourTextTestResult, self).addSkip(test, reason)
        self.printResult('s', 'skipped {0!r}'.format(reason), 'skip')

    def addExpectedFailure(self, test, err):
        super(ColourTextTestResult, self).addExpectedFailure(test, err)
        self.printResult('x', 'expected failure', 'expected')

    def addUnexpectedSuccess(self, test):
        super(ColourTextTestResult, self).addUnexpectedSuccess(test)
        self.printResult('u', 'unexpected success', 'unexpected')

    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        colour = self.colours[flavour.lower()]

        for test, err in errors:
            self.stream.writeln(self.separator1)
            title = '%s: %s' % (flavour, self.getLongDescription(test))
            self.stream.writeln(colour(title))
            self.stream.writeln(self.separator2)
            self.stream.writeln(colour(err))
