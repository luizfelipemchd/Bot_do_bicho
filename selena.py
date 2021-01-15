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

FILE_NAME = "last_col_update.txt"



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
    matrix = [[0 for x in range(8)] for y in range(8)]

    matrix[0][6] = "0000-0" #to facilitate the stopping parameter

    # (var - 1) -> positions in the list // (var) -> positions in the xpath
    for r  in range(1, 8):
        for c in range(1, 7):
            element = driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/table/tbody/tr["+str(r)+"]/td["+str(c)+"]").text
            matrix [r - 1][c - 1] = element

    day = driver.find_element_by_tag_name("caption").text
    driver.quit()
    
    return (matrix, day)

def read_col(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    col_update = int(file_read.read().strip())
    file_read.close()
    return col_update

def write_col(FILE_NAME, col):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(col))
    file_write.close()


def results_to_display(matrix, last_col):

    winnin_nums =[ 0 for x in range(7)]
    type_of_game = ["PTM", "PT", "PTV", "PTN", "COR"]
    
    col = -1

    if(matrix[0][1] == "0000-0"): #in case of a new day
        last_col = -1
    
    for x in range(0, 6):
        if(matrix[0][x + 1] == "0000-0" and matrix[0][x] != "1º" and matrix[0][x] != "0000-0"):
            col = x
        if col > last_col:
            for y in range(0, 7):
                winnin_nums[y] = matrix[y][col]
            write_col(FILE_NAME, col)
            return (winnin_nums, col, type_of_game[col - 1])
    return ([], last_col, "")
    
def animals(winnin_num):
    divided_nums = winnin_num.split("-")
    for bicho in Animals:
        if(str(bicho.value) == divided_nums[1]):
            return bicho.name


def put_it_in_a_tweet(winnin, type_of_game, day):
    message = day + '\n' + type_of_game + '\n'
    for y in range(0, 7):
        message = message + str(y + 1) + ')' + winnin[y] + '(' + animals(winnin[y])+ ')' +'\n'
    return message
    
        
############################################################

last_col = read_col(FILE_NAME)
winnin = []
matrix, day = matrix_results()
winnin, last_col, type_of_game = results_to_display(matrix, last_col)   
if(winnin):
    api.update_status(put_it_in_a_tweet(winnin, type_of_game, day))