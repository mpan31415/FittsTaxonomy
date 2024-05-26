from pandas import read_csv
from os import getcwd
import matplotlib.pyplot as plt
from scipy.stats import zscore
from numpy import abs, array, column_stack, linspace, meshgrid, sqrt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from math import pi


##################################################
def read_part_data(part_id, operation_type):
    csv_dir = getcwd() + "\\user_study_results\\headers\\part" + str(part_id) + "_" + operation_type + "_header.csv"
    raw_df = read_csv(csv_dir)
    return raw_df

##################################################
def read_data(operation_type):
    # csv_dir = getcwd() + "\\user_study_results\\combined_headers\\"+operation_type+".csv"
    csv_dir = getcwd() + "\\user_study_results\\fitts_headers\\"+operation_type+".csv"
    raw_df = read_csv(csv_dir)
    return raw_df

##################################################
def remove_outliers_zscore(df, column_name, threshold=3):
    
    # Calculate Z-scores for the specified column
    z_scores = zscore(df[column_name])
    
    # Create a mask for non-outliers
    non_outliers_mask = abs(z_scores) < threshold
    
    # Filter the DataFrame
    cleaned_df = df[non_outliers_mask]
    
    return cleaned_df


##################################################
def remove_rot_outlier(df, threshold=pi/2):
    
    non_outliers_mask = df['path_rot'] < threshold
    cleaned_df = df[non_outliers_mask]
    
    return cleaned_df


##################################################
def linreg_and_plot(lst1, lst2, lst3, operation_type:str):

    # Plot the data points
    fig = plt.figure()
    ax = plt.axes(projection ='3d')   
    
    # Convert inputs to numpy arrays
    x1 = array(lst1)
    x2 = array(lst2)
    y = array(lst3)
    
    # Combine independent variables into a single 2D array
    X = column_stack((x1, x2))
    
    # Perform linear regression
    model = LinearRegression()
    model.fit(X, y)
    # Get predictions
    y_pred = model.predict(X)
    
    # Get coefficients and intercept
    coefficients = model.coef_
    intercept = model.intercept_
    
    # Calculate metrics
    r2 = r2_score(y, y_pred)
    rmse = sqrt(mean_squared_error(y, y_pred))
    mae = mean_absolute_error(y, y_pred)
    
    # Print model details and metrics
    print(f"Coefficients: {model.coef_}")
    print(f"Intercept: {model.intercept_}")
    print(f"R-squared (R2): {r2}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"Mean Absolute Error (MAE): {mae}")
    
    # Generate grid for plotting plane
    x1_range = linspace(x1.min(), x1.max(), 10)
    x2_range = linspace(x2.min(), x2.max(), 10)
    x1_grid, x2_grid = meshgrid(x1_range, x2_range)
    y_grid = intercept + coefficients[0] * x1_grid + coefficients[1] * x2_grid
    
    # Plot data points and regression plane
    ax.scatter(x1, x2, y, color='red', label='Data points')
    ax.plot_surface(x1_grid, x2_grid, y_grid, alpha=0.5, color='blue', label='Regression plane')
    
    # axes labels
    ax.set_xlabel("translation")
    ax.set_ylabel("rotation")
    ax.set_zlabel("move time (s)")
    
    # syntax for plotting
    if operation_type == "kt":
        title = "Kinesthetic Teaching"
    if operation_type == "teleop":
        title = "Teleoperation"
    ax.set_title(title)
    plt.show()



##################################################
def main():
    
    # operation_type = "kt"
    operation_type = "teleop"
    
    
    # read data
    df = read_data(operation_type)
    
    # df = remove_outliers_zscore(df, "path_rot")
    df = remove_rot_outlier(df)
    
    
    ###### TYPE NUMBER ######
    type = 2
    
    match type:
        case 1:
            # type 1: use path trans + rot
            trans_list = df['path_trans'].tolist()
            rot_list = df['path_rot'].tolist()
        case 2:
            # type 2: use nominal trans + rot Fitts ID values
            trans_list = df['nom_trans_fid'].tolist()
            rot_list = df['nom_rot_fid'].tolist()
        case 3:
            # type 3: use effective trans + rot Fitts ID values
            trans_list = df['eff_trans_fid'].tolist()
            rot_list = df['eff_rot_fid'].tolist()
        case _:
            print("Did not match any of cases!")
            return
    
    ### output: movement time ###
    time_list = df['move_time'].tolist()
    
    # perform linear regression, and plot the datapoints and the regressed plane
    linreg_and_plot(trans_list, rot_list, time_list, operation_type)
    
    



##################################################
if __name__ == "__main__":
    main()