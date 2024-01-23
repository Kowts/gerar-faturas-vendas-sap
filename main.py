import asyncio
import logging
import pandas as pd
from helpers import *

# Set logging for debug.
logging.basicConfig(level=logging.INFO)

async def main():
    try:
        # Load configuration settings
        config = load_config()

        notify = config['notify']
        database = config['database']

        # sap configs
        sap_db = database['sap']
        sap_app = config['sap_app']
        sap_collection = sap_db['collection']
        sap_query = sap_db['query']
        sap_transaction_code = sap_app['transaction_code']

        # Auth into OpenIAP
        client = await connect_to_service()

        # Initialize the ExceptionHandler
        exception_handler = ExceptionHandler(client, config)

        # Connect to the service and fetch SAP data
        sap_args_data = await fetch_data(client, sap_collection, sap_query)

        if not sap_args_data:
            raise ValueError("No data retrieved for SAP processing.")

        # assuming the first item contains the required data
        sap_args = sap_args_data[0]

        # Validate the structure of the SAP data.
        if 'platform' in sap_args and 'username' in sap_args and 'password' in sap_args:

            # Read Excel file
            excel_file_path = 'resources/ListaSAP.xlsx'
            df = pd.read_excel(excel_file_path)

            print(df)
            exit()

            # Perform Verifications
            column_to_verify = 'Ordem'
            if all(df[column_to_verify] > 0):
                print(f"All values in '{column_to_verify}' are positive.")

            # Perform operation in SAP
            # process_status, text = sap_session.perform_operation(sap_transaction_code, account)


            # mail configs
            subject = notify['subject']
            recipient_email = notify['recipient_email']
            message_body = notify['message_body']

            # Send email
            # await send_email(client, recipient_email, subject, message_body, html_body=True)

        else:
            logging.error("Invalid data format for SAP arguments.")


    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        await exception_handler.get_exception(e)
        logging.error(e)

    finally:
        # Close the connection to the OpenIAP service, if it's open
        if 'client' in locals():
            client.Close()

# Run the main async function
if __name__ == "__main__":
    asyncio.run(main())
