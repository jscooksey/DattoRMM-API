"""
Set variable from CSV import in DattoRMM 

Returns:
    Adds Site Varibale

SwaggerUI: https://syrah-api.centrastage.net/api/swagger-ui/index.html
"""

import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv

from dattormmapi import (dattormm_api_new_site_variable, dattormm_api_put,
                         dattormm_api_site_variables,
                         dattormm_api_update_site_variable, dattormm_get_token)


def main():
    """
    Main Function script
    """

    # Load URL and Keys from Environment variables
    load_dotenv()
    api_url = os.environ.get("API_URL")
    api_key = os.environ.get("API_KEY")
    api_secret_key = os.environ.get("API_SECRET_KEY")

    # Load in CSV of variable names

    csv_filename = r"data/all_data_20230602.csv"
    df_variables = pd.read_csv(csv_filename)

    api_access_token = dattormm_get_token(api_url, api_key, api_secret_key)


    for index, row in df_variables.iterrows():
        str_install = f"CUSTOMERID={row.nc_id} REGISTRATION_TOKEN={row.nc_token}"
        if(not np.isnan(row.datto_id)):


            variable_list = dattormm_api_site_variables(api_url=api_url, api_access_token=api_access_token, site_uid=row.datto_uid)
   
            id = 0
            for variable in variable_list:
                if variable['name'] == 'strInstall':
                    id = variable['id']
            
            if id == 0:
                dattormm_api_new_site_variable(api_url, api_access_token, site_uid=row.datto_uid, value=str_install)
            else:
                dattormm_api_update_site_variable(api_url, api_access_token, site_uid=row.datto_uid, var_id=id, value=str_install)

            print(row.psa_name)
            print(str_install)
        


if __name__ == "__main__":
    main()
