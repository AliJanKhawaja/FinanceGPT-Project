from bs4 import BeautifulSoup
from simplegmail import Gmail
import os

# ---------------------- Gmail Interaction ---------------------- #

def get_starred_messages():
    """
    Connects to Gmail and retrieves the most recent starred message's HTML content.
    """
    gmail = Gmail(
        client_secret_file=os.path.join("client_secret.json"),
        creds_file=os.path.join("gmail_token.json")
    )

    # Get starred messages
    messages = gmail.get_starred_messages()

    if messages:
        # Return the HTML content of the first starred message
        html_message = messages[0].html
        return html_message
    else:
        return ""

# ---------------------- HTML Parsing Utilities ---------------------- #

def find_image_url(html, class_name):
    """
    Finds the first image URL inside a <p> tag with a specific class name.
    """
    soup = BeautifulSoup(html, 'html.parser')
    image_wrap = soup.find('p', class_=class_name)
    
    if image_wrap and image_wrap.find('img'):
        image_url = image_wrap.find('img')['src']
        return image_url
    
    return "No image found"

def find_class(html):
    """
    Finds the first class name that contains both 'image' and 'wrap'
    (e.g., classes like 'm_xxxxxxx_image-wrap') from the HTML.
    """
    soup = BeautifulSoup(html, 'html.parser')
    classes = set()
    image_classes = []

    # Find all tags that have a class attribute
    tags_with_classes = soup.find_all(class_=True)

    for tag in tags_with_classes:
        class_names = tag.get('class', [])
        classes.update(class_names)

    for class_name in classes:
        if "image" in class_name and "wrap" in class_name:
            image_classes.append(class_name)

    if image_classes:
        return image_classes[0]
    
    return None

# ---------------------- Main URL Extraction ---------------------- #

def get_url():
    """
    Retrieves the heatmap image URL from the most recent starred Gmail message.
    """
    html_message = get_starred_messages()

    if not html_message:
        print("No starred message found.")
        return "No image found"
    
    class_name = find_class(html_message)

    if not class_name:
        print("No suitable class found in the email HTML.")
        return "No image found"
    
    url = find_image_url(html_message, class_name)
    return url

# ---------------------- Execution ---------------------- #

if __name__ == "__main__":
    try:
        result = get_url()
        print(result)
    except Exception as e:
        print(f"Unexpected error in 'get_url': {e}")
