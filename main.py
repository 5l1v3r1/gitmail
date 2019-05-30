from collections import defaultdict
import json
import requests
import sys

banner = """
    
      ▄████  ██▓▄▄▄█████▓ ███▄ ▄███▓ ▄▄▄       ██▓ ██▓    
     ██▒ ▀█▒▓██▒▓  ██▒ ▓▒▓██▒▀█▀ ██▒▒████▄    ▓██▒▓██▒    
    ▒██░▄▄▄░▒██▒▒ ▓██░ ▒░▓██    ▓██░▒██  ▀█▄  ▒██▒▒██░    
    ░▓█  ██▓░██░░ ▓██▓ ░ ▒██    ▒██ ░██▄▄▄▄██ ░██░▒██░    
    ░▒▓███▀▒░██░  ▒██▒ ░ ▒██▒   ░██▒ ▓█   ▓██▒░██░░██████▒
     ░▒   ▒ ░▓    ▒ ░░   ░ ▒░   ░  ░ ▒▒   ▓▒█░░▓  ░ ▒░▓  ░
      ░   ░  ▒ ░    ░    ░  ░      ░  ▒   ▒▒ ░ ▒ ░░ ░ ▒  ░
    ░ ░   ░  ▒ ░  ░      ░      ░     ░   ▒    ▒ ░  ░ ░   
          ░  ░                  ░         ░  ░ ░      ░  ░
   
                                                    @daley
"""

print(banner)

def main():
    if len(sys.argv) == 1:
        print(" Usage: {} [username]".format(sys.argv[0]))
        print(" Usage: {} 0days\n".format(sys.argv[0]))
        sys.exit(0)

    username = sys.argv[1]

    initial = requests.get('https://api.github.com/users/' + username)
    json_initial = json.loads(initial.content)

    userid = json_initial['id']
    name = json_initial['name']
    location = json_initial['location']

    print(" Username: " + username)
    print(" User ID: " + str(userid))
    print(" Name: " + str(name))
    print(" Location: " + str(location))

    if json_initial['email'] is None:
        print(" Email: Hidden")
        print("\n Checking commits for email since it's hidden... \n")

        request2 = requests.get('https://api.github.com/users/' + username + '/events')
        json_two = json.loads(request2.content)

        VALID_EMAILS = defaultdict(int)
        max_email_len = 0

        for event in json_two:
            event_id = event['id']
            if "payload" in event:
                if "commits" in event['payload']:
                    commits = event['payload']['commits']
                    for commit in commits:
                        email = commit['author']['email']

                        VALID_EMAILS[email] += 1
                        if len(email) > max_email_len:
                            max_email_len = len(email)
        if VALID_EMAILS:
            print("{: <{pad}}\tTimes seen".format('Email', pad=max_email_len))
            for email_cnt in sorted(VALID_EMAILS.items(), key=lambda ecnt: ecnt[1], reverse=True):
                print("{: <{pad}}\t{}".format(pad=max_email_len, *email_cnt))
            print()
        else:
            print(" No commits found with emails")

    else:
        print(" Email: " + json_initial['email'])

if __name__ == "__main__":
    main()
