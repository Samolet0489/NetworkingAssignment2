import socket
import sys
from connection_helper import create_connection


def send_request(host, path):
    conn = create_connection((host, 80))  # Use port 80
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    conn.sendall(request.encode())

    response = b""
    while True:
        data = conn.recv(1024)
        if not data:
            break
        response += data

    conn.close()
    return response.decode()


def parse_response(response):
    if "\r\n\r\n" not in response:
        return {}, ""

    header_data, body_data = response.split("\r\n\r\n", 1)
    headers = {}
    for line in header_data.split("\r\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value
    return headers, body_data


def extract_links(html):
    links = []
    pos = html.find('<a href="')
    while pos != -1:
        start_pos = pos + len('<a href="')
        end_pos = html.find('"', start_pos)
        url = html[start_pos:end_pos]
        text_start = html.find('>', end_pos) + 1
        text_end = html.find('</a>', text_start)
        text = html[text_start:text_end]
        links.append((text, url))
        pos = html.find('<a href="', text_end)
    return links


def display_page(host, path):
    response = send_request(host, path)
    if not response:
        print("Error: No response received from server.")
        return [], ""

    headers, body = parse_response(response)

    print("\nResponse Headers:")
    for key, value in headers.items():
        print(f"{key}: {value}")

    if not body:
        print("Error: No body received in response.")
        return [], ""

    links = extract_links(body)
    if links:
        print("\nLinks:")
        for i, (text, link) in enumerate(links):
            print(f"[{i + 1}] {text} -> {link}")
    else:
        print("No links found on this page.")

    return links, path


def main(url):
    if "http://" in url:
        url = url[7:]
    if "/" in url:
        host, path = url.split("/", 1)
        path = "/" + path
    else:
        host = url
        path = "/"

    history = []
    links, current_path = display_page(host, path)
    history.append((links, current_path))

    while True:
        choice = input("\nEnter the number of the link to follow, 'b' to go back, or 0 to exit: ")
        if choice == "0":
            break
        elif choice.lower() == 'b':
            if len(history) > 1:
                history.pop()  # Remove current page
                links, current_path = history[-1]
                print("Going back to the previous page:")
                display_page(host, current_path)
            else:
                print("No previous page to go back to.")
        elif choice.isdigit() and 1 <= int(choice) <= len(links):
            next_url = links[int(choice) - 1][1]
            if not next_url.startswith("/"):
                next_url = "/" + next_url
            links, current_path = display_page(host, next_url)
            history.append((links, current_path))
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
    if len(sys.argv) != 2:
        print("Usage: python webbrowser.py <URL>")
    else:
        main(sys.argv[1])
