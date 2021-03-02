import time
import logging
import datetime
import numbers


def format_line(extra):
    outarr = []
    for k, v in extra.items():
        if v is None:
            outarr.append("%s=" % k)
            continue

        if isinstance(v, bool):
            v = "true" if v else "false"
        elif isinstance(v, numbers.Number):
            pass
        else:
            if isinstance(v, (dict, object)):
                v = str(v)
            v = '"%s"' % v.replace('"', '\\"')
        outarr.append("%s=%s" % (k, v))
    return " ".join(outarr)


class LogfmtFormatter(logging.Formatter):
    def format(self, record):
        record.asctime = self.formatTime(record)
        log_format_msg = [
            'time=%s' % record.asctime,
            'level=%s' % record.levelname,
            'location=%s:%s:%s'
            % (record.filename, record.lineno, record.funcName),
            'msg="%s"' % record.getMessage().replace('"', '\\"'),
            format_line(getattr(record, "context", {})),
        ]
        if record.exc_info:
            log_format_msg += [
                'exception="%s"'
                % self.formatException(record.exc_info).replace('"', '\\"'),
            ]
        if record.stack_info:
            log_format_msg += [
                'stack="%s"' % self.formatStack(
                    record.stack_info).replace('"', '\\"'),
            ]
        return " ".join(log_format_msg)

    def formatTime(self, record):
        """
        Return the creation time of the specified LogRecord as formatted text.

        This method should be called from format() by a formatter which
        wants to make use of a formatted time.

        It provides an ISO 8601 format with milliseconds.
        """
        ct = self.converter(record.created)
        ct_with_ms = time.mktime(ct) + (record.msecs / 1000)
        ct_full = datetime.datetime.fromtimestamp(ct_with_ms)
        return ct_full.isoformat()


def getLogger(name, level=logging.INFO):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding an new handler if there is already one
    if len(logger.handlers) == 0:
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # create formatter
        formatter = LogfmtFormatter()
        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)
    return logger
