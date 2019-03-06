# -*- coding: utf-8 -*-
"""
Parsing string utilities
"""

import re


def try_parse(serialized_num):
        try:
            return int(serialized_num)
        except:
            try: 
                return float(serialized_num)
            except:
                return serialized_num


def normalize_mac_address(mac_address):
    regex = r"[:_-]"
    subst = ""
    return re.sub(regex, subst, mac_address, 0)