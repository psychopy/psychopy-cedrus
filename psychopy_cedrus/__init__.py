#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Originally from the PsychoPy library
# Copyright (C) 2002-2018 Jonathan Peirce (C) 2019-2022 Open Science Tools Ltd.
# Distributed under the terms of the GNU General Public License (GPL).

import importlib.metadata

try:
    __version__ = importlib.metadata.version("psychopy-cedrus")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.dev"

from .cedrus import RB730
