from typing import List, Tuple


UNICODE_ASCII_CHARACTER_SET = ('abcdefghijklmnopqrstuvwxyz'
                               'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                               '0123456789')


def generate_token(length: int=30, chars: str=UNICODE_ASCII_CHARACTER_SET) -> str: ...


# vim: filetype=python :
