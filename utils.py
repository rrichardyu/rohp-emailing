import csv
import re
import sys

# Class for terminal colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def read_host_guest_csv(csv_file: str):
    """Processes host-guest matching .csv and returns corresponding dictionary.
    
    Args:
        csv_file (str): path to host-guest matching .csv file

    Returns:
        hosts (dict): mapping from host to matched guest(s)
        guests (dict): mapping from guest to matched host
    """
    hosts = {}
    guests = {}

    with open(csv_file, mode="r", encoding="utf-8-sig") as file:
        csv_file = csv.reader(file)
        next(csv_file) 

        for line in csv_file:
            line = list(line)
            host_name, host_email, host_phone = line[0], line[1], line[2]
            guest_name, guest_email, guest_phone = line[3], line[4], line[5]

            # Validate email addresses
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", host_email) or not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", guest_email):
                print("Invalid email address")
                sys.exit(1)

            host = (host_name, host_email, host_phone)
            guest = (guest_name, guest_email, guest_phone)

            if host in hosts:
                hosts[host].append(guest)
            else:
                hosts[host] = [guest]

            guests[guest] = host

    return hosts, guests

def parse_markdown(raw: str):
    """Parses email template and returns properly formatted HTML code.
    
    Args:
        raw (str): raw markdown text

    Returns:
        str: formatted email template with HTML code as needed
    """
    # Replace all bolded text with strong tags
    raw = re.sub(r"\*\*([^*]+)\*\*", lambda match: f"<strong>{match.group(1)}</strong>", raw)

    # Replace all links with anchor tags
    raw = re.sub(r"\[([^\]]+)\]\((.*?)\)", lambda match: f"<a href=\"{match.group(2)}\">{match.group(1)}</a>", raw)

    # Format list using ul and li tags
    raw = raw.replace("<!-- BEGIN LIST -->", "<ul>").replace("<!-- END LIST -->", "</ul>").replace("<ul>\n", "<ul>").replace("</ul>\n", "</ul>")
    raw = raw.replace("<!-- GUEST INFORMATION -->", "<GUEST INFORMATION>")
    raw = raw.replace("<!-- HOST INFORMATION -->", "<HOST INFORMATION>")
    raw = re.sub(r"\*\s(.*)", lambda match: f"<li>{match.group(1)}</li>", raw)

    return raw