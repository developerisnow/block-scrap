import csv
import datetime

start_date = datetime.datetime.strptime("2023-06-04_15:32:00", "%Y-%m-%d_%H:%M:%S")
end_date = datetime.datetime.strptime("2023-06-04_23:00:00", "%Y-%m-%d_%H:%M:%S")
current_date = start_date

with open("timestamp.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["timestamp", "human-readable"])

    while current_date <= end_date:
        timestamp = int(current_date.timestamp())
        human_readable = current_date.strftime("%Y-%m-%d_%H:%M:%S")
        writer.writerow([timestamp, human_readable])

        current_date += datetime.timedelta(seconds=1)

print("timestamp.csv file created successfully!")
