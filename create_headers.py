from pandas import read_csv, DataFrame
from os import getcwd
from math import sqrt, acos, log2


NUM_PARTICIPANTS = 10



##################################################
def read_data(part_id, task_id, trial_id, operation_type):
    csv_dir = getcwd()+"/user_study_results/cleaned_traj/"+operation_type+"/part"+str(part_id)+"-task"+str(task_id)+"-t"+str(trial_id)+".csv"
    raw_df = read_csv(csv_dir)
    return raw_df

##################################################
def get_trans_diff(x1, y1, z1, x2, y2, z2):
    return sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

##################################################
def get_quat_diff(w1, x1, y1, z1, w2, x2, y2, z2):
    dot_prod = w1*w2 + x1*x2 + y1*y2 + z1*z2
    clipped_dot_prod = max(-1, min(dot_prod, 1))
    return acos(clipped_dot_prod)


##################################################
def generate_part_header(part_id, operation_type):
    
    # trial parameters lists
    task_id_list = []
    trial_id_list = []
    section_num_list = []
    
    # metrics lists: {trans, path_trans, rot, path_rot, move_time}
    trans_list = []
    path_trans_list = []
    rot_list = []
    path_rot_list = []
    move_time_list = []
    
    # loop through all 3 tasks
    for task_id in range(1, 4):
        
        # loop through all 3 trials
        for trial_id in range(1, 4):
    
            df = read_data(part_id, task_id, trial_id, operation_type)
            
            ############ Section 1: From "home" -> "grasping" (just starting to grasp) ############
            sec1_df = df[df['gr_state']=="Empty"]
            # print(sec1_df)
            # get amount of translation (using both end-to-end and integral forms)
            # translation lists
            txs = sec1_df['tx'].tolist()
            tys = sec1_df['ty'].tolist()
            tzs = sec1_df['tz'].tolist()
            trans = get_trans_diff(txs[0], tys[0], tzs[0], txs[-1], tys[-1], tzs[-1])
            path_trans = 0
            for i in range(len(txs)-1):
                path_trans += get_trans_diff(txs[i], tys[i], tzs[i], txs[i+1], tys[i+1], tzs[i+1])
            
            # get amount of rotation (using both end-to-end and integral forms)
            # quaternion lists
            qws = sec1_df['qw'].tolist()
            qxs = sec1_df['qx'].tolist()
            qys = sec1_df['qy'].tolist()
            qzs = sec1_df['qz'].tolist()
            rot = get_quat_diff(qws[0], qxs[0], qys[0], qzs[0], qws[-1], qxs[-1], qys[-1], qzs[-1])
            path_rot = 0
            for i in range(len(qws)-1):
                path_rot += get_quat_diff(qws[i], qxs[i], qys[i], qzs[i], qws[i+1], qxs[i+1], qys[i+1], qzs[i+1])
            
            # get movement time
            times_list = sec1_df['time'].tolist()
            move_time = times_list[-1] - times_list[0]
            # print("translation = %.3f" % trans)
            # print("rotation = %.3f" % rot)
            # print("move time = %d" % move_time)
            
            ###### add data to lists ######
            task_id_list.append(task_id)
            trial_id_list.append(trial_id)
            section_num_list.append(int(1))
            
            trans_list.append(trans)
            path_trans_list.append(path_trans)
            rot_list.append(rot)
            path_rot_list.append(path_rot)
            move_time_list.append(move_time)
            
            
            ############ Section 2: From "grasped" -> "successful task completion" ############
            sec2_df = df[df['gr_state']=="Done"]
            # get amount of translation (using both end-to-end and integral forms)
            # translation lists
            txs = sec2_df['tx'].tolist()
            tys = sec2_df['ty'].tolist()
            tzs = sec2_df['tz'].tolist()
            trans = get_trans_diff(txs[0], tys[0], tzs[0], txs[-1], tys[-1], tzs[-1])
            path_trans = 0
            for i in range(len(txs)-1):
                path_trans += get_trans_diff(txs[i], tys[i], tzs[i], txs[i+1], tys[i+1], tzs[i+1])
            
            # get amount of rotation (using both end-to-end and integral forms)
            # quaternion lists
            qws = sec2_df['qw'].tolist()
            qxs = sec2_df['qx'].tolist()
            qys = sec2_df['qy'].tolist()
            qzs = sec2_df['qz'].tolist()
            rot = get_quat_diff(qws[0], qxs[0], qys[0], qzs[0], qws[-1], qxs[-1], qys[-1], qzs[-1])
            path_rot = 0
            for i in range(len(qws)-1):
                path_rot += get_quat_diff(qws[i], qxs[i], qys[i], qzs[i], qws[i+1], qxs[i+1], qys[i+1], qzs[i+1])
            
            # get movement time
            times_list = sec2_df['time'].tolist()
            move_time = times_list[-1] - times_list[0]
            
            ###### add data to lists ######
            task_id_list.append(task_id)
            trial_id_list.append(trial_id)
            section_num_list.append(int(2))
            
            trans_list.append(trans)
            path_trans_list.append(path_trans)
            rot_list.append(rot)
            path_rot_list.append(path_rot)
            move_time_list.append(move_time)
            
            
    # generate Dataframe dictionary
    df_dict = {
        "task_id": task_id_list,
        "trial_id": trial_id_list,
        "section": section_num_list,
        "trans": trans_list,
        "path_trans": path_trans_list,
        "rot": rot_list,
        "path_rot": path_rot_list,
        "move_time": move_time_list
    }
    result_df = DataFrame(df_dict)
    
    return result_df
        


##################################################
def main():
    
    for part_id in range(1, NUM_PARTICIPANTS+1):
        
        # kinesthetic teaching
        kt_df = generate_part_header(part_id, "kt")
        dest_path = getcwd() + "\\user_study_results\\headers\\part" + str(part_id) + "_kt_header.csv"
        kt_df.to_csv(dest_path, index=False)
        
        # teleoperation
        teleop_df = generate_part_header(part_id, "teleop")
        dest_path = getcwd() + "\\user_study_results\\headers\\part" + str(part_id) + "_teleop_header.csv"
        teleop_df.to_csv(dest_path, index=False)
    
    print("\n\n  Finished generating all header files!  \n\n")
    
    
    
##################################################
if __name__ == "__main__":
    main()
