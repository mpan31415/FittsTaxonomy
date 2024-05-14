from pandas import read_csv
from os import getcwd
import matplotlib.pyplot as plt


##################################################
def read_data(part_id, operation_type):
    csv_dir = getcwd() + "\\user_study_results\\headers\\part" + str(part_id) + "_" + operation_type + "_header.csv"
    raw_df = read_csv(csv_dir)
    return raw_df



##################################################
def main():
    
    df = read_data(1,"kt")
    print(df)
    
    trans_list = df['path_trans'].tolist()
    rot_list = df['path_rot'].tolist()
    time_list = df['move_time'].tolist()
    
    # syntax for 3-D projection
    ax = plt.axes(projection ='3d')
    
    ax.scatter(trans_list, rot_list, time_list)
    
    # syntax for plotting
    ax.set_title('3d Scatter plot')
    plt.show()



##################################################
if __name__ == "__main__":
    main()