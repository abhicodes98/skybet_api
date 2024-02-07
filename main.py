import uuid , requests ,os, time ,json,io,re
from datetime import datetime
import xml.etree.ElementTree as ET 

from flask import Flask, jsonify, request, abort
import  pandas as pd
from dotenv import load_dotenv
load_dotenv()
from rapidapi_flask_extensions import app

session=requests.session()

# app = Flask(__name__)

CREDS = os.getenv("CREDS")

name_n_ids = {
    'mystery1': 'Champions of Poseidon (Mini)',
    'mystery2': 'Champions of Poseidon (Maxi)',
    'mystery3': 'Champions of Poseidon (Mega)',
    'abbj': 'All Bets Blackjack',
    'mrj-1': 'Age of the Gods Bonus Roulette Live (Power)',
    'mrj-2': 'Age of the Gods Bonus Roulette Live (Extra Power)',
    'mrj-3': 'Age of the Gods Bonus Roulette Live (Super Power)',
    'mrj-4': 'Age of the Gods Bonus Roulette Live (Ultimate Power)',
    'ctivj-1': 'Cat in Vegas',
    'drgj-1': 'Dragon Jackpot Roulette (Gold)',
    'drgj-2': 'Dragon Jackpot Roulette (Red)',
    'drgj-3': 'Dragon Jackpot Roulette (Blue)',
    'drgj-4': 'Dragon Jackpot Roulette (Green)',
    'ejl-1': "Everybody's Jackpot Live (Daily)",
    'ejl-2': "Everybody's Jackpot Live (Grand)",
    'fdtjp-1': "Frankie Dettori's Jackpot Roulette (Silver 5)",
    'fdtjp-2': "Frankie Dettori's Jackpot Roulette (Golden 7)",
    'lndg-1': 'Land Of Gold',
    'bjp-1': 'Rhino Blitz (Mini)',
    'bjp-2': 'Rhino Blitz (Minor)',
    'bjp-3': 'Rhino Blitz (Major)',
    'bjp-4': 'Rhino Blitz (Blitz)',
    'jhreelsj-1': 'Rocky (Mini)',
    'jhreelsj-2': 'Rocky (Grand)',
    'ashtmd-1': 'Time for a Deal',
    'dcjp-1': 'Vikings: Empire Treasures(Mini)',
    'dcjp-2': 'Vikings: Empire Treasures (Minor)',
    'dcjp-3': 'Vikings: Empire Treasures (Major)',
    'dcjp-4': 'Vikings: Empire Treasures (Grand)',
    '54001': '10001 Nights (1)',
    '54002': '10001 Nights (2)',
    '54003': '10001 Nights (3)',
    '54004': '10001 Nights (4 Progressive)',
    'BaronVonRichoftenProg1': 'Baron Von Rich-Often (Green)',
    'BaronVonRichoftenProg2': 'Baron Von Rich-Often (Blue)',
    'BaronVonRichoftenProg3': 'Baron Von Rich-Often (Purple)',
    'BaronVonRichoftenProg4': 'Baron Von Rich-Often (Yellow)',
    'BaronVonRichoftenProg5': 'Baron Von Rich-Often (Orange)',
    'BarStarBronzeProg': 'Bar Star (Bronze)',
    'BarStarGoldProg': 'Bar Star (Gold)',
    'BarStarSilverProg': 'Bar Star (Silver)',
    'BeehiveProg': 'Beehive Bedlam Reactors',
    'CaptainCashfallBronzeLobsterProg': 'Captain Cashfall (Bronze)',
    'CaptainCashfallGoldLobsterProg': 'Captain Cashfall (Gold)',
    'CaptainCashfallSilverLobsterProg': 'Captain Cashfall (Silver)',
    'DiamondHeistProg1': 'Diamond Heist (Green)',
    'DiamondHeistProg2': 'Diamond Heist (Blue)',
    'DiamondHeistProg3': 'Diamond Heist (Purple)',
    'DiamondHeistProg4': 'Diamond Heist (Yellow)',
    'DiamondHeistProg5': 'Diamond Heist (Red)',
    'dondlightningspins': 'Deal Or No Deal: Lightning Spins',
    'dondpowertimeawprf-10': 'Deal Or No Deal: Power Time (10)',
    'dondpowertimeawprf-8': 'Deal Or No Deal: Power Time (8)',
    'dondpowertimeawprf-6': 'Deal Or No Deal: Power Time (6)',
    'dondpowertimeawprf-5': 'Deal Or No Deal: Power Time (5)',
    'dealornodealrf-10': "Deal or No Deal: What's In Your Box Rapid Fire (10)",
    'dealornodealrf-8': "Deal or No Deal: What's In Your Box Rapid Fire (8)",
    'dealornodealrf-6': "Deal or No Deal: What's In Your Box Rapid Fire (6)",
    'dealornodealrf-5': "Deal or No Deal: What's In Your Box Rapid Fire(5)",
    'EskimoDoughProg1': 'Eskimo Dough (Red)',
    'EskimoDoughProg2': 'Eskimo Dough (Green)',
    'EskimoDoughProg3': 'Eskimo Dough (Yellow)',
    'EskimoDoughProg4': 'Eskimo Dough (Blue)',
    'EskimoDoughProg5': 'Eskimo Dough (Purple)',
    'FranksFreakSpinsSlotBronzeProg': "Frank's Freak Spins (Bronze)",
    'FranksFreakSpinsSlotGoldProg': "Frank's Freak Spins (Gold)",
    'FranksFreakSpinsSlotSilverProg': "Frank's Freak Spins (Silver)",
    'goldfrenzyrf-10': 'Gold Frenzy Rapid Fire (10)',
    'goldfrenzyrf-8': 'Gold Frenzy Rapid Fire (8)',
    'goldfrenzyrf-6': 'Gold Frenzy Rapid Fire (6)',
    'goldfrenzyrf-5': 'Gold Frenzy Rapid Fire (5)',
    'GrabbaDabba2Prog': 'Grabba Dabba 2',
    'GrabbaDabbaDoughProg': 'Grabba Dabba Dough',
    'Jackpot7sProg': 'Jackpot 7s',
    'LuckysJackpotTavernBronzeProg': 'Luckys Jackpot Tavern (Bronze)',
    'LuckysJackpotTavernGoldProg': 'Luckys Jackpot Tavern (Gold)',
    'LuckysJackpotTavernSilverProg': 'Luckys Jackpot Tavern (Silver)',
    'Magic500Prog1': 'Magic 500 (Purple)',
    'Magic500Prog2': 'Magic 500 (Teal)',
    'Magic500Prog3': 'Magic 500 (Green)',
    'Magic500Prog4': 'Magic 500 (Yellow)',
    'Magic500Prog5': 'Magic 500 (Red)',
    'monkeybusinessdeluxejk-king': 'Monkey Business Deluxe (King)',
    'monkeybusinessdeluxejk-regal': 'Monkey Business Deluxe (Regal)',
    'monkeybusinessdeluxejk-royal': 'Monkey Business Deluxe (Royal)',
    'pixies-gold': 'Pixies of the forest 2 (Gold)',
    'pixies-silver': 'Pixies of the forest 2 (Silver)',
    'pixies-bronze': 'Pixies of the forest 2 (Bronze)',
    'RobinHoodBlueProg': 'Robin Hood and his Merry Jackpots (Blue)',
    'RobinHoodGoldProg': 'Robin Hood and his Merry Jackpots (Gold)',
    'RobinHoodRedProg': 'Robin Hood and his Merry Jackpots (Red)',
    'RollingStoneAgeBronzeProg': 'Rolling Stone Age (Bronze)',
    'RollingStoneAgeGoldProg': 'Rolling Stone Age (Gold)',
    'RollingStoneAgeSilverProg': 'Rolling Stone Age (Silver)',
    'RollOutTheBarrelProg1': 'Roll Out The Barrel (Green)',
    'RollOutTheBarrelProg2': 'Roll Out The Barrel (Blue)',
    'RollOutTheBarrelProg3': 'Roll Out The Barrel (Pink)',
    'Santa600Prog1': 'Santa 600 (Purple)',
    'Santa600Prog2': 'Santa 600 (Teal)',
    'Santa600Prog3': 'Santa 600 (Green)',
    'Santa600Prog4': 'Santa 600 (Yellow)',
    'Santa600Prog5': 'Santa 600 (Blue)',
    'SirJackpotsAlotGreenProg': 'Sir Jackpotsalot (Green)',
    'SirJackpotsAlotPurpleProg': 'Sir Jackpotsalot (Purple)',
    'SirJackpotsAlotRedProg': 'Sir Jackpotsalot (Red)',
    'rainbowgoldrf-10': 'Slots O Gold Rapid Fire (10)',
    'rainbowgoldrf-8': 'Slots O Gold Rapid Fire (8)',
    'rainbowgoldrf-6': 'Slots O Gold Rapid Fire (6)',
    'rainbowgoldrf-5': 'Slots O Gold Rapid Fire (5)',
    'VivaScratchVegasProg': 'Viva Scratch Vegas'
}


id_dict = {
        "skyvegas_servlet": ['BaronVonRichoftenProg1', 'BaronVonRichoftenProg2', 'BaronVonRichoftenProg3', 'BaronVonRichoftenProg4', 'BaronVonRichoftenProg5', 'BarStarBronzeProg', 'BarStarGoldProg', 'BarStarSilverProg', 'BeehiveProg', 'CaptainCashfallBronzeLobsterProg', 'CaptainCashfallGoldLobsterProg', 'CaptainCashfallSilverLobsterProg', 'DiamondHeistProg1', 'DiamondHeistProg2', 'DiamondHeistProg3', 'DiamondHeistProg4', 'DiamondHeistProg5', 'EskimoDoughProg1', 'EskimoDoughProg2', 'EskimoDoughProg3', 'EskimoDoughProg4', 'EskimoDoughProg5', 'FranksFreakSpinsSlotBronzeProg', 'FranksFreakSpinsSlotGoldProg', 'FranksFreakSpinsSlotSilverProg', 'GrabbaDabba2Prog', 'GrabbaDabbaDoughProg', 'Jackpot7sProg', 'LuckysJackpotTavernBronzeProg', 'LuckysJackpotTavernGoldProg', 'LuckysJackpotTavernSilverProg', 'Magic500Prog1', 'Magic500Prog2', 'Magic500Prog3', 'Magic500Prog4', 'Magic500Prog5', 'RobinHoodBlueProg', 'RobinHoodGoldProg', 'RobinHoodRedProg', 'RollingStoneAgeBronzeProg', 'RollingStoneAgeGoldProg', 'RollingStoneAgeSilverProg', 'RollOutTheBarrelProg1', 'RollOutTheBarrelProg2', 'RollOutTheBarrelProg3', 'Santa600Prog1', 'Santa600Prog2', 'Santa600Prog3', 'Santa600Prog4', 'Santa600Prog5', 'SirJackpotsAlotGreenProg', 'SirJackpotsAlotPurpleProg', 'SirJackpotsAlotRedProg', 'VivaScratchVegasProg'],
        "skyvegas_commsmesssky":['dondlightningspins', 'dondpowertimeawprf-10', 'dondpowertimeawprf-8', 'dondpowertimeawprf-6', 'dondpowertimeawprf-5', 'dealornodealrf-10', 'dealornodealrf-8', 'dealornodealrf-6', 'dealornodealrf-5', 'goldfrenzyrf-10', 'goldfrenzyrf-8', 'goldfrenzyrf-6', 'goldfrenzyrf-5', 'monkeybusinessdeluxejk-king', 'monkeybusinessdeluxejk-regal', 'monkeybusinessdeluxejk-royal', 'rainbowgoldrf-10', 'rainbowgoldrf-8', 'rainbowgoldrf-6', 'rainbowgoldrf-5'],
        "skyvegas_10001Nights":["54001", "54002", "54003", "54004"],
        "skyvegas_pixiesforest":['pixies-gold', 'pixies-silver', 'pixies-bronze'],
        "sky_casino_games":['abbj', 'mrj-1', 'mrj-2', 'mrj-3', 'mrj-4', 'ctivj-1', 'drgj-1', 'drgj-2', 'drgj-3', 'drgj-4', 'ejl-1', 'ejl-2', 'fdtjp-1', 'fdtjp-2', 'lndg-1', 'bjp-1', 'bjp-2', 'bjp-3', 'bjp-4', 'jhreelsj-1', 'jhreelsj-2', 'ashtmd-1', 'dcjp-1', 'dcjp-2', 'dcjp-3', 'dcjp-4'],
        "sky_bingo_champion_poidon":["mystery1","mystery2","mystery3"]
        }

game_meta_file = "skybet_jackpot_meta"
game_meta_path = os.path.join(f"{game_meta_file}.xlsx")
game_data = pd.read_excel(game_meta_path, sheet_name="Game Details")

proxies = {
        "http": "http://kacgmqby-GB-rotate:ciyqkobqlqbt@p.webshare.io:80",
        "https": "http://kacgmqby-GB-rotate:ciyqkobqlqbt@p.webshare.io:80",
    }

session.proxies.update(proxies)

uuid1 = uuid.uuid4()

# request functions

def skyvegas_servlet(IBS_Login=None): 
    dict={}
    servlet_game_names = game_data.loc[
        game_data["Scrape"] == "Servlet", "Jackpot Name"
    ]
    for game_name in servlet_game_names.unique():
        print(f"Starting for sky vegas's game - {game_name}  | uuid - {uuid1}",flush=True )
        try:
            slot = game_data.loc[
                game_data["Jackpot Name"] == game_name, "Jackpot Type"
            ].tolist()[0]
            cookies = {
                "IBS_Login": IBS_Login,
            }
            data = f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE GameRequest SYSTEM "http://www.orbisuk.com/igf/dtd/GameRequest.dtd"><GameRequest> <Header><GameDetails class="{slot}" name="{game_name}" free_play="No" channel="a" /><Customer balance="" is_guest="No" affiliate="" /></Header><Init definition="Yes" payout="Yes" promotions="Yes" freebets="Yes" /></GameRequest>'
            response = session.post(
                "https://www.skyvegas.com/secure/casino/Servlet",
                cookies=cookies,
                data=data,
                proxies=proxies,
            )
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                for item in root.findall(".//Progressive"):
                    id = item.get("name")
                    amount = item.get("jackpot")                      
                    dict[id] = eval(amount)
                
            else:
                abort(response.status_code)

        except Exception as e:
            print(
                f"Failed to scrape sky vegas's game - {game_name}. | Error - {str(e)} | uuid - {uuid1}",flush=True
            )
    return dict

def skyvegas_commsmesssky(IBS_Login=None):
    dict={}
    CommsMessSky_game_names = game_data.loc[    
        game_data["Scrape"] == "CommsMessSky", "Jackpot Name"
    ]
    for game_name in CommsMessSky_game_names.unique():
        print(f"Starting for sky vegas's game - {game_name}  | uuid - {uuid1}",flush=True)
        try:
            data = f'<GameRequest><header><sessionid>0000000000000000</sessionid><userid/><gameid>{game_name}</gameid><timestamp>0</timestamp><sequence>1</sequence><clientid>00000</clientid></header><Init name="{game_name}"/><token>{IBS_Login};38837143;C</token><demomode>0</demomode><channel>a</channel><promotions>0</promotions><affiliate/><language>en</language><currency>undefined</currency></GameRequest>'
            response = requests.post(
                "https://skyrgs.blueprintgaming.com/RGSMess.asmx/CommsMessSky",
                data=data,
                proxies=proxies,
            )
            root = ET.fromstring(response.text)
            progressive_info = root.find("./ProgressiveInfo")
            if progressive_info is not None:
                game_id_list = game_data.loc[
                    game_data["Jackpot Name"] == game_name, "ID"
                ].tolist()
                amount_list = progressive_info.get("jackpotBalance").split("|")
                for id, amount in zip(game_id_list, amount_list):
                    dict[id] = eval(amount)

        except Exception as e:
            print(
                f"Failed to scrape sky vegas's game - {game_name}. | Error - {str(e)} | uuid - {uuid1}",flush=True
            )
    return dict        

def skyvegas_10001Nights():
    dict={}
    try:
        print(f"Starting scraping for sky vagas's 10001Nights. | uuid - {uuid1}",flush=True)

        params = {
            "currency": "GBP",
        }
        response = requests.get(
            "https://feed-evo-skymga0000000000.redtiger.cash/jackpots/sky",
            params=params,
            proxies=proxies,
        )
        for game in response.json()["result"]["jackpots"]["pots"]:
            id = game.get("id")
            amount = game.get("amount")
            dict[id] = eval(amount)
    except Exception as e:
        print(
            f"Failed to scrape for sky vagas's 10001Nights. | Error - {str(e)} | uuid - {uuid1}",flush=True
        )
    return dict    

def skyvegas_pixiesforest():
    dict={}
    try:
        print(f"Starting scraping for sky vagas's pixiesforest. | uuid - {uuid1}",flush=True)

        headers = {
            "Accept": "application/json",
        }

        params = {
            "currencycode": "GBP",
        }
        response = session.get(
            "https://jackpot.gi.rgsgames.com/jackpotmeter/ws/meter/L01-05-293",
            params=params,
            headers=headers,
            proxies=proxies,
        )
        amount = response.json()["jackpots"]["jackpot"][0]["payNow"]
        if amount:
            id = "pixies-gold"
            dict[id] = amount / 100
        dict["pixies-silver"] = 2700 / 100
        dict["pixies-bronze"] = 900 / 100
    except Exception as e:
        print(
            f"Failed to scrape for sky vagas's pixiesforest. | Error - {str(e)} | uuid - {uuid1}",flush=True
        )
    return dict

def sky_casino_games():
    dict={}
    try:
        print(f"Starting scraping for sky casino games. | uuid - {uuid1}",flush=True)

        response = session.get(
            "https://www.skycasino.com/data/jackpots", proxies=proxies
        )
        for game in response.json():
            id = game.get("id")
            amount = game.get("amount_gbp")
            amount = game.get("amount_gbp").replace(",", "")
            dict[id] = eval(amount)
    except Exception as e:
        print(f"Failed to scrape sky casino games. | Error - {str(e)} | uuid - {uuid1}",flush=True)
    return dict

def sky_bingo_champion_poidon():
    dict={}
    try:
        print(f"Starting scraping for sky bingo's Champions of Poseidon. | uuid - {uuid1}",flush=True)
        response = session.get(
            "https://play.eyeconalderney.gg/maroon/servlet/vfapi?Token=f2162c4f-4f6f-4248-9b6b-c20ac72011ef&GameType=Champions%20of%20Poseidon%20JP%20SA&brand=VF&nid=skybingo.com&currency=GBP&lang=en&plt=d&embedded=true",
            proxies=proxies,
        )
        match = re.search(r'"jackpotServletUrl" : "(.*?)"', response.text)
        if match:
            jackpotServletUrl = match.group(1)
            params = {
                "excludeConfig": "true",
                "currencyCode": "GBP",
            }
            response = session.get(jackpotServletUrl, params=params)
            for game in response.json()["data"]["state"]["games"][0]["state"][   # use get fucion and track error 
                "pools"
            ]:
                id = game["id"]
                amount = game["current"]
                dict[id] = amount / 100

    except Exception as e:
        print(
            f"Failed to scrape sky bingo's Champions of Poseidon. | Error - {str(e)} | uuid - {uuid1}",flush=True
        )
    return dict
    

# Define the API endpoint
@app.route('/api/ids', methods=['GET'])
def game_list():
    r_data={
            "req_id": f"{uuid1}",
            "message": "success",
            "data": f"{name_n_ids}"
        }
    response = jsonify(r_data)
    response.status_code = 200
    return response
    
@app.route('/api', methods=['GET'])
def get_data():
    global IBS_Login
    IBS_Login= None
    try:
        input_value=None
        input_value = request.args.get('g_id')
        result_keys = [key for key, values in id_dict.items() if input_value in values]

        # Print the result
        if result_keys:
            print(f"req_id- {uuid1}",flush=True)
            result_key=result_keys[0]
        else:
            print(f"req_id  {uuid1}",flush=True)
            abort(404, description="No data available for this game id")
    except Exception as e:
        print(f"Error while searching game_id -  {e} | uuid - {uuid1}",flush=True)
        abort(500)
        
    #loggig in
# try: 
    url = 'https://www.skybet.com/secure/identity/m/login/onevegas'
    headers = {
        'authority': 'www.skybet.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.skybet.com',
        'referer': 'https://www.skybet.com/secure/identity/m/login/onevegas?urlconsumer=https%3A%2F%2Fwww.skyvegas.com&dl=1',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    session.headers.update(headers)

    data = CREDS

    response = session.post(url,data=data)
    try:
        if response.status_code == 200:
            match = re.search(r'"oxitoken":"(.*?)"', response.text)
            if match:
                ibs_login = match.group(1)
                print(f"IBS_Login scraped | value - {ibs_login} | uuid - {uuid1}",flush=True)
            IBS_Login=ibs_login
        else:
            print(f"IBS_Login scraped | value - {IBS_Login} | uuid - {uuid1}",flush=True)
            abort(500)
    except Exception as e:
        print(f"Failed to scrape IBS_Login token. | Error - {str(e)} | uuid - {uuid1}",flush=True)
        abort(500)
        
    #game_extractin fuctions 

    if result_key == "skyvegas_servlet":
        if IBS_Login:
            skyvegas_servlet(IBS_Login)
        else:
            print(f"ibs login not found req_id= {uuid1}", flush=True)
            abort(500)
                
    if result_key == "skyvegas_commsmesssky":
        if IBS_Login:
            jackpot_amounts=skyvegas_commsmesssky(IBS_Login)
        else:
            print(f"ibs login not found req_id= {uuid1}", flush=True)
            abort(500)
            
    if result_key == "skyvegas_10001Nights":
        input_value=int(input_value)
        jackpot_amounts=skyvegas_10001Nights()
    if result_key == "skyvegas_pixiesforest":
        jackpot_amounts=skyvegas_pixiesforest()
    if result_key == "sky_casino_games":
        jackpot_amounts=sky_casino_games()
    if result_key == "sky_bingo_champion_poidon":
        jackpot_amounts=sky_bingo_champion_poidon()

    output_data= jackpot_amounts[input_value]
    if output_data:
        status= 200
        r_data={
            "req_id": f"{uuid1}",
            "message": "success",
            "data":{  
                    f"{input_value}": f"{output_data}",
                    } 
        }
    else:
        print(f"found data====>>>", jackpot_amounts, flush=True)
        print(f"Did not find value |  | uuid - {uuid1}",flush=True)
        status= 404 
        r_data={
            "req_id": f"{uuid1}",
            "message": "error",
            "data":"No data found" 
        }
    response = jsonify(r_data)
    response.status_code = status
    return response

# Run the application
if __name__ == "__main__":
    app.run()
