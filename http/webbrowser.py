
#---------------------------------------------------------
# GROUP MEMBERS: Alexander Savov and Balazs Csaba Madarasi
#---------------------------------------------------------

# python webbrowser.py localhost/example to run the app

# Needed imports
import sys
from connection_helper import create_connection  # Import the create_connection function from connection_helper module


def send_request(host, path):
    # Establish a TCP connection to the host on port 80 (HTTP)
    conn = create_connection((host, 80))

    # Create an HTTP GET request string
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    # Send the request over the connection
    conn.sendall(request.encode())

    response = b""

    # Continuously receive data from the server
    while True:
        data = conn.recv(1024)
        if not data:
            break
        response += data

    # Close the connection
    conn.close()
    return response.decode()  # Decode the response to a string


# A function to parse the response and make it more readable for humans
def parse_response(response):
    # Check if response contains both headers and body
    if "\r\n\r\n" not in response:
        return {}, ""

    # Split the response into header and body parts
    header_data, body_data = response.split("\r\n\r\n", 1)
    headers = {}

    # Parse headers into a dictionary
    for line in header_data.split("\r\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value
    return headers, body_data


# A function to extract all links from the HTML content, which is needed to go through them
def extract_links(html):
    # Initialize an empty list to store the extracted links
    links = []

    # Find the first occurrence of the <a href=" pattern (start of the link tag) in the HTML content
    pos = html.find('<a href="')

    # Loop until no more <a href=" patterns are found in the HTML content
    while pos != -1:

        # Calculate the starting position of the URL
        start_pos = pos + len('<a href="')  # The beginning of the link tag

        # Find the ending position of the URL by locating the next double quote
        end_pos = html.find('"', start_pos)

        # Extract the URL from the HTML content
        url = html[start_pos:end_pos]

        # Find the starting position of the link text by locating the next closing angle bracket
        text_start = html.find('>', end_pos) + 1

        # Find the ending position of the link text by locating the closing </a> tag
        text_end = html.find('</a>', text_start)

        # Extract the text between the opening <a> tag and the closing </a> tag
        text = html[text_start:text_end]

        # Append a tuple of (link text, URL) to the links list
        links.append((text, url))

        # Find the next occurrence of the <a href=" pattern in the HTML content
        pos = html.find('<a href="', text_end)

    # Return the list of extracted links
    return links


# A function to display (print out in the console) the pages
def display_page(host, path):

    # Send a request to the given host and path, and store the response
    response = send_request(host, path)

    # Check if the response is empty or None, indicating an error in the request
    if not response:
        print("Error: No response received from server.")
        return [], ""  # Return empty list and empty string indicating failure

    # Parse the HTTP response into headers and body
    headers, body = parse_response(response)

    # Print the response headers
    print("\nResponse Headers:")
    for key, value in headers.items():
        print(f"{key}: {value}")

    # Check if the body of the response is empty
    if not body:
        print("Error: No body received in response.")
        return [], ""  # Return empty list and empty string indicating failure

    # Extract and display links from the body content
    links = extract_links(body)

    # If links are found (the list is not empty), print them
    if links:
        print("\nLinks:")
        for i, (text, link) in enumerate(links):
            # Remove "http/" prefix if present in the link
            if link.startswith("http/"):
                link = link[5:]
            print(f"[{i + 1}] {text} -> {link}")
    else:
        # If no links are found, inform the user
        print("No links found on this page.")

    # Return the list of extracted links and the path
    return links, path


def main(url):

    # Remove "http://" from the URL if present
    if "http://" in url:
        url = url[7:]

    # Split the URL into host and path
    if "/" in url:
        host, path = url.split("/", 1)
        path = "/" + path
    else:
        host = url
        path = "/"

    # Initialize browsing history
    history = []

    # Display the initial page and store the links and path in history
    links, current_path = display_page(host, path)
    history.append((links, current_path))

    while True:
        # Prompt the user for input
        choice = input("\nEnter the number of the link to follow, 'b' to go back, or 0 to exit: ")

        # Exit the loop if the user chooses (enters) 0
        if choice == "0":
            break

        # Go back to the previous page if the user chooses (enters) the letter "b"
        # and there is more than 1 page in the history
        elif choice.lower() == 'b':
            if len(history) > 1:
                history.pop()  # Remove current page from history
                links, current_path = history[-1]  # Get the previous page's links and path
                print("Going back to the previous page:")
                display_page(host, current_path)  # Display the previous page
            # If there are not more than 1 pages in the history inform the user that there are no previous pages
            else:
                print("No previous page to go back to.")

        # Follow the selected link if the user's input is a digit and between 1 and the number of links
        elif choice.isdigit() and 1 <= int(choice) <= len(links):
            next_url = links[int(choice) - 1][1]  # Get the URL of the selected link

            # Ensure the URL starts with a '/'
            if not next_url.startswith("/"):
                next_url = "/" + next_url
            links, current_path = display_page(host, next_url)  # Display the next page
            history.append((links, current_path))  # Add the next page to history

        # Handle invalid input
        else:
            print("Invalid choice, try again.")
            if links:
                # Re-display current page links for convenience
                print("\nLinks:")
                for i, (text, link) in enumerate(links):
                    print(f"[{i + 1}] {text} -> {link}")
            else:
                print("No links to display. Enter 0 to exit or 'b' to go back.")


if __name__ == "__main__":

    # Check if the script is executed with exactly one command-line argument (the URL)
    if len(sys.argv) != 2:
        print("Usage: python webbrowser.py <URL>")

    # If not, call the main function with the provided URL argument
    else:
        main(sys.argv[1])
