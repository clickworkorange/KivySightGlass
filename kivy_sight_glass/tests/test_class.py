#!/usr/bin/env python3

import pytest

class TestClass:
  def test_import(self):
    from kivy_sight_glass import SightGlass
    sg = SightGlass()
    assert hasattr(sg, "level")