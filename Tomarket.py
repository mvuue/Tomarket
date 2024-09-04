import requests
import random
import time
import sys
import os
from colorama import Fore, Style, init

def countdown_timer(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        print(f"{Fore.CYAN + Style.BRIGHT}Wait {hours:02}:{mins:02}:{secs:02}", end='\r')
        time.sleep(1)
        seconds -= 1
    print("Wait 00:00:00          ", end='\r')

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def art():
    print("\033[1;91m" + r""" ______  _               _    
 | ___ \| |             | |   
 | |_/ /| |  __ _   ___ | | __
 | ___ \| | / _` | / __|| |/ /
 | |_/ /| || (_| || (__ |   < 
 \____/ |_| \__,_| \___||_|\_\
""" + "\033[0m" + "\033[1;92m" + r""" ______                                   
 |  _  \                                  
 | | | | _ __   __ _   __ _   ___   _ __  
 | | | || '__| / _` | / _` | / _ \ | '_ \ 
 | |/ / | |   | (_| || (_| || (_) || | | |
 |___/  |_|    \__,_| \__, | \___/ |_| |_|
                       __/ |              
                      |___/               
""" + "\033[0m" + "\033[1;93m" + r"""  _   _               _                
 | | | |             | |               
 | |_| |  __ _   ___ | | __  ___  _ __ 
 |  _  | / _` | / __|| |/ / / _ \| '__|
 | | | || (_| || (__ |   < |  __/| |   
 \_| |_/ \__,_| \___||_|\_\ \___||_| 
""" + "\033[0m\n\033[1;96m---------------------------------------\033[0m\n\033[1;93mScript created by: Black Dragon Hacker\033[0m\n\033[1;92mJoin Telegram: \nhttps://t.me/BlackDragonHacker007\033[0m\n\033[1;91mVisit my GitHub: \nhttps://github.com/BlackDragonHacker\033[0m\n\033[1;96m---------------------------------------\033[0m\n\033[1;38;2;139;69;19;48;2;173;216;230m-------------[Tomarket Bot]------------\033[0m\n\033[1;96m---------------------------------------\033[0m")
    
def check_proxy(proxy):
    try:
        response = requests.get("http://www.google.com", proxies=proxy, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_proxy():
    try:
        with open("proxy.txt", "r") as file:
            proxies = file.readlines()
            if not proxies:
                print(f"{Fore.RED + Style.BRIGHT}No proxies found in proxy.txt")
                return None
            random.shuffle(proxies)
            for proxy in proxies:
                proxy = proxy.strip()
                if not proxy.startswith("http://") and not proxy.startswith("https://"):
                    proxy = f"http://{proxy}"
                proxy_dict = {
                    "http": proxy,
                    "https": proxy
                }
                if check_proxy(proxy_dict):
                    print(f"{Fore.GREEN + Style.BRIGHT}Live Proxy: {proxy[:3]}.....{proxy[-3:]}")
                    return proxy_dict
            print(f"{Fore.RED + Style.BRIGHT}No working proxies found.")
            return None
    except FileNotFoundError:
        print(f"{Fore.RED + Style.BRIGHT}proxy.txt file not found.")
        return None

def make_request(url, headers, body=None, proxy=None):
    try:
        response = requests.post(url, headers=headers, json=body, proxies=proxy, timeout=10)
        status_code = response.status_code
        response.raise_for_status()
        return response.json(), status_code
    except requests.RequestException as e:
        print(f"Request to {url} failed: {e}")
        return None, response.status_code

def save_token(query_id, token):
    with open("token.txt", "w") as file:
        file.write(f"{query_id}: {token}\n")

def login(query_id, use_proxy, checking_tasks, account_number):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/user/login"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    body = {
        "init_data": query_id,
        "invite_code": "",
        "from": "",
        "is_bot": False
    }
    print(f"{Fore.CYAN + Style.BRIGHT}------Account No.{account_number}------")
    proxy = get_proxy() if use_proxy else None
    if not proxy and use_proxy:
        print(f"{Fore.RED + Style.BRIGHT}Skipping login as no valid proxy is available.")
        return
    
    response_json, status_code = make_request(url, headers, body, proxy)
    if response_json:
        token = response_json.get("data", {}).get("access_token")
        if token:
            save_token(query_id, token)
            game_id, play_pass = check_balance(token, proxy)
            
            claim_daily_reward(token, proxy)
            claim_farming(token, proxy)
            start_farming(token, proxy)
            t_stars = level_data(token, proxy)
            
            # New rank upgrade function call
            upgrade_rank(token, proxy, t_stars)
            
            if checking_tasks:
                check_list(token, proxy, query_id)   
                
            while play_pass > 0:
                play_game(token, proxy)
                claim_game(token, proxy)
                _, play_pass = check_balance(token, proxy)             
                if play_pass <= 0:
                    print(f"{Fore.RED + Style.BRIGHT}No play passes left.")
                    countdown_timer(5)
                    break
        
    else:
        print(f"{Fore.RED + Style.BRIGHT}Token not found in response for query_id: {query_id}")


def check_balance(token, proxy):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/user/balance"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    
    response_json, _ = make_request(url, headers, proxy=proxy)
    if response_json:
        data = response_json.get("data", {})
        balance = data.get("available_balance")
        play_pass = data.get("play_passes")
        game_id = data.get("farming", {}).get("game_id")
        print(f"{Fore.GREEN + Style.BRIGHT}Balance: {balance}")
        print(f"{Fore.CYAN + Style.BRIGHT}Play Pass: {play_pass}")
        return game_id, play_pass  # Return play_pass as well
    return None, None


def claim_daily_reward(token, proxy):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/daily/claim"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    
    body = {"game_id": "fa873d13-d831-4d6f-8aee-9cff7a1d0db1"}
    
    response_json, status_code = make_request(url, headers, body, proxy)
    if response_json:
        status = response_json.get("status")
        if status == 400:
            print(f"{Fore.RED + Style.BRIGHT}Daily Reward Already Claimed")
        elif status == 0:
            check_counter = response_json.get("data", {}).get("check_counter")
            today_points = response_json.get("data", {}).get("today_points")
            print(f"{Fore.GREEN + Style.BRIGHT}Daily Reward Claimed Successfully")
            print(f"{Fore.YELLOW + Style.BRIGHT}Check Counter: {check_counter}")
            print(f"{Fore.MAGENTA + Style.BRIGHT}Today Points: {today_points}")
        else:
            print(f"{Fore.RED + Style.BRIGHT}Unexpected Status Code: {status}")
            print(f"{Fore.RED + Style.BRIGHT}Response Text:", response_json)
    else:
        print(f"{Fore.RED + Style.BRIGHT}Failed to claim daily reward.")


def check_list(token, proxy, query_id):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/tasks/list"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    
    body = {"language_code": "en"}
    
    response_json, _ = make_request(url, headers, body, proxy)
    
    if response_json:
        tasks = response_json.get("data", {}).get("special", []) + \
                response_json.get("data", {}).get("standard", []) + \
                response_json.get("data", {}).get("expire", []) + \
                response_json.get("data", {}).get("default", [])

        if tasks:
            for task in tasks:
                task_id = task.get("taskId")
                task_name = task.get("name")
                wait_second = task.get("waitSecond", 0)  # Get waitSecond, default to 0 if not present
                if task_id is not None:
                    task_start(token, proxy, task_id, query_id, task_name)
                    if wait_second > 0:
                        time.sleep(wait_second)
                    task_check(token, proxy, task_id, query_id, task_name)
                    time.sleep(5)  
                    task_claim(token, proxy, task_id, task_name)
        else:
            print(f"{Fore.RED + Style.BRIGHT}No tasks found in the response.")
    else:
        print(f"{Fore.RED + Style.BRIGHT}Failed to get a valid response.")

def task_start(token, proxy, task_id, query_id, task_name):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/tasks/start"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    
    body = {"task_id": task_id, "init_data": query_id}
    
    _, _ = make_request(url, headers, body, proxy)
    print(f"{Fore.GREEN + Style.BRIGHT}Task Checking: {task_name}")

def task_check(token, proxy, task_id, query_id, task_name):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/tasks/check"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    
    body = {"task_id": task_id, "init_data": query_id}
    
    _, _ = make_request(url, headers, body, proxy)

def task_claim(token, proxy, task_id, task_name):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/tasks/claim"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    
    body = {"task_id": task_id}
    response_json, _ = make_request(url, headers, body, proxy)
    
    if response_json:
        data = response_json.get("data")
        if data == "ok":
            print(f"{Fore.YELLOW + Style.BRIGHT}Task: {task_name} Already Claimed")
        else:
            print(f"{Fore.RED + Style.BRIGHT}Task Not Complete: {task_name}")
    else:
        print(f"{Fore.RED + Style.BRIGHT}Failed to get a valid response.")


def claim_farming(token, proxy):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/farm/claim"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    
    body = {"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"}
    
    response_json, status_code = make_request(url, headers, body, proxy)
    
    if response_json:
        data = response_json.get("data", {})
        points = data.get("points", "No points found")
        finished = data.get("finished")
        
        if finished == True:
            print(f"{Fore.GREEN + Style.BRIGHT}Farming Claimed Successfully")
            print(f"{Fore.YELLOW + Style.BRIGHT}Claimed Points: {points}")
        else:
            print(f"{Fore.RED + Style.BRIGHT}Farming Already Claimed")
    else:
        print(f"{Fore.RED + Style.BRIGHT}Failed to get a valid response.")

def start_farming(token, proxy):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/farm/start"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    
    body = {"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"}
    
    response_json, status_code = make_request(url, headers, body, proxy)
    
    if response_json:
        data = response_json.get("data", {})
        points = data.get("points", "No points found")
        finished = data.get("finished")
        f_points = data.get("points")
    
        if f_points == 0:
            print(f"{Fore.GREEN + Style.BRIGHT}Farming Started Successfully")
        if finished == False:
            if response_json:
                data = response_json.get("data", {})
                mining_points = data.get("points", "No mining points found")
                times = data.get("need_time", "No time found")
                print(f"{Fore.YELLOW + Style.BRIGHT}Again Claim {times} seconds Later")       
                print(f"{Fore.MAGENTA + Style.BRIGHT}Mining Points: {mining_points}")
            else:
                print(f"{Fore.RED + Style.BRIGHT}Failed to get a valid response. Status Code: {status_code}")

def play_game(token, proxy):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/game/play"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    
    body = {"game_id": "59bcd12e-04e2-404c-a172-311a0084587d"}
    
    response_json, _ = make_request(url, headers, body, proxy)
    
    if response_json:
        print(f"{Fore.MAGENTA + Style.BRIGHT}Playing.....")
        time.sleep(32)  # Simulate playing time
    else:
        print(f"{Fore.RED + Style.BRIGHT}Failed to get a valid response. Response: {response_json}")

def claim_game(token, proxy):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/game/claim"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    
    points = random.randint(400, 550)
    body = {"game_id": "59bcd12e-04e2-404c-a172-311a0084587d", "points": points}
    
    response_json, _ = make_request(url, headers, body, proxy)
    
    if response_json:
        data = response_json.get("data", {})
        claimed_points = data.get("points", "No points found")
        print(f"{Fore.YELLOW + Style.BRIGHT}Claimed Points: {claimed_points}")
        return claimed_points
    else:
        print(f"{Fore.RED + Style.BRIGHT}Failed to get a valid response. Response: {response_json}")
        return None

def level_data(token, proxy):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/rank/data"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    
    response_json, _ = make_request(url, headers, proxy)
    if response_json:
        data = response_json.get("data", {})
        rank_info = data.get("currentRank", {}).get("name", "Unknown")
        t_stars = data.get("unusedStars", 0)
        
        print(f"Rank: {rank_info}")
        print(f"Total Stars: {t_stars}")
        
        return t_stars
    return 0    

def upgrade_rank(token, proxy, stars):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/rank/upgrade"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    
    body = {"stars": stars}
    
    response_json, status_code = make_request(url, headers, body, proxy)
    if response_json:
        massage = response_json.get("message")
        if massage == "Star must be greater than zero":
        	print("Not Enough Stars to Upgrade Rank")
        else:
        	print("Rank Upgrade Successfully")
    
def main():
    clear_terminal()
    art()
    try:
        with open('data.txt', 'r') as file:
            query_ids = file.readlines()

        if not query_ids:
            print(f"{Fore.RED + Style.BRIGHT}No query_ids found in data.txt")
            return
        
        use_proxy = input(f"{Fore.WHITE + Style.BRIGHT}Do you use proxy? (y/n): ").lower() == 'y'
        checking_tasks = input(f"{Fore.WHITE + Style.BRIGHT}Do you check tasks? (y/n): ").lower() == 'y'
        clear_terminal()
        art()
        
        while True:
            account_number = 1  # Reset account number for each loop iteration
            for query_id in query_ids:
                login(query_id.strip(), use_proxy, checking_tasks, account_number)
                account_number += 1  # Increment account number
            
            countdown_timer(1*60*60)
            clear_terminal()
            art()


    except FileNotFoundError:
        print(f"{Fore.RED + Style.BRIGHT}data.txt file not found. Please make sure the file exists in the same directory.")
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}An unexpected error occurred: {str(e)}")
        clear_terminal()
        art()

if __name__ == "__main__":
    main()
