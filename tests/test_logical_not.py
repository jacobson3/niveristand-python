import sys

from niveristand import decorators, RealTimeSequence
from niveristand import realtimesequencetools
from niveristand.clientapi.datatypes import BooleanValue, DoubleValue, I32Value, I64Value
from niveristand.exceptions import TranslateError, VeristandError
import pytest
from testutilities import rtseqrunner, validation

a = 1
b = 2


@decorators.nivs_rt_sequence
def return_true():
    a = BooleanValue(True)
    return a.value


@decorators.nivs_rt_sequence
def logical_not_simple_numbers():
    a = BooleanValue(0)
    a.value = not 2
    return a.value


@decorators.nivs_rt_sequence
def logical_not_simple_numbers1():
    a = BooleanValue(0)
    a.value = not 0
    return a.value


@decorators.nivs_rt_sequence
def logical_not_nivsdatatype_double():
    a = BooleanValue(0)
    a.value = not DoubleValue(3)
    return a.value


@decorators.nivs_rt_sequence
def logical_not_nivsdatatype_double1():
    a = BooleanValue(0)
    a.value = not DoubleValue(0)
    return a.value


@decorators.nivs_rt_sequence
def logical_not_nivsdatatype_int32():
    a = BooleanValue(0)
    a.value = not I32Value(0)
    return a.value


@decorators.nivs_rt_sequence
def logical_not_nivsdatatype_int64():
    a = BooleanValue(0)
    a.value = not I64Value(0)
    return a.value


@decorators.nivs_rt_sequence
def logical_not_bool():
    a = BooleanValue(True)
    a.value = not True
    return a.value


@decorators.nivs_rt_sequence
def logical_not_bool1():
    a = BooleanValue(False)
    a.value = not False
    return a.value


@decorators.nivs_rt_sequence
def logical_not_variables():
    a = BooleanValue(False)
    b = BooleanValue(False)
    a.value = not b.value
    return a.value


@decorators.nivs_rt_sequence
def logical_not_rtseq():
    a = BooleanValue(True)
    a.value = not return_true()
    return a.value


@decorators.nivs_rt_sequence
def logical_not_parantheses():
    a = BooleanValue(True)
    a.value = not (True and (DoubleValue(2) and I32Value(3)) and False)
    return a.value


@decorators.nivs_rt_sequence
def logical_not_unary():
    a = BooleanValue(True)
    a.value = not -1
    return a.value


@decorators.nivs_rt_sequence
def logical_not_sequence():
    a = BooleanValue(False)
    a.value = not not not False
    return a.value


# region invalid tests
@decorators.nivs_rt_sequence
def logical_not_invalid_variables():
    return not a.value


@decorators.nivs_rt_sequence
def logical_not_None():
    a = BooleanValue(False)
    a.value = not None
    return a.value


@decorators.nivs_rt_sequence
def logical_not_invalid_rtseq_call():
    a = BooleanValue(False)
    a.value = not return_true
    return a.value

# endregion


run_tests = [
    (return_true, (), True),
    (logical_not_simple_numbers, (), False),
    (logical_not_simple_numbers1, (), True),
    (logical_not_bool, (), False),
    (logical_not_bool1, (), True),
    (logical_not_variables, (), True),
    (logical_not_parantheses, (), True),
    (logical_not_sequence, (), True),
    (logical_not_unary, (), False),
    (logical_not_sequence, (), True),
    (logical_not_rtseq, (), False),
]

skip_tests = [
    (logical_not_None, (), "Name transformer doesn't raise an exception for NoneType with python 2.7."),
    (logical_not_invalid_rtseq_call, (), "RTSeq call not implemented yet."),
    (logical_not_nivsdatatype_double, (), "Not of a constant DataType returns a DataType object, we have to"
                                          "research this how to solve it. A solution is to always use variables in"
                                          "logical operators, and use var.value."),
    (logical_not_nivsdatatype_double1, (), "Not of a constant DataType returns a DataType object, we have to"
                                           "research this how to solve it. A solution is to always use variables in"
                                           "logical operators, and use var.value."),
    (logical_not_nivsdatatype_int32, (), "Not of a constant DataType returns a DataType object, we have to"
                                         "research this how to solve it. A solution is to always use variables in"
                                         "logical operators, and use var.value."),
    (logical_not_nivsdatatype_int64, (), "Not of a constant DataType returns a DataType object, we have to"
                                         "research this how to solve it. A solution is to always use variables in"
                                         "logical operators, and use var.value."),
]

fail_transform_tests = [
    (logical_not_invalid_variables, (), TranslateError),
]


def idfunc(val):
    return val.__name__


@pytest.mark.parametrize("func_name, params, expected_result", run_tests, ids=idfunc)
def test_transform(func_name, params, expected_result):
    RealTimeSequence(func_name)


@pytest.mark.parametrize("func_name, params, expected_result", run_tests, ids=idfunc)
def test_runpy(func_name, params, expected_result):
    actual = func_name(*params)
    assert actual == expected_result


@pytest.mark.parametrize("func_name, params, expected_result", run_tests, ids=idfunc)
def test_run_py_as_rts(func_name, params, expected_result):
    actual = realtimesequencetools.run_py_as_rtseq(func_name)
    assert actual == expected_result


@pytest.mark.parametrize("func_name, params, expected_result", run_tests, ids=idfunc)
def test_run_in_VM(func_name, params, expected_result):
    actual = rtseqrunner.run_rtseq_in_VM(func_name)
    assert actual == expected_result


@pytest.mark.parametrize("func_name, params, expected_result", fail_transform_tests, ids=idfunc)
def test_failures(func_name, params, expected_result):
    try:
        RealTimeSequence(func_name)
    except expected_result:
        pass
    except VeristandError as e:
        pytest.fail('Unexpected exception raised:' +
                    str(e.__class__) + ' while expected was: ' + expected_result.__name__)
    except Exception as exception:
        pytest.fail('ExpectedException not raised: ' + exception)


@pytest.mark.parametrize("func_name, params, reason", skip_tests, ids=idfunc)
def test_skipped(func_name, params, reason):
    pytest.skip(func_name.__name__ + ": " + reason)


def test_check_all_tested():
    validation.test_validate(sys.modules[__name__])
