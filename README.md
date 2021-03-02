# Logfmt Logger for Python

An opinionated logging Formatter following the Logfmt format with sane
defaults.

It is production ready, fully tested, and based on the standard Python
[logging library](https://docs.python.org/3/library/logging.html).

This is base on the work of https://github.com/wlonk/logfmt-python

## Usage

```python
from logfmt_logger import getLogger

logger = getLogger("my_app")


def run():
    logger.info('Service "my_app" is running!')


if __name__ == "__main__":
    run()
```
Running `python test.py` will output this to stderr:
```
time=2021-03-02T17:11:04.632448 level=INFO location=test.py:7:run msg="Service is running!"
```

Some details about the log content:
- The time is in ISO 8601 format with milliseconds (from datetime.isoFormat)
- The level is always in uppercase letter
- the location is formated as "<filename>:<line number>:<function name>"
- double quotes in strings are escaped

## Setting logging level

You can set the logging level using the `level` option of getLogger using the
standard `logging` levels, for example:
```python
import logging
from logfmt_logger import getLogger

logger = getLogger("my_app", logging.ERROR)
logger.info("This won't appear...")
logger.error("This will appear!")
```

## Log exceptions
Exception can be logged with `exc_info=True`:

```python
from logfmt_logger import getLogger

logger = getLogger("my_app")

try:
    raise ValueError('Exception message with "double quotes"')
except ValueError:
    logger.info("exception", exc_info=True)
```

Result log line is:
```
time=2021-03-02T17:24:55.424014 level=INFO location=test.py:8:<module> msg="exception"  exception="Traceback (most recent call last):
  File \"test.py\", line 6, in <module>
    raise ValueError('Exception message with \"double quotes\"')
ValueError: Exception message with \"double quotes\""
```

## Add more context

If you need to include extra data to the log line use the `extra` option with a
`context` entry containing your custom key values:

```python
from logfmt_logger import getLogger

logger = getLogger("my_app")

logger.error(
    "log context",
    extra={"context": {"test": 'this is a "with double quote" context'}},
)
```
Will result in:
```
time=2021-03-02T17:33:17.567084 level=ERROR location=test.py:5:<module> msg="log context" test="this is a \"with double quote\" context"
```

# Contributing

The package use [Poetry](https://python-poetry.org/) for its packaging.
You can enter a development shell by running:
```sh
poetry install
poetry shell
```

The code is checked and tested with:
```
poetry install
poetry shell
./lint.sh # Use -f for autoformat
./test.sh
```
