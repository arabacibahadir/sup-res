import os
import settings


def remove():
    print("Data analysis is done. Browser opening.")
    if os.path.exists(settings.full_filename):  # <- Delete .csv file
        os.remove(settings.full_filename)
        print(f"{settings.full_filename} deleted.")
    else:
        print("The file does not exist.")
