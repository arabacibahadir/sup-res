import os


def remove(csv_filename):
    """
    Removes the .csv file that was created by the function "get_historical_data"
    """
    print("Data analysis is done. Browser opening.")
    if os.path.exists(csv_filename):
        os.remove(csv_filename)
        print(f"{csv_filename} deleted.")
    else:
        print(f"{csv_filename} does not exist.")
