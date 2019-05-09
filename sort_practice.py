# from sample_class import SampleClass


# sample_dict = {
#     'goo': 3, 
#     'zoo' : 4,
#     'pam': 2,
#     'dog': 1,
#     'myer': 5
# }

# classes = []
# index = 0
# for term in sample_dict:
#     classes.append(SampleClass(term, sample_dict[term]))
#     index += 1
    
# print(classes)

# print(sorted(classes)[-2:])

# for term in sorted(sample_dict, key = lambda kv:kv[1]):
#     print(term)

# print(sorted(sample_dict, key = lambda kv:kv[1])[-2:])
sample = [[2,3],[6,7,8]]
print(sum([term[1] for term in sample]))