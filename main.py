import yagmail
import markdown
import sys
import re
import csv

from utils import bcolors, parse_markdown, read_host_guest_csv

# Check length of program arguments
if len(sys.argv) < 4:
    print("Usage: python3 main.py <path to host template file (.md)> <path to guest template file (.md)> <path to host-guest file (.csv)> <attachments> ...")
    sys.exit(1)

# Gather program arguments
host_template_md_file = sys.argv[1]
guest_template_md_file = sys.argv[2]
host_guest_info_file = sys.argv[3]

attachments = []

argv_iterator = iter(sys.argv)
[next(argv_iterator) for _ in range(4)]

for arg in argv_iterator:
    attachments.append(arg)

# Read host email template
with open(host_template_md_file, "r") as f:
    host_template = f.read()
parsed_host_template = parse_markdown(host_template)

# Read guest email template
with open(guest_template_md_file, "r") as f:
    guest_template = f.read()
parsed_guest_template = parse_markdown(guest_template)

# Read host-guest matching .csv file
hosts, guests = read_host_guest_csv(host_guest_info_file)

# Initialize emailing wrapper
yag = yagmail.SMTP("berkeleyrohp@gmail.com", oauth2_file="credentials.json")

# Send emails to hosts
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
        
# Send emails to guests
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