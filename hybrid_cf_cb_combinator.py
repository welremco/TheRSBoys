

def combine(b_s, b_w, cf_s, cf_w, cb_s, cb_w):
    # combine dictionary scores of cf_s and and cb_s with weights cf_w and cb_w respectively
    combined = {}
    for key in cb_s:
        int_key = int(key)
        if int_key in b_s:
            combined[int_key] = b_s[int_key] * b_w
            if int_key in cf_s:
                combined[int_key] += cf_s[int_key] * cf_w
            else:
                combined[int_key] += cb_s[key] * cb_w
        elif key in cf_s:
            combined[int_key] = cf_s[int_key] * cf_w
        else:
            combined[int_key] = cb_s[key] * cb_w
    # convert combined dictionary to list of tuples
    combined_list = []
    for key in combined:
        combined_list.append((key, combined[key]))
    # sort combined list by score
    combined_list.sort(key=lambda tup: tup[1], reverse=True)
    return combined_list


# list1 = [(1, 0.6), (3, 0.4), (2, 0.3), (4, 0.2), (5, 0.1)]
# list2 = [(3, 0.8), (5, 0.7), (2, 0.6), (1, 0.5), (4, 0.2)]

# w1 = 0.5
# w2 = 0.5

# results = combine(list1, w1, list2, w2)

# print(results)


