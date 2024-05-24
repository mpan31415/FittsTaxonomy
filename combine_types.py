from pandas import read_csv, DataFrame, concat
from os import getcwd
from math import sqrt, acos, log2


##################################################
def read_header_data(operation_type):
    csv_dir = getcwd()+"\\user_study_results\\fitts_headers\\"+operation_type+".csv"
    raw_df = read_csv(csv_dir)
    return raw_df


##################################################
def main():
    
    ###### read header dataframes ######
    kt_df = read_header_data("kt")
    teleop_df = read_header_data("teleop")
    
    ### add in "op_type" column ###
    op_type_list = []
    for i in range(kt_df.shape[0]):
        op_type_list.append("kt")
    for i in range(teleop_df.shape[0]):
        op_type_list.append("teleop")
    
    # print(kt_df)
    # print(teleop_df)
    
    concat_df = concat([kt_df, teleop_df], axis=0, ignore_index=True)
    concat_df.insert(4, "op_type", op_type_list)
    # print(concat_df)
    
    dest_path = getcwd() + "\\user_study_results\\fitts_headers\\overall.csv"
    concat_df.to_csv(dest_path, index=False)
    
    print("\n\n  Finished combining header files across operation types!  \n\n")
    
    
    
##################################################
if __name__ == "__main__":
    main()