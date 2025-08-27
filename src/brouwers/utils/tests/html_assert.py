# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2022 Dimpact
"""
HTML assertion utilities.

Taken from https://github.com/open-formulieren/open-forms.git
"""

from lxml_html_clean import Cleaner


def strip_all_attributes(document: str):
    """
    Reduce an HTML document to just the tags, stripping any attributes.

    Useful for testing with self.assertInHTML without having to worry about class
    names, style tags etc.

    Taken and adapted from https://stackoverflow.com/a/7472003
    """
    cleaner = Cleaner(safe_attrs_only=True, safe_attrs=frozenset())
    return str(cleaner.clean_html(document))
