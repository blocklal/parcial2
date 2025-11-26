import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .forms import ScraperForm


@login_required
def scrape_view(request):
    results = {}
    keyword = None

    if request.method == "POST":
        form = ScraperForm(request.POST)

        if form.is_valid():
            keyword = form.cleaned_data["keyword"]

            search_url = "https://es.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "search",
                "srsearch": keyword,
                "format": "json"
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; DjangoScraper/1.0; +https://example.com)"
            }


            response = requests.get(search_url, params=params, headers=headers)

            try:
                data = response.json()
            except ValueError:
                results["error"] = "Error al recibir datos desde Wikipedia."
                return render(request, "scraper/scrape.html", {
                    "form": form,
                    "results": results
                })

            if not data["query"]["search"]:
                results["error"] = "No se encontró ninguna página relacionada."
                return render(request, "scraper/scrape.html", {"form": form, "results": results})

            page_title = data["query"]["search"][0]["title"]
            page_url = f"https://es.wikipedia.org/wiki/{page_title.replace(' ', '_')}"

            html = requests.get(page_url, headers=headers).text
            soup = BeautifulSoup(html, "html.parser")

            title = soup.find("h1").get_text()
            summary = soup.find("p").get_text().strip()

            content = soup.find("div", {"class": "mw-parser-output"})
            links = content.find_all("a", href=True)[:10]

            link_list = [
                {"texto": a.get_text(), "url": "https://es.wikipedia.org" + a["href"]}
                for a in links if a.get_text().strip()
            ]

            results = {
                "title": title,
                "summary": summary,
                "links": link_list,
                "page_url": page_url,
            }

    else:
        form = ScraperForm()

    return render(request, "scrape.html", {
        "form": form,
        "results": results,
        "keyword": keyword,
    })

def send_results_email(email, keyword, results):
    body = f"Resultados del scraping de Wikipedia para: {keyword}\n\n"
    body += f"Título: {results['title']}\n"
    body += f"URL: {results['page_url']}\n"
    body += f"Resumen: {results['summary']}\n\n"
    body += "Enlaces:\n"

    for link in results["links"]:
        body += f"- {link['texto']}: {link['url']}\n"

    msg = EmailMessage(
        subject=f"Wikipedia: {keyword}",
        body=body,
        from_email="tu_correo@example.com",
        to=[email],
    )

    msg.send()
