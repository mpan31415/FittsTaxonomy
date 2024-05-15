import matplotlib.pyplot as plt


lst1 = [1, 3, 2, 4, 3, 5, 4, 6, 5, 7, 6, 8]
lst2 = [n-5 for n in lst1]
lst3 = [5*n for n in lst2]

# plt.plot(lst2)
# plt.plot(lst3)
# plt.show()


def normalize_list(lst):
    lst_min = min(lst)
    lst_max = max(lst)
    range = lst_max - lst_min
    new_lst = []
    for n in lst:
        new_lst.append((n-lst_min)/range)
    return new_lst


lst2 = normalize_list(lst2)
lst3 = normalize_list(lst3)

plt.plot(lst2)
plt.plot(lst3)
plt.show()