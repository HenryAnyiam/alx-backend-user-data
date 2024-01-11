#!/usr/bin/env python3
"""obfuscate log messages"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, seperator: str) -> str:
    """
     Returns the log message obfuscated
     Arguments:
     fields: a list of strings
             representing all fields to obfuscate
     redaction: a string representing by what
                the field will be obfuscated
     message: a string representing the log line
     separator: a string representing by which character is
                separating all fields in the log line (message)
    """
    for i in fields:
        message = re.sub(re.compile(fr"(?<={i}=)(\w|\d|/)+{seperator}"),
                         redaction + seperator, message)
    return message
