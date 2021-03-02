import logging

from logfmt_logger import getLogger


def test_log_with_context(capsys):
    logger = getLogger("TEST1")

    logger.error(
        "log context",
        extra={"context": {"test": 'this is "with double quote" a context'}},
    )
    captured = capsys.readouterr()
    assert 'test="this is \\"with double quote\\" a context"' in captured.err


def test_log_level(capsys):
    logger = getLogger("TEST2")

    logger.info("info message")
    captured = capsys.readouterr()
    assert 'level=INFO' in captured.err
    logger.warning("warn message")
    captured = capsys.readouterr()
    assert 'level=WARNING' in captured.err
    logger.error("error message")
    captured = capsys.readouterr()
    assert 'level=ERROR' in captured.err
    logger.critical("critical message")
    captured = capsys.readouterr()
    assert 'level=CRITICAL' in captured.err


def test_log_with_execeptions(capsys):
    logger = getLogger("TEST3")

    try:
        raise ValueError('Exception message with "double quotes"')
    except ValueError:
        logger.info("exception", exc_info=True)
    captured = capsys.readouterr()
    assert (
        'ValueError: Exception message with \\"double quotes\\"' in captured.err
    )


def test_log_level_avoid_debug_when_in_info(capsys):
    logger = getLogger("TEST4", level=logging.WARN)

    logger.info("info message")
    captured = capsys.readouterr()
    assert 'level=INFO' not in captured.err

    logger.error("error message")
    captured = capsys.readouterr()
    assert 'level=ERROR' in captured.err
