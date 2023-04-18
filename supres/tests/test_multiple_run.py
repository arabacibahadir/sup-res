import subprocess
import pytest
import csv


@pytest.mark.parametrize("coin_name,timeframe", [("BTCUSDT", "1H"), ("ETHUSDT", "4H")])
def test_script_runs_successfully(coin_name, timeframe):
    # Run the main.py script with the required parameters
    command = ["python", "../src/main.py", coin_name, timeframe]
    completed_process = subprocess.run(command, check=True, shell=True)
    assert completed_process.returncode == 0


def test_csv_file_is_accessible():
    # Check if the CSV file exists and can be opened
    with open("miniscripts/coin_list.csv") as csvfile:
        reader = csv.reader(csvfile)
        assert reader is not None
