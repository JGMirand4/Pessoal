import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def configurar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver_path = "/opt/homebrew/bin/chromedriver"
    return webdriver.Chrome(service=Service(driver_path), options=chrome_options)

def baixar_arquivo(url, pasta_destino):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    nome_arquivo = url.split("/")[-1]
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
    with open(caminho_arquivo, "wb") as f:
        f.write(response.content)
    return caminho_arquivo

def baixar_diario_oficial():
    driver = configurar_driver()
    arquivos_baixados = []
    try:
        url_site = "https://diariooficial.cepe.com.br/diariooficialweb/#/home?diario=MQ%3D%3D"
        driver.get(url_site)
        wait = WebDriverWait(driver, 20)
        links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='.pdf']")))
        urls_pdf = [link.get_attribute("href") for link in links]

        pasta_destino = "diarios_pernambuco"
        os.makedirs(pasta_destino, exist_ok=True)
        for url in urls_pdf:
            arquivos_baixados.append(baixar_arquivo(url, pasta_destino))
    finally:
        driver.quit()
    return arquivos_baixados
