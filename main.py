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

    adress = soup.find("a", class_="css-1eowip8 e1aypsbg1").text
    adress_list = [a.strip() for a in adress.split(",")]

    # Parsing the street name or er the exact location (street name, building number)

    street = adress_list[0]
    street_list = [s.strip() for s in street.split()]

    is_exact_location = False
    is_only_street_name = False

    if street_list[-1].isnumeric():
        is_exact_location = True
    else:
        is_only_street_name = True

    # Parsing the price (without currency), add a notif. when a currency is different than PLN
    different_currency = False

    price = soup.find("strong", class_="css-1o51x5a engclhh1").text
    if "zł" in price:
        price = price.replace("zł", "")
        price = price.strip()
    else:
        different_currency = True

    price_square_meter = soup.find("div", class_="css-1mwdge5 engclhh5").text
    if different_currency == False:
        price_square_meter = price_square_meter.replace("zł/m²", "")
        price_square_meter.strip()

    property_type_header = soup.find("h2", class_="Bey1v _6Q9oO css-1xm0deg e16gw7u22").text
    
    is_apartment = False
    is_house_alike = False
    
    detail_div_list = [div.text for div in soup.find_all("div", class_="css-1okys8k e178zspo0")]
    
    interior_area = detail_div_list[1].split()[0]

    number_of_rooms = detail_div_list[3]
        
    property_type = None
    
    year_of_construction = None
    
    owner_expenses = None
        
    if "Mieszkanie" in property_type_header:
        property_type = "Apartment"
        is_balcony = None
        is_basement = None
        is_elevator = None
        is_terrace = None
        
        floor_number = detail_div_list[7]
        floor_number = floor_number.replace("parter/", "0/")
        
        # owner_expenses = detail_div_list[9]
        # owner_expenses = owner_expenses.replace("/miesiąc", "")
        
        for i, detail in enumerate(detail_div_list):
            if "balkon" in detail:
                is_balcony = True
            if "piwnica" in detail:
                is_basement = True
            if "winda" in detail:
                is_elevator = True
            if "Winda:" in detail:
                current_idx = i
                if detail_div_list[current_idx + 1] == "tak":
                    is_elevator = True
                elif detail_div_list[current_idx + 1] == "nie":
                    is_elevator = False                
            if "taras" in detail:
                is_terrace = True
                
            if "Rok budowy:" in detail:
                current_idx = i
                if detail_div_list[current_idx + 1].isnumeric():
                    year_of_construction = detail_div_list[current_idx + 1]
            
            if "Czynsz:" in detail:
                current_idx = i
                if any(char.isdigit() for char in detail_div_list[current_idx + 1]):
                    owner_expenses = detail_div_list[current_idx + 1].replace("/miesiąc", "")

        
    if "Dom" in property_type_header:
        property_type_temp = detail_div_list[5]
        plot_area = None
        
        if "wolnostojący" in property_type_temp:
            property_type = "Single-family-house"
        elif "bliźniak" in property_type_temp:
            property_type = "Duplex"
        elif "szeregowiec" in property_type_temp:
            property_type = "Townhouse"
        elif "kamienica" in property_type_temp:
            property_type = "Tenement"
        elif "gospodarstwo" in property_type_temp:
            property_type = "Farm"
        else:
            property_type = "Other"
            
        for i, detail in enumerate(detail_div_list):
            if "Rok budowy:" in detail:
                current_idx = i
                if detail_div_list[current_idx + 1].isnumeric():
                    year_of_construction = detail_div_list[current_idx + 1]
            
            if "Liczba pięter:" in detail:
                current_idx = i
                if any(char.isdigit() for char in detail_div_list[current_idx + 1]):
                    number_of_floors = detail_div_list[current_idx + 1].split()[0]
            
            if "Powierzchnia działki:" in detail:
                current_idx = i
                if any(char.isdigit() for char in detail_div_list[current_idx + 1]):
                    plot_area = detail_div_list[current_idx + 1]
                    plot_area = plot_area.split(" ")[0]
                    

    print("Test dla mieszkania:")
    print(f"interior_area: {interior_area}")
    print(f"number_of_rooms: {number_of_rooms}")
    print(f"property_type: {property_type}")
    print(f"is_balcony: {is_balcony}")
    print(f"is_basement: {is_basement}")
    print(f"is_elevator: {is_elevator}")
    print(f"is_terrace: {is_terrace}")
    print(f"floor_number: {floor_number}")
    print(f"year_of_construction: {year_of_construction}")
    print(f"owner_expenses: {owner_expenses}")
    
    
    

            

    
    
    
otodom_parse(
    "https://www.otodom.pl/pl/oferta/4-pokoje-blisko-centrum-idealne-dla-rodziny-lub-inwestora-ID4Bt11"
)
