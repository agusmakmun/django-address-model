# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ast
import json


def parse_json_string(text, default={}):
    """
    function to parse the json string
    into json parse or dict

    :param `text` is the value of text model to parse.
    :paran `default` is default output, eg: {}, []
    :return json loads or dict.
    """
    output = default

    if not text:
        return default

    if isinstance(text, list) or isinstance(text, dict):
        return text

    try:
        output = json.loads(text)
    except json.decoder.JSONDecodeError:
        try:
            output = ast.literal_eval(text)
        except Exception:
            # invalid format
            pass

    if type(default) == type(output):
        return output

    return default
