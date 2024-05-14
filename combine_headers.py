from pandas import read_csv, DataFrame, concat
from os import getcwd
from math import sqrt, acos, log2


NUM_PARTICIPANTS = 10


##################################################
def read_header_data(part_id, operation_type):
    csv_dir = getcwd()+"\\user_study_results\\headers\\part"+str(part_id)+"_"+operation_type+"_header.csv"
    raw_df = read_csv(csv_dir)
    return raw_df



##################################################
def main():
    
    ###### kinesthetic teaching ######
    kt_df_list = []
    for part_id in range(1, NUM_PARTICIPANTS+1):
        kt_df_list.append(read_header_data(part_id, "kt"))
        
    concat_kt_df = concat(kt_df_list, axis=0, ignore_index=True)
    dest_path = getcwd() + "\\user_study_results\\combined_headers\\kt.csv"
    concat_kt_df.to_csv(dest_path, index=False)
        
        
    ###### teleoperation ######
    teleop_df_list = []
    for part_id in range(1, NUM_PARTICIPANTS+1):
        teleop_df_list.append(read_header_data(part_id, "teleop"))
    
    concat_teleop_df = concat(teleop_df_list, axis=0, ignore_index=True)
    dest_path = getcwd() + "\\user_study_results\\combined_headers\\teleop.csv"
    concat_teleop_df.to_csv(dest_path, index=False)
    
    
    print("\n\n  Finished combining all header files!  \n\n")
    
    
    
##################################################
if __name__ == "__main__":
    main()