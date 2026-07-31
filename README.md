# Property group analytics

## Property details
- Address
  - Is it an exact location or only street name
- Price
  - Is it in national currency or something different
- Interior area
- Number of rooms
- Property type
- Year of construction
- Owner expenses
- Plot area

### For an apartment
- Balcony
- Basement
- Terrace
- Elevator
- Owner expenses

### For a house
- Number of floors
- Plot area

## Future features
- Adding property details like adress, price, interior area, ..., just by pasting a link to the property
- Comparing groups of properties in an attractive manner (two column layout for bigger screens)
- Option of currency conversion
- Compatibility with websites from:
  -  Poland (otodom, olx)
  -  Denmark (boligsiden)
  -  Norway (finn.no)
  -  Austria (willhaben)
- Add a geolocation to each property via OSM Nominatim
- Add m to ft conversion
- Add a final price (with all the taxes and fees if possible)
- For now I'm focusing on houses-alike and apartments, in the future maybe I'll add support for rooms, plots of land
- Add explanations for owner_expenses, beacuse they mean something different in pretty much every country
- Add different color schemes for properties (like in hemnet.se, boligsiden.dk)

## To do:
- Store useful commands like: python -m pipreqs.pipreqs . --encoding=utf-8 --ignore .venv,venv --force
- Finish testing variables
- Add None protected variables
- Add more functions to clean up code
- Think about is df be the best for 2d data?
