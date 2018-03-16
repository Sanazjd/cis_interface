import nose.tools as nt
from cis_interface.tests import CisTestClassInfo
from cis_interface import backwards, tools, serialize


class TestDefaultSerialize(CisTestClassInfo):
    r"""Test class for DefaultSerialize class."""

    def __init__(self, *args, **kwargs):
        super(TestDefaultSerialize, self).__init__(*args, **kwargs)
        self._cls = 'DefaultSerialize'
        self._empty_msg = backwards.unicode2bytes('')
        self._empty_obj = backwards.unicode2bytes('')
        self._header_info = dict(arg1='1', arg2='two')
        self._objects = self.file_lines

    @property
    def mod(self):
        r"""Module for class to be tested."""
        return 'cis_interface.serialize.%s' % self.cls

    def empty_head(self, msg):
        r"""dict: Empty header for message only contains the size."""
        out = dict(size=len(msg))
        if msg == tools.CIS_MSG_EOF:
            out['eof'] = True
        return out

    def assert_result_equal(self, x, y):
        r"""Assert that serialized/deserialized objects equal."""
        nt.assert_equal(x, y)

    def test_serialize(self):
        r"""Test serialize/deserialize."""
        for iobj in self._objects:
            msg = self.instance.serialize(iobj)
            iout, ihead = self.instance.deserialize(msg)
            self.assert_result_equal(iout, iobj)
            nt.assert_equal(ihead, self.empty_head(msg))
        
    def test_serialize_sinfo(self):
        r"""Test serialize/deserialize with serializer info."""
        hout = self._header_info
        hout.update(**self.instance.serializer_info)
        temp_seri = serialize.DefaultSerialize.DefaultSerialize()
        for iobj in self._objects:
            msg = self.instance.serialize(iobj, header_kwargs=self._header_info,
                                          add_serializer_info=True)
            iout, ihead = self.instance.deserialize(msg)
            self.assert_result_equal(iout, iobj)
            nt.assert_equal(ihead, hout)
            # Use info to reconstruct serializer
            iout, ihead = temp_seri.deserialize(msg)
            nt.assert_equal(ihead, hout)
            new_seri = serialize.get_serializer(**ihead)
            iout, ihead = new_seri.deserialize(msg)
            self.assert_result_equal(iout, iobj)
            nt.assert_equal(ihead, hout)
        
    def test_serialize_header(self):
        r"""Test serialize/deserialize with header."""
        for iobj in self._objects:
            msg = self.instance.serialize(iobj, header_kwargs=self._header_info)
            iout, ihead = self.instance.deserialize(msg)
            self.assert_result_equal(iout, iobj)
            nt.assert_equal(ihead, self._header_info)
        
    def test_serialize_eof(self):
        r"""Test serialize/deserialize EOF."""
        iobj = tools.CIS_MSG_EOF
        msg = self.instance.serialize(iobj)
        iout, ihead = self.instance.deserialize(msg)
        nt.assert_equal(iout, iobj)
        nt.assert_equal(ihead, self.empty_head(msg))
        
    def test_serialize_eof_header(self):
        r"""Test serialize/deserialize EOF with header."""
        iobj = tools.CIS_MSG_EOF
        msg = self.instance.serialize(iobj, header_kwargs=self._header_info)
        iout, ihead = self.instance.deserialize(msg)
        nt.assert_equal(iout, iobj)
        nt.assert_equal(ihead, self.empty_head(msg))
        
    def test_serialize_no_format(self):
        r"""Test serialize/deserialize without format string."""
        if (len(self._inst_kwargs) == 0) and (self._cls == 'DefaultSerialize'):
            for iobj in self._objects:
                msg = self.instance.serialize([iobj], header_kwargs=self._header_info)
                iout, ihead = self.instance.deserialize(msg)
                self.assert_result_equal(iout, iobj)
                nt.assert_equal(ihead, self._header_info)
            nt.assert_raises(Exception, self.instance.serialize, ['msg', 0])
        
    def test_deserialize_empty(self):
        r"""Test call for empty string."""
        out, head = self.instance.deserialize(self._empty_msg)
        nt.assert_equal(out, self._empty_obj)
        nt.assert_equal(head, self.empty_head(self._empty_msg))


class TestDefaultSerialize_format(TestDefaultSerialize):
    r"""Test class for DefaultSerialize class with format."""

    def __init__(self, *args, **kwargs):
        super(TestDefaultSerialize_format, self).__init__(*args, **kwargs)
        self._inst_kwargs = {'format_str': self.fmt_str}
        self._empty_obj = tuple()
        self._objects = self.file_rows


class TestDefaultSerialize_func(TestDefaultSerialize):
    r"""Test class for DefaultSerialize class with functions."""

    def __init__(self, *args, **kwargs):
        super(TestDefaultSerialize_func, self).__init__(*args, **kwargs)
        self._inst_kwargs = {'func_serialize': self.func_serialize,
                             'func_deserialize': self.func_deserialize}
        self._objects = self.file_rows

    def func_serialize(self, args):
        r"""Method that serializes using repr."""
        return backwards.unicode2bytes(repr(args))

    def func_deserialize(self, args):
        r"""Method that deserializes using eval."""
        if len(args) == 0:
            return self._empty_obj
        x = eval(backwards.bytes2unicode(args))
        return x

    def test_serialize_sinfo(self):
        r"""Disabled: Test serialize/deserialize with serializer info."""
        pass


class TestDefaultSerialize_func_error(TestDefaultSerialize_func):
    r"""Test class for DefaultSerialize class with incorrect functions."""

    def func_serialize(self, args):
        r"""Method that serializes using repr."""
        return args

    def func_deserialize(self, args):
        r"""Method that deserializes using eval."""
        if len(args) == 0:
            return self._empty_obj
        x = eval(backwards.bytes2unicode(args))
        return x

    def test_serialize(self):
        r"""Test serialize with function that dosn't return correct type."""
        nt.assert_raises(TypeError, self.instance.serialize, (1,))

    def test_serialize_header(self):
        r"""Disabled: Test serialize/deserialize with header."""
        pass

    def test_serialize_sinfo(self):
        r"""Disabled: Test serialize/deserialize with serializer info."""
        pass
