# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 Taneli Hukkinen
# Licensed to PSF under a Contributor Agreement.

__all__ = ("toml_tools",)

import os

# By changing this one line, we can run the tests against
# a different module name.
import toml_tools as toml_tools

def stem(file_path):
    #type(str) -> str
    return os.path.splitext(os.path.basename(file_path))[0]