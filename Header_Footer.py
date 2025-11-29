print(" TEST HEADER & FOOTER SAUCEDEMO ")

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

driver = webdriver.Chrome()
driver.maximize_window()
time.sleep(1)

# --- Création dossier screenshots ---
SCREENSHOT_FOLDER = "HF_screenshots"
if not os.path.exists(SCREENSHOT_FOLDER):
    os.makedirs(SCREENSHOT_FOLDER)

# Vérifier si un élément existe
def element_existe(by, value):
    try:
        driver.find_element(by, value)
        return True
    except:
        return False

# Screenshot sans affichage
def screenshot_pass(nom_test):
    filename = f"{SCREENSHOT_FOLDER}/{nom_test.replace(' ', '_')}.png"
    driver.save_screenshot(filename)

#  TC1 — Vérification HEADER AVANT LOGIN

driver.get("https://www.saucedemo.com")
time.sleep(2)
print("\nTC1 : Vérification du HEADER avant login")

if element_existe(By.CLASS_NAME, "app_logo"):
    print("PASS: Logo présent")
    screenshot_pass("TC1_Logo_AVANT")
else:
    print("FAIL: Logo absent")

if element_existe(By.CLASS_NAME, "login_logo"):
    print("PASS: Titre présent")
    screenshot_pass("TC1_Titre_AVANT")
else:
    print("FAIL: Titre absent")

if element_existe(By.ID, "react-burger-menu-btn"):
    print("FAIL: Burger devrait être absent avant login")
else:
    print("PASS: Burger absent")

if element_existe(By.CLASS_NAME, "search_input"):
    print("FAIL: Search bar devrait être absente")
else:
    print("PASS: Search bar absente")


#  TC2 — Vérification FOOTER AVANT LOGIN


print("\nTC2 : Vérification du FOOTER avant login")

if element_existe(By.CLASS_NAME, "footer"):
    print("FAIL: Footer devrait être absent")
else:
    print("PASS: Footer absent")

if element_existe(By.CLASS_NAME, "footer_copy"):
    print("FAIL: Copyright devrait être absent")
else:
    print("PASS: Copyright absent")


#  TC3 — Vérification absence logos sociaux AVANT LOGIN


print("\nTC3 : Vérification des logos sociaux avant login")

logos_avant = [
    ("Twitter", By.CSS_SELECTOR, "a[href='https://twitter.com/saucelabs']"),
    ("Facebook", By.CSS_SELECTOR, "a[href='https://www.facebook.com/saucelabs']"),
    ("LinkedIn", By.CSS_SELECTOR, "a[href='https://www.linkedin.com/company/sauce-labs/']")
]

for nom, by, selector in logos_avant:
    if element_existe(by, selector):
        print(f"FAIL: {nom} devrait être absent")
    else:
        print(f"PASS: {nom} absent")

#  TC4 — LOGIN

print("\nTC4 : Login avec credentials valides")

try:
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    print("PASS: Login réussi")
except:
    print("FAIL: Login impossible")

#  TC5 — Vérification HEADER APRÈS LOGIN

print("\nTC5 : Vérification du HEADER après login")

if element_existe(By.CLASS_NAME, "app_logo"):
    print("PASS: Logo présent")
    screenshot_pass("TC5_Logo_APRES")

if element_existe(By.ID, "react-burger-menu-btn"):
    print("PASS: Burger présent")
    screenshot_pass("TC5_Burger_APRES")
else:
    print("FAIL: Burger manquant")

if element_existe(By.CLASS_NAME, "shopping_cart_link"):
    print("PASS: Panier présent")
    screenshot_pass("TC5_Panier_APRES")
else:
    print("FAIL: Panier manquant")

if element_existe(By.CLASS_NAME, "search_input"):
    print("FAIL: Search bar ne doit pas exister après login")
else:
    print("PASS: Search bar absente")

# TC6 — Vérification FOOTER APRÈS LOGIN

print("\nTC6 : Vérification du FOOTER après login")

if element_existe(By.CLASS_NAME, "footer"):
    print("PASS: Footer présent")
    screenshot_pass("TC6_Footer_APRES")
else:
    print("FAIL: Footer absent")

if element_existe(By.CLASS_NAME, "footer_copy"):
    print("PASS: Copyright présent")
    screenshot_pass("TC6_Copy_APRES")
else:
    print("FAIL: Copyright absent")

# Utilitaire : Test du logo
def tester_logo(by, value, nom, attendu):
    try:
        onglet = driver.current_window_handle
        elem = driver.find_element(by, value)
        elem.click()
        time.sleep(2)

        # Switch nouvel onglet
        for h in driver.window_handles:
            if h != onglet:
                driver.switch_to.window(h)
                break

        url = driver.current_url
        if attendu in url:
            print(f"PASS: {nom} URL correcte")
            screenshot_pass(f"TC7_{nom}")
        else:
            print(f"FAIL: {nom} URL incorrecte ({url})")

        driver.close()
        driver.switch_to.window(onglet)

    except:
        print(f"FAIL: {nom} bouton introuvable")

#  TC7 — Vérification logos SOCIAUX APRÈS LOGIN

print("\nTC7 : Vérification des logos sociaux après login")

tester_logo(By.CSS_SELECTOR, "a[href='https://twitter.com/saucelabs']", "Twitter", "twitter.com")
tester_logo(By.CSS_SELECTOR, "a[href='https://www.facebook.com/saucelabs']", "Facebook", "facebook.com")
tester_logo(By.CSS_SELECTOR, "a[href='https://www.linkedin.com/company/sauce-labs/']", "LinkedIn", "linkedin.com")

#  TC8 — Vérification COPYRIGHT APRÈS LOGIN
print("\nTC8 : Vérification du copyright")

try:
    txt = driver.find_element(By.CLASS_NAME, "footer_copy").text
    if "©" in txt:
        print("PASS: Copyright")
        screenshot_pass("TC8_Copy")
    else:
        print("FAIL: Texte incorrect")
except:
    print("FAIL: Élément introuvable")

driver.quit()
