#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import sys
import os
import glob

test_root = os.path.dirname(os.path.abspath(__file__))
test_files = glob.glob(os.path.join(test_root, 'test_*.py'))

os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)
test_names = [os.path.basename(name)[:-3] for name in test_files]

suite = unittest.defaultTestLoader.loadTestsFromNames(test_names)


def run():
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit((result.errors or result.failures) and 1 or 0)

if __name__ == '__main__':
    run()
