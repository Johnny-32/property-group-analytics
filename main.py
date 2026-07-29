import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def otodom_parse(url):

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = "utf-8"
        html_content = response.text

    except requests.exceptions.HTTPError as errh:
        print(f"Błąd HTTP (np. złe uprawnienia, brak strony): {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Błąd połączenia (np. problem z internetem, błędny URL): {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Serwer nie odpowiedział w określonym czasie: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Coś poszło nie tak: {err}")

    soup = BeautifulSoup(html_content, "html.parser")

    adress_div = soup.find("a", class_="css-1eowip8 e1aypsbg1")
    adress = adress_div.text
    adress_list = [a.strip() for a in adress.split(",")]
        
    street = adress_list[0]
    street_list = [s.strip() for s in street.split()]
    
    is_exact_location = False
    is_only_street_name = False
    
    if (street_list[-1].isnumeric()):
        is_exact_location = True
    else:
        is_only_street_name = True
        
    if is_exact_location:
        print("Exact location")
    elif is_only_street_name:
        print("Only street")
    else:
        print("Nothing")
        

otodom_parse(
    # "https://www.otodom.pl/pl/oferta/przepieknie-wykonczone-po-remoncie-3-pok-lsm-bez-piecyka-ID4BT2w"
    "https://www.otodom.pl/pl/oferta/przestronne-umeblowane-mieszkanie-z-balkonem-i-garazem-ID4Cf46"
)
