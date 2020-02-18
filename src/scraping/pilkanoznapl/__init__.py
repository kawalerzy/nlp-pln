MAX_PAGE_NUM = 1899
base_url = 'https://pilkanozna.pl'
columns = ['link', 'title', 'category', 'date']

categories = {
    64: "ekstraklasa",
    65: "1liga",
    66: "reprezentacja",
    117: "bundesliga",
    134: "premierleague"
}

categories_map = {
    'Reprezentacja Polski': 'reprezentacja',
    'Ligi zagraniczne - Anglia': 'premierleague',
    'Ligi zagraniczne - Niemcy': 'bundesliga',
    "I Liga": "1liga",
    "Ekstraklasa": "ekstraklasa"
}

page_limits = {
    64: 1891,
    65: 244,
    66: 296,
    117: 365,
    134: 721
}

months = {
    'Styczeń': 1,
    'Luty': 2,
    'Marzec': 3,
    'Kwiecień': 4,
    'Maj': 5,
    'Czerwiec': 6,
    'Lipiec': 7,
    'Sierpień': 8,
    'Wrzesień': 9,
    'Październik': 10,
    'Listopad': 11,
    'Grudzień': 12
}
