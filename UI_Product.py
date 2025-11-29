import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ============================================================
# UI_ProductSuite
# Description : Suite de tests UI pour vérifier les fonctionnalités principales
#               de SauceDemo : tri, panier, reset, menu, liens et logout.
# ============================================================

# --- Créer le dossier screenshots_products si il n'existe pas ---
screenshot_dir = "screenshots_products"
os.makedirs(screenshot_dir, exist_ok=True)

# --- Initialisation du navigateur ---
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.saucedemo.com")

# --- Login ---
driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()
time.sleep(2)

# --- Fonction pour format d'affichage des résultats ---
def result(tc_id, ok, message):
    status = "PASS" if ok else "FAIL"
    print(f"{tc_id} : {status} – {message}")


def check_name_sort(order="asc"):
    # TC-01 et  TC-02: Vérifie le tri alphabétique des noms de produits(A to Z et Z to A)
    products = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    names = [p.text for p in products]
    sorted_names = sorted(names) if order=="asc" else sorted(names, reverse=True)

    passed = (names == sorted_names)
    result(f"TC-01" if order=="asc" else "TC-02",
           passed,
           f"Tri Name {order} avec succès" if passed else "Tri Name incorrect")

    driver.save_screenshot(os.path.join(screenshot_dir, f"Name_{order}.png"))
    assert passed

def check_price_sort(order="asc"):
    # TC-03 / TC-04: Vérifie le tri des prix des produits(High to Low et Low to High)
    prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    prices_float = [float(p.text.replace("$","")) for p in prices]
    sorted_prices = sorted(prices_float) if order=="asc" else sorted(prices_float, reverse=True)

    passed = (prices_float == sorted_prices)
    result(f"TC-03" if order=="asc" else "TC-04",
           passed,
           f"Tri Price {order} avec succès" if passed else "Tri Price incorrect")

    driver.save_screenshot(os.path.join(screenshot_dir, f"Price_{order}.png"))
    assert passed

def check_about_link():
    # TC-05: Vérifie que le lien "About" du menu fonctionne
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
    ).click()
    time.sleep(1)

    driver.find_element(By.ID, "about_sidebar_link").click()
    time.sleep(2)

    passed = ("saucelabs.com" in driver.current_url)
    result("TC-05", passed, "Lien About fonctionne" if passed else "Lien About cassé")

    driver.save_screenshot(os.path.join(screenshot_dir, "Link_About.png"))

    driver.back()
    time.sleep(2)

def test_add_product_then_reset():
    # TC-06: Ajouter un produit au panier
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    time.sleep(1)

    button_text = driver.find_element(By.ID, "remove-sauce-labs-backpack").text
    passed_add = (button_text == "Remove")
    result("TC-06", passed_add, "Produit ajouté avec succès")
    assert passed_add

    # TC-07: Vérifie le compteur du panier
    cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    passed_count = (cart_count == "1")
    result("TC-07", passed_count, "Compteur panier correct")
    assert passed_count

    # TC-08: Reset App State
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
    ).click()
    time.sleep(1)
    driver.find_element(By.ID, "reset_sidebar_link").click()
    time.sleep(1)

    cart_badge = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    passed_reset = (len(cart_badge) == 0)
    result("TC-08", passed_reset, "Reset App State OK")
    driver.save_screenshot(os.path.join(screenshot_dir, "ResetAppState_after_add.png"))
    assert passed_reset

def test_search_bar_absence_fail():
    # TC-09:Verifier la  barre de recherche
    
    try:
        driver.find_element(By.CSS_SELECTOR, "input[type='search'], #search, .search, .search-input")
        result("TC-09", False, "Une barre de recherche existe (FAIL attendu)")
    except:
        result("TC-09", False, "Barre de recherche introuvable")
        driver.save_screenshot(os.path.join(screenshot_dir, "Fail_SearchBar.png"))

def test_logout():
    # TC-10: Vérifie la déconnexion
    try:
        menu_panel = driver.find_element(By.CLASS_NAME, "bm-menu")
        if menu_panel.is_displayed():
            driver.find_element(By.ID, "react-burger-cross-btn").click()
            time.sleep(1)
    except:
        pass

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
    ).click()
    time.sleep(1)

    driver.find_element(By.ID, "logout_sidebar_link").click()
    time.sleep(2)

    passed = ("https://www.saucedemo.com/" in driver.current_url)
    result("TC-10", passed, "Logout OK")
    driver.save_screenshot(os.path.join(screenshot_dir, "Logout_OK.png"))
    assert passed



# 1. Filtrages (Tri)
Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_visible_text("Name (A to Z)")
time.sleep(1)
check_name_sort(order="asc")

Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_visible_text("Name (Z to A)")
time.sleep(1)
check_name_sort(order="desc")

Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_visible_text("Price (low to high)")
time.sleep(1)
check_price_sort(order="asc")

Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_visible_text("Price (high to low)")
time.sleep(1)
check_price_sort(order="desc")

# 2. Vérification du lien About
check_about_link()

# 3. Ajouter produit et verifier le bouton Reset App State
test_add_product_then_reset()

# 4. Verifier la barre de recherche
test_search_bar_absence_fail()

# 5. Vérification du Logout
test_logout()

# Fin 

driver.close()
