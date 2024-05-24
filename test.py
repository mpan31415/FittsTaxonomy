# from math import acos, degrees

# gripper_width = 0.8
# object_width = 0.5

# theta_max = acos(object_width / gripper_width)
# theta_max = degrees(theta_max)

# print(theta_max)


lst1 = [1, 2, 3, 2, 1]
lst2 = [1, 2, 40, 2, 1]

abs_diff_lst = [abs(lst1[i]-lst2[i]) for i in range(len(lst1))]
norm_abs_diff = sum(abs_diff_lst) / len(abs_diff_lst)

print(norm_abs_diff*100)