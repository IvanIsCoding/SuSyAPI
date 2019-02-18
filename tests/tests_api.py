import unittest
import datetime

try:
    import susyapi
except ModuleNotFoundError:
    import sys
    sys.path.append("..")
    import susyapi


class TestArguments(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
