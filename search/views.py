from django.shortcuts import render
from .forms import SearchForm
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
import csv
import urllib.parse


# Funkce pro vyhledávání
def search_google(keyword):
    url = f'https://www.google.com/search?q={keyword}&num=10'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    search_results = []
    for g in soup.find_all('div', class_='g'):
        title = g.find('h3')
        link = g.find('cite', class_='cHaqb')
        description = g.find('div', class_='VwiC3b')
        if title and link and description:
            search_results.append({
                'title': title.text.strip(),
                'link': link.text.strip(),
                'description': description.text.strip()
            })

    return search_results


# Funkce pro vytvoření a stažení CSV souboru
def download_csv(request, keyword):
    search_results = request.session.get('search_results', [])

    # Kontrola, zda jsou výsledky k dispozici
    if not search_results:
        return HttpResponse("Žádné výsledky ke stažení.", status=404)

    # Vytvoření CSV odpovědi
    response = HttpResponse(content_type='text/csv')
    filename = f'results_{keyword.replace(" ", "_")}.csv'
    quoted_filename = urllib.parse.quote(filename)
    response['Content-Disposition'] = f'attachment; filename="{quoted_filename}"'

    writer = csv.writer(response)

    for result in search_results:
        writer.writerow([result.get('title', '')])
        writer.writerow([result.get('link', '')])
        writer.writerow([result.get('description', '')])
        writer.writerow([])  # Přidání prázdného řádku pro oddělení jednotlivých výsledků

    return response


# Funkce pro zpracování a zobrazení výsledků vyhledávání
def index(request):
    form = SearchForm()
    results = None
    keyword = ''

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            search_results = search_google(keyword)
            request.session['search_results'] = search_results
            request.session['keyword'] = keyword
            results = search_results

    return render(request, 'search/index.html', {
        'form': form,
        'results': results,
        'keyword': keyword,
    })
