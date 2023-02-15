import csv
import subprocess

with open("coin_list.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        coin_name, timeframe = row
        command = ["python", "../main.py", coin_name, timeframe]
        subprocess.run(command, check=True, shell=True)
