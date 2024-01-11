#!/usr/bin/env python3
"""obfuscate log messages"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, seperator: str) -> str:
    """returns the log message obfuscated"""
    for f in fields:
        message = re.sub(f'{f}=.*?{seperator}',
                         f'{f}={redaction}{seperator}', message)
    return message
