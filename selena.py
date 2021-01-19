from selenium import webdriver
from enum import Enum
import tweepy
import os

consumer_key = os.environ.get("API_KEY")

consumer_secret = os.environ.get("API_SECRET_KEY")

key = os.environ.get("ACCESS_TOKEN")

secret = os.environ.get("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

class Animals(Enum):
    Avestruz = 1
    Aguia = 2
    Burro = 3
    Borboleta = 4
    Cachorro = 5
    Cabra = 6
    Carneiro = 7
    Camelo = 8
    Cobra = 9
    Coelho = 10
    Cavalo = 11
    Elefante = 12
    Galo = 13
    Gato = 14
    Jacare = 15
    Leao = 16
    Macaco = 17
    Porco = 18
    Pavao = 19
    Peru = 20
    Touro = 21
    Tigre = 22
    Urso = 23
    Veado = 24
    Vaca = 25


def matrix_results():
    op = webdriver.ChromeOptions()
    op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-sh-usage")

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)
    driver.get("https://www.ojogodobicho.com/deu_no_poste.htm")

    cols = len(driver.find_elements_by_xpath("/html/body/div[5]/div/div/div[2]/table/tbody/tr[1]/td"))
    rows = len(driver.find_elements_by_xpath("/html/body/div[5]/div/div/div[2]/table/tbody/tr"))

    matrix = [[0 for x in range(cols + 1)] for y in range(rows)]
    matrix[0][cols] = "0000-0" #to facilitate the stopping parameter

    # (var - 1) -> positions in the list // (var) -> positions in the xpath
    for r  in range(1, rows + 1):
        for c in range(1, cols + 1):
            element = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/table/tbody/tr["+str(r)+"]/td["+str(c)+"]").text
            matrix [r - 1][c - 1] = element

    day = driver.find_element_by_tag_name("caption").text
    driver.quit()
    
    return (matrix, day)


def results_to_display(matrix):

    winnin_nums =[ 0 for x in range(7)]
    type_of_game = ["PTM", "PT", "PTV", "PTN", "COR"]
    
    for x in range(len(matrix[0])):
        if(matrix[0][x + 1] == "0000-0" and matrix[0][x] != "1º" and matrix[0][x] != "0000-0"):
            for y in range(len(matrix)):
                winnin_nums[y] = matrix[y][x]
            return (winnin_nums, type_of_game[x - 1])
    return ([], "")
    

def animals(winnin_num):
    divided_nums = winnin_num.split("-")
    for bicho in Animals:
        if(str(bicho.value) == divided_nums[1]):
            return bicho.name


def put_it_in_a_tweet(winnin, type_of_game, day):
    message = day + '\n' + type_of_game + '\n'
    for y in range(0, 7):
        message = message + str(y + 1) + ') ' + winnin[y] + ' (' + animals(winnin[y])+ ')' +'\n'
    return message


def check_duplicated_tweets(string_of_tweet, type_of_game):
    position = latest_tweet.find(type_of_game)

    if(position == -1):
        return True

    string_test = ''

    for y in range(4):
        if( latest_tweet[position + y] != "\n"):
            return (type_of_game != string_test)
        string_test += latest_tweet[position + y]


############################################################

winnin = []
matrix, day = matrix_results()
winnin, type_of_game = results_to_display(matrix)

latest_tweet = api.user_timeline(id=api.me().id, count=1)[0].text

print("\nEXECUTING...\n")
print(put_it_in_a_tweet(winnin, type_of_game, day))
print("\n\n")

if(check_duplicated_tweets(latest_tweet, type_of_game)):
    try:
        api.update_status(put_it_in_a_tweet(winnin, type_of_game, day))
        print("\nRESULTS UPDATED!\n")
    except tweepy.TweepError as e:
        print("\nERROR:\n")
        print(e.reason)
else:
    print("\nRESULTS ARE UP TO DATE\n")
