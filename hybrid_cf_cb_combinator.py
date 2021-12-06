

def combine(cf_s, cf_w, cb_s, cb_w):
    final_scores = []
    for cb in range(len(cb_s)):
        cb_score = cb_s[cb][1] * cb_w
        #print(cf_score)
        is_present = 0
        for cf in range(len(cf_s)):
            if int(cf_s[cf][0]) == int(cb_s[cb][0]):
                cf_score = cf_s[cf][1] * cf_w
                #print(cb_score)
                # print(cf_score, '  -- ', cb_score)
                final_score = cf_score + cb_score
                #print(final_score)
                final_score_tuple = (cf_s[cf][0], final_score)
                #print(final_score_tuple)
                final_scores.append(final_score_tuple)
                is_present = 1
        if is_present == 0:
            final_score_tuple = (cb_s[cb][0], cb_score*1.5)
            final_scores.append(final_score_tuple)


    #print(final_scores)
    output = list(sorted(final_scores, key=lambda x: x[1], reverse=True))

    return output


# list1 = [(1, 0.6), (3, 0.4), (2, 0.3), (4, 0.2), (5, 0.1)]
# list2 = [(3, 0.8), (5, 0.7), (2, 0.6), (1, 0.5), (4, 0.2)]

# w1 = 0.5
# w2 = 0.5

# results = combine(list1, w1, list2, w2)

# print(results)


