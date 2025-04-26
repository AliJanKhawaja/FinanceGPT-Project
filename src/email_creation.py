import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from utils import get_ticker_data_as_dict, get_date
from logger import logging

def send_email(sender_email, sender_password, subject):
    """
    Sends an email with the newsletter body, ticker data table, and images (logo and heatmap).
    """

    try:
        # Read the body of the newsletter from the file
        with open(f"news_letters//{get_date()}//news_letter_final.txt", "r") as file:
            body = file.read()
    except Exception as e:
        logging.error(f"Error reading newsletter file: {e}")
        return

    # Define SMTP server settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        # Connect and start TLS for security
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        logging.info("Server connection started.")

        # Login to the sender email account
        server.login(sender_email, sender_password)

        # List of receivers
        receivers = ["azarkhowaja111@gmail.com"]

        # Create a MIMEMultipart email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(receivers)
        msg['Subject'] = subject

        # Add a logo image placeholder in the email body
        msg.attach(MIMEText("<img src='cid:logo'>", 'html'))

        # Attach the plain text newsletter body
        msg.attach(MIMEText(body, 'plain'))

        # Get ticker data and create an HTML table
        ticker_data = get_ticker_data_as_dict()
        ticker_data_text = f"""<br><br><b>Here is the day's performance for QQQ and SPY:</b>
        <table border="1">
            <tr>
                <th>Ticker</th>
                <th>Open</th>
                <th>Close</th>
                <th>High</th>
                <th>Low</th>
            </tr>
            <tr>
                <td>QQQ</td>
                <td>{ticker_data["QQQ Open"]}</td>
                <td>{ticker_data["QQQ Close"]}</td>
                <td>{ticker_data["QQQ Highest"]}</td>
                <td>{ticker_data["QQQ Lowest"]}</td>
            </tr>
            <tr>
                <td>SPY</td>
                <td>{ticker_data["SPY Open"]}</td>
                <td>{ticker_data["SPY Close"]}</td>
                <td>{ticker_data["SPY Highest"]}</td>
                <td>{ticker_data["SPY Lowest"]}</td>
            </tr>
        </table>
        """

        msg.attach(MIMEText(ticker_data_text, 'html'))

        # Add heatmap section and image placeholder
        heatmap_text = "<br><br><b>Check out today's Heatmap!</b>"
        msg.attach(MIMEText(heatmap_text, 'html'))
        msg.attach(MIMEText("<img src='cid:heatmap'>", 'html'))

        # Attach the heatmap image
        try:
            with open(f"heatmaps//heatmap-{get_date()}.png", "rb") as image:
                img = MIMEImage(image.read())
                img.add_header('Content-ID', '<heatmap>')
                msg.attach(img)
            logging.info("Heatmap attached.")
        except Exception as e:
            logging.error(f"Error attaching heatmap: {e}")

        # Attach the logo image
        try:
            with open("dags//src//logo.png", "rb") as logo:
                logo_img = MIMEImage(logo.read())
                logo_img.add_header('Content-ID', '<logo>')
                msg.attach(logo_img)
            logging.info("Logo attached.")
        except Exception as e:
            logging.error(f"Error attaching logo: {e}")

        # Send the email
        # server.sendmail(sender_email, get_receivers(f"subscriber_list.txt"), msg.as_string())
        server.sendmail(sender_email, "alijan1234@gmail.com", msg.as_string())

        # Close the SMTP connection
        server.quit()
        logging.info("Email sent successfully.")

    except Exception as e:
        logging.error("Email failed to send.")
        logging.error(e)

if __name__ == "__main__":
    try:
        # Example usage (make sure to replace with actual sender email and password)
        send_email("your_email@example.com", "your_password", "Today's Newsletter")
    except Exception as e:
        logging.error(f"Unexpected error in sending email: {e}")
