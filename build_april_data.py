"""
Build events_data.json for April 2026 from manually collected WebFetch data.
Uses only Python stdlib - no external dependencies required.
"""
import json

MONTH = 4
YEAR = 2026
MONTH_NAME = "duben"

def e(day, time, artist, venue, city, url, status=None):
    """Create event dict."""
    d = {
        "date": f"{day:02d}.{MONTH:02d}.{YEAR}",
        "day": day,
        "month": MONTH,
        "year": YEAR,
        "time": time,
        "artist": artist,
        "venue": venue,
        "city": city,
        "url": url
    }
    if status:
        d["status"] = status
    return d


def validate(events, venue_name, min_e, max_e):
    total = len(events)
    weekend_days = {4, 5, 11, 12, 18, 19, 25, 26}  # April 2026 weekends
    weekend_events = sum(1 for ev in events if ev["day"] in weekend_days)
    if total < min_e * 0.5:
        status = "RED"
        val = "FAIL"
    elif total < min_e:
        status = "YELLOW"
        val = "WARN"
    else:
        status = "GREEN"
        val = "PASS"
    return {
        "venue": venue_name,
        "total_events": total,
        "weekend_events": weekend_events,
        "status": status,
        "expected_range": f"{min_e}-{max_e}",
        "validation": val
    }


# ─── O2 ARENA ───────────────────────────────────────────────────────────────
o2arena_events = [
    e(5,  "20:00", "Louis Tomlinson", "O2 Arena", "Praha", "https://www.o2arena.cz/en/events/louis-tomlinson-2026-en/"),
    e(9,  "20:00", "Pentatonix – UK/European Tour 2026", "O2 Arena", "Praha", "https://www.o2arena.cz/en/events/pentatonix-uk-european-tour-2026-2/"),
    e(10, "19:00", "Eros Ramazzotti – Una Storia Importante", "O2 Arena", "Praha", "https://www.o2arena.cz/en/events/eros-ramazzotti-una-storia-importante-2/"),
    e(20, "20:00", "Tame Impala – Deadbeat Tour", "O2 Arena", "Praha", "https://www.o2arena.cz/en/events/tame-impala-deadbeat-tour-en/"),
]

# ─── O2 UNIVERSUM ────────────────────────────────────────────────────────────
o2universum_events = [
    e(27, "19:30", "ABBAMANIA THE SHOW Dancing Queen Tour", "O2 Universum", "Praha", "https://www.o2universum.cz/en/events/abbamania-the-show-dancing-queen-tour-with-orchestra-and-band-2/"),
    e(29, "19:00", "Jan Smigmator 40", "O2 Universum", "Praha", "https://www.o2universum.cz/en/events/jan-smigmator-40-en/"),
]

# ─── TIPSPORT ARENA ──────────────────────────────────────────────────────────
tipsport_events = []  # Could not fetch data

# ─── FORUM KARLÍN ────────────────────────────────────────────────────────────
forumkarlin_events = [
    e(6,  "20:00", "Dita Von Teese – Nocturnelle", "Forum Karlín", "Praha", "https://www.forumkarlin.cz/en/event/dita-von-teese"),
    e(12, "19:00", "Kreator – Krushers Of The World Tour + Carcass, Exodus, Nails", "Forum Karlín", "Praha", "https://www.forumkarlin.cz/en/event/kreator"),
    e(24, "20:00", "JAMARON", "Forum Karlín", "Praha", "https://www.forumkarlin.cz/en/event/jamaron-forum-karlin"),
]

# ─── PALÁC AKROPOLIS ─────────────────────────────────────────────────────────
akropolis_base = "https://palacakropolis.cz"
akropolis_events = [
    e(1,  "20:00", "Mélanie Pain of Nouvelle Vague /FR", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40173"),
    e(2,  "20:00", "Judith Hill /US", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40571"),
    e(7,  "20:00", "Kalle + Babylonely", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40174"),
    e(8,  "20:00", "Apparat /DE + BI Disc Live /DE", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40398"),
    e(9,  "20:00", "The 113 /UK + Blve Velvet /SK", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40369"),
    e(10, "20:00", "Flore Laurentienne /CA + Zuzanna Całka /PL", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40244"),
    e(11, "20:00", "Iam Oskar + Simon Opp", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40175"),
    e(15, "20:00", "Luna /UA", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40358"),
    e(16, "20:00", "House of Waters /US /JP", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40037"),
    e(18, "20:00", "Stayj + Marie April & The Fools | Chapter 2", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40145"),
    e(20, "20:00", "Talaqpo /CZ", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40187"),
    e(23, "20:00", "Afel Bocoum /ML", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40147"),
    e(24, "20:00", "Tinariwen – The Hoggar Tour /ML", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40287"),
    e(29, "20:00", "Eydís Evensen /IS", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40137"),
    e(30, "20:00", "Iva Bittová & Duo Jedlinský-Fischer", "Palác Akropolis", "Praha", f"{akropolis_base}/work/33298?event_id=40192"),
]

# ─── LUCERNA VELKÝ SÁL ───────────────────────────────────────────────────────
lucerna_velky_base = "https://www.lucpra.com"
lucerna_velky_events = [
    e(18, "18:00", "The Ring Lucerna", "Lucerna Velký sál", "Praha", f"{lucerna_velky_base}/index.php/cz/programs/eventdetail/1066/the-ring-lucerna"),
    e(25, "19:00", "Jodok Cello", "Lucerna Velký sál", "Praha", f"{lucerna_velky_base}/index.php/cz/programs/eventdetail/1045/jodok-cello"),
    e(26, "19:00", "Pavel Žalman Lohonka – 80 | Narozeninový koncert s kapelou a hosty", "Lucerna Velký sál", "Praha", f"{lucerna_velky_base}/index.php/cz/programs/eventdetail/1068/pavel-zalman-lohonka-80-narozeninovy-koncert-s-kapelou-a-hosty"),
]

# ─── ROXY ────────────────────────────────────────────────────────────────────
roxy_base = "https://www.roxy.cz"
roxy_events = [
    e(2,  "20:00", "Mind Healer: Steve Sniff, Skardu, Wedry", "Roxy", "Praha", f"{roxy_base}/events/detail/4843/vyprodano-mind-healer-steve-sniff-skardu-wedry", "VYPRODÁNO"),
    e(3,  "23:00", "Hard Dance Vol. 2", "Roxy", "Praha", f"{roxy_base}/events/detail/4877/hard-dance-vol-2"),
    e(4,  "23:00", "House Party", "Roxy", "Praha", f"{roxy_base}/events/detail/4841/house-party"),
    e(6,  "17:30", "Fit For A King", "Roxy", "Praha", f"{roxy_base}/events/detail/4673/fit-for-a-king"),
    e(7,  "19:00", "Naomi Jon", "Roxy", "Praha", f"{roxy_base}/events/detail/4787/naomi-jon"),
    e(8,  "20:00", "Gufrau", "Roxy", "Praha", f"{roxy_base}/events/detail/4823/vyprodano-gufrau", "VYPRODÁNO"),
    e(9,  "20:00", "Gufrau (Day 2)", "Roxy", "Praha", f"{roxy_base}/events/detail/4825/vyprodano-gufrau", "VYPRODÁNO"),
    e(10, "22:00", "Netsky (Day 1)", "Roxy", "Praha", f"{roxy_base}/events/detail/4749/netsky"),
    e(11, "22:00", "Netsky (Day 2)", "Roxy", "Praha", f"{roxy_base}/events/detail/4751/netsky"),
    e(13, "19:00", "Kollárovci", "Roxy", "Praha", f"{roxy_base}/events/detail/4801/kollarovci"),
    e(17, "22:00", "Claptone", "Roxy", "Praha", f"{roxy_base}/events/detail/4777/claptone"),
    e(18, "22:00", "MHD Therapy", "Roxy", "Praha", f"{roxy_base}/events/detail/4871/mhd-therapy"),
    e(22, "18:00", "Manfred Mann's Earth Band", "Roxy", "Praha", f"{roxy_base}/events/detail/4735/manfred-mann-s-earth-band"),
    e(23, "19:00", "Fox Stevenson", "Roxy", "Praha", f"{roxy_base}/events/detail/4691/fox-stevenson"),
    e(24, "23:05", "Johannes Schuster", "Roxy", "Praha", f"{roxy_base}/events/detail/4815/johannes-schuster"),
    e(25, "23:05", "Ollie Lishman", "Roxy", "Praha", f"{roxy_base}/events/detail/4847/ollie-lishman"),
    e(26, "19:30", "Smash Into Pieces", "Roxy", "Praha", f"{roxy_base}/events/detail/4723/smash-into-pieces"),
    e(28, "19:00", "Skynd", "Roxy", "Praha", f"{roxy_base}/events/detail/4613/skynd"),
]

# ─── MEETFACTORY ─────────────────────────────────────────────────────────────
meetfactory_base = "https://meetfactory.cz"
meetfactory_events = [
    e(3,  "21:00", "Pain + Special Guests: křest alba Cíl?", "MeetFactory", "Praha", f"{meetfactory_base}/cs/program/detail/pain-special-guests-krest-alba-cil"),
    e(7,  "20:00", "Radio 1 – 35 let: james K + GbClifford & Tasya + R1 DJs", "MeetFactory", "Praha", f"{meetfactory_base}/cs/program/detail/radio-1-35-let-james-k-tba-r1-djs"),
    e(9,  "20:00", "Treska Jednoskvrnná: křest desky + in.numbers", "MeetFactory", "Praha", f"{meetfactory_base}/cs/program/detail/treska-jednoskvrnna-krest-desky-innumbers"),
    e(10, "20:00", "Fource: Xaviersobased + ksuuvi + Backend", "MeetFactory", "Praha", f"{meetfactory_base}/cs/program/detail/fource-xaviersobased"),
    e(15, "20:00", "Live Nation: Balu Brigada", "MeetFactory", "Praha", f"{meetfactory_base}/cs/program/detail/live-nation-balu-brigada"),
    e(16, "20:00", "Bitchin Bajas + Gurun Gurun", "MeetFactory", "Praha", f"{meetfactory_base}/cs/program/detail/bitchin-bajas"),
    e(19, "20:00", "Unsane + Děti deště", "MeetFactory", "Praha", f"{meetfactory_base}/cs/program/detail/unsane"),
    e(22, "20:00", "Great Lake Swimmers", "MeetFactory", "Praha", f"{meetfactory_base}/cs/program/detail/great-lake-swimmers"),
    e(25, "17:00", "GR◎◎VOLVER: Groove Culture Festival", "MeetFactory", "Praha", f"{meetfactory_base}/cs/program/detail/grvolver-groove-culture-festival"),
    e(27, "20:00", "Orcutt Shelley Miller + Michal Berec", "MeetFactory", "Praha", f"{meetfactory_base}/cs/program/detail/orcutt-shelley-miller"),
]

# ─── LUCERNA MUSIC BAR ───────────────────────────────────────────────────────
musicbar_base = "https://musicbar.cz"
musicbar_events = [
    e(1,  "18:30", "Vojtěch Dyk & D.Y.K.", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/vojtech-dyk-d-y-k-4/", "VYPRODÁNO"),
    e(2,  "20:00", "Mutanti hledaj východisko", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/mutanti-hledaj-vychodisko/"),
    e(3,  "21:00", "Pop 80's & 90's video party DJ Jirka Neumann", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/pop-80s-90s-video-party-dj-jirka-neumann-890/"),
    e(4,  "21:00", "Pop 80's & 90's video party DJ Jirka Neumann", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/pop-80s-90s-video-party-dj-jirka-neumann-892/"),
    e(5,  "21:00", "Easter Lucerna Never Sleeps", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/velikonocni-lucerna-never-sleeps/"),
    e(6,  "19:00", "Mesh /UK", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/mesh-uk/"),
    e(9,  "20:00", "Gruppo Salsiccia", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/gruppo-salsiccia/"),
    e(10, "19:00", "YAKTAK /UA", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/yaktak-ua-2/"),
    e(10, "22:00", "Pop 80's & 90's video party DJ Jirka Neumann", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/pop-80s-90s-video-party-dj-jirka-neumann-895/"),
    e(11, "21:00", "Pop 80's & 90's video party DJ Jirka Neumann", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/pop-80s-90s-video-party-dj-jirka-neumann-896/"),
    e(14, "19:00", "Anna K.", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/anna-k-5/"),
    e(15, "19:00", "Anna K.", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/anna-k-4/", "VYPRODÁNO"),
    e(16, "19:30", "Mňága a Žďorp", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/mnaga-a-zdorp-35/"),
    e(17, "21:00", "Pop 80's & 90's video party DJ Jirka Neumann", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/pop-80s-90s-video-party-dj-jirka-neumann-891/"),
    e(18, "21:00", "Pop 80's & 90's video party DJ Jirka Neumann", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/pop-80s-90s-video-party-dj-jirka-neumann-893/"),
    e(19, "20:00", "Mobb Deep feat. Havoc along with Big Noyd & DJ L.E.S.", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/mobb-deep/"),
    e(21, "19:30", "Mig 21", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/mig-21-76/", "VYPRODÁNO"),
    e(22, "19:30", "Mig 21", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/mig-21-77/", "VYPRODÁNO"),
    e(23, "19:30", "Mig 21", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/mig-21-78/", "VYPRODÁNO"),
    e(24, "21:00", "Pop 80's & 90's video party DJ Jirka Neumann", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/pop-80s-90s-video-party-dj-jirka-neumann-894/"),
    e(25, "17:30", "Drevo /UA", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/drevo-ua/"),
    e(25, "22:00", "Pop 80's & 90's video party DJ Jirka Neumann", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/pop-80s-90s-video-party-dj-jirka-neumann-897/"),
    e(26, "19:00", "Oleg Skrypka & Vopli Vidopliassova /UA", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/oleg-skrypka-vopli-vidopliassova-ua/"),
    e(28, "18:30", "Luboš Pospíšil & 5P + guests, special guest: Pavel Váně", "Lucerna Music Bar", "Praha", f"{musicbar_base}/en/program/lubos-pospisil-5p-75-let/"),
]

# ─── ROCK CAFÉ ────────────────────────────────────────────────────────────────
rockcafe_base = "https://rockcafe.cz"
rockcafe_events = [
    e(2,  "13:00", "Music Bar – free entry!", "Rock Café", "Praha", f"{rockcafe_base}/en/program/music-bar-vstup-zdarma-382/"),
    e(3,  "20:00", "Už jsme doma", "Rock Café", "Praha", f"{rockcafe_base}/en/program/uz-jsme-doma/"),
    e(4,  "19:30", "SoundCheck (IT), The Aisha (IT), Youlie", "Rock Café", "Praha", f"{rockcafe_base}/en/program/soundcheck-it-the-aisha-it-youlie/"),
    e(6,  "20:00", "Udělejme spolu show: Komissarenko, Belyj, Detkov", "Rock Café", "Praha", f"{rockcafe_base}/en/program/udelejme-spolu-show-komissarenko-belyj-detkov-2/"),
    e(7,  "20:00", "Space of Variations (UA) + Up!Great", "Rock Café", "Praha", f"{rockcafe_base}/en/program/space-of-variations-ua-guest-upgreat/"),
    e(8,  "19:00", "Slavíček + host: Beira", "Rock Café", "Praha", f"{rockcafe_base}/en/program/slavicek-host-beira/"),
    e(9,  "20:00", "Snak The Ripper (CAN), Junk (CAN), The Bermuda (USA)", "Rock Café", "Praha", f"{rockcafe_base}/en/program/snak-the-ripper-can-junk-can-the-bermuda-usa/"),
    e(10, "18:00", "GymVod Fest vol. 6", "Rock Café", "Praha", f"{rockcafe_base}/en/program/gymvod-fest-vol-6/"),
    e(11, "19:00", "Obscure presents: Myrath (TN)", "Rock Café", "Praha", f"{rockcafe_base}/en/program/obscure-presents-myrath-tn/"),
    e(13, "19:30", "Graabner", "Rock Café", "Praha", f"{rockcafe_base}/en/program/graabner/"),
    e(14, "19:00", "Selection presents: ClockClock (DE)", "Rock Café", "Praha", f"{rockcafe_base}/en/program/selection-presents-clockclock-de/", "ODLOŽENO"),
    e(15, "20:00", "Sex Deviants, Kohout Plaší Smrt, Louty", "Rock Café", "Praha", f"{rockcafe_base}/en/program/sex-deviants-a-bude-hur-louty/"),
    e(16, "19:00", "The Gripes, Yelling Orangutans, Offbeat 5", "Rock Café", "Praha", f"{rockcafe_base}/en/program/the-gripes-yelling-orangutans-offbeat-5/"),
    e(17, "16:30", "Groovy & Stinky FEST 2026", "Rock Café", "Praha", f"{rockcafe_base}/en/program/groovy-stinky-fest-2026/"),
    e(18, "15:30", "Groovy & Stinky FEST 2026 (Day 2)", "Rock Café", "Praha", f"{rockcafe_base}/en/program/groovy-stinky-fest-2026-2/"),
    e(21, "19:00", "Obscure presents: Lansdowne (USA) + support", "Rock Café", "Praha", f"{rockcafe_base}/en/program/obscure-presents-lansdowne-usa-support/"),
    e(22, "20:00", "Fource presents: Kiki Rockwell (USA) + support", "Rock Café", "Praha", f"{rockcafe_base}/en/program/fource-presents-kiki-rockwell-usa/"),
    e(23, "20:00", "Fource presents: Aries (USA)", "Rock Café", "Praha", f"{rockcafe_base}/en/program/fource-presents-aries-usa-2/"),
    e(24, "20:00", "Selection presents: Natalie Jane (USA)", "Rock Café", "Praha", f"{rockcafe_base}/en/program/selection-presents-natalie-jane-usa/"),
    e(25, "20:00", "VPŘEDSKOK x BOLESLAM 2026", "Rock Café", "Praha", f"{rockcafe_base}/en/program/vpredskok-x-boleslam-2026/"),
    e(26, "19:00", "The Virginmarys (UK) + support: Atomy nevadí", "Rock Café", "Praha", f"{rockcafe_base}/en/program/the-virginmarys-uk-support/"),
    e(27, "20:00", "Nanday (album release) + guests", "Rock Café", "Praha", f"{rockcafe_base}/en/program/nanday-krest-desky-hoste/"),
    e(28, "20:00", "Fource presents: Yellow Days (UK)", "Rock Café", "Praha", f"{rockcafe_base}/en/program/fource-presents-yellow-days-uk/"),
    e(29, "20:00", "Fource presents: Ásgeir (IS) + support: Bríet (IS)", "Rock Café", "Praha", f"{rockcafe_base}/en/program/fource-presents-asgeir-is/"),
    e(30, "20:00", "Psycho čarodky: Demented Are Go + The Gangnails", "Rock Café", "Praha", f"{rockcafe_base}/en/program/psycho-carodky-demented-are-go-the-gangnails/"),
]

# ─── VAGON ───────────────────────────────────────────────────────────────────
vagon_url = "https://www.vagon.cz/next.php"
vagon_events = [
    e(1,  "21:00", "Jiří Schelinger Revival", "Vagon", "Praha", "https://www.facebook.com/JiriSchelingerRevival"),
    e(2,  "21:00", "Krausberry", "Vagon", "Praha", "https://krausberry.cz"),
    e(3,  "21:00", "Prague Queen", "Vagon", "Praha", "https://praguequeen.cz"),
    e(4,  "21:00", "Benjaming's Clan + Jakofakt?", "Vagon", "Praha", "https://benjamingsclan.com"),
    e(5,  "20:00", "Music Video Party", "Vagon", "Praha", vagon_url),
    e(7,  "21:00", "Dire Straits Tribute", "Vagon", "Praha", "https://direstraits.cz"),
    e(8,  "21:00", "Záviš", "Vagon", "Praha", "https://www.facebook.com/ZavisOFFICIAL"),
    e(9,  "21:00", "The Cell", "Vagon", "Praha", vagon_url),
    e(10, "21:00", "Brutus", "Vagon", "Praha", "https://brutus.cz"),
    e(11, "21:00", "Iron Maiden Revival", "Vagon", "Praha", vagon_url),
    e(14, "21:00", "Celtic Tuesday: Vintage Wine + Flat Fly", "Vagon", "Praha", vagon_url),
    e(15, "21:00", "Bruce Adams Tribute", "Vagon", "Praha", vagon_url),
    e(16, "20:00", "Five O'Clock Tea + Bikkinyshop + Různorohý", "Vagon", "Praha", "https://fiveoclocktea.com"),
    e(17, "21:00", "Znouzectnost + Ctib", "Vagon", "Praha", vagon_url),
    e(18, "21:00", "Paprikacze (Red Hot Chili Peppers Revival)", "Vagon", "Praha", vagon_url),
    e(21, "21:00", "Celtic Tuesday: Dick O'Brass + Five Leaf Clover", "Vagon", "Praha", vagon_url),
    e(22, "21:00", "Riders on Fire (The Doors Tribute)", "Vagon", "Praha", vagon_url),
    e(23, "21:00", "Dr. Vykape + Buzerant", "Vagon", "Praha", vagon_url),
    e(24, "21:00", "Ozzy Osbourne & Black Sabbath Revival", "Vagon", "Praha", vagon_url),
    e(25, "21:00", "Professor", "Vagon", "Praha", vagon_url),
    e(27, "19:30", "Pavel Sedláček & Cadillac", "Vagon", "Praha", "https://cadillacband.cz"),
    e(28, "21:00", "Lars + Maryana", "Vagon", "Praha", vagon_url),
    e(29, "21:00", "Garage & Tony Ducháček", "Vagon", "Praha", "https://garageband.cz"),
    e(30, "21:00", "Nirvana Revival Praha", "Vagon", "Praha", vagon_url),
]

# ─── JAZZ DOCK ───────────────────────────────────────────────────────────────
jazzdock_base = "https://www.jazzdock.cz"
jazzdock_events = [
    e(1,  "20:00", "Kirill Yakovlev Trio", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/kirill-yakovlev-trio-1-1"),
    e(2,  "20:00", "Dan Bárta & Robert Balzar Trio", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/dan-barta-robert-balzar-trio-20"),
    e(3,  "19:00", "Marta Kloučková Quintet", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/marta-klouckova-quintet-5"),
    e(3,  "22:00", "Dan Bárta & Robert Balzar Trio (late)", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/dan-barta-robert-balzar-trio-21"),
    e(4,  "19:00", "Peter Lipa Band", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/peter-lipa-band-1-5"),
    e(4,  "22:00", "Yvonne Sanchez Band", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/yvonne-sanchez-band-60"),
    e(5,  "20:00", "Peter Lipa Band (Sunday)", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/peter-lipa-band-1-6"),
    e(6,  "20:00", "Buty", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/buty-12"),
    e(7,  "20:00", "Buty", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/buty-13"),
    e(8,  "21:00", "Larry Goldings / Peter Bernstein / Bill Stewart /USA", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/larry-goldings-peter-bernstein-bill-stewart-usa-1"),
    e(9,  "21:00", "Brian Charette Trio ft. Šoltis/Štveráček", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/soltis-charette-stveracek-super-trio-1-2"),
    e(10, "19:00", "Pat Bianchi Trio /USA", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/pat-bianchi-trio-usa-1"),
    e(10, "22:00", "Jan Kořínek 50 ft. Soul Hitchhikers", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/jan-korinek-1"),
    e(11, "19:00", "Ondrej Pivec Organic Quartet", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/ondrej-pivec-organic-quartet-17"),
    e(11, "22:00", "Ondrej Pivec Organic Quartet (late)", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/ondrej-pivec-organic-quartet-18"),
    e(12, "20:00", "Steven's", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/stevens-1"),
    e(13, "21:00", "Justin Lavash", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/justin-lavash-10"),
    e(14, "20:00", "The Bad Week (SRB)", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/the-bad-week-srb-1"),
    e(16, "20:00", "Igor Orozovič & Co.", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/igor-orozovic-co-3"),
    e(17, "20:00", "Guy Bennett Duo", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/guy-bennett-1"),
    e(17, "22:00", "Terne Čhave", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/terne-chave-27"),
    e(18, "21:00", "Ondřej Štveráček band", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/ondrej-stveracek-1-7"),
    e(18, "23:00", "Groove Dock – Jazz to Dance", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/groove-dock-jazz-to-dance-88"),
    e(19, "16:00", "Big Band Pražského salónního orchestru (Sunday Dixie)", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/big-band-prazskeho-salonniho-orchestru-sunday-dixie-22"),
    e(19, "20:00", "Elisabeth Lohninger / Walter Fischbacher", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/elisabeth-lohninger-walter-fischbacher-plays-songs-of-the-queen-1-1"),
    e(20, "20:00", "Jazz Dock Orchestra", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/jazz-dock-orchestra-85"),
    e(21, "20:00", "E Converso", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/e-converso-9"),
    e(22, "20:00", "Jazbit / Mladí lidi", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/jazbit-mladi-ladi-jazz-2026-2"),
    e(23, "20:00", "Nicole Zuraitis Trio", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/nicole-zuraitis-trio-1-1"),
    e(26, "16:00", "Metropolitan Jazz Band (Sunday Dixie)", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/metropolitan-jazz-band-eva-emingerova-sunday-dixie-23"),
    e(26, "20:00", "Hugo Race Fatalists", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/hugo-race-fatalists-2"),
    e(29, "20:00", "Forq /USA", "Jazz Dock", "Praha", f"{jazzdock_base}/en/koncert/forq-1-1"),
]

# ─── REDUTA JAZZ CLUB ────────────────────────────────────────────────────────
reduta_base = "https://www.redutajazzclub.cz"
reduta_events = [
    e(1,  "19:00", "The Billie Holiday Tribute: A Journey into the Jazz Era", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/the-billie-holiday-tribute-a-journey-into-the-jazz-era"),
    e(2,  "19:00", "The Ultimate Jazz, Soul & Funk Experience with Lee Andrew Davison /USA", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/the-ultimate-jazz-soul-funk-experience-with-lee"),
    e(2,  "21:15", "The Ray Charles Experience by Lee Andrew Davison /USA", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/ray-charles-lee"),
    e(3,  "19:00", "Ella Fitzgerald: The Voice of Jazz, Forever Resonating", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/ella-fitzgerald-the-voice-of-jazz-forever-resona"),
    e(3,  "21:15", "Swinging Melodies: A Journey through Unforgettable Jazz Performances", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/swinging-melodies-a-journey-through-unforgettable"),
    e(4,  "19:00", "Remembering Sinatra: A Timeless Tribute", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/remembering-sinatra-a-timeless-tribute"),
    e(4,  "21:15", "Swingin' with Sinatra", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/swingin-with-sinatra"),
    e(5,  "19:00", "Melodic Journey with Louis Armstrong, Gershwin, Jobim – Metropolitan Jazz Band", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/melodic-journey-metropolitan-jazz-band-10"),
    e(5,  "21:15", "Great Melodies of Jazz: Armstrong, Gershwin, Jobim by Metropolitan Jazz Band", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/melodic-journey-metropolitan-jazz-band-10"),
    e(6,  "19:00", "The Essence of French Chanson: Piaf, Aznavour, Brel...", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/the-best-of-french-chanson-charles-aznavour-jac-1"),
    e(7,  "19:00", "Tribute to the Legends of 1950s Hard Bop: Miles Davis, Art Blakey, Cannonball Adderley", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/legends-of-1950s-hard-bop"),
    e(8,  "19:00", "VV BRAZIL – Hot Latin Groove", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/vv-brazil-hot-latin-groove"),
    e(9,  "19:00", "The Nina Simone Experience: An Unforgettable Jazz Tribute", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/the-nina-simone-experience-an-unforgettable-jazz-tribute"),
    e(10, "19:00", "The Golden Voice: A Celebration of Tony Bennett", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/the-golden-voice-a-celebration-of-tony-bennett"),
    e(10, "21:15", "Two Voices & Jazz Band: Romantic Night", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/two-voices-jazz-band-romantic-night"),
    e(11, "19:00", "Ella Fitzgerald: The Voice of Jazz, Forever Resonating", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/ella-fitzgerald-the-voice-of-jazz-forever-resona"),
    e(11, "21:15", "Swinging Melodies: A Journey through Unforgettable Jazz Performances", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/swinging-melodies-a-journey-through-unforgettable"),
    e(12, "19:00", "Big Band Trumpets – Kings of Swing Tribute: Duke Ellington, Quincy Jones, Dizzy Gillespie", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/big-band-trumpets-kings-of-swing-tribute-to-duke"),
    e(13, "19:00", "Queens Sing the Blue Notes: Bessie Smith, Dinah Washington, Etta James, Janis Joplin", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/queens-sing-the-blue-notes-a-tribute-to-bessie-sm"),
    e(14, "19:00", "The Billie Holiday Tribute: A Journey into the Jazz Era", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/the-billie-holiday-tribute-a-journey-into-the-jazz-era"),
    e(15, "19:00", "Piano Legends Unite: Chick Corea, Herbie Hancock, Oscar Peterson", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/piano-legends-unite-a-tribute-to-chick-corea-her"),
    e(16, "19:00", "Timeless Legends: Michael Jackson, AC Jobim, Herbie Hancock, Duke Ellington", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/timeless-legends-m-novak"),
    e(17, "19:00", "The Ray Charles Experience by Lee Andrew Davison /USA", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/ray-charles-lee"),
    e(17, "21:15", "The Ultimate Jazz, Soul & Funk Experience with Lee Andrew Davison /USA", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/the-ultimate-jazz-soul-funk-experience-with-lee"),
    e(18, "19:00", "The Nina Simone Experience: An Unforgettable Jazz Tribute", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/the-nina-simone-experience-an-unforgettable-jazz-tribute"),
    e(18, "21:15", "The Beatles Groove: A Jazz Tribute", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/the-beatles-groove-a-jazz-tribute"),
    e(19, "19:00", "Tribute to Jazz Legends: Timeless Melodies", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/tribute-to-jazz-legends-timeless-melodies-eming-1"),
    e(20, "19:00", "Jazz Treasures: A Tribute Concert to the American Jazz Masters", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/jazz-treasures-a-tribute-concert-to-the-american-31"),
    e(21, "19:00", "Legendary Pop Icons in Jazz: Adele / Lady Gaga / Amy Winehouse (Dorota Tóthová)", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/pop-icons-dorota-tothova-1"),
    e(22, "19:00", "Ella Fitzgerald: The Voice of Jazz, Forever Resonating", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/ella-fitzgerald-the-voice-of-jazz-forever-resona"),
    e(23, "19:00", "The Saxophone Legacy: Tribute to Coltrane, Getz, Rollins & Young", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/saxophone-47"),
    e(24, "19:00", "Bohemia Big Band: Glenn Miller, Duke Ellington, Benny Goodman", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/bohemia-big-band-tribute-to-glenn-miller-duke-el-1"),
    e(24, "21:15", "Timeless Jazz: Bohemia Big Band Pays Tribute to Gershwin, Basie & Miller", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/timeless-jazz-bohemia-big-band-pays-tribute-to-gershwin-basie-miller"),
    e(25, "19:00", "Remembering Sinatra: A Timeless Tribute", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/remembering-sinatra-a-timeless-tribute"),
    e(25, "21:15", "Swingin' with Sinatra", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/swingin-with-sinatra"),
    e(26, "19:00", "The Golden Voice: A Celebration of Tony Bennett", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/the-golden-voice-a-celebration-of-tony-bennett"),
    e(27, "19:00", "Louis Armstrong Forever: Old Timers Jazz Band", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/louis-armstrong-forever-celebrating-a-jazz-icon-with-old-timers-jazz-band-2"),
    e(28, "19:00", "Piano Legends Unite: Chick Corea, Herbie Hancock, Oscar Peterson", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/piano-legends-unite-a-tribute-to-chick-corea-her"),
    e(29, "19:00", "Big Band Trumpets – Kings of Swing: Duke Ellington, Quincy Jones, Dizzy Gillespie", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/big-band-trumpets-kings-of-swing-tribute-to-duke"),
    e(30, "19:00", "Backside Big Band Plays the Greats: Ellington, Gillespie, Prima & Gershwin", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/backside-big-band-plays-the-great"),
    e(30, "21:15", "A Night of Jazz Legends: Backside Big Band Honors Ellington, Gillespie, Prima & Gershwin", "Reduta Jazz Club", "Praha", f"{reduta_base}/artists-cs/noname-44"),
]

# ─── MALOSTRANSKÁ BESEDA ─────────────────────────────────────────────────────
beseda_url = "https://www.malostranska-beseda.cz/club/program"
beseda_events = [
    e(1,  "20:30", "Hrací skříň Praha", "Malostranská beseda", "Praha", beseda_url),
    e(2,  "20:00", "Žáha", "Malostranská beseda", "Praha", beseda_url),
    e(3,  "20:30", "The Stylist + special guest", "Malostranská beseda", "Praha", beseda_url),
    e(6,  "20:00", "Jan Burian: Jarní večírek", "Malostranská beseda", "Praha", beseda_url),
    e(7,  "20:00", "Hot Sisters", "Malostranská beseda", "Praha", beseda_url),
    e(8,  "20:00", "Petr Kalandra Memory Band (LP release)", "Malostranská beseda", "Praha", beseda_url),
    e(9,  "20:30", "Precedens", "Malostranská beseda", "Praha", beseda_url),
    e(10, "19:00", "Éra – 10 let", "Malostranská beseda", "Praha", beseda_url),
    e(12, "20:00", "Cimbal Classic", "Malostranská beseda", "Praha", beseda_url),
    e(14, "20:00", "Ivan Hlas Trio", "Malostranská beseda", "Praha", beseda_url),
    e(15, "20:00", "Monogram a Royal Flush", "Malostranská beseda", "Praha", beseda_url),
    e(16, "20:30", "Lorraine Leckie & Her Demons (album release) + Něžná noc", "Malostranská beseda", "Praha", beseda_url),
    e(17, "20:00", "Šouflšou + Ladislav Bonita", "Malostranská beseda", "Praha", beseda_url),
    e(18, "19:30", "Kába 80 – The Plastic People & Umělá Hmota", "Malostranská beseda", "Praha", beseda_url),
    e(19, "20:00", "Olin Nejezchleba a KyBaBu", "Malostranská beseda", "Praha", beseda_url),
    e(20, "19:30", "Jitka Keltie & band", "Malostranská beseda", "Praha", beseda_url),
    e(21, "20:00", "Vladimír Merta duo (s O. Fenclem)", "Malostranská beseda", "Praha", beseda_url),
    e(22, "20:00", "Petr Vondráček & Lokomotiva", "Malostranská beseda", "Praha", beseda_url),
    e(23, "20:00", "Hm...", "Malostranská beseda", "Praha", beseda_url),
    e(24, "20:00", "Ve světle písní Davida Stypky", "Malostranská beseda", "Praha", beseda_url),
    e(25, "20:00", "Václav Koubek s kapelou: 30 let kapely", "Malostranská beseda", "Praha", beseda_url),
    e(26, "19:30", "Petra Janů a Amsterdam (EP/video release)", "Malostranská beseda", "Praha", beseda_url),
    e(27, "20:00", "Edith Piaf: Dnes nechci spát sama", "Malostranská beseda", "Praha", beseda_url),
    e(28, "20:30", "Timudej", "Malostranská beseda", "Praha", beseda_url),
]

# ─── CROSS CLUB ──────────────────────────────────────────────────────────────
crossclub_base = "https://www.crossclub.cz"
crossclub_events = [
    e(1,  "22:00", "Psytrance Night", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8479-psytrance-night/"),
    e(2,  "22:00", "Rock Party MMVI & DNB Stage", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8465-rock-party-mmvi-dnb-stage/"),
    e(3,  "22:00", "DNB Production Night w/ Norty /UK", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8466-dnb-production-night-w-norty-uk/"),
    e(4,  "22:00", "Okupe & Friends", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8468-okupe-friends/"),
    e(6,  "22:00", "Los Tekkenos: Werca B-Day", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8476-los-tekkenos-werca-b-day/"),
    e(7,  "22:00", "Techno Stage", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8486-techno-stage/"),
    e(8,  "22:00", "Křižovatka", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8485-krizovatka/"),
    e(9,  "22:00", "Rock Night", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8480-rock-night/"),
    e(10, "22:00", "Somabody Says Pull Up", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8463-somabody-says-pull-up/"),
    e(11, "22:00", "Hard Rave & DNB Fire", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8481-hard-rave-dnb-fire/"),
    e(12, "20:00", "Koncert", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8482-koncert/"),
    e(13, "22:00", "Los Tekkenos", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8464-los-tekkenos/"),
    e(14, "22:00", "DNB Stage", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8484-dnb-stage/"),
    e(15, "22:00", "Psytrance Night", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8483-psytrance-night/"),
    e(16, "22:00", "Obscure.cz", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8467-obscure-cz/"),
    e(17, "22:00", "Moordoor", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8469-moordoor/"),
    e(20, "22:00", "Los Tekkenos", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8470-los-tekkenos/"),
    e(21, "20:00", "Crack Cloud back in Prague", "Cross Club", "Praha", f"{crossclub_base}/cs/program/8471-crack-cloud-back-in-prague/"),
]

# ─── PLZEŇ VENUES ────────────────────────────────────────────────────────────

# Buena Vista Club
bvc_events = [
    e(17, "20:00", "Anymen (Faith No More, RATM, Pearl Jam covers)", "Buena Vista Club", "Plzeň", "https://www.smsticket.cz/vstupenky/66667-matej-plsek-alien-tour-2026-buena-vista-plzen"),
    e(18, "20:00", "Rimortis + Vanaheim + Roxor", "Buena Vista Club", "Plzeň", "https://www.buenavistaclub.cz/program-klubu.aspx"),
    e(26, "20:00", "Brutus", "Buena Vista Club", "Plzeň", "https://www.buenavistaclub.cz/program-klubu.aspx"),
]

# Divadlo Pod lampou
podlampou_base = "https://podlampou.cz"
podlampou_events = [
    e(1,  "20:00", "Veřejná zkušebna – Pod lampou na baru (revival)", "Divadlo Pod lampou", "Plzeň", f"{podlampou_base}/events/verejna-zkusebna-pod-lampou-na-baru-revival/"),
    e(3,  "20:00", "DanzHun", "Divadlo Pod lampou", "Plzeň", f"{podlampou_base}/events/danzhun-2/"),
    e(4,  "20:00", "Lochotín + Jáchymov + Bruce nemá odpoledne čas", "Divadlo Pod lampou", "Plzeň", f"{podlampou_base}/events/lochotin-jachymov-bruce-nema-odpoledne-cas/"),
    e(8,  "19:00", "Papersand + Kinotaj + Ali zpívá Amy", "Divadlo Pod lampou", "Plzeň", f"{podlampou_base}/events/papersand-kinotaj-ali-zpiva-amy/"),
    e(10, "20:00", "In memory of Kurt Cobain + support: Diazepam", "Divadlo Pod lampou", "Plzeň", f"{podlampou_base}/events/in-memory-of-kurt-cobain-support-diazepam/"),
    e(11, "20:00", "Fobia Kid /SK + support: Adam The World /SK", "Divadlo Pod lampou", "Plzeň", f"{podlampou_base}/events/fobia-kid-sk/"),
    e(17, "20:00", "Fast Food Orchestra – Vidíme to růžově Tour", "Divadlo Pod lampou", "Plzeň", f"{podlampou_base}/events/fast-food-orchestra-vidime-to-ruzove-tour/"),
    e(18, "20:00", "Tangerinecat /UK /UA + Vivid Vision /FR", "Divadlo Pod lampou", "Plzeň", f"{podlampou_base}/events/tangerinecat-uk-ua-vivid-vision-fr/"),
    e(24, "20:00", "Cringe Prince + Temný Rudo", "Divadlo Pod lampou", "Plzeň", f"{podlampou_base}/events/cringe-prince-temny-rudo/"),
    e(25, "20:00", "Koby Fray", "Divadlo Pod lampou", "Plzeň", f"{podlampou_base}/events/koby-fray-2/"),
    e(30, "20:00", "Berlin Manson – nič nebude ok tour + support: The Flood", "Divadlo Pod lampou", "Plzeň", f"{podlampou_base}/events/berlin-manson-nic-nebude-ok-tour/"),
]

# Šeříkovka
serikovka_base = "https://www.serikovka.cz"
serikovka_events = [
    e(2,  "20:00", "Tata Bojs", "Kulturní dům Šeříkovka", "Plzeň", f"{serikovka_base}/koncerty/100-2-4-2026-tata-bojs"),
    e(9,  "20:00", "Lunetic & Band", "Kulturní dům Šeříkovka", "Plzeň", f"{serikovka_base}/koncerty/117-9-4-2026-lunetic-band"),
    e(10, "20:00", "Komunál + Alžběta", "Kulturní dům Šeříkovka", "Plzeň", f"{serikovka_base}/koncerty/110-10-4-2026-komunal-alzbeta"),
    e(12, "20:00", "Mňága a Žďorp + Slobodná Evropa", "Kulturní dům Šeříkovka", "Plzeň", f"{serikovka_base}/koncerty/97-11-4-2026-mnaga-a-zdorp-slobodna-europa"),
    e(25, "20:00", "Motorband – MB40 Tour / 40 let na cestě", "Kulturní dům Šeříkovka", "Plzeň", f"{serikovka_base}/koncerty/115-25-4-2026-motorband-mb40-tour-40-let-na-ceste"),
]

# ─── BRNO VENUES ─────────────────────────────────────────────────────────────

# Sono Centrum
sono_base = "https://www.sono.cz"
sono_events = [
    e(2,  "20:00", "Zelený čtvrtek", "Sono Centrum", "Brno", f"{sono_base}/event/zeleny-ctvrtek/"),
    e(4,  "20:00", "Shimmi", "Sono Centrum", "Brno", f"{sono_base}/event/shimmi/"),
    e(10, "20:00", "Hypocrisy", "Sono Centrum", "Brno", f"{sono_base}/event/hypocrisy/"),
    e(11, "20:00", "Motorband – 40 let na cestě", "Sono Centrum", "Brno", f"{sono_base}/event/motorband-40-let-na-ceste/"),
    e(12, "19:00", "Druhá tráva & Tim O'Brien / 35 let", "Sono Centrum", "Brno", f"{sono_base}/event/druha-trava-tim-obrien-35-let/"),
    e(13, "20:00", "TURNÉ 80: Legenda Petr Novák", "Sono Centrum", "Brno", f"{sono_base}/event/turne-80-legenda-petr-novak/"),
    e(16, "20:00", "The Best ABBA Revival Show – ABBORN", "Sono Centrum", "Brno", f"{sono_base}/event/the-best-abba-revival-show-abborn-2/"),
    e(17, "20:00", "G'oldies is BACK! Největší hity 80's & 90's", "Sono Centrum", "Brno", f"{sono_base}/event/goldies-is-back-nejvetsi-hity-80s-90s/"),
    e(21, "20:00", "Za hranou iluze – moderní kabaret", "Sono Centrum", "Brno", f"{sono_base}/event/za-hranou-iluze-premiera-2-2/"),
    e(22, "20:00", "Michal Prokop", "Sono Centrum", "Brno", f"{sono_base}/event/michal-prokop/"),
    e(23, "20:00", "Manfred Mann's Earth Band", "Sono Centrum", "Brno", f"{sono_base}/event/manfred-manns-earth-band/"),
    e(25, "20:00", "The Machine Performs Pink Floyd", "Sono Centrum", "Brno", f"{sono_base}/event/the-machine-performs-pink-floyd-2/"),
    e(28, "20:00", "JFB / GoGo Penguin", "Sono Centrum", "Brno", f"{sono_base}/event/jfb-gogo-penguin/"),
    e(29, "20:00", "Pražský výběr", "Sono Centrum", "Brno", f"{sono_base}/event/prazsky-vyber-3/"),
    e(30, "20:00", "Deloraine a Irdorath – Beltine", "Sono Centrum", "Brno", f"{sono_base}/event/deloraine-a-irdorath-beltine/"),
]

# Fléda
fleda_base = "https://www.fleda.cz"
fleda_events = [
    e(1,  "22:00", "Nobodylisten LIVE x Easter Party", "Fléda", "Brno", f"{fleda_base}/event/2262/"),
    e(3,  "19:20", "Ektomorf /HU + Ivory /IT + Asylum Road /IRL + Memoria Damnata /DE", "Fléda", "Brno", f"{fleda_base}/event/2323/"),
    e(4,  "22:00", "Erasmus Spring Festival", "Fléda", "Brno", f"{fleda_base}/event/2386/"),
    e(9,  "20:00", "Fast Food Orchestra & Heľenine oči", "Fléda", "Brno", f"{fleda_base}/event/2159/"),
    e(16, "20:00", "Michal Hrůza x Imodium – JARO 2026 tour", "Fléda", "Brno", f"{fleda_base}/event/2255/"),
    e(18, "20:00", "Mobb Deep /USA: Havoc feat. Big Noyd & DJ L.E.S", "Fléda", "Brno", f"{fleda_base}/event/2180/"),
    e(21, "19:30", "Richard Autner & Band", "Fléda", "Brno", f"{fleda_base}/event/2361/"),
    e(23, "20:00", "Sara Zozaya /ES", "Fléda", "Brno", f"{fleda_base}/event/2375/"),
    e(24, "20:00", "Annet X – BBYGIRL TOUR 2026", "Fléda", "Brno", f"{fleda_base}/event/2293/"),
    e(25, "20:30", "Mind Healing x Brno", "Fléda", "Brno", f"{fleda_base}/event/2253/"),
    e(30, "20:00", "Karlo + Fobia Kid + Edúv syn", "Fléda", "Brno", f"{fleda_base}/event/2269/"),
]

# Kabinet Múz
kabinet_base = "https://www.kabinetmuz.cz"
kabinet_events = [
    e(1,  "20:00", "Květy", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-01-kvety"),
    e(2,  "20:00", "Sbohem jak sen!", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-02-sbohem-jak-sen"),
    e(3,  "20:00", "Lik /SWE + Macocha", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-03-lik-swe"),
    e(4,  "20:00", "Michajlov", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-04-michajlov"),
    e(7,  "20:00", "Kruh 19 (křest) + Beata", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-07-kruh-19-beata"),
    e(8,  "20:00", "Michael Krásný Quartet", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-08-michael-krasny-quattro-formaggi"),
    e(9,  "20:00", "Vltava", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-09-vltava"),
    e(10, "20:00", "A Place To Bury Strangers /USA + Kontravoid /CAN", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-10-a-place-to-bury-strangers-usa-kontravoid-can"),
    e(11, "20:00", "Temný Rudo + Cringe Prince", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-11-temny-rudo-cringe-prince"),
    e(13, "20:00", "Tomáš Havlen (křest) + Lichnovský", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-13-tomas-havlen-krest-lichnovsky"),
    e(14, "20:00", "Korben Dallas /SK", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-14-korben-dallas"),
    e(15, "22:00", "ENC: Night Circulation: Hansen + Serge X + Midnight Swimmers", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-15-enc-night-circulation-hansen-serge-x-midnight-swimmers"),
    e(17, "20:00", "Exorcizphobia (křest) + Deviance + Lord Skull", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-17-exorcizphobia-krest"),
    e(18, "20:00", "Emonight – My Chemical Romance Tribute CZ + Fall From Everest + Dirty Way", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-18-emonight--my-chemical-romance-tribute-cz-fall-from-everest-dirty-way"),
    e(20, "20:00", "Author & Punisher /USA + Fange /FR", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-20-author-punisher-fange"),
    e(21, "20:00", "Medial Banana + Ley Lofaj", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-21-medial-banana-ley-lofaj"),
    e(22, "20:00", "Berlin Manson", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-22-berlin-manson"),
    e(23, "20:00", "Berlin Manson", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-23-berlin-manson"),
    e(24, "20:00", "Ctib (křest) + Divo Institute + Včera bylo pozdě + S.G.A.T.V. /CH", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-24-ctib-krest"),
    e(25, "20:00", "Dub from the Ground Session", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-25-dub-from-the-underground"),
    e(26, "20:00", "Veronika Valová", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-26-veronika-valova"),
    e(27, "20:00", "Barbora Piešová – akustické turné Na správnej ceste", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-27-barbora-piesova-akusticke-turne-na-spravnej-ceste"),
    e(28, "20:00", "FAZE /CAN + Matter Tua (křest) + Kölmo", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-28-faze-can-host"),
    e(29, "20:00", "Ak'chamel /USA + Medard J. Zeman", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-29-akchamel-usa"),
    e(30, "20:00", "1914 /UA + Katla /DK", "Kabinet Múz", "Brno", f"{kabinet_base}/program/2026-04-30-1914-katla"),
]

# Stará Pekárna
stara_pekarna_events = [
    e(2,  "20:00", "Aakrum + Disonant", "Stará Pekárna", "Brno", "https://www.smsticket.cz/vstupenky/67402-aakrum-disonant-stara-pekarna-brno"),
    e(8,  "20:00", "Kumbalu (Etno Brno 2026)", "Stará Pekárna", "Brno", "https://www.smsticket.cz/vstupenky/68506-etno-jaro-2026-kumbalu-stara-pekarna-brno-musica-balkanika-damar"),
    e(9,  "20:00", "Létající rabín (Etno Brno 2026)", "Stará Pekárna", "Brno", "https://www.smsticket.cz/vstupenky/68513-etno-jaro-2026-letajici-rabin-25-let-stara-pekarna-brno"),
    e(10, "20:00", "Tisíc let od ráje + RLG", "Stará Pekárna", "Brno", "https://www.smsticket.cz/vstupenky/68529-tlor-rlg-stara-pekarna-brno-tisic-let-od-raje"),
    e(11, "20:00", "Ať se snaží Ona + Calienté", "Stará Pekárna", "Brno", "https://www.smsticket.cz/vstupenky/67403-at-se-snazi-ona-calinte-stara-pekarna-brno-caliente"),
    e(16, "20:00", "Tomáš Kočko & Orchestr", "Stará Pekárna", "Brno", "https://www.smsticket.cz/vstupenky/64970-tomas-kocko-orchestr-stara-pekarna-brno"),
    e(17, "20:00", "Čtvrt na smrt + Makaklan", "Stará Pekárna", "Brno", "https://www.smsticket.cz/vstupenky/67998-ctvrt-na-smrt-makaklan-stara-pekarna-brno"),
    e(18, "20:00", "Občan Trhan + Kakktus", "Stará Pekárna", "Brno", "https://www.smsticket.cz/vstupenky/68802-obcan-trhan-kakktus-stara-pekarna-brno"),
    e(20, "20:00", "Kikibobolapokeb + Haranti", "Stará Pekárna", "Brno", "https://www.smsticket.cz/vstupenky/69128-kikibobolapokeb-haranti-stara-pekarna-brno"),
    e(21, "20:00", "The Bad Week (Jazz & Blues Brno 2026)", "Stará Pekárna", "Brno", "https://www.smsticket.cz/vstupenky/67365-the-bad-week-nejlepsi-blues-z-celeho-srbska-stara-pekarna-brno"),
    e(23, "20:00", "Obludárium (s úctou Petru Hapkovi)", "Stará Pekárna", "Brno", "https://www.smsticket.cz/vstupenky/68804-obludarium-s-uctou-petru-hapkovi-stara-pekarna-brno"),
    e(25, "20:00", "The Newmour Experience", "Stará Pekárna", "Brno", "https://www.smsticket.cz/vstupenky/67717-the-newmour-experience-stara-pekarna-brno"),
    e(28, "20:00", "Mariachi Espuelas (Etno Brno 2026)", "Stará Pekárna", "Brno", "https://www.smsticket.cz/vstupenky/68515-etno-jaro-2026-mariachi-espuelas-stara-pekarna-brno-musica-balkanika-damar"),
]

# Melodka
melodka_base = "https://www.melodka.cz"
melodka_events = [
    e(2,  "20:00", "Afterglow Rock 2 – Liquid Jesus, Rocket Bunny...", "Melodka", "Brno", f"{melodka_base}/program/akce/02-04-2026-afterglow-rock-2-liquid-jesus-rocket-bunny"),
    e(3,  "19:00", "Kill The Night: Bestial Therapy, Landscape of Shadows...", "Melodka", "Brno", f"{melodka_base}/program/akce/03-04-2026-kill-the-night-bestial-therapy-landscape-of-shadows"),
    e(4,  "20:00", "Clubber Die Younger vol. 46 – Black Nail Cabaret...", "Melodka", "Brno", f"{melodka_base}/program/akce/04-04-2026-clubber-die-younger-vol-46-black-nail-cabaret"),
    e(8,  "20:00", "Snak The Ripper, Junk, Bermuda", "Melodka", "Brno", f"{melodka_base}/program/akce/08-04-2026-snak-the-ripper-junk-bermuda"),
    e(10, "19:30", "J.H.Krchovský & Krch-off band", "Melodka", "Brno", f"{melodka_base}/program/akce/10-04-2026-j-h-krchovsky-krch-off-band"),
    e(11, "19:30", "Převaděč spojitosti, Hihead", "Melodka", "Brno", f"{melodka_base}/program/akce/11-04-2026-prevadec-spojitosti-hihead"),
    e(12, "20:00", "Ancient Fragments", "Melodka", "Brno", f"{melodka_base}/program/akce/12-04-2026-ancient-fragments"),
    e(13, "19:30", "Free Night: Jan Hilar a Noční s, Aldente, Vážky", "Melodka", "Brno", f"{melodka_base}/program/akce/13-04-2026-free-night-jan-hilar-a-nocni-s-aldente-vazky"),
    e(16, "20:00", "Záviš", "Melodka", "Brno", f"{melodka_base}/program/akce/16-04-2026-zavis"),
    e(17, "20:00", "Space of Variations, Up Great", "Melodka", "Brno", f"{melodka_base}/program/akce/17-04-2026-space-of-variations-up-great"),
    e(22, "20:00", "Slehní Mech, PCHAAA", "Melodka", "Brno", f"{melodka_base}/program/akce/22-04-2026-slehni-mech-pchaaa"),
    e(23, "20:00", "Marianas Rest, Aeonian Sorrow, Wooden Veins", "Melodka", "Brno", f"{melodka_base}/program/akce/23-04-2026-marianas-rest-aeonian-sorrow-wooden-veins"),
    e(24, "19:30", "Křest 301 + Zrcadla + Rezervoar Dogz", "Melodka", "Brno", f"{melodka_base}/program/akce/24-04-2026-krest-301-zrcadla-rezervoar-dogz"),
    e(25, "20:00", "Malphas, Cvinger, Kybalion, Eternal Damnation", "Melodka", "Brno", f"{melodka_base}/program/akce/25-04-2026-malphas-cvinger-kybalion-eternal-damnation"),
    e(27, "19:30", "Pepsi Free Night: Projekt Húrka, Moře Kuřat...", "Melodka", "Brno", f"{melodka_base}/program/akce/27-04-2026-pepsi-free-night-projekt-hurka-more-kurat"),
    e(30, "20:00", "Maniak (křest alba)", "Melodka", "Brno", f"{melodka_base}/program/akce/30-04-2026-maniak-krest-alba-streamtape"),
]


# ─── BUILD FINAL STRUCTURE ───────────────────────────────────────────────────

venues_data = [
    {"venue": "O2 Arena",                           "city": "Praha",  "events": o2arena_events,         "validation": validate(o2arena_events, "O2 Arena", 4, 15)},
    {"venue": "O2 Universum",                       "city": "Praha",  "events": o2universum_events,      "validation": validate(o2universum_events, "O2 Universum", 3, 10)},
    {"venue": "Sportovní hala Fortuna (Tipsport Arena)", "city": "Praha", "events": tipsport_events,    "validation": validate(tipsport_events, "Sportovní hala Fortuna (Tipsport Arena)", 2, 8)},
    {"venue": "Forum Karlín",                       "city": "Praha",  "events": forumkarlin_events,      "validation": validate(forumkarlin_events, "Forum Karlín", 5, 15)},
    {"venue": "Palác Akropolis",                    "city": "Praha",  "events": akropolis_events,        "validation": validate(akropolis_events, "Palác Akropolis", 15, 30)},
    {"venue": "Lucerna Velký sál",                  "city": "Praha",  "events": lucerna_velky_events,    "validation": validate(lucerna_velky_events, "Lucerna Velký sál", 8, 20)},
    {"venue": "Roxy",                               "city": "Praha",  "events": roxy_events,             "validation": validate(roxy_events, "Roxy", 15, 30)},
    {"venue": "MeetFactory",                        "city": "Praha",  "events": meetfactory_events,      "validation": validate(meetfactory_events, "MeetFactory", 3, 12)},
    {"venue": "Lucerna Music Bar",                  "city": "Praha",  "events": musicbar_events,         "validation": validate(musicbar_events, "Lucerna Music Bar", 20, 30)},
    {"venue": "Rock Café",                          "city": "Praha",  "events": rockcafe_events,         "validation": validate(rockcafe_events, "Rock Café", 20, 30)},
    {"venue": "Vagon",                              "city": "Praha",  "events": vagon_events,            "validation": validate(vagon_events, "Vagon", 10, 25)},
    {"venue": "Jazz Dock",                          "city": "Praha",  "events": jazzdock_events,         "validation": validate(jazzdock_events, "Jazz Dock", 8, 20)},
    {"venue": "Reduta Jazz Club",                   "city": "Praha",  "events": reduta_events,           "validation": validate(reduta_events, "Reduta Jazz Club", 5, 20)},
    {"venue": "Malostranská beseda",                "city": "Praha",  "events": beseda_events,           "validation": validate(beseda_events, "Malostranská beseda", 5, 15)},
    {"venue": "Cross Club",                         "city": "Praha",  "events": crossclub_events,        "validation": validate(crossclub_events, "Cross Club", 8, 20)},
    {"venue": "Watt Music Club",                    "city": "Plzeň",  "events": [],                      "validation": validate([], "Watt Music Club", 3, 10)},
    {"venue": "Buena Vista Club",                   "city": "Plzeň",  "events": bvc_events,              "validation": validate(bvc_events, "Buena Vista Club", 3, 10)},
    {"venue": "Divadlo Pod lampou",                 "city": "Plzeň",  "events": podlampou_events,        "validation": validate(podlampou_events, "Divadlo Pod lampou", 0, 5)},
    {"venue": "Kulturní dům Šeříkovka",             "city": "Plzeň",  "events": serikovka_events,        "validation": validate(serikovka_events, "Kulturní dům Šeříkovka", 1, 8)},
    {"venue": "Papírna Plzeň",                      "city": "Plzeň",  "events": [],                      "validation": validate([], "Papírna Plzeň", 1, 8)},
    {"venue": "Sono Centrum",                       "city": "Brno",   "events": sono_events,             "validation": validate(sono_events, "Sono Centrum", 20, 35)},
    {"venue": "Fléda",                              "city": "Brno",   "events": fleda_events,            "validation": validate(fleda_events, "Fléda", 15, 35)},
    {"venue": "Kabinet Múz",                        "city": "Brno",   "events": kabinet_events,          "validation": validate(kabinet_events, "Kabinet Múz", 10, 20)},
    {"venue": "Stará Pekárna",                      "city": "Brno",   "events": stara_pekarna_events,    "validation": validate(stara_pekarna_events, "Stará Pekárna", 8, 15)},
    {"venue": "Melodka",                            "city": "Brno",   "events": melodka_events,          "validation": validate(melodka_events, "Melodka", 5, 12)},
]

# Count total events
all_events = []
for v in venues_data:
    all_events.extend(v["events"])
total = len(all_events)

# Check day coverage
days_covered = set(ev["day"] for ev in all_events)
missing_days = [d for d in range(1, 31) if d not in days_covered]

output = {
    "month": MONTH,
    "year": YEAR,
    "month_name": MONTH_NAME,
    "total_events": total,
    "venues": venues_data
}

with open("events_data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Total events: {total}")
print(f"Days covered: {len(days_covered)}/30")
if missing_days:
    print(f"Missing days: {missing_days}")
else:
    print("All 30 days covered!")

# Print validation summary
print("\n=== VALIDATION REPORT ===")
for v in venues_data:
    val = v["validation"]
    status = val["status"]
    marker = "GREEN" if status == "GREEN" else ("YELLOW" if status == "YELLOW" else "RED")
    print(f"[{marker}] {v['venue']}: {val['total_events']} events (expected {val['expected_range']})")
