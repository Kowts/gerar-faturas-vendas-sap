import subprocess
import time
import logging
import win32com.client as win32
from datetime import datetime, timedelta
from helpers.configuration import *
import keyboard
import sys


# Define the SapGui class
class SapGui():

    # This code opens a SAP session using the win32 library.
    def __init__(self, sap_args):

        try:

            # Load configuration settings
            config = load_config()
            sap = config['sap_app']

            # Initialize instance variables for SAP configurations
            self.system = sap_args["platform"]
            self.client = sap['client']
            self.user = sap_args["username"]
            self.password = sap_args["password"]
            self.language = sap['language']

            # Path to SAPLogon executable
            self.path = sap['path']

            # Open SAPLogon
            subprocess.Popen(self.path)
            time.sleep(2)  # Give it some time to open

            # Connect to the SAP GUI Scripting engine
            self.SapGuiAuto = win32.GetObject("SAPGUI")
            if not isinstance(self.SapGuiAuto, win32.CDispatch):
                return None

            # Get the SAP Scripting engine
            application = self.SapGuiAuto.GetScriptingEngine
            if not isinstance(application, win32.CDispatch):
                self.SapGuiAuto = None
                return None

            # Open a connection to the SAP system
            self.connection = application.OpenConnection(self.system, True)
            if not isinstance(self.connection, win32.CDispatch):
                application = None
                self.SapGuiAuto = None
                return None

            # Wait for the connection to be established
            time.sleep(3)

            # Get the first available session
            self.session = self.connection.Children(0)
            if not isinstance(self.session, win32.CDispatch):
                self.connection = None
                application = None
                self.SapGuiAuto = None
                return None

            # Resize the SAP GUI window
            self.session.findById("wnd[0]").resizeWorkingPane(169, 30, False)

            # Maximize the main window (window 0) in SAP GUI.
            # self.session.findById("wnd[0]").maximize()

        except Exception as e:
            logging.error(f"An exception occurred in __init__: {str(e)}")
            return None

    # Method to login to SAP using the SAP GUI Scripting API and the win32 library.
    def sapLogin(self):
        try:
            # Set the SAP login credentials and language in the GUI
            self.session.findById("wnd[0]/usr/txtRSYST-MANDT").text = self.client  # Mandante
            self.session.findById("wnd[0]/usr/txtRSYST-BNAME").text = self.user  # Utilizador
            self.session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = self.password  # Password
            self.session.findById("wnd[0]/usr/txtRSYST-LANGU").text = self.language  # Idioma

            # Perform the login
            self.session.findById("wnd[0]").sendVKey(0)

            # Wait for a short time to see if any popup appears
            time.sleep(2)

            # Check for the specific popup window
            if self.session.ActiveWindow.Name == "wnd[1]":
                # Check if the popup is the multiple login warning by checking some unique text or title
                if "logon múltiplo" in self.session.findById("wnd[1]").Text:
                    logging.info("Multiple logins detected. Closing other sessions.")
                    # Select the option to close other sessions and click OK
                    self.session.findById("wnd[1]/usr/radMULTI_LOGON_OPT1").select()
                    self.session.findById("wnd[1]/tbar[0]/btn[0]").press()

                    # click enter to close the popup
                    shell = win32.Dispatch("WScript.Shell")
                    shell.SendKeys("{ENTER}", 0)

            # Check if login is successful by finding a UI element that appears only when logged in
            if self.session.findById("wnd[0]/tbar[0]/btn[15]"):
                # login sucessfull
                logging.info("Successfully connected to SAP.")
                return True
            else:
                # Login failed and Close the SAP GUI connection
                self.close_connection()
                return False

        except Exception as e:
            logging.error(f"Error during SAP login: {str(e)}")
            logging.error(sys.exc_info())


    # A method to close a SAP connection
    def close_connection(self):
        # Check if a connection object exists
        try:
            if self.connection is not None:
                self.connection.CloseSession('ses[0]')
                # Set the connection to None, indicating it's closed
                self.connection = None
                # Log a message indicating that the SAP connection is closed
                logging.info("SAP connection closed.")
            if self.SapGuiAuto is not None:
                self.SapGuiAuto = None
            logging.info("SAP connection closed safely.")
        except Exception as e:
            # Handle any exceptions that may occur during the closing process
            # Log an error message with details about the exception
            logging.error(f"Error closing SAP connection: {str(e)}")


    def sapLogout(self):
        """
        Logs out of SAP.

        Args:
            self: The instance of the SAP session.

        Raises:
            Exception: If there is an error during SAP logout.

        Examples:
            sap_session = SAPSession()
            sap_session.sapLogout()
        """
        try:
            # Enter the logout command '/nex' in the command field
            self.session.findById("wnd[0]/tbar[0]/okcd").text = "/nex"
            self.session.findById("wnd[0]").sendVKey(0)

            logging.info("Successfully logged out of SAP.")
        except Exception as e:
            logging.error(f"Error during SAP logout: {str(e)}")


    @staticmethod
    def get_dates():
        current_date = datetime.now()

        # Get the first day of the current month
        first_day_current_month = current_date.replace(day=1)

        # Subtract one day from the first day of the current month to get the last day of the previous month
        previous_month_last_day = first_day_current_month - timedelta(days=1)

        # Set the start_date as the first day of the previous month
        start_date = previous_month_last_day.replace(day=1).strftime("%d.%m.%Y")
        end_date = current_date.strftime("%d.%m.%Y")

        return start_date, end_date


    # Waits for the SAP GUI element with the specified ID to appear within the given timeout.
    def wait_for_element(self, element_id, timeout=60):
        """
        Args:
            element_id (str): SAP GUI Scripting ID of the element to wait for.
            timeout (int, optional): The number of seconds to wait for the element. Defaults to 60.

        Returns:
            bool: True if the element appears within the timeout, otherwise False.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if self.session.findById(element_id):
                    return True
            except Exception:
                time.sleep(1)  # wait for 1 second before trying again
        return False

    def get_sap_element_text(self, element_path):
        """
        Retrieves the text of a SAP element identified by the given element_path.

        Args:
            element_path (str): The path of the SAP element.

        Returns:
            str: The text of the SAP element, or None if the element is not found or an error occurs.
        """
        try:
            element = self.session.FindById(element_path)
            return element.Text
        except Exception as e:
            print(f"Error: {e}")
            return None


    # Enter a command in the SAP command field, submit, and perform additional operations.
    def perform_operation(self, command, ordem):
        """
        Performs the specified command in the SAP GUI.

        Args:
            command (str): The command to be executed.

        Returns:
            None
        """
        try:

            # Set the value of the specified field and Submit the command
            self.session.findById("wnd[0]/tbar[0]/okcd").text = command
            self.session.findById("wnd[0]").sendVKey(0)

            # Wait for a specific element from the new page to be present
            element_to_wait_for = "wnd[0]/tbar[1]/btn[5]"

            # Element found, now perform the operations for the new page
            if self.wait_for_element(element_to_wait_for):
                # Set the text
                self.session.findById("wnd[0]/usr/ctxtVBAK-VBELN").text = "5100234350"

                self.session.findById("wnd[0]/usr/ctxtVBAK-VBELN").text = "5100234350"
                self.session.findById("wnd[0]/tbar[1]/btn[5]").press()
                self.session.findById("wnd[1]/tbar[0]/btn[0]").press()
                self.session.findById("wnd[0]/mbar/menu[3]/menu[13]/menu[0]/menu[0]").select()
                self.session.findById("wnd[0]/tbar[1]/btn[5]").press()
                self.session.findById("wnd[0]/usr/cmbNAST-VSZTP").key = "4"
                self.session.findById("wnd[0]/tbar[0]/btn[3]").press()
                self.session.findById("wnd[0]/tbar[0]/btn[11]").press()

        except Exception as e:
            logging.error(f"Error during command execution: {str(e)}")
