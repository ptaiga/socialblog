import unittest
from cipher import Caesar, Rot13, Vigenere


class TestCipherMixin:
    text = 'the quick brown fox jumps over the lazy dog'

    def encode(self, text):
        raise NotImplementedError

    def decode(self, code):
        raise NotImplementedError

    def test_encode(self):
        code = self.encode(self.text)
        self.assertNotEqual(code, self.text)  # The encoded text is different from the original one
        self.assertEqual(len(code), len(self.text))  # The length of the encoded and source text is the same

    def test_decode(self):
        decoded = self.decode(self.encode(self.text))
        self.assertEqual(decoded, self.text)  # The decoded cipher matches the original text


class TestCaesar(TestCipherMixin, unittest.TestCase):
    def encode(self, text):
        return Caesar.encode(text, 5)

    def decode(self, code):
        return Caesar.decode(code, 5)


class TestRot13(TestCipherMixin, unittest.TestCase):
    def encode(self, text):
        return Rot13.encode(text)

    def decode(self, code):
        return Rot13.decode(code)


class TestVigenere(TestCipherMixin, unittest.TestCase):
    text = 'the five boxing wizards jump quickly'
    key = 'helloworld'

    def encode(self, text):
        return Vigenere.encode(text, self.key)

    def decode(self, code):
        return Vigenere.decode(code, self.key)


if __name__ == '__main__':
    unittest.main()
