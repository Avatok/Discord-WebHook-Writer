import requests
import colorama
import time
import os

def exit_with_delay(seconds):
    time.sleep(seconds)
    exit()

def is_valid_hook(hook):
    response = requests.get(hook)
    return "\"message\": \"Unknown Webhook\"" not in response.text

def send_messages(webhook, name, delay, amount, message, delete_hook):
    counter = 0
    max_count = float('inf') if amount == "inf" else int(amount)

    while counter < max_count:
        try:
            payload = {
                "content": str(message),
                "name": str(name),  # 'username' anstelle von 'name'
                "avatar_url": "https://i.imgur.com/w0CDQoO.png"  # Direkter Bildlink
            }
            response = requests.post(webhook, json=payload)
            
            if response.status_code == 204:
                print(f"{colorama.Back.RED} {colorama.Fore.WHITE}[+] Message Sent!{colorama.Back.RESET}")
            else:
                print(f"{colorama.Back.YELLOW} {colorama.Fore.RED}[-] Sending Failed!{colorama.Back.RESET}")
        except Exception as e:
            print(f"{colorama.Back.RED} {colorama.Fore.WHITE}Error: {e}{colorama.Back.RESET}")
        time.sleep(float(delay))
        counter += 1

    if delete_hook.lower() == "y":
        requests.delete(webhook)
        print(f'{colorama.Fore.RED}⚠️ Webhook Deleted! ⚠️{colorama.Fore.RESET}')
    
    print(f'{colorama.Fore.RED}🔥 FINISHED 🔥{colorama.Fore.RESET}')

def initialize():
    print(f"""{colorama.Fore.RED}
▒▄▀▄░█▒█▒▄▀▄░▀█▀░▄▀▄░█▄▀░░░█░░▒█▒██▀░██▄░█▄█░▄▀▄░▄▀▄░█▄▀░░░█░░▒█▒█▀▄░█░▀█▀▒██▀▒█▀▄
░█▀█░▀▄▀░█▀█░▒█▒░▀▄▀░█▒█▒░░▀▄▀▄▀░█▄▄▒█▄█▒█▒█░▀▄▀░▀▄▀░█▒█▒░░▀▄▀▄▀░█▀▄░█░▒█▒░█▄▄░█▀▄
    """)

    with open("webhook.txt", "r") as file:
        webhook = file.read().strip()

    if webhook == "twoj_webhook":
        print(f"{colorama.Fore.RED}Please enter your webhook in webhook.txt{colorama.Fore.RESET}")
        exit()

    name = "Wumpus"  # Name auf Wumpus ändern
    message = input(f"{colorama.Fore.RED}Enter a message\n> {colorama.Fore.RESET}")
    delay = input(f"{colorama.Fore.RED}Enter a delay (in seconds)\n> {colorama.Fore.RESET}")
    amount = input(f"{colorama.Fore.RED}Enter an amount of messages\n> {colorama.Fore.RESET}")
    delete_hook = input(f"{colorama.Fore.RED}Delete webhook after sending messages? (y/n)\n> {colorama.Fore.RESET}")

    try:
        delay = float(delay)
    except ValueError:
        exit_with_delay(3)

    if not is_valid_hook(webhook) or (not amount.isdigit() and amount != "inf") or delete_hook.lower() not in ["y", "n"]:
        exit_with_delay(3)
    
    send_messages(webhook, name, delay, amount, message, delete_hook)
    exit_with_delay(3)

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')  # Use clear for Unix systems
    colorama.init()
    initialize()
