#!/usr/bin/env python

from tempfile import mkdtemp

HELPER_SETTINGS = dict(
    ROOT_URLCONF="tests.example_app.urls",
    INSTALLED_APPS=["meta", "tests.example_app"],
    FILE_UPLOAD_TEMP_DIR=mkdtemp(),
    TEST_RUNNER="app_helper.pytest_runner.PytestTestRunner",
    SECRET_KEY="dont-use-me",
)

try:
    import sekizai  # NOQA

    HELPER_SETTINGS["INSTALLED_APPS"].append("sekizai")
    HELPER_SETTINGS["TEMPLATE_CONTEXT_PROCESSORS"] = [
        "sekizai.context_processors.sekizai",
    ]
except ImportError:
    pass


def run():
    from app_helper import runner

    runner.run("meta")


def setup():
    import sys

    from app_helper import runner

    runner.setup("meta", sys.modules[__name__])


if __name__ == "__main__":
    run()


if __name__ == "cms_helper":
    setup()
