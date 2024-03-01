import yagmail
import markdown
import sys
import re
import csv

if len(sys.argv) < 4:
    print("Usage: python3 main.py <path to host template file (.md)> <path to guest template file (.md)> <path to host-guest file (.csv)> <attachments> ...")
    sys.exit(1)

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

host_template_md_file = sys.argv[1]
guest_template_md_file = sys.argv[2]
host_guest_info_file = sys.argv[3]

attachments = []

argv_iterator = iter(sys.argv)
[next(argv_iterator) for _ in range(4)]

for arg in argv_iterator:
    attachments.append(arg)

def parse_markdown(raw):
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

with open(host_template_md_file, "r") as f:
    host_template = f.read()

parsed_host_template = parse_markdown(host_template)

with open(guest_template_md_file, "r") as f:
    guest_template = f.read()

parsed_guest_template = parse_markdown(guest_template)

def read_host_guest_csv(csv_file):
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

hosts, guests = read_host_guest_csv(host_guest_info_file)

yag = yagmail.SMTP("berkeleyrohp@gmail.com", oauth2_file="credentials.json")

for host in hosts:
    _, host_email, _ = host
    guest_info = ""

    for guest in hosts[host]:
        guest_name, guest_email, guest_phone = guest
        guest_info = guest_info + (f"{', '.join(str(info) for info in guest)}\n")

    guest_info = guest_info.rstrip("\n")
    host_body = parsed_host_template.replace("<GUEST INFORMATION>", guest_info)
    print(f"\nSending email to {bcolors.BOLD}HOST{bcolors.ENDC} {bcolors.OKCYAN}{host}{bcolors.ENDC}")
    for guest in hosts[host]:
        print(f" \u2192 Guest: {bcolors.OKGREEN}{guest}{bcolors.ENDC}")

    yag.send(
        to=host_email,
        subject="Upcoming ROHP Program and Host Information",
        contents=host_body
    )

    # yag.send(
    #     to="berkeleyrohp@gmail.com",
    #     subject="Testing emailing script for HOSTS",
    #     contents=host_body
    # )
        
for guest in guests:
    host_info = ", ".join(str(info) for info in guests[guest])
    guest_body = parsed_guest_template.replace("<HOST INFORMATION>", host_info)
    _, guest_email, _ = guest
    print(f"\nSending email to {bcolors.BOLD}GUEST{bcolors.ENDC} {bcolors.OKCYAN}{guest}{bcolors.ENDC}")
    print(f" \u2192 Host: {bcolors.OKGREEN}{guests[guest]}{bcolors.ENDC}")

    yag.send(
        to=guest_email,
        subject="Upcoming ROHP Program and Host Information",
        contents=guest_body,
        attachments=attachments
    )

    # yag.send(
    #     to="berkeleyrohp@gmail.com",
    #     subject="Testing emailing script for GUESTS",
    #     contents=guest_body,
    #     attachments=attachments
    # )

print("\nDone. \U0001F43B \n")