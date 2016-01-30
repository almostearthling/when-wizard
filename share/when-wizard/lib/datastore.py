# file: share/when-wizard/lib/datastore.py
# -*- coding: utf-8 -*-
#
# A very simplistic CLOB and pickle based datastore implementation
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import pickle


class PicklingDatastore(object):

    def __init__(self):
        self._data = {}
        self.filename = None

    def __iter__(self):
        for k in self._data:
            yield k

    def save(self):
        if self.filename is not None:
            with open(self.filename, 'wb') as f:
                pickle.dump(self._data, f)

    def load(self):
        if self.filename is not None:
            with open(self.filename, 'rb') as f:
                self._data = pickle.load(f)

    def get(self, unique_id):
        if not self._data:
            self.load()
        if unique_id in self._data:
            return self._data[unique_id]
        else:
            return None

    def put(self, unique_id, value):
        self._data[unique_id] = value
        self.save()

    def remove(self, unique_id):
        del self._data[unique_id]
        self.save()


# end.
