import requests
import json
from datetime import datetime

apiKey = '7C56250591ACD590DA983DB1DA9B4BE3'
ID = input("steam id: ")

basicInfoR = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+apiKey+'&steamids='+ID)
BI = json.loads(basicInfoR.text)

totalGames = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='+apiKey+'&steamid='+ID+'&format=json')
TG = json.loads(totalGames.text)

recentGames = requests.get('http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key='+apiKey+'&steamid='+ID+'&format=json')
RG = json.loads(recentGames.text)

friendList = requests.get('http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key='+apiKey+'&steamid='+ID+'&relationship=friend')
FL = json.loads(friendList.text)

visibility = BI['response']['players'][0]['communityvisibilitystate']
if visibility == 1:
    print("this profile is not visible to you/private")
else:
    print("this profile is visible to you/public")

profile = BI['response']['players'][0]['profilestate']
if profile == 1:
    print("this user has a profile configured\n")
else:
    print("this user does not have a profile configured\n")

print('name: '+BI['response']['players'][0]['personaname'])

status = BI['response']['players'][0]['personastate']
print("currently: ", end='')
if status == 0:
    print("offline/status unavailable")
elif status == 1:
    print("online")
elif status == 2:
    print("busy")
elif status == 3:
    print("away")
elif status == 4:
    print("snoozing")
elif status == 5:
    print("looking to trade")
elif status == 6:
    print("looking to play")

print("last logoff: " + datetime.utcfromtimestamp(BI['response']['players'][0]['lastlogoff']).strftime('%Y-%m-%d %H:%M:%S'))

print('')

totalmin = 0
mostmin=0
mostID=0
for i in range(TG['response']['game_count']):
    if TG['response']['games'][i]['playtime_forever'] > mostmin:
        mostmin = TG['response']['games'][i]['playtime_forever']
        mostID = TG['response']['games'][i]['appid']
    totalmin += TG['response']['games'][i]['playtime_forever']
print("total playtime: " + str(round(totalmin/60, 1)) + " hours")

recentmin = 0
for i in range(RG['response']['total_count']):
    recentmin += RG['response']['games'][i]['playtime_2weeks']

print("playtime last two weeks : " + str(round(recentmin/60, 1)) + " hours")
print("most played game: https://store.steampowered.com/app/" + str(mostID))

print("\nnumber of friends: ", len(FL['friendslist']['friends']))




    
    

