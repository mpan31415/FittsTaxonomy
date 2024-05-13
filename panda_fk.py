import PyKDL
from urdf_parser_py.urdf import URDF
import kdl_parser_py.urdf
from math import pi
from numpy import array


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
    urdf_file = 'panda.urdf'
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
def compute_fk(joint_positions, chain):
    # Compute the forward kinematics
    end_frame = compute_forward_kinematics(chain, joint_positions)
    translation = end_frame.p
    rotation = end_frame.M
    trans = [translation.x(), translation.y(), translation.z()]
    rot_mat = array([[rotation[0,0], rotation[0,1], rotation[0,2]],
                             [rotation[1,0], rotation[1,1], rotation[1,2]],
                             [rotation[2,0], rotation[2,1], rotation[2,2]]])
    quaternion = rotation.GetQuaternion()
    # Store as numpy array or list (depending on your preference)
    quat = array([quaternion[0], quaternion[1], quaternion[2], quaternion[3]])

    return trans, rot_mat, quat



###################################################
def main():

    panda_chain = get_chain()

    joint_positions = [0.0, -pi/8, 0.0, -5*pi/8, 0.0, pi/2, pi/4]  # example joint positions

    trans, rot_mat, quat = compute_fk(joint_positions, panda_chain)

    # Output the position and orientation of the end effector
    print("Translation:", trans)
    print("Rotation Matrix:\n", rot_mat)
    print("Rotation quaternion:\n", quat)



if __name__ == "__main__":
    main()