import requests
from bs4 import BeautifulSoup
import csv

j = -1
matches_details = []
round = []
rt = []

page = requests.get(f"https://www.yallakora.com/uefa/2917/fixtures/%d8%af%d9%88%d8%b1%d9%8a-%d8%a3%d8%a8%d8%b7%d8%a7%d9%84-%d8%a3%d9%88%d8%b1%d9%88%d8%a8%d8%a7?roundid=12226")

src = page.content
soup = BeautifulSoup(src,"lxml")

round_link = soup.find("ul",{'class' : 'dropdown'}).find_all("li")

for link in round_link:
    round.append(link.a.attrs['href'])
    rt.append(link.a.text.strip())
#print(rt)
#print(len(rt),len(round))

for i in round:
    page = requests.get(f"https://www.yallakora.com{i}")

    src = page.content
    soup = BeautifulSoup(src,"lxml")
    j+=1
    
    def get_match_info (soup) :
        #************************ this part needs to be modified ***************************************
        #round_title = soup.find("script",{'type' : 'text/javascript'}).text
        #round_title = soup.find("a",{'href' : '{i} index'}).text.strip()
        #round_title = soup.find("li",{'class' : 'filter'}).a.text.strip()
        
        if (j<len(rt)) :
            round_title = rt[j]
        #************************************************************************************************
        #print(round_title)
        all_matches = soup.find("div",{'class' : 'matchesList'}).contents[1].find_all("div",{'class' : 'finish liItem'})

        number_of_matches = len(all_matches)
        
        for i in range (number_of_matches) :
            #get teams name
            team_A = all_matches[i].find("div", {'class':'teams teamA'}).text.strip()
            team_B = all_matches[i].find("div",{'class' : 'teams teamB'}).text.strip()

            #get score
            match_result = all_matches[i].find("div", {'class':'MResult'}).find_all("span",{'class' : 'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"

            #get match time
            match_time = all_matches[i].find("div",{'class' : 'date'}).find("span").text.strip()

            #add information to matches_detailes
            matches_details.append({"رقم الجولة" : round_title ,"الفريق الأول" : team_A , " الفريق الثاني" : team_B , "موعد المباراة" : match_time , "النتيحة" : score})

    get_match_info(soup)

keys = matches_details[0].keys()
with open('match_details.csv','w' , newline="", encoding="utf-8") as output_file :
    dict_writer = csv.DictWriter(output_file,keys)
    dict_writer.writeheader()
    dict_writer.writerows(matches_details)
    print("file created")

