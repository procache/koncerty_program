# Produkční stabilizace — TO-DO

Cíl: opravit kritické problémy před nasazením na vlastní doménu.

## Fáze 1: Bezpečnost + kritické opravy

- [x] **1.1** XSS fix — `generate_html.py`: obalit artist/venue/url přes `html.escape()`
- [x] **1.2** Playwright cleanup — `browser_scraper.py`: `browser.close()` do `try/finally` (metody `fetch_html_with_browser` + `fetch_with_infinite_scroll`)
- [x] **1.3** Dynamické víkendy — `base_scraper.py`: nahradit hardcoded NOV 2025 weekends dynamickým výpočtem přes `calendar` modul
- [x] **1.4** Dynamický rok — `scraper_rockcafe.py`: nahradit `range(2010, 2027)` výrazem `range(2000, self.year + 1)`

## Fáze 2: Retry + error handling

- [x] **2.1** Retry mechanismus — `base_scraper.py`: exponential backoff (3 pokusy, 2/4/8s), pouze pro transient chyby
- [x] **2.2** Vlastní error typy — `base_scraper.py`: `ScraperError`, `NetworkError` místo generic `Exception`
- [x] **2.3** Interaktivní potvrzení — `scrape_concerts.py`: validační report + `input()` při RED venues + flag `--force`

## Fáze 3: Config helper

- [x] **3.1** `update_month_config.py`: auto-update `kluby.json` pro nový měsíc (bez manuální editace JSON)
