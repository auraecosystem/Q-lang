# Python 3 and future
import base91
import base85
import base64
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# --- Base64 Utilities ---

def encode_file_to_base64(file_path: str) -> str:
    """Encode a file (binary or text) to Base64 string."""
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    return encoded

def encode_string_to_base64(data: str) -> str:
    """Encode a string to Base64."""
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')

def decode_base64_to_string(encoded_data: str) -> str:
    """Decode a Base64 string back to a normal string."""
    return base64.b64decode(encoded_data.encode('utf-8')).decode('utf-8')

# --- Web/URL Content ---
def encode_url_content_to_base64(url: str) -> str:
    """Fetch content from URL and encode it to Base64."""
    response = requests.get(url)
    response.raise_for_status()
    return base64.b64encode(response.content).decode('utf-8')

# --- API / JSON Payload ---
def encode_json_to_base64(json_data: dict) -> str:
    """Encode JSON-like dictionary into Base64."""
    import json
    json_str = json.dumps(json_data)
    return encode_string_to_base64(json_str)

# --- HTML Content ---
def encode_html_to_base64(html_content: str) -> str:
    """Encode raw HTML content to Base64."""
    return encode_string_to_base64(html_content)

# --- Email Attachment ---
def create_email_with_base64_attachment(sender: str, recipient: str, subject: str, body: str, attachment_path: str) -> MIMEMultipart:
    """Create an email with a Base64 encoded attachment."""
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject
    
    # Attach body text
    message.attach(MIMEText(body, 'plain'))
    
    # Attach file in Base64
    part = MIMEBase('application', 'octet-stream')
    with open(attachment_path, 'rb') as f:
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={Path(attachment_path).name}')
    message.attach(part)
    
    return message

# --- Usage Examples ---

if __name__ == "__main__":
    # Encode file
    print("File Base64:", encode_file_to_base64("example.txt"))
    
    # Encode string
    print("String Base64:", encode_string_to_base64("Hello World!"))
    
    # Encode URL content
    url = "https://www.example.net"
    print("URL Base64:", encode_url_content_to_base64(url))
    
    # Encode JSON for API
    sample_json = {"name": "Alice", "age": 30}
    print("JSON Base64:", encode_json_to_base64(sample_json))
    
    # Encode HTML content
    html_content = "<html><body><h1>Title</h1></body></html>"
    print("HTML Base64:", encode_html_to_base64(html_content))
    
    # Create email with attachment
    email_msg = create_email_with_base64_attachment(
        sender="web4@example.com",
        recipient="recipient@example.com",
        subject="Test Email",
        body="This email contains a Base64 encoded attachment.",
        attachment_path="example.txt"
    )
    print("Email ready to send with attachment:", email_msg.as_string()[:200], "...")  # Print first 200 characters
