from pandas import read_csv
from os import getcwd
import matplotlib.pyplot as plt


##################################################
def read_data(part_id, task_id, trial_id, operation_type):
    
    csv_dir = getcwd()+"/user_study_results/cleaned_traj/"+operation_type+"/part"+str(part_id)+"-task"+str(task_id)+"-t"+str(trial_id)+".csv"
    raw_df = read_csv(csv_dir)
    
    return raw_df


##################################################
def main():
    
    df = read_data(6, 3, 1, "teleop")
    
    # get translation points across the traj
    txs = df['tx']
    tys = df['ty']
    tzs = df['tz']
    
    # plot
    ax = plt.figure().add_subplot(projection='3d')
    ax.scatter(txs, tys, tzs, label='trajectory')
    ax.view_init(elev=15., azim=20, roll=0)
    
    plt.show()
    
    
    
##################################################
if __name__ == "__main__":
    main()
