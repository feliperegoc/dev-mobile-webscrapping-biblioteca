import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def scrape_book_info(driver, url):
    driver.get(url)
    time.sleep(2)  # Aguarda o carregamento da página

    books = []
    try:
        book_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-item"))
        )

        for book in book_elements:
            try:
                title = book.find_element(By.CSS_SELECTOR, ".product-item__name").text.strip()
                author = book.find_element(By.CSS_SELECTOR, ".product-item__author").text.strip()
                
                try:
                    year = book.find_element(By.CSS_SELECTOR, ".product-item__year").text.strip()
                except NoSuchElementException:
                    year = "Ano não disponível"
                
                # Nova lógica para capturar a URL da imagem
                img_element = book.find_element(By.CSS_SELECTOR, ".product-item__image")
                image_url = img_element.get_attribute("src") or img_element.get_attribute("data-src")
                
                if not image_url:
                    print(f"AVISO: URL da imagem não encontrada para o livro '{title}'")
                    continue  # Pula este livro se não houver URL de imagem
                
                books.append({
                    'title': title,
                    'author': author,
                    'year': year,
                    'image_url': image_url
                })
                print(f"Livro extraído: {title} por {author}")
            except Exception as e:
                print(f"Erro ao extrair informações do livro: {e}")

    except TimeoutException:
        print("Tempo excedido ao carregar os elementos da página")

    return books

def main():
    driver = initialize_driver()
    base_url = 'https://www.estantevirtual.com.br/busca?sort=best-sellers&page='
    page = 1
    all_books = []

    while True:
        url = f"{base_url}{page}"
        print(f"Scraping página {page}")
        
        books = scrape_book_info(driver, url)
        if not books:
            break

        all_books.extend(books)
        page += 1

        # Opcional: limite de páginas para teste
        if page > 5:
            break

    driver.quit()

    # Imprimir os resultados
    for book in all_books:
        print(f"Título: {book['title']}")
        print(f"Autor: {book['author']}")
        print(f"Ano: {book['year']}")
        print(f"URL da imagem: {book['image_url']}")
        print("---")

    print(f"Total de livros coletados: {len(all_books)}")

if __name__ == "__main__":
    main()