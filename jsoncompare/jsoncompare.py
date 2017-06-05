import json

hit = 0
miss = 0

def _is_dict_same(expected, actual):
    global hit, miss
    temp = True
    for key in expected:
        if key not in actual.keys():
            print(key, "not present\n")
            if isinstance(expected[key],str):
                miss+=1
            else:
                miss+=len(expected[key])
            temp = False

        else:
            are_same_flag = _are_same(expected[key], actual[key])
            if not are_same_flag:
                print("different values in ", key,"\n")

    return temp


def _is_list_same(expected, actual):
    global hit, miss
    temp = True
    if len(expected) > len(actual):
        print("Expected : ", len(expected))
        print("Actual : ", len(actual))
        print("length not same\n")

    for i in range(len(expected)):
        if isinstance(expected[i],(str,int)) and expected[i] in actual:
            hit+=1
        elif type(expected[i])==list and expected[i] in actual:
            if _is_list_same(expected[i],actual[actual.index(expected[i])]):
                hit+=1
            else:
                temp=False
        elif type(expected[i]) == dict:
            if expected[i] in actual:
                hit+=1
            else:
                miss+=len(expected[i])
                print("length of dict not same")
        else:
            temp = False
            miss+=1
            print("miss at", i)
    return temp

def _are_same(expected, actual):
    global hit, miss

    # Ensure they are of same type
    if type(expected) != type(actual):
        miss+=len(expected)
        print("Expected : ", type(expected))
        print("Actual : ", type(actual))
        print("type mismatch\n\n")
        return False

    # Compare primitive types immediately
    if isinstance(expected,(int, str, bool, float)):
        if expected == actual:
            hit += 1
            return True
        else:
            miss+=1
            print("value mismatch\n")
            return False

    else:
        if isinstance(expected, dict):
            return _is_dict_same(expected, actual)

        if isinstance(expected, list):
            return _is_list_same(expected, actual)

    return False


def are_same(original_a, original_b):
    global hit, miss
    a = original_a
    b = original_b
    return _are_same(a, b), ("miss", miss), ("hit", hit)


def json_are_same(a, b, ignore_list_order_recursively=False, ignore_value_of_keys=[]):
    return are_same(json.loads(a), json.loads(b), ignore_list_order_recursively, ignore_value_of_keys)
