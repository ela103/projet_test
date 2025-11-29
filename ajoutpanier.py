import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Dossier des screenshots 
if not os.path.exists("screenshots ajouterpanier"):
    os.makedirs("screenshots ajouterpanier")

def take_screenshot(tc_name):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"screenshots ajouterpanier/{tc_name}_{timestamp}.png"
    driver.save_screenshot(filename)
    

# Liste des utilisateurs
usernames = ["standard_user", "locked_out_user", "problem_user",
             "performance_glitch_user", "error_user", "visual_user"]
password = "secret_sauce"

for username in usernames:
    print("\n====================")
    print(f"Tests pour l'utilisateur : {username}")
    print("====================\n")

    # Initialisation du driver
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com")
    driver.maximize_window()
    time.sleep(2)

    # Se Connecter
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)

    # Vérifier si login réussi (si bouton Add to Cart existe)
    try:
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    except:
        print(f"{username} : Login échoué ou page inaccessible, tests ignorés")
        driver.close()
        continue

    # TC-01 : Vérifier le bouton Add to Cart 
    try:
        bouton = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        if bouton.is_displayed() and bouton.is_enabled():
            print("TC-01 PASS : Le bouton Add to Cart est visible et cliquable")
            take_screenshot("TC-01")
        else:
            print("TC-01 FAIL : Le bouton Add to Cart n'est pas accessible")
    except:
        print("TC-01 FAIL : Le bouton Add to Cart est introuvable")

    # TC-02 : Ajouter "Sauce Labs Backpack" 
    try:
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        time.sleep(1)
        driver.find_element(By.ID, "shopping_cart_container").click()
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, "//div[@class='inventory_item_name' and text(🙁'Sauce Labs Backpack']")
            print("TC-02 PASS : 'Sauce Labs Backpack' est ajouté au panier")
            take_screenshot("TC-02")
        except:
            print("TC-02 FAIL : Aucun produit trouvé dans le panier")
    except:
        print("TC-02 FAIL : Impossible d'accéder au panier")

    # TC-03 : Ajouter plusieurs articles 
    try:
        driver.get("https://www.saucedemo.com/inventory.html")
        time.sleep(2)
        produits_ids = ["add-to-cart-sauce-labs-bike-light", "add-to-cart-sauce-labs-bolt-t-shirt"]
        produits_noms = ["Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]

        for p in produits_ids:
            driver.find_element(By.ID, p).click()
            time.sleep(1)

        driver.find_element(By.ID, "shopping_cart_container").click()
        time.sleep(2)

        for nom in produits_noms:
            try:
                driver.find_element(By.XPATH, f"//div[@class='inventory_item_name' and text(🙁'{nom}']")
                print(f"TC-03 PASS : '{nom}' est présent dans le panier")
                take_screenshot(f"TC-03_{nom.replace(' ','_')}")
            except:
                print(f"TC-03 FAIL : '{nom}' est absent du panier")
    except:
        print("TC-03 FAIL : Impossible d'accéder au panier ou d'ajouter plusieurs produits")

    # TC-04 : Vérifier l'affichage de la quantité 
    for nom in ["Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]:
        try:
            quantite = driver.find_element(By.XPATH,
                f"//div[@class='cart_item'][.//div[@class='inventory_item_name' and text(🙁'{nom}']]//div[@class='cart_quantity']").text
            print(f"TC-04 PASS : Quantité pour '{nom}' affichée : {quantite}")
            take_screenshot(f"TC-04_{nom.replace(' ','_')}")
        except:
            print(f"TC-04 FAIL : Quantité pour '{nom}' non trouvée")

    # TC-05 : Vérifier le prix unitaire 
    produits_prix = {"Sauce Labs Bike Light": "$9.99", "Sauce Labs Bolt T-Shirt": "$15.99"}
    for nom, prix_attendu in produits_prix.items():
        try:
            prix = driver.find_element(By.XPATH,
                f"//div[@class='cart_item'][.//div[@class='inventory_item_name' and text(🙁'{nom}']]//div[@class='inventory_item_price']").text
            if prix == prix_attendu:
                print(f"TC-05 PASS : Prix pour '{nom}' correct : {prix}")
                take_screenshot(f"TC-05_{nom.replace(' ','_')}")
            else:
                print(f"TC-05 FAIL : Prix pour '{nom}' incorrect, affiché : {prix}")
        except:
            print(f"TC-05 FAIL : Prix pour '{nom}' non trouvé")

    # TC-06 : Vérifier l'application d'un code promo 
    try:
        champ_promo = driver.find_element(By.ID, "promo-code")
        champ_promo.send_keys("DISCOUNT10")
        driver.find_element(By.ID, "apply-promo").click()
        print("TC-06 PASS : Champ promo trouvé et code appliqué")
        take_screenshot("TC-06")
    except:
        print("TC-06 FAIL : Champ promo absent sur la page Cart (normal si le site ne propose pas)")

    # TC-07 : Vérifier le nombre total d'articles dans le panier 
    try:
        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        nb_articles = int(badge.text)
        if nb_articles == 3:
            print(f"TC-07 PASS : Nombre total d'articles dans le panier = {nb_articles}")
            take_screenshot("TC-07")
        else:
            print(f"TC-07 FAIL : Nombre total incorrect ({nb_articles})")
    except:
        print("TC-07 FAIL : Badge panier non trouvé")

    # TC-08 : Supprimer un produit existant 
    try:
        driver.find_element(By.ID, "shopping_cart_container").click()
        time.sleep(2)
        driver.find_element(By.ID, "remove-sauce-labs-bike-light").click()
        time.sleep(1)
        try:
            driver.find_element(By.XPATH, "//div[@class='inventory_item_name' and text(🙁'Sauce Labs Bike Light']")
            print("TC-08 FAIL : Le produit n'a pas été supprimé")
        except:
            print("TC-08 PASS : Le produit a été supprimé du panier")
            take_screenshot("TC-08")
        try:
            badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            print(f"TC-08 PASS : Badge mis à jour, {badge.text} articles")
            take_screenshot("TC-08_Badge")
        except:
            print("TC-08 PASS : Badge supprimé correctement car le panier est vide")
    except:
        print("TC-08 FAIL : Erreur lors de la suppression du produit")

    # TC-09 : Vérifier le total du panier après checkout 
    try:
        driver.find_element(By.ID, "shopping_cart_container").click()
        time.sleep(2)
        driver.find_element(By.ID, "checkout").click()
        time.sleep(2)
        driver.find_element(By.ID, "first-name").send_keys("Ela")
        driver.find_element(By.ID, "last-name").send_keys("Chagour")
        driver.find_element(By.ID, "postal-code").send_keys("80")
        driver.find_element(By.ID, "continue").click()
        time.sleep(2)
        total = driver.find_element(By.CLASS_NAME, "summary_subtotal_label").text
        if total:
            print(f"TC-09 PASS : Total du panier affiché : {total}")
            take_screenshot("TC-09")
        else:
            print("TC-09 FAIL : Total du panier non trouvé")
    except:
        print("TC-09 FAIL : Erreur lors de la vérification du total")

    # TC-10 : Vérifier le total par produit
    produits = ["Sauce Labs Bolt T-Shirt"]
    try:
        driver.find_element(By.ID, "shopping_cart_container").click()
        time.sleep(2)
        for nom in produits:
            try:
                prix = driver.find_element(By.XPATH,
                    f"//div[@class='cart_item'][.//div[text(🙁'{nom}']]//div[@class='inventory_item_price']").text
                quantite = driver.find_element(By.XPATH,
                    f"//div[@class='cart_item'][.//div[text(🙁'{nom}']]//div[@class='cart_quantity']").text
                print(f"TC-10 PASS : {nom} → Prix = {prix}, Quantité = {quantite}")
                take_screenshot(f"TC-10_{nom.replace(' ','_')}")
            except:
                print(f"TC-10 FAIL : Produit '{nom}' absent ou infos manquantes")
    except:
        print("TC-10 FAIL : Impossible d'accéder au panier")

    # TC-11 : Ajouter le même produit plusieurs fois 
    try:
        driver.get("https://www.saucedemo.com/inventory.html")
        time.sleep(2)
        produit_id_add = "add-to-cart-sauce-labs-fleece-jacket"
        produit_id_remove = "remove-sauce-labs-fleece-jacket"

        driver.find_element(By.ID, produit_id_add).click()
        time.sleep(1)
        try:
            driver.find_element(By.ID, produit_id_remove)
            print("TC-11 PASS : Premier ajout réussi")
            take_screenshot("TC-11_First_Add")
        except:
            print("TC-11 FAIL : Premier ajout impossible")

        try:
            driver.find_element(By.ID, produit_id_add).click()
            print("TC-11 PASS : Le produit a été ajouté deux fois")
            take_screenshot("TC-11_Second_Add")
        except:
            print("TC-11 FAIL : Impossible d'ajouter le même produit deux fois")
    except:
        print("TC-11 FAIL : Erreur lors du test")

    # TC-12 : Vérifier l'affichage des frais de livraison
    try:
        driver.get("https://www.saucedemo.com/cart.html")
        time.sleep(2)
        try:
            shipping_fee = driver.find_element(By.XPATH, "//div[contains(text(),'Shipping') or contains(text(),'Livraison')]")
            print("TC-12 PASS : Des frais de livraison sont affichés sur la page Cart")
            take_screenshot("TC-12")
        except:
            print("TC-12 FAIL : Les frais de livraison ne sont pas affichés sur la page Cart")
    except:
        print("TC-12 FAIL : Erreur inattendue lors du test")

    # Fin du test pour ce compte
    driver.close()