import requests
from bs4 import BeautifulSoup
import json

# URL de la page du classement Bundesliga
base_url = 'https://www.bundesliga.com'
classement_url = 'https://www.bundesliga.com/fr/bundesliga/classement'

# En-têtes HTTP pour simuler une requête depuis un navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# Fonction pour convertir une valeur en entier ou flottant
def convert_to_number(value):
    try:
        if ":" in value:  # Gérer le cas "36:36"
            return [int(v) for v in value.split(":")]
        elif "." in value:  # Gérer les valeurs décimales
            return float(value)
        else:
            return int(value)
    except ValueError:
        return value  # Retourner la valeur d'origine si elle n'est pas convertible

# Requête HTTP vers la page du classement
response = requests.get(classement_url, headers=headers)

if response.status_code == 200:
    # Analyser le contenu HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Trouver le tableau de classement
    tbody = soup.find('tbody')
    if not tbody:
        print("Impossible de trouver le tableau de classement.")
        exit()
    
    clubs = []
    
    # Parcourir chaque ligne du tableau
    for tr in tbody.find_all('tr'):
        # Récupérer le numéro de classement
        rank_span = tr.find('td', class_='rank')
        rank = int(rank_span.find('span').get_text(strip=True)) if rank_span else None  # Conversion directe
        
        # Récupérer le nom de l'équipe
        team_span = tr.find('td', class_='team').find_all('span')
        team_name = team_span[1].get_text(strip=True) if len(team_span) > 1 else None
        
        # Récupérer le lien de la page du club
        logolink_tag = tr.find('td', class_='logo').find('a', href=True)
        club_page_url = base_url + logolink_tag['href'] if logolink_tag else None
        
        # Initialiser les statistiques et URL du logo
        club_stats = None
        focused_stats = None
        logo_url = None
        
        if club_page_url:
            # Requête vers la page du club
            club_page_response = requests.get(club_page_url, headers=headers)
            if club_page_response.status_code == 200:
                club_page_soup = BeautifulSoup(club_page_response.content, 'html.parser')
                
                # Récupérer le logo depuis .logo img src
                logo_img = club_page_soup.find('img', class_='logo')
                if logo_img:
                    logo_url = logo_img.get('src')
                
                # Extraire les lignes de statistiques dans .club-stats-table
                stats_table = club_page_soup.find('div', class_='club-stats-table')
                if stats_table:
                    stats_rows = stats_table.find_all('div', class_='row')  # Chaque ligne de statistiques
                    club_stats = {}
                    for row in stats_rows:
                        key = row.find('div', class_='key')
                        value = row.find('div', class_='value')
                        if key and value:
                            stat_key = key.get_text(strip=True)
                            stat_value = convert_to_number(value.get_text(strip=True))  # Convertir en nombre
                            club_stats[stat_key] = stat_value
                
                # Extraire les statistiques de .table-club-focused
                focused_table = club_page_soup.find('tr', class_='table-club-focused')
                if focused_table:
                    focused_stats = {
                        'nbr_matches': convert_to_number(focused_table.find('td', class_='matches').find('span').get_text(strip=True)),
                        'nbr_wins': convert_to_number(focused_table.find('td', class_='wins').find('span').get_text(strip=True)),
                        'nbr_draws': convert_to_number(focused_table.find('td', class_='draws').find('span').get_text(strip=True)),
                        'nbr_losses': convert_to_number(focused_table.find('td', class_='losses').find('span').get_text(strip=True)),
                        'goals': convert_to_number(focused_table.find('td', class_='goals').find('span').get_text(strip=True))  # Gérer "36:36"
                    }
        
        # Ajouter les données dans la liste
        if rank and team_name and logo_url:
            clubs.append({
                'rank': rank,
                'team': team_name,
                'logo': logo_url,
                'club_page': club_page_url,
                'stats': club_stats,
                'focused_stats': focused_stats
            })
    
    # Sauvegarder les données dans un fichier JSON
    with open('bundes.json', 'w', encoding='utf-8') as f:
        json.dump(clubs, f, ensure_ascii=False, indent=4)
    
    print("Les données des clubs avec leur classement et statistiques détaillées ont été sauvegardées dans 'bundes.json'.")
else:
    print(f"Erreur lors de la requête : {response.status_code}")
