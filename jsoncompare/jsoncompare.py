import json
from itertools import repeat

hit = 0
miss = 0
actual_match = []


def _is_dict_same(expected, actual):
    """ This function checks if 2 dictionaries are same """
    global hit, miss, actual_match
    temp = True
    for key in expected:
        if key not in actual.keys():
            if isinstance(expected[key], str):
                miss += 1
                print("Missing :", key, "\n")
                actual_match.append(0)
            else:
                miss += len(expected[key])
                print("Missing :", key, "\n")
                actual_match.extend(repeat(0, len(expected[key])))
            temp = False
        else:
            are_same_flag = _are_same(expected[key], actual[key])
            if not are_same_flag:
                pass
    return temp


def _is_list_same(expected, actual):
    """ This function checks if 2 lists are same """
    global hit, miss, actual_match
    temp = True
    for i in range(len(expected)):
        if isinstance(expected[i], (str, int)) and expected[i] in actual:
            hit += 1
            actual_match.append(1)
        elif type(expected[i]) == list and expected[i] in actual:
            if _is_list_same(expected[i], actual[actual.index(expected[i])]):
                hit += 1
                actual_match.append(1)
            else:
                temp = False
        elif type(expected[i]) == dict:
            if _is_dict_same(expected[i], actual[i]):
                pass
        # list element is not in actual
        else:
            temp = False
            miss += 1
            print("Missing :", expected[i], "\n")
            actual_match.append(0)
    return temp


def _are_same(expected, actual):
    global hit, miss, actual_match
    # Ensure they are of same type
    if type(expected) != type(actual):
        if type(expected) == str:
            miss += 1
        else:
            miss += len(expected)
        print("type mismatch")
        print("Expected :", type(expected))
        print("Actual :", type(actual), "\n")
        actual_match.extend(repeat(0, len(expected)))
        return False

    # Compare primitive types immediately
    if isinstance(expected, (int, str, bool, float)):
        if expected.lower().strip().replace(" ", "") == actual.lower().strip().replace(" ", ""):
            hit += 1
            actual_match.append(1)
            return True
        else:
            miss += 1
            print("Expected :", expected)
            print("Actual :", actual, "\n")
            actual_match.append(1)
            return False

    # type is dictionary or list
    else:
        if isinstance(expected, dict):
            return _is_dict_same(expected, actual)
        if isinstance(expected, list):
            return _is_list_same(expected, actual)

    return False


def are_same(original_a, original_b):
    global hit, miss, actual_match
    a = original_a
    b = original_b
    return _are_same(a, b), ("miss", miss), ("hit", hit), actual_match


def json_are_same(a, b, ignore_list_order_recursively=False, ignore_value_of_keys=[]):
    return are_same(json.loads(a), json.loads(b), ignore_list_order_recursively, ignore_value_of_keys)
