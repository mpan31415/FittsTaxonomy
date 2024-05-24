from pandas import read_csv
from ast import literal_eval
import matplotlib.pyplot as plt
from os import getcwd


##########################################
def read_data(operation_type):
    file_dir = getcwd() + "\\user_study_results\\combined_headers\\"+operation_type+".csv"
    raw_df = read_csv(file_dir)
    return raw_df

##########################################
def normalize_list(lst):
    lst_min = min(lst)
    lst_max = max(lst)
    range = lst_max - lst_min
    new_lst = []
    for n in lst:
        new_lst.append((n-lst_min)/range)
    return new_lst

##########################################
def moving_mean_filter(data, window_size):
    if not data or window_size <= 0:
        return []
    filtered_data = []
    for i in range(len(data)):
        window = data[max(i - window_size + 1, 0):i + 1]
        filtered_data.append(sum(window) / len(window))
    return filtered_data


####################################################################################
def compute_diff(operation_type, plotting=False):
    
    df = read_data(operation_type)
    
    ###### result lists ######
    diff_lists_list = []
    abs_diff_lists_list = []
    norm_abs_diff_list = []

    ###### get the source lists ######
    inc_trans_list = df['inc_trans'].tolist()
    trans_lists_list = [literal_eval(lst) for lst in inc_trans_list]

    inc_rot_list = df['inc_rot'].tolist()
    rot_lists_list = [literal_eval(lst) for lst in inc_rot_list]
    
    
    ###### loop through all the inc_trans and inc_rot lists ######
    for i in range(len(trans_lists_list)):
        
        # get this row's translation and rotation lists
        trans_list = trans_lists_list[i]
        rot_list = rot_lists_list[i]

        ##############################################################
        ##############################################################
        
        # apply moving-mean filter
        window_size = 16
        trans_list = moving_mean_filter(trans_list, window_size)
        rot_list = moving_mean_filter(rot_list, window_size)

        # normalize the lists
        trans_list = normalize_list(trans_list)
        rot_list = normalize_list(rot_list)
        diff_list = [trans_list[i] - rot_list[i] for i in range(len(trans_list))]   # log this
        
        # compute normalized sum of absolute value of all differences
        abs_diff_list = [abs(val) for val in diff_list]    # log this
        norm_abs_diff = sum(abs_diff_list) / len(abs_diff_list)    # log this
        print("Normalized sum of absolute differences = %.4f" % norm_abs_diff)
        
        ##############################################################
        # generate the lists to add to df
        diff_lists_list.append(diff_list)
        abs_diff_lists_list.append(abs_diff_list)
        norm_abs_diff_list.append(norm_abs_diff)                
        
        ##############################
        if plotting:

            # Create a figure and three subplots in a vertical layout
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

            # First subplot
            ax1.plot(trans_list, label='translation')
            ax1.set_title('Translation')
            ax1.set_xlabel('time')
            ax1.set_ylabel('translation')
            ax1.legend()
            ax1.grid(True)

            # Second subplot
            ax2.plot(rot_list, label='rotation', color='r')
            ax2.set_title('Rotation')
            ax2.set_xlabel('time')
            ax2.set_ylabel('rotation')
            ax2.legend()
            ax2.grid(True)
            
            # Second subplot
            ax3.plot(diff_list, label='trans - rot', color='g')
            ax3.set_title('Trans - Rot')
            ax3.set_xlabel('time')
            ax3.set_ylabel('Difference')
            ax3.legend()
            ax3.grid(True)

            # Adjust layout to prevent overlap
            plt.tight_layout()

            plt.show()
                        
    ################ ADD COLUMNS TO DATAFRAME ################
    df.insert(9, "norm_abs_diff", norm_abs_diff_list)
    df.insert(12, "diff_list", diff_lists_list)
    df.insert(13, "abs_diff_list", abs_diff_lists_list)
    
    ################ WRITE TO HEADER CSV FILE ################
    dest_dir = getcwd() + "\\user_study_results\\combined_headers\\"+operation_type+".csv"
    df.to_csv(dest_dir, index=False)
    

##########################################
def main():
    
    # kt
    compute_diff(operation_type="kt")
    # teleop
    compute_diff(operation_type="teleop")
        
    print("\n Finished computing the 'series/parallel' differences and added to headers \n")
                    


##########################################
if __name__ == "__main__":
    main()