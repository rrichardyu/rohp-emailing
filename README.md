# Host-Guest Emailing

## Usage

1. Add any attachments you'd like to send to `/attachments`
2. Add host-guest matching data to `/matchings`
3. Modify email templates
4. Add OAuth2 token (`credentials.json`) to the project. You'll download this from [Google Cloud Platform](console.cloud.google.com/apis/credentials) (switch to the Berkeley ROHP Google account). Click "Create Credentials" > "OAuth Client ID" > "Desktop app" > "Create". Then, download the JSON. 

Run the emailing script: `python3 main.py templates/{HOST-EMAIL-TEMPLATE} templates/{GUEST-EMAIL-TEMPLATE} matchings/{HOST-GUEST-MATCHING-DATA} attachments/{ATTACHMENT} ...`. You can add as many attachments as you'd like to send.

For example, if you want to send emails to all hosts and guests for the March 2-3 program, you would run `python3 main.py templates/march2-host.md templates/march2-guest.md matchings/march2.csv attachments/2024-Overnight.pdf attachments/APR_directions.pdf`. This would send 2 attachments with the guest email: the overnight agenda and the directions to the Unit 2 APR.
