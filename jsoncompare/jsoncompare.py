import json

hit = 0
miss = 0

def _is_dict_same(expected, actual):
    global hit, miss
    temp = True
    for key in expected:
        if key not in actual.keys():
            # miss += 1
            print(key, "not present")
            temp = False
            # have to change order
            # are_same_flag, stack = _are_same(actual[key], expected[key], ignore_value_of_keys)
        else:
            are_same_flag = _are_same(expected[key], actual[key])
            if not are_same_flag:
                # print("Expected : ",expected[key])
                # print("Actual : ",actual[key])
                print("different values in ", key)

                # miss += 1

    return temp


def _is_list_same(expected, actual):
    global hit, miss
    temp = True
    for i in range(len(expected)):
        if not _are_same(expected[i], actual[i]):
            temp = False
            print("miss at", i)

    return temp


def _are_same(expected, actual):
    global hit, miss

    # Ensure they are of same type
    if type(expected) != type(actual):
        miss += 1
        print("Expected : ", type(expected))
        print("Actual : ", type(actual))
        print("type mismatch\n\n")
        return False

    # Compare primitive types immediately
    if type(expected) in (int, str, bool, float):
        if expected == actual:
            hit += 1
            return True
        else:
            miss += 1
            print("value mismatch")
            return False

    else:
        # Ensure collections has same length
        temp = True
        if len(expected) != len(actual):
            miss += abs(len(expected) - len(actual))
            print("Expected : ", len(expected))
            print("Actual : ", len(actual))
            print("length not same\n\n")
            temp = False
            # return False

        if isinstance(expected, dict):
            return _is_dict_same(expected, actual)

        if isinstance(expected, list) and not temp and len(expected) < len(actual):
            return _is_list_same(expected, actual)
        else:
            return _is_list_same(actual, expected)

    return False


def are_same(original_a, original_b):
    global hit, miss
    a = original_a
    b = original_b
    return _are_same(a, b), ("miss", miss), ("hit", hit)


def json_are_same(a, b, ignore_list_order_recursively=False, ignore_value_of_keys=[]):
    return are_same(json.loads(a), json.loads(b), ignore_list_order_recursively, ignore_value_of_keys)
