from __future__ import absolute_import, unicode_literals

import unittest

import mock

from mopidy.internal import encoding


@mock.patch('mopidy.internal.encoding.locale.getpreferredencoding')
class LocaleDecodeTest(unittest.TestCase):

    def test_can_decode_utf8_strings_with_french_content(self, mock):
        mock.return_value = 'UTF-8'

        result = encoding.locale_decode(
            b'[Errno 98] Adresse d\xc3\xa9j\xc3\xa0 utilis\xc3\xa9e')
        expected = '[Errno 98] Adresse d\xe9j\xe0 utilis\xe9e'

        self.assertEqual(expected, result)

    def test_can_decode_an_ioerror_with_french_content(self, mock):
        mock.return_value = 'UTF-8'

        error = IOError(98, b'Adresse d\xc3\xa9j\xc3\xa0 utilis\xc3\xa9e')
        result = encoding.locale_decode(error)

        expected = [
            '[Errno 98] Adresse d\xe9j\xe0 utilis\xe9e',  # Py2
            r"[Errno 98] b'Adresse d\xc3\xa9j\xc3\xa0 utilis\xc3\xa9e'",  # Py3
        ]

        self.assertIn(result, expected)

    def test_does_not_use_locale_to_decode_unicode_strings(self, mock):
        mock.return_value = 'UTF-8'

        encoding.locale_decode('abc')

        self.assertFalse(mock.called)

    def test_does_not_use_locale_to_decode_ascii_bytestrings(self, mock):
        mock.return_value = 'UTF-8'

        encoding.locale_decode(b'abc')

        self.assertFalse(mock.called)

    def test_replaces_unknown_bytes_instead_of_crashing(self, mock):
        mock.return_value = 'US-ASCII'

        result = encoding.locale_decode(b'abc\xc3def')

        assert result == 'abc\ufffddef'
