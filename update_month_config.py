"""
Update Month Config
===================
Updates kluby.json config for a new month without manual JSON editing.

Usage:
    python update_month_config.py              # Uses next month automatically
    python update_month_config.py --month 7 --year 2026
    python update_month_config.py --preview    # Show what would change, don't save
"""

import argparse
import calendar
import json
from datetime import date


CZECH_MONTHS = {
    1: 'leden', 2: 'únor', 3: 'březen', 4: 'duben',
    5: 'květen', 6: 'červen', 7: 'červenec', 8: 'srpen',
    9: 'září', 10: 'říjen', 11: 'listopad', 12: 'prosinec',
}

ENGLISH_MONTHS = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December',
}


def next_month(year: int, month: int):
    """Return (year, month) for the following month."""
    if month == 12:
        return year + 1, 1
    return year, month + 1


def main():
    parser = argparse.ArgumentParser(description='Update kluby.json config for a new month')
    parser.add_argument('--month', type=int, help='Month number (1-12)')
    parser.add_argument('--year', type=int, help='Year (e.g. 2026)')
    parser.add_argument('--preview', action='store_true', help='Show changes without saving')
    args = parser.parse_args()

    # Determine target month
    if args.month and args.year:
        target_month = args.month
        target_year = args.year
    else:
        today = date.today()
        target_year, target_month = next_month(today.year, today.month)
        print(f"Žádný měsíc nezadán — používám příští měsíc: {CZECH_MONTHS[target_month]} {target_year}")

    if not (1 <= target_month <= 12):
        print(f"Chyba: Neplatný měsíc {target_month} (musí být 1-12)")
        return

    days_in_month = calendar.monthrange(target_year, target_month)[1]

    # Load config
    with open('kluby.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    current = data['config']
    print(f"\nAktuální config: {current['mesic']} {current['rok']} (měsíc {current['mesic_cislo']}, {current['pocet_dni']} dní)")

    new_config = {
        'mesic': CZECH_MONTHS[target_month],
        'mesic_en': ENGLISH_MONTHS[target_month],
        'rok': target_year,
        'mesic_cislo': target_month,
        'pocet_dni': days_in_month,
    }

    print(f"Nový config:     {new_config['mesic']} {new_config['rok']} (měsíc {new_config['mesic_cislo']}, {new_config['pocet_dni']} dní)")

    if args.preview:
        print("\n[Preview] Změny nebyly uloženy (použij bez --preview pro uložení).")
        return

    data['config'].update(new_config)

    with open('kluby.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ kluby.json aktualizován pro {new_config['mesic']} {new_config['rok']}.")
    print("Spusť: python scrape_concerts.py")


if __name__ == '__main__':
    main()
