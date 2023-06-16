import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import logging

# Configure logging
logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def process_ticket(args):
    ticket, iteration_number, total_tickets = args
    url = "https://blockchainwave.org/tickets/view"
    data = {"ticket_no": str(ticket), "form1": "Submit"}

    # Send POST request
    response = requests.post(url, data=data)
    logging.info(f"Processing by worker #{ticket % num_workers} ticket_no {ticket}, iteration number {iteration_number}/{total_tickets}")

    # Parse HTML response
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the result table
    table = soup.find("table", attrs={"class": "table table-bordered table-sm"})

    # Prepare a dictionary to hold data
    data_dict = {}

    if table:
        # Loop over all rows and collect data
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            key = cols[0].text.strip()  # field name
            value = cols[1].text.strip()  # field value
            data_dict[key] = value
    else:
        logging.info(f"No results found for ticket_no {ticket}")

    return data_dict

# Read timestamp.csv file
df_timestamp = pd.read_csv("timestamp.csv")

# Define the number of workers/threads
num_workers = 1000

# Get the total number of tickets
end_ticket = df_timestamp.shape[0]

# Create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=num_workers) as executor:
    # Prepare arguments for each ticket
    args_list = [(ticket, i+1, end_ticket) for i, ticket in enumerate(df_timestamp["timestamp"])]

    # Process each ticket in parallel
    results = executor.map(process_ticket, args_list)

    # Convert the results to a list of dictionaries, excluding empty results
    list_results = [result for result in results if result]

if list_results:
    # Convert the list of dictionaries to a DataFrame
    df_results = pd.DataFrame(list_results)

    # Export the DataFrame to result.csv
    df_results.to_csv("result.csv", index=False)

    logging.info("Processing completed!")
else:
    logging.info("No non-empty results found. Skipping CSV export.")
