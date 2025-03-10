import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
# URL страницы с диванами
base_url = "https://www.divan.ru/category/divany-i-kresla"

# Основной цикл для перехода по страницам
page = 1
url = base_url
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
# Список для хранения данных
data = []

while True:
    # Формируем URL для каждой страницы
    #url = f"{base_url}?page={page}"
    print(f"Переход на страницу: {url}")


    response = requests.get(url, headers=headers)
    # HTTP-запрос к странице
    response = requests.get(url)

    # Проверка успешности запроса
    if response.status_code == 200:
        # Парсинг HTML-контента с помощью BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')



        divans = soup.find_all('div', class_="lsooF")
        if divans:
            for divan in divans:
                try:
                    name = divan.find('span', itemprop='name').text.strip()
                    price = divan.find('meta', itemprop='price')['content']
                    currency = divan.find('meta', itemprop='priceCurrency')['content']
                    data.append({'Name': name, 'Price': price, 'Currency': currency})
                except Exception as e:
                    print(f"Ошибка при парсинге элемента: {e}")


        else:
            print("No divans found on the page.")
        #next_button = soup.find('a', class_='next')  # Пример класса для кнопки "Следующая страница"
        #if not next_button:
            #break  # Если кнопки "Следующая страница" нет, завершаем цикл

        # Переходим на следующую страницу
        page += 1
        url = f"{base_url}?page-{page}"
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        break
    if page==2:
        break
df = pd.DataFrame(data)
#print(df)
#df.to_csv('divan_price.csv', index=False)
print("Data saved to divan_price.csv")

df['Price'] = df['Price'].str.replace(',', '').astype(float)
print(df['Price'].mean())#Среднее значение цены
#Выводим данные в виде гистограммы
plt.hist(df['Price'], bins=10)
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.title('Price Distribution')
plt.show()
'''
plt.scatter(df['Price'])
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.title('Price Distribution')
plt.show()'''