# colour-runner

Colour formatting for `unittest` test output.

## Installation

    pip install colour-runner

### Django

Mix the `ColourRunnerMixin` into your `unittest` test runner (eg: in `project/runner.py`):

    from django.test.runner import DiscoverRunner  # Django 1.6's default
    from colour_runner.django_runner import ColourRunnerMixin

    class MyTestRunner(ColourRunnerMixin, DiscoverRunner):
        pass

Point django at it in `settings.py`:

    TEST_RUNNER = 'project.runner.MyTestRunner'

### Other Python

Where you would normally use:

* `unittest.TextTestRunner`, use `colour_runner.runner.ColourTextTestRunner`.
* `unittest.TextTestResult`, use `colour_runner.result.ColourTextTestResult`.

### Configure colours

You can change default colours like this :

    from colour_runner.result import ColourTextTestResult
    ColourTextTestResult.colour_defaults.update({"test_title": "cyan",
                                                 "test_name": "bold_magenta"})
    test_runner = unittest.runner.TextTestRunner(verbosity=verbosity, resultclass=ColourTextTestResult)

You can use any colour in this list: black, red, green, yellow, blue, magenta, cyan, white  
And you can change the colour of these variables: 
 - "default": the colour of the text,
 - "error": for errors,
 - "success": for success,
 - "fail": for fails,
 - "skip": for skips,
 - "expected": for expected failures,
 - "unexpected": for unexpected failures,
 - "test_title": for the test class name,
 - "test_name": for the test name
