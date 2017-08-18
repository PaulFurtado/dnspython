# Copyright (C) 2003-2017 Nominum, Inc.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose with or without fee is hereby granted,
# provided that the above copyright notice and this permission notice
# appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND NOMINUM DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL NOMINUM BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

class Set(object):

    """A simple set class.

    This class was originally used to deal with sets being missing in
    ancient versions of python, but dnspython will continue to use it
    as these sets are based on lists and are thus indexable, and this
    ability is widely used in dnspython applications.
    """

    __slots__ = ['items', 'map']

    def __init__(self, items=None):
        """Initialize the set.

        *items*, an iterable or ``None``, the initial set of items.
        """
        self.items = []
        self.map = {}
        if items is not None:
            for item in items:
                self.add(item)

    def __repr__(self):
        return "dns.simpleset.Set(%s)" % repr(self.items)

    def add(self, item):
        """Add an item to the set.
        """
        if item not in self.map:
            self.map[item] = len(self.items)
            self.items.append(item)

    def __contains__(self, item):
        return item in self.map

    def remove(self, item):
        """Remove an item from the set.
        """
        if item in self.map:
            i = self.map[item]
            del self.items[i]
            del self.map[item]
            for k, v in self.map.items():
                if v >= i:
                    self.map[k] = v - 1

    def discard(self, item):
        """Remove an item from the set if present.
        """
        self.remove(item)

    def _clone(self):
        """Make a (shallow) copy of the set.

        There is a 'clone protocol' that subclasses of this class
        should use.  To make a copy, first call your super's _clone()
        method, and use the object returned as the new instance.  Then
        make shallow copies of the attributes defined in the subclass.

        This protocol allows us to write the set algorithms that
        return new instances (e.g. union) once, and keep using them in
        subclasses.
        """
        cls = self.__class__
        obj = cls.__new__(cls)
        obj.items = list(self.items)
        obj.map = dict(self.map)
        return obj

    def __copy__(self):
        """Make a (shallow) copy of the set.
        """

        return self._clone()

    def copy(self):
        """Make a (shallow) copy of the set.
        """

        return self._clone()

    def union_update(self, other):
        """Update the set, adding any elements from other which are not
        already in the set.
        """

        if not isinstance(other, Set):
            raise ValueError('other must be a Set instance')
        if self is other:
            return
        for item in other:
            self.add(item)

    def intersection_update(self, other):
        """Update the set, removing any elements from other which are not
        in both sets.
        """

        if not isinstance(other, Set):
            raise ValueError('other must be a Set instance')
        if self is other:
            return
        # we make a copy of the list so that we can remove items from
        # the list without breaking the iterator.
        for item in list(self.items):
            if item not in other:
                self.remove(item)

    def difference_update(self, other):
        """Update the set, removing any elements from other which are in
        the set.
        """

        if not isinstance(other, Set):
            raise ValueError('other must be a Set instance')
        if self is other:
            self.clear()
        else:
            for item in other:
                self.discard(item)

    def union(self, other):
        """Return a new set which is the union of ``self`` and ``other``.

        Returns the same Set type as this set.
        """

        obj = self._clone()
        obj.union_update(other)
        return obj

    def intersection(self, other):
        """Return a new set which is the intersection of ``self`` and
        ``other``.

        Returns the same Set type as this set.
        """

        obj = self._clone()
        obj.intersection_update(other)
        return obj

    def difference(self, other):
        """Return a new set which ``self`` - ``other``, i.e. the items
        in ``self`` which are not also in ``other``.

        Returns the same Set type as this set.
        """

        obj = self._clone()
        obj.difference_update(other)
        return obj

    def __or__(self, other):
        return self.union(other)

    def __and__(self, other):
        return self.intersection(other)

    def __add__(self, other):
        return self.union(other)

    def __sub__(self, other):
        return self.difference(other)

    def __ior__(self, other):
        self.union_update(other)
        return self

    def __iand__(self, other):
        self.intersection_update(other)
        return self

    def __iadd__(self, other):
        self.union_update(other)
        return self

    def __isub__(self, other):
        self.difference_update(other)
        return self

    def update(self, other):
        """Update the set, adding any elements from other which are not
        already in the set.

        *other*, the collection of items with which to update the set, which
        may be any iterable type.
        """

        for item in other:
            self.add(item)

    def clear(self):
        """Make the set empty."""
        self.items = []
        self.map = {}

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for item in self:
            if item not in other:
                return False
        for item in other:
            if item not in self:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, i):
        return self.items[i]

    def __delitem__(self, i):
        if isinstance(i, int):
            items = [self[i]]
        else:
            items = self[i]
        for item in items:
            self.remove(item)

    def issubset(self, other):
        """Is this set a subset of *other*?

        Returns a ``bool``.
        """

        if not isinstance(other, Set):
            raise ValueError('other must be a Set instance')
        for item in self:
            if item not in other:
                return False
        return True

    def issuperset(self, other):
        """Is this set a superset of *other*?

        Returns a ``bool``.
        """

        if not isinstance(other, Set):
            raise ValueError('other must be a Set instance')
        for item in other:
            if item not in self:
                return False
        return True
