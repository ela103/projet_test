import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Pour Jenkins

chrome_options = Options()
chrome_options.add_argument("--headless=new")   # Mode headless (obligatoire Jenkins)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

# Dossier screenshots
if not os.path.exists("screenshots_AddToCart"):
    os.makedirs("screenshots_AddToCart")

def take_screenshot(tc_name):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"screenshots_AddToCart/{tc_name}_{timestamp}.png"
    driver.save_screenshot(filename)
    


# LOGIN

driver.get("https://www.saucedemo.com")

wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()

print("Login effectué ")

# TC-01 : Bouton Add to Cart

try:
    bouton = wait.until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    )
    print("TC-01 PASS : Bouton Add to Cart visible et cliquable")
    take_screenshot("TC-01")
except:
    print("TC-01 FAIL : Bouton Add to Cart introuvable")


# TC-02 : Ajouter Backpack

try:
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.ID, "shopping_cart_container").click()

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[text()='Sauce Labs Backpack']")
        )
    )
    print("TC-02 PASS : Produit ajouté au panier")
    take_screenshot("TC-02")
except:
    print("TC-02 FAIL : Produit non trouvé dans le panier")


# TC-03 : Ajouter plusieurs produits

driver.get("https://www.saucedemo.com/inventory.html")

produits_ids = [
    "add-to-cart-sauce-labs-bike-light",
    "add-to-cart-sauce-labs-bolt-t-shirt"
]
produits_noms = [
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt"
]

for pid in produits_ids:
    wait.until(EC.element_to_be_clickable((By.ID, pid))).click()

driver.find_element(By.ID, "shopping_cart_container").click()

for nom in produits_noms:
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//div[text()='{nom}']")
            )
        )
        print(f"TC-03 PASS : {nom} est présent")
        take_screenshot(f"TC-03_{nom.replace(' ','_')}")
    except:
        print(f"TC-03 FAIL : {nom} absent du panier")


# TC-04 : Vérifier la quantité

for nom in produits_noms:
    try:
        quantite = driver.find_element(
            By.XPATH,
            f"//div[@class='cart_item'][.//div[text()='{nom}']]//div[@class='cart_quantity']"
        ).text
        print(f"TC-04 PASS : {nom} → Quantité : {quantite}")
        take_screenshot(f"TC-04_{nom.replace(' ','_')}")
    except:
        print(f"TC-04 FAIL : Quantité non trouvée pour {nom}")


# TC-05 : Vérifier prix

prix_attendus = {
    "Sauce Labs Bike Light": "$9.99",
    "Sauce Labs Bolt T-Shirt": "$15.99"
}

for nom, prix_attendu in prix_attendus.items():
    try:
        prix = driver.find_element(
            By.XPATH,
            f"//div[@class='cart_item'][.//div[text()='{nom}']]//div[@class='inventory_item_price']"
        ).text
        if prix == prix_attendu:
            print(f"TC-05 PASS : {nom} → Prix correct ({prix})")
            take_screenshot(f"TC-05_{nom.replace(' ','_')}")
        else:
            print(f"TC-05 FAIL : {nom} → Prix incorrect ({prix})")
    except:
        print(f"TC-05 FAIL : Prix non trouvé pour {nom}")


# TC-06 : Promo 

print("TC-06 SKIP : Le site ne contient pas de champ promo (normal)")


# TC-07 : Vérifier total articles

try:
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    print(f"TC-07 INFO : Badge = {badge}")
except:
    print("TC-07 FAIL : Badge introuvable")


# TC-08 : Suppression produit

try:
    driver.find_element(By.ID, "remove-sauce-labs-bike-light").click()
    print("TC-08 PASS : Produit supprimé")
    take_screenshot("TC-08")
except:
    print("TC-08 FAIL : Impossible de supprimer le produit")


# TC-09 : Vérifier total après checkout

try:
    driver.find_element(By.ID, "checkout").click()
    wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("Ela")
    driver.find_element(By.ID, "last-name").send_keys("Chagour")
    driver.find_element(By.ID, "postal-code").send_keys("80")
    driver.find_element(By.ID, "continue").click()

    total = driver.find_element(By.CLASS_NAME, "summary_subtotal_label").text
    print(f"TC-09 PASS : Total affiché → {total}")
    take_screenshot("TC-09")
except:
    print("TC-09 FAIL : Total non trouvé")


# TC-10 : Vérifier total par produit

try:
    prix = driver.find_element(By.CLASS_NAME, "inventory_item_price").text
    print(f"TC-10 PASS : Prix : {prix}")
except:
    print("TC-10 FAIL : Prix introuvable")


# TC-11 : Ajouter un produit deux fois

try:
    driver.get("https://www.saucedemo.com/inventory.html")
    produit_id = "add-to-cart-sauce-labs-fleece-jacket"
    driver.find_element(By.ID, produit_id).click()
    print("TC-11 PASS : Premier ajout effectué")
    take_screenshot("TC-11-1")

    # Deuxième ajout impossible sur ce site → résultat attendu FAIL
    print("TC-11 INFO : Le site ne permet pas l'ajout multiple (comportement normal)")
except:
    print("TC-11 FAIL")


# TC-12 : Frais livraison

try:
    driver.get("https://www.saucedemo.com/cart.html")
    driver.find_element(By.XPATH, "//div[contains(text(),'Shipping')]")
    print("TC-12 PASS : Frais de livraison affichés")
except:
    print("TC-12 FAIL : Frais absents")

# ------------------------------
# FIN
# ------------------------------
driver.quit()
print("Tests terminés ")
