from pandas import read_csv
from os import getcwd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


##################################################
def read_data(part_id, task_id, trial_id, operation_type):
    
    csv_dir = getcwd()+"/user_study_results/cleaned_traj/"+operation_type+"/part"+str(part_id)+"-task"+str(task_id)+"-t"+str(trial_id)+".csv"
    raw_df = read_csv(csv_dir)
    
    return raw_df


##################################################
def main():
    
    df = read_data(1, 3, 1, "kt")
    
    # get translation points across the traj
    txs = df['tx']
    tys = df['ty']
    tzs = df['tz']
    npoints = len(txs)
    every_n_points = 10
    
    # get the coordinate axes
    xxs = df['xx']
    xys = df['xy']
    xzs = df['xz']

    yxs = df['yx']
    yys = df['yy']
    yzs = df['yz']
    
    zxs = df['zx']
    zys = df['zy']
    zzs = df['zz']
    
    # gripper states
    gr_states = df['gr_state']
    
    # plot
    ax = plt.figure().add_subplot(projection='3d')
    ax.view_init(elev=15., azim=20, roll=0)
    
    # # Set labels
    # ax.set_xlabel('X axis')
    # ax.set_ylabel('Y axis')
    # ax.set_zlabel('Z axis')

    # # Set the range for each axis
    # ax.set_xlim([-10, 10])
    # ax.set_ylim([-10, 10])
    # ax.set_zlim([-10, 10])
    
    grasped_point_plotted = False
    
    # loop through all points
    for i in range(npoints):
        
        # plot grasping point if grasping
        if gr_states[i] == "Grasping" and not grasped_point_plotted:
            ax.scatter([txs[i]], [tys[i]], [tzs[i]], color="k", s=200)
            grasped_point_plotted = True
        
        if i % every_n_points == 0:
            
            # Plot the origin
            ax.scatter([txs[i]], [tys[i]], [tzs[i]], color="k", s=10)

            # Plot the axes (x, y, z)
            ax.quiver(txs[i], tys[i], tzs[i], xxs[i], xys[i], xzs[i], length=0.05, color='r')
            ax.quiver(txs[i], tys[i], tzs[i], yxs[i], yys[i], yzs[i], length=0.05, color='g')
            ax.quiver(txs[i], tys[i], tzs[i], zxs[i], zys[i], zzs[i], length=0.05, color='b')
            
            # ax.quiver(0, 0, 0, 1, 0, 0, length=10, color='r')
            # ax.quiver(0, 0, 0, 0, 1, 0, length=10, color='g')
            # ax.quiver(0, 0, 0, 0, 0, 1, length=10, color='b')

    plt.show()
    
    
    
##################################################
if __name__ == "__main__":
    main()
