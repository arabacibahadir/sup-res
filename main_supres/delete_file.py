import os
import historical_data


def remove():
    """
    Removes the .csv file that was created by the function "get_historical_data"
    """
    print("Data analysis is done. Browser opening.")
    if os.path.exists(historical_data.file_name):
        os.remove(historical_data.file_name)
        print(f"{historical_data.file_name} deleted.")
    else:
        print("The file does not exist.")
