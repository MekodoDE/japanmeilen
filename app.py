import requests
import re
import smtplib
import os
from email.message import EmailMessage

# environment variables
url = os.getenv("URL")
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASSWORD")

# Function to send an email notification
def send_email():
    # Create the email message
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Tokyo Option Found in Dropdown"
    msg.set_content("A Tokyo-related option was found in the dropdown on the website.")
    
    try:
        # Establish a secure session with SMTP server using SMTP_SSL for implicit TLS on port 465
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)  # Login
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Send POST request to fetch the page content
response = requests.post(url, data={
    "originCountry" : "DE",
    "originAirport" : "",
    "destinationAirport" : "",
    "mileage" : "",
    "travelperiod" : "",
    "bookingclass" : "",
    "airline" : ""
})

# Check if request was successful
if response.status_code == 200:
    # Decode content to a string
    html_content = response.text

    print(html_content)
    
    # Use regex to find the select element by its ID and capture its contents
    select_pattern = re.compile(r'<select id="filterDestinationAirport".*?>(.*?)</select>', re.DOTALL)
    select_match = select_pattern.search(html_content)
    
    if select_match:
        select_content = select_match.group(1)
        
        # Use regex to find each option within the select content
        option_pattern = re.compile(r'<option.*?>(.*?)</option>', re.DOTALL)
        options = option_pattern.findall(select_content)
        
        # Check each option for "tokyo" or "tokio"
        tokyo_found = False
        for option in options:
            if "tokyo" in option.lower() or "tokio" in option.lower():
                tokyo_found = True
                print(f"Found Tokyo-related option: {option.strip()}")
                break  # Stop after finding the first match
        
        # Send email if Tokyo-related option is found
        if tokyo_found:
            send_email()
            exit(0)
        else:
            print("No Tokyo-related options found in the dropdown.")
            exit(0)
    else:
        print("Dropdown with id 'filterOriginAirport' not found.")
        exit(1)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    exit(1)