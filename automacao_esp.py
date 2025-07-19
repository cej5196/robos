import pytesseract
import fitz  # PyMuPDF
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def extrair_dados_ocr(filepath):
    texto_total = ""
    nota, serie, matricula, cpf_cnpj, nome = "", "", "", "", ""

    doc = fitz.open(filepath)
    for page in doc:
        imagem = page.get_pixmap(dpi=300)
        img_path = "pagina_temp.png"
        imagem.save(img_path)

        texto = pytesseract.image_to_string(img_path, lang="por")
        texto_total += texto + "\n"

        if "Nota Fiscal" in texto or "DANFE" in texto:
            nota_match = re.search(r"Nota Fiscal\s*(\d+)", texto)
            if nota_match:
                nota = nota_match.group(1)

            serie_match = re.search(r"Série\s*(\d+)", texto)
            if serie_match:
                serie = serie_match.group(1)

            matricula_match = re.search(r"Matrícula[:\s]*(\d+)", texto)
            if matricula_match:
                matricula = matricula_match.group(1)

            cnpj_match = re.search(r"CNPJ\s*[:\s]*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", texto)
            cpf_match = re.search(r"CPF\s*[:\s]*(\d{3}\.\d{3}\.\d{3}-\d{2})", texto)
            if cnpj_match:
                cpf_cnpj = cnpj_match.group(1).replace(".", "").replace("/", "").replace("-", "")
            elif cpf_match:
                cpf_cnpj = cpf_match.group(1).replace(".", "").replace("-", "")

            nome_match = re.search(r"Destinatário\s*:\s*(.+)", texto)
            if nome_match:
                nome = nome_match.group(1).strip()

            break

    os.remove("pagina_temp.png")

    return {
        "numero_nota": nota,
        "serie": serie,
        "matricula": matricula,
        "cpf_cnpj": cpf_cnpj,
        "nome": nome
    }

def processar_nota(filepath, usuario, senha):
    dados = extrair_dados_ocr(filepath)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://espaider.com.br/Femsa/")
        time.sleep(5)
        driver.find_element(By.ID, "userFieldEdt").send_keys(usuario)
        driver.find_element(By.ID, "passwordFieldEdt").send_keys(senha)
        driver.find_element(By.ID, "loginButton").click()
        time.sleep(5)
        # Continue com automação...
    finally:
        driver.quit()

    return dados
