import json
from itertools import repeat
from collections import OrderedDict
import sys
import operator

hit = 0
miss = 0
actual_match = []

if sys.version_info[0] < 3:
    from future import range
if sys.version_info[0] == 3 and sys.version_info[1] < 5:
    from .is_close import isclose
else:
    from math import isclose


def _bottom_up_sort(unsorted_json):
    if isinstance(unsorted_json, dict):
        return sorted((k, _bottom_up_sort(v)) for k, v in unsorted_json.items())
    if isinstance(unsorted_json, list):
        return sorted(_bottom_up_sort(x) for x in unsorted_json)
    else:
        return unsorted_json


def _to_ordered_dict(sorted_json):
    if isinstance(sorted_json, list):
        ordered = OrderedDict()
        if sorted_json and isinstance(sorted_json[0], list):
            ordered = []
            for i in sorted_json:
                ordered.append(_to_ordered_dict(i))
            return ordered
        else:
            for i in sorted_json:
                if isinstance(i, list):
                    ordered.update(_to_ordered_dict(i))
                elif isinstance(i, tuple):
                    ordered[i[0]] = _to_ordered_dict(i[1])
            return ordered
    else:
        return sorted_json


def _is_dict_same(expected, actual):
    global hit, miss, actual_match
    temp = True
    for key in expected:
        if key not in actual.keys():
            # print(key, "not present\n")
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
                # print("different values in ", key,"\n")

    return temp


def _is_list_same(expected, actual):
    global hit, miss, actual_match
    temp = True
    # if len(expected) > len(actual):
    #     print("Expected : ", len(expected))
    #     print("Actual : ", len(actual))
    #     print("length not same\n")

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
                #     print("dict not same")
        else:
            temp = False
            miss += 1
            print("Missing :", expected[i], "\n")
            actual_match.append(0)
            # print("miss at", i)
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

        # print(expected)
        actual_match.extend(repeat(0, len(expected)))
        # print("Expected : ", type(expected))
        # print("Actual : ", type(actual))
        # print("type mismatch\n\n")
        return False

    # Compare primitive types immediately
    if isinstance(expected, (str, bool)):
        if expected.lower().strip().replace(" ", "") == actual.lower().strip().replace(" ", ""):
            hit += 1
            actual_match.append(1)
            return True
        else:
            miss += 1
            print("Expected :", expected)
            print("Actual :", actual, "\n")
            actual_match.append(1)
            # print("value mismatch\n")
            return False

    if type(expected) in (int, float):
        if isclose(expected, actual):
            hit += 1
            actual_match.append(1)
            return True
        else:
            miss += 1
            print("Expected :", expected)
            print("Actual :", actual, "\n")
            actual_match.append(1)
            # print("value mismatch\n")
            return False

    else:
        if isinstance(expected, dict):
            return _is_dict_same(expected, actual)

        if isinstance(expected, list):
            return _is_list_same(expected, actual)

    return False


def sort_dict(a, b):
    outer_keys = a.keys()
    for outer_key in outer_keys:
        if isinstance(a[outer_key], list):
            for x in range(0, len(a[outer_key])):
                if isinstance((a[outer_key][x]), dict):
                    key_to_sort_with = list(a[outer_key][x].keys())[0]
                    a[outer_key].sort(key=operator.itemgetter(key_to_sort_with))
                    b[outer_key].sort(key=operator.itemgetter(key_to_sort_with))
    return a, b


def are_same(original_a, original_b):
    global hit, miss, actual_match
    a, b = sort_dict(original_a, original_b)
    return _are_same(a, b), ("miss", miss), ("hit", hit), actual_match


def json_are_same(a, b):
    return are_same(json.loads(a), json.loads(b))
