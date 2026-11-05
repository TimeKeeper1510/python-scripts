import asyncio
import aiohttp
import time
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

BASE_URL = "https://tavoranode.vip"
URL_DIVIDEND_SETTLEMENT = f"{BASE_URL}/api/deal/user/dividend/settlement"
URL_CHECK_IN = f"{BASE_URL}/api/user/user/sign-in/create"

# ================= ACCOUNTS CONFIGURATION =================
# အကောင့်အသစ်များ ထပ်ထည့်ရန် ဤနေရာတွင် လိုင်းမကွဲဘဲ တစ်ကြောင်းတည်း ဆက်ထည့်ပါ
ACCOUNTS = [
    {
        "name": "Account 1",
        "auth": "w88RLmNHlYtkxxaRTIbt7wNAA+WV7vpcBJIftuOExII6YkpfjyS97sraCUcD/1l4L9InQAD1KDgzgEsAOqbTzpXpgwukMVQ7m8M46uFd+9mp6qfL0DXRWb+IqMcntdo+rN4MTxbjjiDXr6dJqm6w1hjeV4uEp1cYcUfjLbo7jbc="
    },
    {
        "name": "Account 2",
        "auth": "jZxscaF6d2lTmnXyMZKsWp7TxqsfEcRzwAAjG99CtQBaVJTLqhDCQZjVJtt1sn41MZBmhNBEqyVM1nVwHUpVhvDboiqz8bbVwtJlO0ZGTaPL/f047nz1VE4V1xIf7i4XXqWcKXoCcdTq7tSnyS2wuH0hL0lZIQWTEJWye5xud44="
    },{
        "name": "Account 3",
        "auth": "qP1osk2uCTGJC/yUe1nqwncSGzQCgSRQFfflM0KKDdY81uKBqfLjG3vPvWIS1IUq3a5muP7FKluvDl/RDQXxF5tdor5509eSrKf4RaB6QUO73eahhwkfi+5C6UDIc4pwa36/LdKr0cXoDTy1wrErMF6Th9EN/9j6Tsooapr9g5E="
    },{
        "name": "Account 4",
        "auth": "5SmF+G5SHTwRRJqlrjCWLtT1zAiij0W1dkhG1cJfMwky8jywUcvC9SuoAmNH0DtbQVBtSIO6WL+rTonC8cjugr2PE4Io0cc2e1s85vVnOPkWHSzgLPACJfJMh+SjPVDYoCukZxRPfJI2kNPyYkM7F6xSxM66KXEuMyjYemCYlDk="
    },{
        "name": "Account 5",
        "auth": "rDeIGNgWN4ZWpqdwUC4YG6Ab1vbHr17orBlxS0NgHLbuBH2jvHPDDU2qFZ2YnAiHfnBvM2BMxAebS6832mGwUZ5pSZFmohRnsl65LtC8wMC14bYd4ITrVsysEsw9hRGHI3cWEMV1jwsEOREbPIUxtWqZ4g3kKZsTN91Z7gA6uFs="
    },{
        "name": "Account 6",
        "auth": "ifpS1zRC8g6wSpll7fXLq3kOuFeFM62u2f3sfXPmzQL4xVSMTV6GtGo/9BTnEYUxmuSYKOeAU22x6TqqTPD6l4HpMNL8bfkzYgc7MVXn4mhMixurmitKplwGItRrR4GbWQNrpiUfA/288k8g7FNxqwGLFJvP5QKFCT5XYe/ffaM="
    },{
        "name": "Account 7",
        "auth": "feNYB7WZ8/WY6+4JnygQ+Ak3BBQd41xpHjMaPWeYnxZVrshV1CDl5D4wIx6UMfc4A0IqMiWrfqzmfiEqoymxUvMG2NJSWnmx2A16NZhavf9gfLQ+Kzq0RcaG/ncmikKCDm5H0nqtQOLz86D+a6tc0562cXkgRraOiWvZFWzOMUw="
    },{
        "name": "Account 8",
        "auth": "VADWxo7clJvqMUiSjtrvw2efjaui6GiyxFR6itbk68dThTszn2POVkSmFRpY0XFv3xdAI3DvY6Y50ge87Uu2THxOXt3ZSnQt9GEIdy7KQYHtvvuQ1qhwEoCd25SqOGtOrpuJtSENF8W07H+uWJmB2mH2QGP71ns9Cbl41N5SQ94="
    },{
        "name": "Account 9",
        "auth": "nMSSL+DHMqjxtoFA/0/orI2s1lXObg5+5NJIL0xr2eNGRb8aBRUvLPnbcnTO4ltudZ2K8HnHWI77KqYMA0k3FDOqfoPNDbUD1LArMAVNTd+2x+Q16ani2J9uKgphUzcPu53XyJrPj93YZpvcvKyoax5up0oJlv2dquZnjDdkmzc="
    },{
        "name": "Account 10",
        "auth": "hgjyQnexAqSm+8rtJaAHoByCnQGjVNkom0bU+1We16tvhnK37sFD3GZSs5FdiqvfF3L8vAf7qV5P47MQKKzhOqGGS6lCU0HnRhaR3kR+VunXqiSeGvBvKo+AvH0r961DqdJvVFeAPSGE6qNJDMIQktYNMYC8Cy8kVkovsEaor3U="
    },{
        "name": "Account 11",
        "auth": "/e+qjlbgw8bZZ7KUYkdKjw9UxM2YPE3FvlYQ2tb/FsNQPQefrI4rqoak40KPKhAurBhVgd/t+ZwSIHUWBXpOYVu8P/bKiJ0QKMkT0tGTCTzTOEs8OZiY05BdAN5CIL/1CoI50LfiVNKcmQsOygBQwYam3uDtWrLygMLLGZMp/G4="
    },{
        "name": "Account 12",
        "auth": "ujkINu/PWN/ce6PecAcKe8SoCb0wvXTVxUe4dGJcaHNiY/MU9v4vu5dpFPjEmgpo8tcV8z3Z8xKCM05wdf0BgY6J/Zc8nqg0to8afOPKFxcFSnuwMOZGb8Fyde4vh1KlpVGlukrDsG19WEJTl2RnNuqJp84m7tcMa6Wh69hGi7o="
    },{
        "name": "Account 13",
        "auth": "SxKnrpm3FCjHUlem3xFXPBp4Vc10reu4p145bJWfK4fvODsMzDNyx1TBBUuZIKx0J8aeeL/oKopngp3A4mh0T15Ho59YXIfjyJiWt7AvViHDGv9ddWJsTGKgU/XSDZ1AIUrBntqx0kpCwf9YsnDhz62fIzyq222YoFEa83CjFRQ="
    },{
        "name": "Account 14",
        "auth": "1q+lFmXbM+3Wjmk4bl7w+s61/FPMEYxXUmNtVYftbFA2KiN1AOWr3etZapi0pLuI6Gywt9DlYedtLWYxsxqIvEP4ATsQTchMC7YdXDVZRLls2e6jWS98q26bT0YEbeWjFnDhGHGGk06cvVqqZydly44d9gi1uczI5vEvdgGAWVQ="
    },{
        "name": "Account 15",
        "auth": "NGCAy5FRC5Lf/PEyiACzJjDlpXGWwWKAB3Shkyy91JQj+NT8brx3JEetN5jhQrge++7GvJjud109CBOiL4A6uq1Q+L71rMtx0FHTOUrUliIH8ZSZPGbCAg18pUAYgUr9GX2LB3KC9FCoK738aNVJGl8mtCOUIuIB3g5BeyvZiUs="
    },{
        "name": "Account 16",
        "auth": "IJrOMW04WOgeovnmbKjJg5VXiMjUHxjr+i1AqqO6ICf2hpxIsFFNXvEMRpNtAU3nRJi1+dWDm/Vp1ApRNRW4J3Z4ez6TJZAcb6cWZ8zCi5PcPTqSHi5jfAmhx5ZR7PfFX2gcGkw6tdsM+T9tKRAI8l87Twsws770YzHXv2AVYkg="
    },{
        "name": "Account 17",
        "auth": "XHN7iriuJ1Z4ign92//yazCLQaUQhbjlvDy9KJDTCq3kwRS4jIolXITqbnqx1tJOqfFW98ktzYilr03V8+jB+RUSVRrjYETi27naEtEbEd5npd9uMMDCGES1qDlofbWbbC+dy2GKMtE1D9z4KIy+9Vcns1FxcW7B03kvVRVMllw="
    },{
        "name": "Account 18",
        "auth": "Y4bTQt0AvaGyqPFowZxzQsj4bu6o8C91zK0bgoyMXOmm11IIc4OKmO4HXgS1LP8KjzCYQJpmSBsTQnlm0PkXMtsKtu278Hl4VT8l2dRUgj27BG4b0MaFa/vWznmIl95vC6fJF6AtCQomq32m6r1eLFKVbjbFBWFHWqvk4z3uEY4="
    },{
        "name": "Account 19",
        "auth": "xbGIKy8unbI9E7XgDyrUox7Xc/3bmf9Gd3GbcjcspMcB9BgPP42RmUmjCnN1z9gZ09dKPscJrulVANkDsZQzTcQbocs7XY/Og48VfolpBXBJ9RMwSbyttplyh2p6H7ckFtDn1bSY37EJRhPGsXxrfHrdj7EzKYo0SMitFrhed5U="
    },{
        "name": "Account 20",
        "auth": "1DLpgVLT2Is/L4wO6+gLcEERcZmwU/N0FwvyoiSjCL/KuYC8ZOYYS8agxuQKig4Mor80i7dlsuT0FFfr3dZ4LPFrQUFFF/SnxuHQB/8hKA73WqCb9s+5P1PS+KPocdBCfQe4S3SfBViq8iYFyC6wzBC3yCOpXo75ySL59QiPdug="
    },{
        "name": "Account 21",
        "auth": "iSvJ3DgRsmbNViGZoiOmTmDChGq1p1VTQgtqVaCIkS9sOUBOvCJpqCrfQ3OWzcyzHqEkksPQ5Bkr9+1BrhQhtCk75tJKQjYNC8iDupCvl0JVBOfG76RiHFhLYPYPPQfoo+3K9t5EmEOFVEjIJTpVKh7I5KcJ6CcBc8nYXFiKLlg="
    },{
        "name": "Account 22",
        "auth": "qjvF1wcr9lCfomFj7J24lzXPBEAjI7n/lvvOfnj6vNsHAR0xTEw14Jg9eWlNuta0PqaGDAApy7+UgqPMCCOooofpeebGggWoUUMj5783makh9ynPqeKAsXelAM5X42+lXphZJ5A5cXYm7X0FYhyveq1cYeAEsUgdxVUWj8//Y00="
    },{
        "name": "Account 23",
        "auth": "0u332KENzi/fHIfxdqC5wu612MGRAcq7sApgtn5VFzHPcngMFzcmD9e8Gl+1V9IXhvbl6xLP+Sx1A8mducZ9vK+Z/t2pkkBPdnlABJP3KEb0AtLJuYYV/67uAex6C8UL8QNr26MLJi5saTVh1OPLIHwu3SEI0RymCeFrxFhpcHM="
    },{
        "name": "Account 24",
        "auth": "RVMXI6jzTN6Y2cPsR3s431L5C3hO5rWjc/PrmIxc2EeWa/k6OPdetT7ejl0qapkKbLWQ+rRsEOtYxUuFXhldzeMfbpFB57y1hGdRxz/JQZNV6006K4s51wl/SWqEgnM7GbE/R1O1twieeKHSv+pu6zegztzjrKmbraOlFLJzGDs="
    },{
        "name": "Account 25",
        "auth": "+l2TJrGh3F7TJdJeIBu5p2kVOn3pREypxEnXwHA+qoyRHJmF0Y/iXUW1cbS/ywh1X/Q8qDtbo5cjVz+Eu073UxjaKCoNpdccZ+7QIjo6pXxiY8VXz/qQOTbVXvuW3wVsHhZhVQ+4oZAc4JgKXiY//S4OGEem2rS9NZojmH52mYI="
    }
    # ,{
    #     "name": "Account 3",
    #     "auth": "YOUR_NEW_TOKEN_HERE"
    # }
]
# ==========================================================

def get_headers(auth_token, referer_path="", use_offset=False):
    # Python current time မှ 13-digit timestamp အလိုအလျောက် ထုတ်ပေးခြင်း
    base_ms = int(time.time() * 1000)
    if use_offset:
        base_ms += 21600000  # +6 hours offset (လိုအပ်ပါက သုံးရန်)
    current_timestamp = str(base_ms)
    
    return {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": auth_token.strip(),
        "content-type": "application/json",
        "lang": "en",
        "origin": BASE_URL,
        "priority": "u=1, i",
        "referer": f"{BASE_URL}/{referer_path}",
        "sec-ch-ua": '"Chromium";v="156", "Microsoft Edge";v="156", "Not:A-Brand";v="8", "Microsoft Edge WebView2";v="156"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "time": current_timestamp,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36 Edg/156.0.0.0"
    }

# 1. Dividend Settlement (Claim 1 TVR)
async def run_settlement(session, acc):
    now = datetime.now().strftime("%H:%M:%S")
    name = acc["name"]
    token = acc["auth"]

    try:
        headers = get_headers(token, referer_path="", use_offset=False)
        async with session.get(URL_DIVIDEND_SETTLEMENT, headers=headers, timeout=15) as resp:
            data = await resp.text()
            if resp.status == 200 and '"s":2' not in data and "error" not in data.lower():
                print(f"{Fore.GREEN}[{now}] [{name}] 💰 Claim Success (GET): {data}")
            else:
                print(f"{Fore.YELLOW}[{now}] [{name}] Claim Response (GET): {data}")

            # အကယ်၍ Time ကွာဟချက် သို့မဟုတ် POST လိုအပ်ပါက အလိုအလျောက် ထပ်စမ်းပေးမည်
            if resp.status != 200 or '"s":2' in data or "error" in data.lower():
                headers_offset = get_headers(token, referer_path="", use_offset=True)
                async with session.get(URL_DIVIDEND_SETTLEMENT, headers=headers_offset, timeout=15) as resp2:
                    data2 = await resp2.text()
                    if data2 != data:
                        print(f"{Fore.CYAN}[{now}] [{name}] Claim (GET+Offset): {data2}")

                async with session.post(URL_DIVIDEND_SETTLEMENT, headers=headers, json={}, timeout=15) as resp3:
                    data3 = await resp3.text()
                    if resp3.status == 200 and data3 != data:
                        print(f"{Fore.CYAN}[{now}] [{name}] Claim (POST): {data3}")

    except Exception as e:
        print(f"{Fore.RED}[{now}] [{name}] Claim Error: {e}")

# 2. Daily Check-in (tavora.py မှ ပေါင်းထည့်ထားသော အပိုင်း)
async def do_check_in(session, acc):
    now = datetime.now().strftime("%H:%M:%S")
    headers = get_headers(acc["auth"], referer_path="signin")
    
    try:
        async with session.post(URL_CHECK_IN, headers=headers, json={}, timeout=15) as resp:
            data = await resp.text()
            if "prize" in data:
                print(f"{Fore.GREEN}[{now}] [{acc['name']}] ✅ Check-in Success: {data}")
            else:
                print(f"{Fore.YELLOW}[{now}] [{acc['name']}] Check-in Response: {data}")
    except Exception as e:
        print(f"{Fore.RED}[{now}] [{acc['name']}] Check-in Error: {e}")

async def process_account(session, acc):
    print(f"\n{Fore.CYAN}=== 🚀 [{acc['name']}] Processing started ==={Style.RESET_ALL}")
    
    # 1. Run Dividend Claim
    await run_settlement(session, acc)
    await asyncio.sleep(2)
    
    # 2. Run Daily Check-in
    await do_check_in(session, acc)

async def main():
    print(f"{Fore.CYAN}==================================================")
    print(f"   TAVORA Node Claim & Daily Check-in Bot         ")
    print(f"=================================================={Style.RESET_ALL}")
    
    async with aiohttp.ClientSession() as session:
        while True:
            print(f"\n--- Starting Cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
            for acc in ACCOUNTS:
                await process_account(session, acc)
                await asyncio.sleep(3)
                
            wait_hours = 12
            print(f"\n{Fore.BLUE}[*] All accounts processed. Waiting for {wait_hours} hours...{Style.RESET_ALL}\n")
            await asyncio.sleep(wait_hours * 3600)

if __name__ == "__main__":
    asyncio.run(main())