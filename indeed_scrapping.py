from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import pandas as pd


def run_scrapping():

    driver = webdriver.Chrome()

    URL = "https://fr.indeed.com/jobs?q=alternance&l=Dijon+%2821%29&from=searchOnHP&vjk=ea7ad82f11da0aed"
    driver.get(URL)

    Company = driver.find_element(By.CLASS_NAME, 'companyName').text
    Title = driver.find_element(By.CLASS_NAME, 'jobTitle-newJob').text
    Description = driver.find_element(By.CLASS_NAME, 'job-snippet').text
    Publish_Date = driver.find_element(By.CLASS_NAME, 'date').text

    Publish_Date = Publish_Date.replace('Posted\nOffre publiée', ' ') # la fonction replace() permet de retirer les chaines de caractères inutiles


        # nous mettons les résultats dans un tableau qui sera affiché plus tard dans le navigateur
    results = pd.DataFrame(columns=['Entreprise', 'Offre', 'Description', 'Date de publication'],
            data=[[Company, Title, Description, Publish_Date]])

    # print(results)

    driver.close()

    return results