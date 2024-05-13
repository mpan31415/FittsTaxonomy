from panda_fk import get_chain, compute_fk
from math import pi
from pandas import read_csv, DataFrame
from os import getcwd
from re import search, IGNORECASE
from ast import literal_eval


NUM_PARTICIPANTS = 10


##################################################
def clean_data(part_id, task_id, trial_id, operation_type, panda_chain):
    
    csv_dir = getcwd()+"/FittsTaxonomy/user_study_results/trajectory/" + operation_type + "/task"+str(task_id)+"-"+str(trial_id)+"-"+str(part_id)+".csv"
    raw_df = read_csv(csv_dir)
    
    # raw (sec, nanosec)
    raw_sec_list = raw_df['sec'].tolist()
    raw_nanosec_list = raw_df['nanosec'].tolist()
    
    # get times from start (in seconds) and store into a single list
    raw_sec_start = raw_sec_list[0]
    raw_nanosec_start = raw_nanosec_list[0]
    sec_list = [raw_sec_list[i] - raw_sec_start for i in range(len(raw_sec_list))]
    nanosec_list = [round((raw_nanosec_list[i] - raw_nanosec_start)/1e9, 4) for i in range(len(raw_nanosec_list))]
    times_from_start = [round(sec_list[i]+nanosec_list[i], 3) for i in range(len(sec_list))]
    
    # get joint positions and forward kinematics and store into separate lists
    gr_list = []
    
    tx_list = []
    ty_list = []
    tz_list = []
    
    qw_list = []
    qx_list = []
    qy_list = []
    qz_list = []
    
    rx_list = []
    ry_list = []
    rz_list = []
    
    positions = raw_df['positions'].tolist()
    
    # loop through all recorded positions
    for pos_vec in positions:
        
        joint_positions = literal_eval(search("array\('d'\, (.*)\)", pos_vec, IGNORECASE).group(1))
        
        gr_list.append(joint_positions[7])
        
        # remove the last two elements from the joint positions list (they are the gripper values which have already been saved)
        joint_positions.pop(-1)
        joint_positions.pop(-1)
        
        # calculate forward kinematics
        trans, rot_mat, quat, euler = compute_fk(joint_positions, panda_chain)
        
        tx_list.append(trans[0])
        ty_list.append(trans[1])
        tz_list.append(trans[2])
        
        qw_list.append(quat[0])
        qx_list.append(quat[1])
        qy_list.append(quat[2])
        qz_list.append(quat[3])
        
        rx_list.append(euler[0])
        ry_list.append(euler[1])
        rz_list.append(euler[2])
        
    df_dict = {
        "time": times_from_start,
        "gr": gr_list,
        "tx": tx_list,
        "ty": ty_list,
        "tz": tz_list,
        "rx": rx_list,
        "ry": ry_list,
        "rz": rz_list,
        "qw": qw_list,
        "qx": qx_list,
        "qy": qy_list,
        "qz": qz_list
    }
    new_df = DataFrame(df_dict)
    
    return new_df



##################################################
def main():
    
    panda_chain = get_chain()
    
    ###### clean all data for kinesthetic teaching ######
    for part_id in range(1, NUM_PARTICIPANTS+1):
        for task_id in range(1, 4):
            for trial_id in range(1, 4):
                data = clean_data(part_id, task_id, trial_id, "kinesthetic", panda_chain)
                dest_dir = getcwd()+"/FittsTaxonomy/user_study_results/cleaned_traj/kt/part"+str(part_id)+"-task"+str(task_id)+"-t"+str(trial_id)+".csv"
                data.to_csv(dest_dir, index=False)
    
    ###### clean all data for teleoperation ######
    for part_id in range(1, NUM_PARTICIPANTS+1):
        for task_id in range(1, 4):
            for trial_id in range(1, 4):
                data = clean_data(part_id, task_id, trial_id, "teleoperation", panda_chain)
                dest_dir = getcwd()+"/FittsTaxonomy/user_study_results/cleaned_traj/teleop/part"+str(part_id)+"-task"+str(task_id)+"-t"+str(trial_id)+".csv"
                data.to_csv(dest_dir, index=False)

    print("\n\n Finished cleaning all data!! \n\n") 
    
    

##################################################
if __name__ == "__main__":
    main()