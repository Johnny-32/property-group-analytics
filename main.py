from bs4 import BeautifulSoup
from curl_cffi import requests
import json


def parse_website(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(
            url, headers=headers, impersonate="chrome120", timeout=10
        )
        response.raise_for_status()

    except Exception as e:
        print("Błąd pobierania: {e}")
        return None
    
    html_text = response.content.decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html_text, "html.parser")

    return soup

def otodom_parse(url):

    soup = parse_website(url)

    adress_div = soup.find("a", class_="css-1eowip8 e1aypsbg1").text
    adress_parts = [a.strip() for a in adress_div.split(",")]

    # Parsing the street name or er the exact location (street name, building number)

    street = adress_parts[0]
    street_words = [s.strip() for s in street.split()]

    is_exact_location = False
    is_only_street_name = False

    if street_words[-1].isnumeric():
        is_exact_location = True
    else:
        is_only_street_name = True

    # Parsing the price (without currency), add a notif. when a currency is different than PLN
    price = soup.find("strong", class_="css-1o51x5a engclhh1").text
    different_currency = False

    if "zł" in price:
        price = price.replace("zł", "").strip()
    else:
        different_currency = True

    price_square_meter = soup.find("div", class_="css-1mwdge5 engclhh5").text

    if not different_currency:
        price_square_meter = (
            price_square_meter.replace("zł/m²", "").replace(",", ".").strip()
        )

    property_type_header = soup.find(
        "h2", class_="Bey1v _6Q9oO css-1xm0deg e16gw7u22"
    ).text

    detail_div_list = [
        div.text for div in soup.find_all("div", class_="css-1okys8k e178zspo0")
    ]

    interior_area = detail_div_list[1].split()[0]
    number_of_rooms = detail_div_list[3]

    is_apartment = False
    is_house_alike = False

    property_type = None
    year_of_construction = None
    owner_expenses = None
    plot_area = None

    if "Mieszkanie" in property_type_header:
        property_type = "Apartment"
        is_balcony = None
        is_basement = None
        is_elevator = None
        is_terrace = None

        floor_number = detail_div_list[7].replace("parter/", "0/")

        for i, detail in enumerate(detail_div_list):
            next_val = detail_div_list[i + 1] if i + 1 < len(detail_div_list) else ""
            if "balkon" in detail:
                is_balcony = True
            if "piwnica" in detail:
                is_basement = True
            if "taras" in detail:
                is_terrace = True

            if "Winda:" in detail:
                current_idx = i
                if next_val == "tak":
                    is_elevator = True
                elif next_val == "nie":
                    is_elevator = False
            if "winda" in detail:
                is_elevator = True

            if "Rok budowy:" in detail and next_val.isnumeric():
                year_of_construction = next_val

            if "Czynsz:" in detail and any(char.isdigit() for char in next_val):
                owner_expenses = next_val.replace("/miesiąc", "")

    elif "Dom" in property_type_header:
        property_type_temp = detail_div_list[5]

        house_types = {
            "wolnostojący": "Single-family-house",
            "bliźniak": "Duplex",
            "szeregowiec": "Townhouse",
            "kamienica": "Tenement",
            "gospodarstwo": "Farm",
        }

        property_type = "Other"
        for key, val in house_types.items():
            if key in property_type_temp:
                property_type = val
                break

        for i, detail in enumerate(detail_div_list):
            next_val = detail_div_list[i + 1] if i + 1 < len(detail_div_list) else ""

            if "Rok budowy:" in detail and next_val.isnumeric():
                year_of_construction = next_val

            if "Liczba pięter:" in detail and any(char.isdigit() for char in next_val):
                number_of_floors = next_val.split()[0]

            if "Powierzchnia działki:" in detail and any(
                char.isdigit() for char in next_val
            ):
                plot_area = next_val.split()[0]

    # print("Test for an apartment:")
    # print(f"interior_area: {interior_area}")
    # print(f"number_of_rooms: {number_of_rooms}")
    # print(f"property_type: {property_type}")
    # print(f"year_of_construction: {year_of_construction}")
    # print(f"price_square_meter: {price_square_meter}")
    # print(f"is_balcony: {is_balcony}")
    # print(f"is_basement: {is_basement}")
    # print(f"is_elevator: {is_elevator}")
    # print(f"is_terrace: {is_terrace}")
    # print(f"floor_number: {floor_number}")
    # print(f"owner_expenses: {owner_expenses}")

    # print("Test for a house:")
    # print(f"interior_area: {interior_area}")
    # print(f"number_of_rooms: {number_of_rooms}")
    # print(f"property_type: {property_type}")
    # print(f"year_of_construction: {year_of_construction}")
    # print(f"number_of_floors: {number_of_floors}")
    # print(f"plot_area: {plot_area}")


def olx_parse(url):

    soup = parse_website(url)

    # adress_div = soup.find("div", class_="css-1r8egxr")

    # # for adress in adress_div:
    # #     print(f"{adress}\n\n")
    # adress_words = adress_div.find_all("p")
    # adress_words = [word.text for word in adress_words]
    # print(adress_words)

    adress_divs = soup.find_all("div", class_="css-1r8egxr")

    for i, div in enumerate(adress_divs):
        texts = [p.text.strip() for p in div.find_all("p")]
        print(f"Index {i}: {texts}")


# otodom_parse(
#     # "https://www.otodom.pl/pl/oferta/dom-w-komfortowej-lokalizacji-na-wyzwolenia-ID4zraw"
#     "https://www.otodom.pl/pl/oferta/4-pokoje-blisko-centrum-idealne-dla-rodziny-lub-inwestora-ID4Bt11"
# )

olx_parse(
    "https://www.olx.pl/d/oferta/sprzedam-mieszkanie-39-7-m2-lublin-czechow-CID3-ID1bzMNv.html?search_reason=search%7Corganic"
)
