import os
import historical_data


def remove():
    print("Data analysis is done. Browser opening.")
    if os.path.exists(historical_data.file_name):  # Delete .csv file
        os.remove(historical_data.file_name)
        print(f"{historical_data.file_name} deleted.")
    else:
        print("The file does not exist.")
