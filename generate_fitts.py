from pandas import read_csv, DataFrame, concat
from os import getcwd
from math import sqrt, acos, log2, pi
from statistics import mean, variance


NUM_PARTICIPANTS = 1

###### Goal widths for each task, order = {sec1 amp, sec1 width, sec2 amp, sec2 width} ######
NOMINAL_TRANS_PARAMS = [[0.5574, 0.000075, 0.4826, 0.0004],
                        [0.4946, 0.0003, 0.3187, 0.00005],
                        [0.5723, 0.0003, 0.5123, 2.69e-5]]

NOMINAL_ROT_PARAMS = [[0.0, 1.0, 0.0, 1.0],
                      [0.7071, 0.7071, 0.7071, 0.8939],
                      [0.0, 1.0, 0.7071, 0.866]]

###### Threshold values, to exclude values before calculating max() and mean() for the EFFECTIVE versions ######
TRANS_THRES = [[1, 1],
               [1, 1],
               [1, 1]]

ROT_THRES = [[pi/4, pi/4],
             [pi/2, pi/2],
             [pi/4, pi/2]]


##################################################
def get_thres_mean_var(lst, thres):
    lst = [n for n in lst if n < thres]
    m = mean(lst)
    v = variance(lst)
    return m, v
            
            
##################################################
def read_combined_header(operation_type:str):
    csv_dir = getcwd()+"\\user_study_results\\combined_headers\\" + operation_type + ".csv"
    raw_df = read_csv(csv_dir)
    return raw_df


##################################################
def compute_fitts_id(amp, width):
    return log2(amp/width + 1)


##################################################
def generate_fitts_params_file(df:DataFrame, operation_type:str):
    
    # drop the final 4 columns of lists
    df.drop(columns=['inc_trans', 'inc_rot', 'diff_list', 'abs_diff_list'], inplace=True)
    
    nom_trans_amp_list = []
    nom_trans_width_list = []
    
    nom_rot_amp_list = []
    nom_rot_width_list = []
    
    for id in df.index:
        task_id = df['task_id'][id]
        section_id = df['section'][id]
        nom_trans_amp_list.append(NOMINAL_TRANS_PARAMS[task_id-1][(section_id-1)*2])
        nom_trans_width_list.append(NOMINAL_TRANS_PARAMS[task_id-1][(section_id-1)*2+1])
        nom_rot_amp_list.append(NOMINAL_ROT_PARAMS[task_id-1][(section_id-1)*2])
        nom_rot_width_list.append(NOMINAL_ROT_PARAMS[task_id-1][(section_id-1)*2+1])
    
    df.insert(4, "nom_trans_amp", nom_trans_amp_list)
    df.insert(5, "nom_trans_width", nom_trans_width_list)
    df.insert(6, "nom_rot_amp", nom_rot_amp_list)
    df.insert(7, "nom_rot_width", nom_rot_width_list)
    
    
    # outer size = task_id, inner size = section_id
    eff_trans_amps = [[0, 0], [0, 0], [0, 0]]
    eff_trans_widths = [[0, 0], [0, 0], [0, 0]]
    
    eff_rot_amps = [[0, 0], [0, 0], [0, 0]]
    eff_rot_widths = [[0, 0], [0, 0], [0, 0]]
    
    # find average translation and rotation of the trajectories
    for task_id in range(1, 4):
        
        for section in range(1, 3):
            
            this_df = df[(df['task_id']==task_id) & (df['section']==section)]
            
            # translation
            this_trans_list = this_df['trans'].tolist()
            this_trans_mean, this_trans_var = get_thres_mean_var(this_trans_list, TRANS_THRES[task_id-1][section-1])
            eff_trans_amps[task_id-1][section-1] = this_trans_mean
            eff_trans_widths[task_id-1][section-1] = 4.133 * this_trans_var
            
            # rotation
            this_rot_list = this_df['rot'].tolist()
            this_rot_mean, this_rot_var = get_thres_mean_var(this_rot_list, ROT_THRES[task_id-1][section-1])
            eff_rot_amps[task_id-1][section-1] = this_rot_mean
            eff_rot_widths[task_id-1][section-1] = 4.133 * this_rot_var
            
    # # print results
    # print("effective translation amplitudes = %s" % eff_trans_amps)
    # print("effective translation widths = %s" % eff_trans_widths)
    # print("effective rotation amplitudes = %s" % eff_rot_amps)
    # print("effective rotation widths = %s" % eff_rot_widths)
    

    eff_trans_amp_list = []
    eff_trans_width_list = []
    eff_rot_amp_list = []
    eff_rot_width_list = []
    
    for id in df.index:
        task_id = df['task_id'][id]
        section_id = df['section'][id]
        eff_trans_amp_list.append(eff_trans_amps[task_id-1][section_id-1])
        eff_trans_width_list.append(eff_trans_widths[task_id-1][section_id-1])
        eff_rot_amp_list.append(eff_rot_amps[task_id-1][section_id-1])
        eff_rot_width_list.append(eff_rot_widths[task_id-1][section_id-1])
        
    df.insert(8, "eff_trans_amp", eff_trans_amp_list)
    df.insert(9, "eff_trans_width", eff_trans_width_list)
    df.insert(10, "eff_rot_amp", eff_rot_amp_list)
    df.insert(11, "eff_rot_width", eff_rot_width_list)
    
    
    ########### compute Fitts ID for each row ###########
    nom_trans_fid_list = [compute_fitts_id(nom_trans_amp_list[i], nom_trans_width_list[i]) for i in range(len(nom_trans_amp_list))]
    nom_rot_fid_list = [compute_fitts_id(nom_rot_amp_list[i], nom_rot_width_list[i]) for i in range(len(nom_rot_amp_list))]
    
    eff_trans_fid_list = [compute_fitts_id(eff_trans_amp_list[i], eff_trans_width_list[i]) for i in range(len(eff_trans_amp_list))]
    eff_rot_fid_list = [compute_fitts_id(eff_rot_amp_list[i], eff_rot_width_list[i]) for i in range(len(eff_rot_amp_list))]
    
    df.insert(12, "nom_trans_fid", nom_trans_fid_list)
    df.insert(13, "nom_rot_fid", nom_rot_fid_list)
    df.insert(14, "eff_trans_fid", eff_trans_fid_list)
    df.insert(15, "eff_rot_fid", eff_rot_fid_list)
    
    
    dest_path = getcwd() + "\\user_study_results\\fitts_headers\\" + operation_type + ".csv"
    df.to_csv(dest_path, index=False)
    print("\n   Finished writing Fitts ID parameters to Dataframe!   \n")
    


##################################################
def main():
    
    ###### kinesthetic teaching ######
    kt_df = read_combined_header("kt")
    generate_fitts_params_file(kt_df, "kt")

    
    ###### teleoperation ######
    teleop_df = read_combined_header("teleop")
    generate_fitts_params_file(teleop_df, "teleop")
    
    
##################################################
if __name__ == "__main__":
    main()