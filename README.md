# MensAPI
## Eine API für die wöchentlichen Menüs des Studierendenwerks Düsseldorf, mit Frontend
Die Anwendung bezieht die Daten der [Website des Studierendenwerks](https://mocca.stw-d.de/mocca.digitalsignage/3500/Speiseplan3500/Index.html). Es stellt diese dann mittels FastAPI zur Verfügung, das automatisch eine OpenAPI Dokumentation der Schnittstelle bereitstellt.

Ein Svelte-Frontend zeigt das wöchentliche Menü an. Dabei sehen sie in mit D3.js visualisierten Donut-Charts die Nähwerte, Preise und auch die Allergene der Speisen auf einen Blick.

# Schnitstelle lokal aufsetzen
Sie klonen das Repository und starten dann mit dem Dependency Management die API:

```bash
git clone https://github.com/kawa800/MensAPI
uv run fastapi dev
```

Das Scraping-Modul holt sich die aktuellen Daten von der Website, speichert diese in einer SQLite-Datenbank ab und stellt diese dann an den Endpunkten bereit. Diese Dokumentiert FastAPI automatisch unter 'http://127.0.0.1:8000/docs'. Dabei gibt das Modul die Garantie, dass die Datenbank keine Duplikate speichert. Sie führen das Modul aus mit:
```bash
uv run scraper
```
Das Frontend starten Sie indem Sie zu ```/frontend``` navigieren und npm starten:
````bash
npm run dev
``````




## 🛠️ Stack

- **Backend:** FastAPI (SQL Alchemy Models und Pydantic Data Verification)
- **Frontend:** Svelte and TypeScript 
- **Datenbank:** SQLite
- **Scraping:** Selenium
- **Visualisierung:** D3.js 
- **Dependency Management:** uv 
