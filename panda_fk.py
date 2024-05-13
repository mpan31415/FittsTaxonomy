import PyKDL
from urdf_parser_py.urdf import URDF
import kdl_parser_py.urdf
from numpy import array
from os import getcwd
from math import pi
from math import atan2, asin

###################################################
def load_robot_model(urdf_file):
    """
    Load the robot model from a URDF file.
    """
    robot = URDF.from_xml_file(urdf_file)
    # Create a KDL tree from the URDF
    success, tree = kdl_parser_py.urdf.treeFromUrdfModel(robot)
    if not success:
        raise Exception("Failed to extract KDL Tree from URDF model.")
    return tree

###################################################
def get_chain():
    urdf_file = getcwd() + '/FittsTaxonomy/panda.urdf'
    # Load the robot model
    tree = load_robot_model(urdf_file)
    # Get the chain for the robot arm
    chain = tree.getChain("panda_link0", "panda_grasptarget")  # Adjust the base and end-effector names as per your URDF
    return chain

###################################################
def compute_forward_kinematics(chain, joint_angles):
    """
    Compute the forward kinematics for the given chain and joint angles.
    """
    # Create a solver from the chain
    fk_solver = PyKDL.ChainFkSolverPos_recursive(chain)

    # Create a joint array
    joint_array = PyKDL.JntArray(chain.getNrOfJoints())

    # Assign the joint angles to the joint array
    for idx, angle in enumerate(joint_angles):
        joint_array[idx] = angle

    # Compute the forward kinematics
    end_frame = PyKDL.Frame()
    fk_solver.JntToCart(joint_array, end_frame)

    return end_frame

###################################################
def euler_from_quaternion(w, x, y, z):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = atan2(t3, t4)
     
        return [roll_x, pitch_y, yaw_z] # in radians

###################################################
def compute_fk(joint_positions, chain):
    # Compute the forward kinematics
    end_frame = compute_forward_kinematics(chain, joint_positions)
    translation = end_frame.p
    rotation = end_frame.M
    trans = [translation.x(), translation.y(), translation.z()]
    trans = [round(n, 5) for n in trans]
    rot_mat = array([[rotation[0,0], rotation[0,1], rotation[0,2]],
                     [rotation[1,0], rotation[1,1], rotation[1,2]],
                     [rotation[2,0], rotation[2,1], rotation[2,2]]])
    quaternion = rotation.GetQuaternion()
    # Store as numpy array or list (depending on your preference)
    quat = [quaternion[0], quaternion[1], quaternion[2], quaternion[3]]
    quat = [round(n, 5) for n in quat]
    euler = euler_from_quaternion(quat[0], quat[1], quat[2], quat[3])
    euler = [round(n, 5) for n in euler]

    return trans, rot_mat, quat, euler


##################################################
def main():
    
    panda_chain = get_chain()

    joint_positions = [0.0, -pi/8, 0.0, -5*pi/8, 0.0, pi/2, pi/4]  # example joint positions

    trans, rot_mat, quat, euler = compute_fk(joint_positions, panda_chain)

    # Output the position and orientation of the end effector
    print("Translation:", trans)
    print("Rotation Matrix:\n", rot_mat)
    print("Rotation quaternion:\n", quat)
    print("Rotation Euler:\n", euler)



if __name__ == "__main__":
    main()