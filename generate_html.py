"""
HTML Generator for Concert Program
====================================
Generates responsive HTML page from events_data.json

Features:
- City filtering (Praha/Plzeň)
- Search functionality
- Responsive design
- Gradient background
- Sorted by date
"""

import json
from datetime import datetime


def load_events_data(filename='events_data.json'):
    """Load events from JSON file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_html(data):
    """Generate complete HTML page"""

    month_name = data['month_name'].capitalize()
    year = data['year']
    total_events = data['total_events']

    # Collect all events and sort by date
    all_events = []
    for venue_data in data['venues']:
        for event in venue_data['events']:
            all_events.append(event)

    # Sort by day
    all_events.sort(key=lambda x: x['day'])

    # Count events by city
    praha_count = sum(1 for e in all_events if e['city'] == 'Praha')
    plzen_count = sum(1 for e in all_events if e['city'] == 'Plzeň')

    html = f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Koncerty {month_name} {year} - Praha & Plzeň</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}

        .subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}

        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}

        .stat {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }}

        .stat strong {{
            font-size: 1.5rem;
        }}

        .controls {{
            padding: 20px 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .search-box {{
            flex: 1;
            min-width: 250px;
        }}

        .search-box input {{
            width: 100%;
            padding: 12px 20px;
            border: 2px solid #dee2e6;
            border-radius: 25px;
            font-size: 1rem;
            transition: all 0.3s;
        }}

        .search-box input:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        .city-filters {{
            display: flex;
            gap: 10px;
        }}

        .city-filter {{
            padding: 10px 20px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
        }}

        .city-filter:hover {{
            background: #667eea;
            color: white;
        }}

        .city-filter.active {{
            background: #667eea;
            color: white;
        }}

        .calendar-section {{
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}

        .calendar-title {{
            text-align: center;
            margin-bottom: 15px;
            color: #2c3e50;
            font-size: 1.1rem;
            font-weight: 600;
        }}

        .calendar-grid {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 5px;
            max-width: 400px;
            margin: 0 auto;
        }}

        .calendar-day-header {{
            text-align: center;
            font-weight: 600;
            color: #6c757d;
            padding: 5px;
            font-size: 0.75rem;
        }}

        .calendar-day {{
            aspect-ratio: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
            font-size: 0.85rem;
            color: #2c3e50;
            position: relative;
        }}

        .calendar-day:hover {{
            border-color: #667eea;
            background: #f0f4ff;
            transform: translateY(-2px);
        }}

        .calendar-day.has-events::after {{
            content: '';
            position: absolute;
            bottom: 2px;
            width: 4px;
            height: 4px;
            background: #667eea;
            border-radius: 50%;
        }}

        .calendar-day.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
        }}

        .calendar-day.active::after {{
            background: white;
        }}

        .calendar-day.empty {{
            background: transparent;
            border: none;
            cursor: default;
        }}

        .calendar-day.empty:hover {{
            transform: none;
        }}

        .clear-date-filter {{
            display: none;
            margin: 15px auto 0;
            padding: 8px 16px;
            background: #6c757d;
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.3s;
        }}

        .clear-date-filter:hover {{
            background: #5a6268;
        }}

        .clear-date-filter.visible {{
            display: block;
        }}

        .events-container {{
            padding: 30px;
        }}

        .event-card {{
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s;
            display: flex;
            gap: 20px;
        }}

        .event-card:hover {{
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
            transform: translateY(-2px);
        }}

        .event-date {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            min-width: 80px;
        }}

        .event-day {{
            font-size: 2rem;
            font-weight: bold;
            line-height: 1;
        }}

        .event-month {{
            font-size: 0.9rem;
            opacity: 0.9;
            margin-top: 5px;
        }}

        .event-info {{
            flex: 1;
        }}

        .event-artist {{
            font-size: 1.3rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 8px;
        }}

        .event-details {{
            color: #6c757d;
            font-size: 0.95rem;
        }}

        .event-venue {{
            font-weight: 600;
            color: #667eea;
        }}

        .event-city {{
            display: inline-block;
            padding: 3px 10px;
            background: #e7f3ff;
            color: #0066cc;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-left: 10px;
        }}

        .event-city.plzen {{
            background: #fff3e0;
            color: #e65100;
        }}

        .event-time {{
            margin-left: 10px;
        }}

        .event-link {{
            align-self: center;
        }}

        .event-link a {{
            display: inline-block;
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 20px;
            font-weight: 600;
            transition: all 0.3s;
        }}

        .event-link a:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}

        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: #6c757d;
        }}

        .no-results h2 {{
            font-size: 1.5rem;
            margin-bottom: 10px;
        }}

        footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 1.8rem;
            }}

            .event-card {{
                flex-direction: column;
            }}

            .event-date {{
                min-width: auto;
            }}

            .controls {{
                flex-direction: column;
                align-items: stretch;
            }}

            .city-filters {{
                justify-content: stretch;
            }}

            .city-filter {{
                flex: 1;
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Koncerty {month_name} {year}</h1>
            <div class="subtitle">Praha & Plzeň</div>
            <div class="stats">
                <div class="stat">
                    <strong>{total_events}</strong> koncertů
                </div>
                <div class="stat">
                    <strong>{len(data['venues'])}</strong> klubů
                </div>
                <div class="stat">
                    Praha: <strong>{praha_count}</strong>
                </div>
                <div class="stat">
                    Plzeň: <strong>{plzen_count}</strong>
                </div>
            </div>
        </header>

        <div class="calendar-section">
            <div class="calendar-title">Vyberte datum</div>
            <div class="calendar-grid">
                <!-- Day headers -->
                <div class="calendar-day-header">Po</div>
                <div class="calendar-day-header">Út</div>
                <div class="calendar-day-header">St</div>
                <div class="calendar-day-header">Čt</div>
                <div class="calendar-day-header">Pá</div>
                <div class="calendar-day-header">So</div>
                <div class="calendar-day-header">Ne</div>
"""

    # Calculate which day of week November 1st falls on (0=Monday, 6=Sunday)
    from datetime import datetime
    first_day = datetime(year, data['month'], 1)
    start_weekday = first_day.weekday()  # 0=Monday, 6=Sunday

    # Get total days in month (from config)
    total_days = 30  # November has 30 days

    # Collect which days have events
    days_with_events = set()
    for event in all_events:
        days_with_events.add(event['day'])

    # Add empty cells before the first day
    for _ in range(start_weekday):
        html += '                <div class="calendar-day empty"></div>\n'

    # Add day cells
    for day in range(1, total_days + 1):
        has_events_class = 'has-events' if day in days_with_events else ''
        html += f'                <div class="calendar-day {has_events_class}" data-day="{day}">{day}</div>\n'

    html += """            </div>
            <button class="clear-date-filter" id="clearDateFilter">Zobrazit všechny dny</button>
        </div>

        <div class="controls">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Hledat kapelu, klub nebo místo...">
            </div>
            <div class="city-filters">
                <button class="city-filter active" data-city="all">Všechny</button>
                <button class="city-filter" data-city="Praha">Praha</button>
                <button class="city-filter" data-city="Plzeň">Plzeň</button>
            </div>
        </div>

        <div class="events-container" id="eventsContainer">
"""

    # Generate event cards
    for event in all_events:
        city_class = 'plzen' if event['city'] == 'Plzeň' else 'praha'

        html += f"""
            <div class="event-card" data-city="{event['city']}" data-day="{event['day']}" data-search="{event['artist'].lower()} {event['venue'].lower()} {event['city'].lower()}">
                <div class="event-date">
                    <div class="event-day">{event['day']}</div>
                    <div class="event-month">{month_name}</div>
                </div>
                <div class="event-info">
                    <div class="event-artist">{event['artist']}</div>
                    <div class="event-details">
                        <span class="event-venue">{event['venue']}</span>
                        <span class="event-city {city_class}">{event['city']}</span>
                        <span class="event-time">⏰ {event['time']}</span>
                    </div>
                </div>
                <div class="event-link">
                    <a href="{event['url']}" target="_blank">Více info</a>
                </div>
            </div>
"""

    html += """
        </div>

        <div class="no-results" id="noResults" style="display: none;">
            <h2>Žádné výsledky</h2>
            <p>Zkuste změnit vyhledávací kritéria</p>
        </div>

        <footer>
            <p>Vygenerováno automaticky · Celkem 20 klubů</p>
            <p style="margin-top: 5px; font-size: 0.9rem;">
                O2 Arena · O2 Universum · Palác Akropolis · Rock Café · Lucerna Music Bar · Roxy · Vagon · Jazz Dock ·
                Forum Karlín · MeetFactory · Malostranská beseda · Reduta Jazz Club · U Staré Paní · Cross Club ·
                Tipsport Arena · Watt Music Club · Divadlo Pod lampou · KD Šeříkovka · Buena Vista Club · Papírna Plzeň
            </p>
        </footer>
    </div>

    <script>
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const eventsContainer = document.getElementById('eventsContainer');
        const noResults = document.getElementById('noResults');
        const eventCards = document.querySelectorAll('.event-card');
        const cityFilters = document.querySelectorAll('.city-filter');
        const calendarDays = document.querySelectorAll('.calendar-day:not(.empty)');
        const clearDateButton = document.getElementById('clearDateFilter');

        let currentCity = 'all';
        let currentSearch = '';
        let currentDay = null;  // null means all days

        function filterEvents() {
            let visibleCount = 0;

            eventCards.forEach(card => {
                const cardCity = card.dataset.city;
                const cardSearch = card.dataset.search;
                const cardDay = parseInt(card.dataset.day);

                const cityMatch = currentCity === 'all' || cardCity === currentCity;
                const searchMatch = cardSearch.includes(currentSearch.toLowerCase());
                const dayMatch = currentDay === null || cardDay === currentDay;

                if (cityMatch && searchMatch && dayMatch) {
                    card.style.display = 'flex';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            if (visibleCount === 0) {
                eventsContainer.style.display = 'none';
                noResults.style.display = 'block';
            } else {
                eventsContainer.style.display = 'block';
                noResults.style.display = 'none';
            }
        }

        searchInput.addEventListener('input', (e) => {
            currentSearch = e.target.value;
            filterEvents();
        });

        cityFilters.forEach(filter => {
            filter.addEventListener('click', () => {
                cityFilters.forEach(f => f.classList.remove('active'));
                filter.classList.add('active');
                currentCity = filter.dataset.city;
                filterEvents();
            });
        });

        // Calendar day click
        calendarDays.forEach(day => {
            day.addEventListener('click', () => {
                const clickedDay = parseInt(day.dataset.day);

                if (currentDay === clickedDay) {
                    // Clicking same day again = deselect
                    currentDay = null;
                    calendarDays.forEach(d => d.classList.remove('active'));
                    clearDateButton.classList.remove('visible');
                } else {
                    // Select new day
                    currentDay = clickedDay;
                    calendarDays.forEach(d => d.classList.remove('active'));
                    day.classList.add('active');
                    clearDateButton.classList.add('visible');
                }

                filterEvents();
            });
        });

        // Clear date filter button
        clearDateButton.addEventListener('click', () => {
            currentDay = null;
            calendarDays.forEach(d => d.classList.remove('active'));
            clearDateButton.classList.remove('visible');
            filterEvents();
        });
    </script>
</body>
</html>
"""

    return html


def main():
    """Main entry point"""
    print("Generuji HTML...")

    # Load data
    data = load_events_data()

    # Generate HTML
    html = generate_html(data)

    # Save to file
    month_name = data['month_name']
    year = data['year']
    filename = f"program_{month_name}_{year}.html"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ HTML vygenerováno: {filename}")
    print(f"✓ Celkem {data['total_events']} koncertů")
    print(f"✓ Z {len(data['venues'])} klubů")


if __name__ == '__main__':
    main()
