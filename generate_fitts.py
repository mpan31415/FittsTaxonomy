from pandas import read_csv, DataFrame, concat
from os import getcwd
from math import sqrt, acos, log2


NUM_PARTICIPANTS = 1

###### Goal widths for each task, order = {trans, rot, trans_width, rot_width} ######
NOMINAL_GOAL_PARAMS = {
    "task1": (1, 1, 1, 1),
    "task2": (1, 1, 1, 1),
    "task3": (1, 1, 1, 1)
}

##################################################
def read_combined_header(operation_type:str):
    csv_dir = getcwd()+"\\user_study_results\\combined_headers\\" + operation_type + ".csv"
    raw_df = read_csv(csv_dir)
    return raw_df


##################################################
def compute_fitts_ids(trans, rot, task_id):
    
    
    
    return None


##################################################
def generate_fitts_params_file(df:DataFrame, operation_type:str):
    
    # outer size = task_id, inner size = section_id
    trans_amps = [[0, 0], [0, 0], [0, 0]]
    rot_amps = [[0, 0], [0, 0], [0, 0]]
    
    # find average translation and rotation of the trajectories
    for task_id in range(1, 4):
        for section in range(1, 3):
            this_df = df[(df['task_id']==task_id) & (df['section']==section)]
            # print(this_df)
            this_trans_list = this_df['trans'].tolist()
            this_ave_trans = sum(this_trans_list) / len(this_trans_list)
            trans_amps[task_id-1][section-1] = this_ave_trans
    
    print(trans_amps)
            
    
    # trans_id_list = []
    # rot_id_list = []
    
    # for ind in df.index:
    #     trans = df['trans'][ind]
    #     rot = df['rot'][ind]
    #     task_id = df['task_id'][ind]
    #     trans_id, rot_id = compute_fitts_ids(trans, rot, task_id)
    #     trans_id_list.append(trans_id)
    #     rot_id_list.append(rot_id)
        
    # sum_id_list = [(trans_id_list[i] + rot_id_list[i]) for i in range(len(trans_id_list))]
    # max_id_list = [max(trans_id_list[i], rot_id_list[i]) for i in range(len(trans_id_list))]
        
    # # add columns
    # df.insert(4, sum_id_list)
    # df.insert(5, max_id_list)
    # df.insert(6, trans_id_list)
    # df.insert(7, rot_id_list)
    
    # dest_path = getcwd() + "\\user_study_results\\fitts_param_headers\\" + operation_type + ".csv"
    # df.to_csv(dest_path, index=False)
    # print("\n   Finished writing Fitts ID parameters to Dataframe!   \n")
    


##################################################
def main():
    
    ###### kinesthetic teaching ######
    kt_df = read_combined_header("kt")
    generate_fitts_params_file(kt_df, "kt")

    
    # ###### teleoperation ######
    # teleop_df = read_combined_header("teleop")
    # generate_fitts_params_file(teleop_df, "teleop")
    
    
##################################################
if __name__ == "__main__":
    main()