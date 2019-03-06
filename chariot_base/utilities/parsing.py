# -*- coding: utf-8 -*-
"""
Parsing string utilities
"""

def try_parse(serialized_num):
        try:
            return int(serialized_num)
        except:
            try: 
                return float(serialized_num)
            except:
                return serialized_num
