import matplotlib.pyplot as plt
import pandas as pd
from transformers import pipeline
from fpdf import FPDF
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from appium.options.android import UiAutomator2Options
import pandas as pd


#Validation Class

class SemanticValidator:
    def __init__(self):
        # Initialize the semantic similarity model
        self.similarity_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.total_cases = 0
        self.passed_cases = 0
        self.failed_cases = 0
        self.pass_or_fail = 0

    def validate_response(self, actual_response, expected_responses):
        """Validates the response using semantic similarity."""
        self.total_cases += 1  # Increment total cases
        print("\nValidating response...")
        result = self.similarity_model(actual_response, candidate_labels=expected_responses)
        scores = result['scores']
        highest_score = max(scores)
        best_match = expected_responses[scores.index(highest_score)]
        print(f"Actual Response: {actual_response}")
        print(f"Best Match: {best_match}")
        print(f"Similarity Score: {highest_score}")
        if highest_score > 0.75:
            print("Validation Passed: Response is relevant.\n")
            self.passed_cases += 1  # Increment passed cases
            self.pass_or_fail = 1
            return True
        else:
            print("Validation Failed: Response is not relevant.\n")
            self.failed_cases += 1  # Increment failed cases
            self.pass_or_fail = 0
            return False

    def print_summary(self):
        """Prints a summary of the test results."""
        print(f"Total Test Cases: {self.total_cases}")
        print(f"Passed Test Cases: {self.passed_cases}")
        print(f"Failed Test Cases: {self.failed_cases}")

    def prepare_pdf(self):
        pass_rate = round((self.passed_cases / self.total_cases) * 100, 2)
        fail_rate = round((self.failed_cases / self.total_cases) * 100, 2)

        # Create a pie chart
        plt.figure(figsize=(8, 6))
        labels = ['Pass Count', 'Fail Count']
        sizes = [self.passed_cases, self.failed_cases]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
        plt.title('Automation Test Report')

        pie_chart_image = "test_report_pie_chart.png"
        plt.savefig(pie_chart_image)
        plt.close()

        # Create a DataFrame for the table
        report_data = pd.DataFrame({
            "Metric": ["Number of Test Cases", "Passed Cases Count", "Failed Cases Count", "Pass Rate", "Fail Rate"],
            "Value": [self.total_cases, self.passed_cases, self.failed_cases, f"{pass_rate}%", f"{fail_rate}%"]
        })

        # Generate PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        # Add title
        pdf.set_font("Arial", size=16, style='B')
        pdf.cell(200, 10, txt="Automation Test Report", ln=True, align='C')
        # Add table
        pdf.set_font("Arial", size=12)
        pdf.ln(10)  # Line break
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(100, 10, txt="Metric", border=1, align='C', fill=True)
        pdf.cell(100, 10, txt="Value", border=1, align='C', fill=True)
        pdf.ln()
        for index, row in report_data.iterrows():
            pdf.cell(100, 10, txt=row["Metric"], border=1)
            pdf.cell(100, 10, txt=str(row["Value"]), border=1)
            pdf.ln()

        # Add pie chart image to PDF
        pdf.ln(10)
        pdf.image(pie_chart_image, x=60, y=None, w=90)

        # Add a custom line of text
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(0, 10, txt='Test cases - 1 to 24 are Historical events | 25 to 50 are Freedom fighters | 51 to 80 are Political events')

        # Save PDF
        pdf_output_path = "Automation_Test_Report.pdf"
        pdf.output(pdf_output_path)
        pdf_output_path



# Appium Automation Functions
def start_appium_session():
    """Starts the Appium session with the desired capabilities."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Pixel_9_Pro_XL_API_35"  # Match emulator/device name
    options.platform_version = "15.0"  # Match emulator version
    options.app_package = "ai.perplexity.app.android"
    options.app_activity = "ai.perplexity.app.android.ui.main.MainActivity"
    options.automation_name = "UiAutomator2"
    options.new_command_timeout = 3600

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    print("Session started successfully!")
    return driver

def click_cancel(driver):
    """Clicks the 'Cancel' button."""
    try:
        element = driver.find_element("xpath", '//android.widget.TextView[@text="Cancel"]')
        element.click()
        print("Clicked 'Cancel'")
        sleep(2)
    except NoSuchElementException as e:
        print(f"'Cancel' element not found: {e}")

def click_ask_anything(driver):
    """Clicks the 'Ask anything...' input field."""
    try:
        element = driver.find_element("xpath", '//android.widget.TextView[@text="Ask anything…"]')
        element.click()
        print("Clicked 'Ask anything...'")
        sleep(2)
    except NoSuchElementException as e:
        print(f"'Ask anything...' element not found: {e}")

def enter_text(driver, text):
    """Enters text into the input field."""
    try:
        input_field = driver.find_element("xpath", '//android.widget.EditText')	
        input_field.click()
        sleep(1)
        input_field.send_keys(text)
        print(f"Entered text: {text}")
        sleep(2)
    except NoSuchElementException as e:
        print(f"Input field not found: {e}")

def click_send_button(driver):
    """Clicks the 'Send' button."""
    try:
        send_button = driver.find_element(
            "xpath", 
            '//X0.p1/android.view.View/android.view.View/android.view.View[2]/android.view.View[3]/android.widget.Button'
        )
        send_button.click()
        print("Clicked 'Send'")
        sleep(20)
    except NoSuchElementException as e:
        print(f"'Send' button not found: {e}")

def click_copy_button_and_get_response(driver):
    """Clicks the 'Copy' button and retrieves copied text."""
    try:
        copy_button = driver.find_element(
            "xpath", 
            '(//android.widget.ImageView[@content-desc="icon"])[5]'
        )
        copy_button.click()
        print("Clicked 'Copy'")
        sleep(2)

        # Get copied text from clipboard
        copied_text = driver.get_clipboard_text()
        return copied_text

    except NoSuchElementException as e:
        copy_button= driver.find_element("xpath", '(//android.widget.ImageView[@content-desc="icon"])[3]')
        copy_button.click()
        print("Clicked 'Copy'")
        sleep(2)

        # Get copied text from clipboard
        copied_text = driver.get_clipboard_text()
        return copied_text
    except Exception as e:
        print(f"An error occurred while copying text: {e}")
        return None

def click_Followup_button(driver):
    """Clicks the 'Send' button."""
    try:
        Followup_button = driver.find_element(
            "xpath", 
            '//android.widget.TextView[@text="Ask follow-up…"]'
        )
        sleep(5)
        Followup_button.click()
        print("Clicked 'Follow up'")
        sleep(2)
    except NoSuchElementException as e:
        print(f"'Follow up' button not found: {e}")

def click_Followup_Send_button(driver):
    """Clicks the 'Send' button."""
    try:
        Followup_send_button = driver.find_element(
            "xpath", 
            '//X0.p1/android.view.View/android.view.View[3]/android.view.View[3]/android.widget.Button'
        )
        Followup_send_button.click()
        print("Clicked 'send'")
        sleep(5)
    except NoSuchElementException as e:
        print(f"'send' button not found: {e}")

def click_Followup_exit_button(driver):
    """Clicks the 'Send' button."""
    try:
        Followup_send_button = driver.find_element(
            "xpath", 
            '//X0.p1/android.view.View/android.view.View[1]/android.view.View[1]/android.widget.Button'
        )
        Followup_send_button.click()
        print("Clicked 'exit'")
        sleep(5)
    except NoSuchElementException as e:
        print(f"'exit' button not found: {e}")



def read_test_cases_from_excel_multiple_questions(file_path):
    """Reads test cases from an Excel file."""
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return pd.DataFrame()
	
def read_test_cases_from_excel_single_question(file_path):
    """Reads test cases from an Excel file."""
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return pd.DataFrame()
    

def main(test_case_id,input_text,expected_responses,driver,validator):
    """Main function to initialize and run the Appium automation."""

    if test_case_id == 'a':
            click_ask_anything(driver)
            enter_text(driver, input_text)
            click_send_button(driver)
            actual_response = click_copy_button_and_get_response(driver)
            if actual_response:
                validator.validate_response(actual_response, expected_responses)


    elif test_case_id == 'b':
            click_Followup_button(driver)
            enter_text(driver, "What were its outcomes?")
            click_Followup_Send_button(driver)
            actual_response = click_copy_button_and_get_response(driver)
            if actual_response:
                validator.validate_response(actual_response, expected_responses)
            click_Followup_exit_button(driver)

    else:
        click_ask_anything(driver)
        enter_text(driver, input_text)
        click_send_button(driver)
        actual_response = click_copy_button_and_get_response(driver)
        if actual_response:
            validator.validate_response(actual_response, expected_responses)
        click_Followup_exit_button(driver)

if __name__ == "__main__":

    main()
