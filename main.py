import asyncio
import json

from login import Login


def get_data_from_doc(file_name):
    with open(file_name, "r") as file:
        data = file.read()
    return data


if __name__ == '__main__':
    proxies = get_data_from_doc("proxies.txt").split("\n")
    accounts = get_data_from_doc("accounts.txt").split("\n")
    if len(accounts) > len(proxies):
        for i in range(int(len(accounts)/len(proxies)) + 1):
            proxies += proxies
    user_agents = json.loads(get_data_from_doc("user-agents.txt"))
    i = 0
    for account in accounts:
        try:
            bot_login = Login(
                proxies[i],
                account,
                user_agents[i]
            )
            i += 1
            loop = asyncio.new_event_loop()
            loop.run_until_complete(asyncio.wait_for(
                bot_login.login_and_add_bots(), 30000))
        except Exception as e:
            print(f"can not add {account}")