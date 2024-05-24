# from math import acos, degrees

# gripper_width = 0.8
# object_width = 0.5

# theta_max = acos(object_width / gripper_width)
# theta_max = degrees(theta_max)

# print(theta_max)


# home = [0.31, 0.0, 0.48]



# q1 = [0, 0, 0.707, 0.707]
# q2 = [0, 0, 0, 1]

# print(1.5e+5)


# from scipy.spatial.transform import Rotation
# # from math import pi


# ###################################################
# def euler2quat(euler):
    
#     # Create a rotation object from Euler angles specifying axes of rotation
#     rot = Rotation.from_euler('xyz', euler, degrees=True)

#     # Convert to quaternions and print
#     rot_quat = rot.as_quat()
#     print(rot_quat)
    
#     return rot_quat


# ###################################################
# def compute_diff(lb, ub):
#     lower_quat = euler2quat(lb)
#     upper_quat = euler2quat(ub)
#     dot_prod = sum([lower_quat[i]*upper_quat[i] for i in range(len(lower_quat))])
#     return dot_prod


# lb = [0, -30, 0]
# ub = [0, 30, 0]

# res = compute_diff(lb, ub)
# print("Result = %.5f" % res)


lst = [1, 2, 3, 4, 5]

lst = [n for n in lst if n < 3]

print(lst)