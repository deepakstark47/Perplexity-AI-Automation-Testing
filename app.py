import os
from flask import Flask, render_template, Response, stream_with_context, send_file
import pandas as pd
from uploads.main import click_cancel, main, SemanticValidator, start_appium_session
import json
import time

app = Flask(__name__)

@app.route('/')
def index():
    """Root endpoint to serve the UI."""
    return render_template('index.html')

def stream_test_updates():
    """Stream test case updates dynamically."""
    try:
        # Path to test cases Excel file
        multiple_file_path = "D:\\cmpe287\\Automation_script\\test_cases_.xlsx"
        df = pd.read_excel(multiple_file_path)
        driver = None
        validator = SemanticValidator()

        print("Starting Appium session...")
        driver = start_appium_session()
        click_cancel(driver)

        print(f"Loaded {len(df)} test cases.")
        for index, row in df.iterrows():
            test_case_id = row["TestCaseID"]
            input_text = row["Input"]
            expected_responses = row["Expected Responses"].split("||")

            # Stream initial details with "Processing" status
            initial_result = {
                "test_case_id": test_case_id,
                "input": input_text,
                "status": "Processing"
            }
            yield f"data: {json.dumps(initial_result)}\n\n"
            time.sleep(1)  # Simulate delay for frontend responsiveness

            # Process the test case
            try:    
                print(f"Processing Test Case ID: {test_case_id}")
                main(test_case_id, input_text, expected_responses, driver, validator)
                passed = validator.pass_or_fail
                final_result = {
                    "test_case_id": test_case_id,
                    "input": input_text,
                    "status": "Passed" if passed == 1 else "Failed"
                }
                print(f"Result for Test Case ID {test_case_id}: {final_result['status']}")
            except Exception as e:
                final_result = {
                    "test_case_id": test_case_id,
                    "input": input_text,
                    "status": "Failed",
                    "error": str(e)
                }
                print(f"Error in Test Case ID {test_case_id}: {str(e)}")

            # Stream final result
            yield f"data: {json.dumps(final_result)}\n\n"
            time.sleep(1)  # Simulate delay for better UX
        yield f"data: {json.dumps({'completed': True, 'message': 'All test cases have run successfully!'})}\n\n"

    except Exception as e:
        # Handle errors
        error_message = {"error": str(e)}
        print(f"Unexpected error: {str(e)}")
        yield f"data: {json.dumps(error_message)}\n\n"
    finally:
        if driver:
            driver.quit()
            validator.print_summary()
            validator.prepare_pdf()
@app.route('/upload', methods=['GET'])
def upload_files():
    """Route for streaming test updates."""
    return Response(stream_with_context(stream_test_updates()), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
