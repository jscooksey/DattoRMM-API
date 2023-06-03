"""
Export all clients in DattoRMM to CSV DattoRMM via API

Returns:
    Create CSV file export_all.csv

SwaggerUI: https://syrah-api.centrastage.net/api/swagger-ui/index.html
"""

import os

import pandas as pd
from dotenv import load_dotenv

from dattormmapi import dattormm_api_request, dattormm_get_token


def main():
    """
    Main Function script
    """

    # Load URL and Keys from Environment variables
    load_dotenv()
    api_url = os.environ.get("API_URL")
    api_key = os.environ.get("API_KEY")
    api_secret_key = os.environ.get("API_SECRET_KEY")

    # Specify the API path and data to be used
    api_request = "/v2/account/sites"
    api_request_body = {}
    api_uri = f"{api_url}/api{api_request}"

    # Call dattormm_get_token function using defined parameters
    api_access_token = dattormm_get_token(api_url, api_key, api_secret_key)

    # Initial call of dattormm_api_request function
    results = dattormm_api_request(api_uri, api_access_token, api_request_body)

    # Import the first page of results in to Pandas DataFrame
    df_sites = pd.DataFrame(results["sites"])

    pageDetails = results["pageDetails"]

    # While we still have another page of results continue to that page
    # and concat results in to primary Pandas DataFrame
    while pageDetails["nextPageUrl"]:
        results = dattormm_api_request(pageDetails["nextPageUrl"], api_access_token, api_request_body)
        pageDetails = results["pageDetails"]
        df_sites = pd.concat([df_sites, pd.DataFrame(results["sites"])], ignore_index=True)

    # Convert the remaining devicesStatus column from JSON string to additional DataFrame columns
    df_devicesStatus = pd.json_normalize(df_sites.devicesStatus)
    df_sites = pd.concat([df_sites, df_devicesStatus], axis=1, sort=False)

    # Drop columns not reuired for the export
    df_sites = df_sites.drop(columns=["devicesStatus", "notes", "onDemand", "splashtopAutoInstall", "proxySettings"])

    # Drop the rows of the DattoRMM System Sites that we dont want to keep for CSV export
    df_sites = df_sites[df_sites["name"].str.contains("Managed") == False]
    df_sites = df_sites[df_sites["name"].str.contains("OnDemand") == False]
    df_sites = df_sites[df_sites["name"].str.contains("Deleted Devices") == False]

    df_sites.to_csv("export_all.csv", index=False)


if __name__ == "__main__":
    main()
