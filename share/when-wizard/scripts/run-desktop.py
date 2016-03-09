#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# When Wizard
#
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)
# Desktop file launcher script
# see: http://askubuntu.com/a/239883/466738 for the source


import sys
from gi.repository import Gio


def main():
    launcher = Gio.DesktopAppInfo.new_from_filename(sys.argv[1])
    launcher.launch()


if __name__ == '__main__':
    main()


# end.
