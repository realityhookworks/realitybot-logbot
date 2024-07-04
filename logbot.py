import requests
import time

# Configuration
file_path = r'C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\chat_log.txt'
webhook_url = 'YOUR_WEBHOOK_HERE'
state_file = 'last_read_line.txt'

def read_last_line_index():
    try:
        with open(state_file, 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return -1

def save_last_line_index(index):
    with open(state_file, 'w') as f:
        f.write(str(index))

def send_message_to_webhook(username, message):
    data = {
        "content": f"`[REALITYHOOK]` `{username}` `{message}`"
    }
    time.sleep(5)
    response = requests.post(webhook_url, json=data)
    return response.status_code == 204

def read_new_lines():
    last_line_index = read_last_line_index()
    new_lines = []

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for i in range(last_line_index + 1, len(lines)):
            try:
                line = lines[i].strip()
                if ':' in line:
                    new_lines.append(line)
            except UnicodeDecodeError:
                print(f"Skipping line due to UnicodeDecodeError: {lines[i].strip()}")

    return new_lines, len(lines) - 1




def main():
    while True:
        new_lines, last_index = read_new_lines()
        
        for line in new_lines:
            if ':' in line:
                username, message = line.split(':', 1)
                if send_message_to_webhook(username, message):
                    print(f'Sent: {username}: {message}')
                else:
                    print(f'Failed to send: {username}: {message}')
        
        save_last_line_index(last_index)
        time.sleep(10)  # Check for new lines every 10 seconds

if __name__ == "__main__":
    main()
