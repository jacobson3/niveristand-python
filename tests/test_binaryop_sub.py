import sys

from niveristand import decorators, RealTimeSequence
from niveristand import realtimesequencetools
from niveristand.clientapi.datatypes import ChannelReference, DoubleValue, I32Value
from niveristand.exceptions import TranslateError, VeristandError
from niveristand.library.primitives import localhost_wait
import pytest
from testutilities import rtseqrunner, validation

a = 1
b = 2


@decorators.nivs_rt_sequence
def return_constant():
    a = DoubleValue(5)
    return a.value


@decorators.nivs_rt_sequence
def sub_simple_numbers():
    a = DoubleValue(0)
    a.value = 1 - 2
    return a.value


def test_sub_simple_numbers():
    RealTimeSequence(sub_simple_numbers)


@decorators.nivs_rt_sequence
def sub_num_nivsdatatype():
    a = DoubleValue(0)
    a.value = 1 - DoubleValue(2)
    return a.value


@decorators.nivs_rt_sequence
def sub_nivsdatatype_nivsdatatype():
    a = DoubleValue(0)
    a.value = DoubleValue(1) - DoubleValue(2)
    return a.value


@decorators.nivs_rt_sequence
def sub_nivsdatatype_nivsdatatype1():
    a = DoubleValue(0)
    a.value = DoubleValue(1) - I32Value(2)
    return a.value


@decorators.nivs_rt_sequence
def sub_nivsdatatype_nivsdatatype2():
    a = DoubleValue(0)
    a.value = I32Value(1) - DoubleValue(2)
    return a.value


@decorators.nivs_rt_sequence
def sub_nivsdatatype_nivsdatatype3():
    a = DoubleValue(0)
    a.value = I32Value(1) - I32Value(2)
    return a.value


@decorators.nivs_rt_sequence
def sub_multiple_types():
    a = DoubleValue(0)
    a.value = 1 - DoubleValue(2) - 3.0
    return a.value


@decorators.nivs_rt_sequence
def sub_multiple_types1():
    a = I32Value(0)
    a.value = 1 - I32Value(2) - 3.0 - DoubleValue(4)
    return a.value


@decorators.nivs_rt_sequence
def sub_use_rtseq():
    a = DoubleValue(0)
    a.value = 1 - return_constant()
    return a.value


@decorators.nivs_rt_sequence
def sub_use_rtseq1():
    a = DoubleValue(0)
    a.value = return_constant() - 1
    return a.value


@decorators.nivs_rt_sequence
def sub_use_rtseq2():
    a = DoubleValue(0)
    a.value = DoubleValue(1) - return_constant()
    return a.value


@decorators.nivs_rt_sequence
def sub_use_rtseq3():
    a = DoubleValue(0)
    a.value = return_constant() - DoubleValue(1)
    return a.value


@decorators.nivs_rt_sequence
def sub_use_rtseq4():
    a = DoubleValue(0)
    a.value = I32Value(1) - return_constant()
    return a.value


@decorators.nivs_rt_sequence
def sub_use_rtseq5():
    a = DoubleValue(0)
    a.value = return_constant() - I32Value(1)
    return a.value


@decorators.nivs_rt_sequence
def sub_with_parantheses():
    a = DoubleValue(0)
    a.value = 1 - (2 - 3)
    return a.value


@decorators.nivs_rt_sequence
def sub_with_parantheses1():
    a = DoubleValue(0)
    a.value = 1 - (DoubleValue(2) - I32Value(5))
    return a.value


@decorators.nivs_rt_sequence
def sub_with_parantheses2():
    a = DoubleValue(0)
    a.value = DoubleValue(5) - (I32Value(2) - 3.0) - DoubleValue(4)
    return a.value


@decorators.nivs_rt_sequence
def sub_variables():
    a = DoubleValue(5)
    b = DoubleValue(0)
    b.value = 1 - a
    return b.value


@decorators.nivs_rt_sequence
def sub_variables1():
    a = DoubleValue(5)
    b = DoubleValue(0)
    b.value = 1 - a.value
    return b.value


@decorators.nivs_rt_sequence
def sub_variable_variable():
    a = DoubleValue(1)
    b = DoubleValue(2)
    c = DoubleValue(0)
    c.value = a.value - b.value
    return c.value


@decorators.nivs_rt_sequence
def sub_variable_variable1():
    a = DoubleValue(1)
    b = DoubleValue(2)
    c = DoubleValue(0)
    c.value = a.value - b.value
    return c.value


@decorators.nivs_rt_sequence
def sub_variable_rtseq():
    a = DoubleValue(1)
    b = DoubleValue(0)
    b.value = a.value - return_constant()
    return b.value


@decorators.nivs_rt_sequence
def sub_variable_rtseq1():
    a = DoubleValue(1)
    b = DoubleValue(0)
    b.value = return_constant() - a.value
    return b.value


@decorators.nivs_rt_sequence
def sub_to_channelref():
    a = DoubleValue(0)
    b = ChannelReference("Aliases/DesiredRPM")
    b.value = 5.0
    localhost_wait()
    a.value = 1 - b.value
    return a.value


@decorators.nivs_rt_sequence
def sub_binary_unary():
    a = DoubleValue(0)
    a.value = 2 - -1
    return a.value


@decorators.nivs_rt_sequence
def sub_binary_unary_sequence():
    a = DoubleValue(0)
    a.value = 1 - -----2  # noqa: E225 it's ok to test this
    return a.value


@decorators.nivs_rt_sequence
def sub_complex_expr():
    a = DoubleValue(0)
    a.value = 1 - (2 if 2 < 3 else 4)
    return a.value


# region augassign tests

@decorators.nivs_rt_sequence
def aug_sub_simple_numbers():
    a = DoubleValue(1)
    a.value -= 2
    return a.value


@decorators.nivs_rt_sequence
def aug_sub_num_nivsdatatype():
    a = DoubleValue(1)
    a.value -= DoubleValue(2)
    return a.value


@decorators.nivs_rt_sequence
def aug_sub_use_rtseq():
    a = DoubleValue(1)
    a.value -= return_constant()
    return a.value


@decorators.nivs_rt_sequence
def aug_sub_with_parantheses():
    a = DoubleValue(1)
    a.value -= (I32Value(2) + 3.0) + DoubleValue(4)
    return a.value


@decorators.nivs_rt_sequence
def aug_sub_variables():
    a = DoubleValue(5)
    b = DoubleValue(1)
    b.value -= a.value
    return b.value


@decorators.nivs_rt_sequence
def aug_sub_to_channelref():
    a = DoubleValue(1)
    b = ChannelReference("Aliases/DesiredRPM")
    b.value = 5.0
    localhost_wait()
    a.value -= b.value
    return a.value


@decorators.nivs_rt_sequence
def aug_sub_unary():
    a = DoubleValue(1)
    a.value -= -1
    return a.value


# end region augassign tests
# region invalid tests
@decorators.nivs_rt_sequence
def sub_invalid_variables():
    return a - b


@decorators.nivs_rt_sequence
def sub_invalid_variables1():
    return a.value - b.value


@decorators.nivs_rt_sequence
def sub_invalid_variables2():
    a = DoubleValue(0)
    b = DoubleValue(0)
    b.value = a.value - 2
    return b.value


@decorators.nivs_rt_sequence
def sub_from_None():
    a = DoubleValue(0)
    a.value = None - 1
    return a.value


@decorators.nivs_rt_sequence
def sub_invalid_rtseq_call():
    a = DoubleValue(0)
    a.value = return_constant - 1
    return a.value

# end region invalid tests


run_tests = [
    (return_constant, (), 5),
    (sub_simple_numbers, (), -1),
    (sub_num_nivsdatatype, (), -1),
    (sub_nivsdatatype_nivsdatatype, (), -1),
    (sub_nivsdatatype_nivsdatatype1, (), -1),
    (sub_nivsdatatype_nivsdatatype2, (), -1),
    (sub_nivsdatatype_nivsdatatype3, (), -1),
    (sub_multiple_types, (), -4),
    (sub_multiple_types1, (), -8),
    (sub_with_parantheses, (), 2),
    (sub_with_parantheses1, (), 4),
    (sub_with_parantheses2, (), 2),
    (sub_variables, (), -4),
    (sub_variables1, (), -4),
    (sub_variable_variable, (), -1),
    (sub_variable_variable1, (), -1),
    (sub_binary_unary, (), 3),
    (sub_binary_unary_sequence, (), 3),
    (aug_sub_simple_numbers, (), -1),
    (aug_sub_num_nivsdatatype, (), -1),
    (aug_sub_with_parantheses, (), -8),
    (aug_sub_variables, (), -4),
    (aug_sub_unary, (), 2),
    (sub_complex_expr, (), -1),
    (sub_use_rtseq, (), -4),
    (sub_use_rtseq1, (), 4),
    (sub_use_rtseq2, (), -4),
    (sub_use_rtseq3, (), 4),
    (sub_use_rtseq4, (), -4),
    (sub_use_rtseq5, (), 4),
    (sub_variable_rtseq, (), -4),
    (sub_variable_rtseq1, (), 4),
    (aug_sub_use_rtseq, (), -4),
    (sub_to_channelref, (), -4.0),
    (aug_sub_to_channelref, (), -4.0),
]

skip_tests = [
    (sub_invalid_variables2, (), "Attribute transformer doesn't catch the a.value.value problem. -DE14612"),
    (sub_from_None, (), "Name transformer doesn't raise an exception for NoneType with python 2.7. - DE14611"),
    (sub_invalid_rtseq_call, (), "RTSeq call not implemented yet."),
]

fail_transform_tests = [
    (sub_invalid_variables, (), TranslateError),
    (sub_invalid_variables1, (), TranslateError),
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
