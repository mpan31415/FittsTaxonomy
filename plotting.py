from pandas import read_csv
from os import getcwd


##################################################
def read_data(part_id, task_id, trial_id, operation_type):
    
    csv_dir = getcwd()+"/user_study_results/cleaned_traj/"+operation_type+"/part"+str(part_id)+"-task"+str(task_id)+"-t"+str(trial_id)+".csv"
    raw_df = read_csv(csv_dir)
    raw_df = raw_df.iloc[: , 1:]
    
    return raw_df


##################################################
def main():
    
    df = read_data(1, 1, 1, "kt")
    print(df)
    
    
    
    
##################################################
if __name__ == "__main__":
    main()
