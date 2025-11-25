#!/usr/bin/env python3
"""Generate December 2025 concert program HTML."""

from datetime import datetime
import html

# Events data organized by date
events_data = {
    1: [  # Pondělí
        ("DIRE STRAITS Tribute", "21:00", "Vagon", "Praha", "https://www.direstraits.cz"),
        ("Klub zadán", "19:00", "Jazz Dock", "Praha", "https://www.jazzdock.cz/cs/koncert/klub-zadan-318"),
        ("Pěvecké vystoupení Konzervatoře Jaroslava Ježka", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-01/pevecke-vystoupeni-konzervatore-jaroslava-jezka/9430827"),
        ("Kateřina Vacková & Jakub Duša in duo", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-01/katerina-vackova-jakub-dusa-in-duo/9431042"),
        ("Tribute to Jazz Legends: Timeless Melodies", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/tribute-to-jazz-legends-timeless-melodies-eming-1"),
        ("Best of Golden Jazz Era", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/best-of-golden-jazz-era"),
        ("321Jedem! + host: Taťjana Medvecká", "19:00", "Malostranská beseda", "Praha", "https://goout.net/cs/321jedem+host-tatjana-medvecka/szpylby"),
        ("Calin", "20:00", "O2 Arena", "Praha", "https://www.o2arena.cz/en/events/calin-2025-en/"),
    ],
    2: [  # Úterý
        ("Calin", "20:00", "O2 Arena", "Praha", "https://www.o2arena.cz/en/events/calin-2025-en/"),
        ("The Subways / UK", "20:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/the-subways-uk-6/"),
        ("Rock for People: James Marriott", "19:00", "MeetFactory", "Praha", "http://www.meetfactory.cz/cs/program/detail/rock-for-people-james-marriott"),
        ("RED BARON BAND + ROMAN DRAGOUN", "21:00", "Vagon", "Praha", "https://redbaronband.cz"),
        ("Tonya Graves", "20:00", "Jazz Dock", "Praha", "https://www.jazzdock.cz/cs/koncert/tonya-graves-1-6"),
        ("Stará paní tančí swing – vinylová edice", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-02/stara-pani-tanci-swing-vinylova-edice/9407808"),
        ("KRISTIAN ENKERUD LIEN'S KRISE /NO", "20:00", "Palác Akropolis", "Praha", "https://palacakropolis.cz/work/33298?event_id=39737"),
        ("THE MUSIC DIGEST (30)", "20:00", "Palác Akropolis", "Praha", "https://palacakropolis.cz/work/33298?event_id=39738"),
        ("Artem Pivovarov Live with Choir & Orchestra", "20:00", "Lucerna Velký sál", "Praha", "https://www.lucpra.com/index.php/cz/programs/eventdetail/1044/artem-pivovarov-live-with-choir-orchestra-prague"),
        ("TRIBUTE TO GIANTS OF THE SAXOPHONE", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/saxophone"),
        ("The Saxophone Legacy", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/the-saxophone-legacy-tribute-to-coltrane-getz-rollins-young"),
        ("Nedivoč", "20:00", "Malostranská beseda", "Praha", "https://goout.net/cs/nedivoc/szcjccy"),
    ],
    3: [  # Středa
        ("LOBODA", "20:00", "Forum Karlín", "Praha", "https://www.forumkarlin.cz/en/event/loboda"),
        ("MARPO", "19:00", "Roxy", "Praha", "https://tickets.nfctron.com/event/universal-music/marpo-making-country-music-cool-again-/cart"),
        ("The Raveonettes + Hothouse", "20:00", "MeetFactory", "Praha", "http://www.meetfactory.cz/cs/program/detail/the-raveonettes"),
        ("Visací zámek", "19:30", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/visaci-zamek-4/"),
        ("THE SOUL UNCLES", "21:00", "Vagon", "Praha", "https://www.thesouluncles.cz"),
        ("Tonya Graves", "20:00", "Jazz Dock", "Praha", "https://www.jazzdock.cz/cs/koncert/tonya-graves-1-7"),
        ("RISE OF THE NORTHSTAR /FR + DEEZ NUTS /AU + HALF ME /DE", "19:00", "Palác Akropolis", "Praha", "https://palacakropolis.cz/work/33298?event_id=39642"),
        ("Latin Legends Live: Tribute to Jobim & Stars", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/latin-legends-live-tribute-to-jobim-stars-luka"),
        ("The Best Rhythms of Brazil", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/the-best-rhythms-of-brazil-honoring-jobim-latin-greats"),
        ("Donovan Kingjay & The Regulators + Boss Foundation", "20:00", "Malostranská beseda", "Praha", "https://goout.net/cs/donovan-kingjay-and-the-regulators%2Bboss-foundation/szuuxcy"),
        ("Vánoční Busking Párty – Feher Fekete Kerek", "20:00", "Divadlo Pod lampou", "Plzeň", "https://podlampou.cz/events/vanocni-busking-party/"),
    ],
    4: [  # Čtvrtek
        ("Live Nation: Nemo", "20:00", "MeetFactory", "Praha", "http://www.meetfactory.cz/cs/program/detail/livenation-nemo"),
        ("Fast Food Orchestra", "19:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/fast-food-orchestra-3/"),
        ("OZZY OSBOURNE Revival", "21:00", "Vagon", "Praha", "http://www.ozzyosbournerevival.cz"),
        ("Madhouse Express + Acid Row", "19:00", "Rock Café", "Praha", "https://rockcafe.cz/en/program/madhouse-express-single-release-party-special-guest-acid-row/"),
        ("Klub zadán", "19:00", "Jazz Dock", "Praha", "https://www.jazzdock.cz/cs/koncert/klub-zadan-319"),
        ("LES TRIABOLIQUES /UK", "20:00", "Palác Akropolis", "Praha", "https://palacakropolis.cz/work/33298?event_id=40035"),
        ("Melodic Journey with Louis Armstrong, Gershwin, Jobim", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/melodic-journey-metropolitan-jazz-band-10"),
        ("Jazz Legends Special evening: Tribute to Louis Armstrong", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/jazz-legends-special-evening-a-tribute-to-louis-a-3"),
        ("Tereza Balonová: Speciální akustický koncert", "20:00", "Malostranská beseda", "Praha", "https://goout.net/cs/tereza-balonova-specialni-akusticky-koncert/szosecy"),
        ("DAN BÁRTA & Illustratosphere + Lash&Grey", "20:00", "Šeříkovka", "Plzeň", "https://www.serikovka.cz/koncerty/80-4-12-2025-dan-barta-illustratospehre-lash-grey"),
    ],
    5: [  # Pátek
        ("ŠKWOR", "19:00", "O2 Universum", "Praha", "https://www.o2universum.cz/en/events/skwor-2025-en/"),
        ("Pop 80's & 90's video party", "21:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/pop-80s-90s-video-party-dj-jirka-neumann-865/"),
        ("KRAUSBERRY", "21:00", "Vagon", "Praha", "http://www.krausberry.cz/"),
        ("Marie April + guests", "19:30", "Rock Café", "Praha", "https://rockcafe.cz/en/program/marie-april-krest-singlu-breakfast-sex-hoste-voita-caramel-jay-austin/"),
        ("COLDRAIN /JP", "19:00", "Palác Akropolis", "Praha", "https://palacakropolis.cz/work/33298?event_id=39323"),
        ("DNBTV.COM BLACK EDITION w/ ZOMBIE CATS & MEAN TEETH", "22:00", "Cross Club", "Praha", "https://www.crossclub.cz/cs/program/8340-dnbtv-com-black-edition-w-zombie-cats-mean-teeth/"),
        ("The Ray Charles Experience by Lee Andrew Davison", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/ray-charles-lee"),
        ("The Ultimate Jazz, Soul & Funk Experience", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/the-ultimate-jazz-soul-funk-experience-with-lee"),
        ("Tereza Balonová: Speciální akustický koncert", "20:00", "Malostranská beseda", "Praha", "https://goout.net/cs/tereza-balonova-specialni-akusticky-koncert/szpsecy"),
        ("Annamaria D'Almeida & Robert Fischmann & Jakub Eben", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-05/annamaria-d-almeida-robert-fischmann-jakub-eben/9355499"),
        ("Elbe * NMBF (PL)", "20:00", "Divadlo Pod lampou", "Plzeň", "https://podlampou.cz/events/elbe-fdk/"),
    ],
    6: [  # Sobota
        ("4TENOŘI: Vánoční přání", "19:00", "O2 Arena", "Praha", "https://www.o2arena.cz/en/events/4tenori-vanocni-prani-2/"),
        ("OLGA LOUNOVÁ – Sraz optimistů", "20:00", "O2 Universum", "Praha", "https://www.o2universum.cz/en/events/olga-lounova-sraz-optimistu-2/"),
        ("BADGER", "23:00", "Roxy", "Praha", "https://goout.net/cs/listky/badger/xqlfb/"),
        ("Live Nation: LEISURE", "20:00", "MeetFactory", "Praha", "http://www.meetfactory.cz/cs/program/detail/live-nation-leisure"),
        ("6arelyhuman / US", "18:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/6arelyhuman-us/"),
        ("Pop 80's & 90's video party", "22:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/pop-80s-90s-video-party-dj-jirka-neumann-866/"),
        ("TOTÁLNÍ NASAZENÍ + DILEMMA IN CINEMA + DERATIZÉŘI", "20:00", "Vagon", "Praha", "http://www.totaci.net/"),
        ("Helmutova Stříkačka + Lety Mimo", "20:00", "Rock Café", "Praha", "https://rockcafe.cz/en/program/helmutova-strikacka-lety-mimo/"),
        ("ÁRSTIDÍR", "20:00", "Palác Akropolis", "Praha", "https://palacakropolis.cz/work/33298?event_id=39666"),
        ("ERA TECHNO & ART EXHIB w/ DJ HELL", "22:00", "Cross Club", "Praha", "https://www.crossclub.cz/cs/program/8341-era-techno-art-exhib-w-dj-hell/"),
        ("Tribute to the Legends of 1950s Hard Bop", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/legends-of-1950s-hard-bop"),
        ("Hard Bop Masters: Miles Davis, Art Blakey & Cannonball Adderley", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/hard-bop-masters-a-tribute-to-miles-davis-art-blakey-cannonball-adderley"),
        ("Veronika & The Band", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-06/veronika-the-band/9355483"),
        ("Karlo", "21:00", "Divadlo Pod lampou", "Plzeň", "https://podlampou.cz/events/karlo/"),
        ("POETIKA 2025 - Slunce v barvách antracitu", "20:00", "Buena Vista Club", "Plzeň", "https://store.united-tickets.cz/event/universal-music/poetika-slunce-v-barvach-antracitu-2025"),
    ],
    7: [  # Neděle
        ("Sto zvířat – 35 let", "18:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/sto-zvirat-35-let/"),
        ("Obscure: All Shall Perish, Peeling Flash, Vulvodynia, Necrotted", "18:30", "MeetFactory", "Praha", "http://www.meetfactory.cz/cs/program/detail/obscure-all-shall-perish-peeling-flash-vulvodynia-necrotted"),
        ("BACK SIDE BIG BAND", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/back-side-big-band21"),
        ("A Night of Jazz Legends: Backside Big Band", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/noname-44"),
    ],
    8: [  # Pondělí
        ("Bladee", "20:00", "Forum Karlín", "Praha", "https://www.forumkarlin.cz/en/event/bladee"),
        ("Sto zvířat – 35 let", "18:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/sto-zvirat-35-let-2/"),
        ("DEFINITIVNÍ ENTENTÝK", "21:00", "Vagon", "Praha", "https://www.ententyk.cz"),
        ("Decline & Jerusalem", "19:00", "Rock Café", "Praha", "https://rockcafe.cz/en/program/decline-jerusalem/"),
        ("Legends of Swing: The Best of Miller, Goodman & Basie", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/legends-of-swing-bara-klara"),
        ("THE BEST OF SWING & JAZZ EVENING", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/the-best-of-swing-jazz-evening-glen-miller-benny-1"),
        ("Libor Šmoldas & Kateřina Hošková", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-08/libor-smoldas-katerina-hoskova/9430828"),
    ],
    9: [  # Úterý
        ("LUCIE – 40 LET", "20:00", "O2 Arena", "Praha", "https://www.o2arena.cz/en/events/lucie-40-let-en/"),
        ("CHIPPENDALES – All Night Long 2025 World Tour", "19:30", "O2 Universum", "Praha", "https://www.o2universum.cz/en/events/chippendales-all-night-long-2025-world-tour-2/"),
        ("Monkey Business", "19:30", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/monkey-business-32/"),
        ("VINTAGE WINE + DICK O'BRASS + PEKELNÉ KONE", "20:00", "Vagon", "Praha", "https://www.facebook.com/vintagewineband"),
        ("Desolated (UK), Bayway (USA), D-Bloc (USA), Sidestep (SWE)", "19:00", "Rock Café", "Praha", "https://rockcafe.cz/en/program/desolated-uk-bayway-usa-d-bloc-usa-sidestep-swe/"),
        ("Louis Armstrong Forever: Old Timers Jazz Band", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/louis-armstrong-forever-celebrating-a-jazz-icon-with-old-timers-jazz-band-2"),
        ("Jazz Legends Special evening: Tribute to Louis Armstrong", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/jazz-legends-special-evening-a-tribute-to-louis-a-2"),
        ("Billy Liar and the Haunted Hearts (SCO) * Lenny", "20:00", "Divadlo Pod lampou", "Plzeň", "https://podlampou.cz/events/billy-liar-and-the-haunted-hearts-us-lenny-lashleys-gang-of-one-street-dogs-us-red-at-night-d/"),
    ],
    10: [  # Středa
        ("LUCIE – 40 LET", "20:00", "O2 Arena", "Praha", "https://www.o2arena.cz/en/events/lucie-40-let-en/"),
        ("KOBLÍŽCI", "18:00", "Roxy", "Praha", "https://www.ticketstream.cz/akce/koblizci-zpatky-na-vrchol-krest-alba-ves-nice-story-186646"),
        ("Monkey Business", "19:30", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/monkey-business-33/"),
        ("RAGE AGAINST THE MACHINE Revival + ALICE IN CHAINS", "21:00", "Vagon", "Praha", "http://www.facebook.com/RATMRevival/"),
        ("Simon Opp", "19:00", "Rock Café", "Praha", "https://rockcafe.cz/en/program/simon-opp/"),
        ("LETNÍ KAPELA", "20:00", "Palác Akropolis", "Praha", "https://palacakropolis.cz/work/33298?event_id=39534"),
        ("The Nina Simone Experience", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/the-nina-simone-experience-an-unforgettable-jazz-tribute"),
        ("The Beatles Groove: A Jazz Tribute", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/the-beatles-groove-a-jazz-tribute"),
    ],
    11: [  # Čtvrtek
        ("HAUSER: THE REBEL IS BACK", "20:00", "O2 Arena", "Praha", "https://www.o2arena.cz/en/events/hauser-the-rebel-is-back-2/"),
        ("NOGA EREZ", "19:30", "Roxy", "Praha", "https://goout.net/cs/listky/the-vandalist-tour-noga-erez+support-uzi-freyja/cugfb/"),
        ("Krucipüsk + Xavier Baumaxa", "19:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/krucipusk-8/", "VYPRODÁNO"),
        ("ZNOUZECTNOST + AKIA B.A.", "21:00", "Vagon", "Praha", "http://www.znc.cz/"),
        ("TH!S", "20:00", "Rock Café", "Praha", "https://rockcafe.cz/en/program/ths-2/"),
        ("SKYLINE", "20:00", "Palác Akropolis", "Praha", "https://palacakropolis.cz/work/33298?event_id=39538"),
        ("Ella Fitzgerald: The Voice of Jazz", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/ella-fitzgerald-the-voice-of-jazz-forever-resona"),
        ("Tribute to the Best Jazz Divas", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/tribute-to-the-best-jazz-divas-sonenshine"),
        ("OvO (IT) * Lyssa * Krecht", "20:00", "Divadlo Pod lampou", "Plzeň", "https://podlampou.cz/events/mistni-borci-uvadeji-ovo-it/"),
    ],
    12: [  # Pátek
        ("JOY ORBISON", "23:00", "Roxy", "Praha", "https://goout.net/cs/listky/joy-orbison/ismib/"),
        ("Pop 80's & 90's video party", "21:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/pop-80s-90s-video-party-dj-jirka-neumann-867/"),
        ("BRUTUS", "21:00", "Vagon", "Praha", "http://www.brutus.cz/"),
        ("Gutafest vol. 1: Gutalax, Stillbirth (DE), Epicardiectomy, Pothead", "19:30", "Rock Café", "Praha", "https://rockcafe.cz/en/program/gutafest-vol-1-gutalax-stillbirth-de-epicardiectomy-pothead/"),
        ("BLITZ UNION", "20:00", "Palác Akropolis", "Praha", "https://palacakropolis.cz/work/33298?event_id=39535"),
        ("DOUBLE TROUBLE w/ APHRODITE & MJOI", "22:00", "Cross Club", "Praha", "https://www.crossclub.cz/cs/program/8342-double-trouble-w-aphrodite-mjoi/"),
        ("Remembering Sinatra: A Timeless Tribute", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/remembering-sinatra-a-timeless-tribute"),
        ("Swingin' with Sinatra", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/swingin-with-sinatra"),
        ("Billy Rudin", "20:00", "Divadlo Pod lampou", "Plzeň", "https://podlampou.cz/events/billy-rudin/"),
    ],
    13: [  # Sobota
        ("JELEN", "20:00", "O2 Arena", "Praha", "https://www.o2arena.cz/en/events/jelen-6/"),
        ("CAMO&KROOKED", "23:00", "Roxy", "Praha", "https://goout.net/cs/listky/camo-and-krooked/vxjfb/"),
        ("COCOTTI V LUCERNĚ!", "19:30", "Lucerna Velký sál", "Praha", "https://www.lucpra.com/index.php/cz/programs/eventdetail/1006/cocotti-v-lucerne"),
        ("Pop 80's & 90's video party", "21:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/pop-80s-90s-video-party-dj-jirka-neumann-868/"),
        ("AC/DC TRIBUTE Pardubice", "21:00", "Vagon", "Praha", "https://www.acdctribute.cz"),
        ("Jana Uriel Kratochvílová & Illuminati.ca – Vánoční koncert", "20:00", "Rock Café", "Praha", "https://rockcafe.cz/en/program/jana-uriel-kratochvilova-illuminati-ca-vanocni-koncert/"),
        ("Bohemia Big Band: Tribute to Glenn Miller, Duke Ellington", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/bohemia-big-band-tribute-to-glenn-miller-duke-el-1"),
        ("Timeless Jazz: Bohemia Big Band", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/timeless-jazz-bohemia-big-band-pays-tribute-to-gershwin-basie-miller"),
        ("KvarteTones", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-13/kvartetones/9408748"),
        ("THE WOPENERS, FREDY a KRASTY, Bára ZEMANOVÁ", "20:00", "Buena Vista Club", "Plzeň", "https://www.buenavistaclub.cz/program-klubu.aspx"),
        ("IRON MAIDEM Tribute (HU) & ALCOHOLICA - Metallica tribute (PL)", "20:00", "Šeříkovka", "Plzeň", "https://www.serikovka.cz/koncerty/81-13-12-2025"),
    ],
    14: [  # Neděle
        ("James Arthur", "20:00", "O2 Universum", "Praha", "https://www.o2universum.cz/en/events/james-arthur-2025-en/"),
        ("NERVY", "19:00", "Roxy", "Praha", "https://ticketshop.store/en/events/106107"),
        ("Ondřej Havelka a jeho Melody Makers", "19:30", "Lucerna Velký sál", "Praha", "https://www.lucpra.com/index.php/cz/programs/eventdetail/1039/ondrej-havelka-a-jeho-melody-makers"),
        ("Mňága a Žďorp – křest alba", "19:30", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/mnaga-a-zdorp-krest-alba-2/"),
        ("Pabst (DE)", "20:00", "Rock Café", "Praha", "https://rockcafe.cz/en/program/pabst-de-support-3/"),
        ("Big Band Trumpets – Kings of Swing", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/big-band-trumpets-kings-of-swing-tribute-to-duke"),
        ("Big Band Trumpets: Tribute to Swing Masters", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/big-band-trumpets-a-tribute-to-swing-masters-ellington-jones-gillespie-miller"),
    ],
    15: [  # Pondělí
        ("Divokej Bill - Praha - Zimní speciál 2025", "20:00", "Lucerna Velký sál", "Praha", "https://www.lucpra.com/index.php/cz/programs/eventdetail/1042/divokej-bill-praha-zimni-special-2025"),
        ("Mňága a Žďorp – křest alba", "19:30", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/mnaga-a-zdorp-krest-alba/"),
        ("BAD TIMES BLUES + NAHOŘE NA HOŘE", "21:00", "Vagon", "Praha", "https://bandzone.cz/_115127"),
        ("Piano Legends Unite: Tribute to Chick Corea, Herbie Hancock, Oscar Peterson", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/piano-legends-unite-a-tribute-to-chick-corea-her"),
        ("Piano Greats: Tribute to Corea, Hancock & Peterson", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/piano-greats-tribute-to-corea-hancock-peterson"),
        ("Libor's Jam Ob-Session", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-15/libor-s-jam-ob-session/9430829"),
    ],
    16: [  # Úterý
        ("Lucerna 2025", "20:00", "Lucerna Velký sál", "Praha", "https://www.lucpra.com/index.php/cz/programs/eventdetail/1007/lucerna-2025"),
        ("Zrní", "19:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/zrni-4/"),
        ("QUEENIE", "21:00", "Vagon", "Praha", "https://www.queenie.cz"),
        ("Blood Command (NOR)", "19:00", "Rock Café", "Praha", "https://rockcafe.cz/en/program/obscure-presents-blood-command-nor/"),
        ("The Ray Charles Experience by Lee Andrew Davison", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/ray-charles-lee"),
        ("The Ultimate Jazz, Soul & Funk Experience", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/the-ultimate-jazz-soul-funk-experience-with-lee"),
        ("Nikola Ďuricová", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-16/nikola-duricova/9430835"),
    ],
    17: [  # Středa
        ("Eva Urbanová & Miroslav Donutil", "19:00", "Lucerna Velký sál", "Praha", "https://www.lucpra.com/index.php/cz/programs/eventdetail/1025/spolecne-a-vanocne-eva-urbanova-miroslav-donutil"),
        ("Vypsaná fiXa", "19:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/vypsana-fixa-15/", "VYPRODÁNO"),
        ("ZÁVIŠ", "21:00", "Vagon", "Praha", "https://www.facebook.com/ZavisOFFICIAL"),
        ("Bohemian Betyars (HU)", "20:00", "Rock Café", "Praha", "https://rockcafe.cz/en/program/bohemian-betyars-hu/"),
        ("LUCY DREAMS /AT", "20:00", "Palác Akropolis", "Praha", "https://palacakropolis.cz/work/33298?event_id=40402"),
        ("THE BEST OF SWING & JAZZ EVENING", "19:00", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/the-best-of-swing-jazz-evening-glen-miller-ben"),
        ("Legends of Swing: The Best of Miller, Goodman & Basie", "21:15", "Reduta Jazz Club", "Praha", "https://www.redutajazzclub.cz/artists-cs/legends-of-swing-bara-klara"),
        ("Znouzectnost * host: Aqua Silentia", "20:00", "Divadlo Pod lampou", "Plzeň", "https://podlampou.cz/events/znouzectnost-5/"),
    ],
    18: [  # Čtvrtek
        ("Till Lindemann – Meine Welt Tour 2025", "20:00", "O2 Arena", "Praha", "https://www.o2arena.cz/en/events/till-lindemann-meine-welt-tour-2025-2/"),
        ("Monika Absolonová – Až do nebes 2025", "19:00", "Lucerna Velký sál", "Praha", "https://www.lucpra.com/index.php/cz/programs/eventdetail/1046/monika-absolonova-az-do-nebes-2025"),
        ("Vypsaná fiXa", "19:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/vypsana-fixa-14/", "VYPRODÁNO"),
        ("PUMPA", "21:00", "Vagon", "Praha", "https://www.pumparock.cz"),
        ("SLAVÍČEK", "20:00", "Palác Akropolis", "Praha", "https://palacakropolis.cz/work/33298?event_id=40125"),
    ],
    19: [  # Pátek
        ("Roman Staněk a Filip Salač", "20:00", "Forum Karlín", "Praha", "https://www.forumkarlin.cz/en/event/roman-stanek-a-filip-salac"),
        ("GREY256", "20:00", "Lucerna Velký sál", "Praha", "https://www.lucpra.com/index.php/cz/programs/eventdetail/975/grey256"),
        ("OZZY OSBOURNE & BLACK SABBATH Revival", "21:00", "Vagon", "Praha", "https://www.facebook.com/profile.php?id=100057519516477"),
        ("Maid of Ace (UK)", "20:00", "Rock Café", "Praha", "https://rockcafe.cz/en/program/maid-of-ace-uk-support-2/"),
        ("Jiří Polydor Sextet & Eva Emingerová", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-19/jiri-polydor-sextet-eva-emingerova/9415860"),
        ("TTIOT * Severals * themayrevolution", "20:00", "Divadlo Pod lampou", "Plzeň", "https://podlampou.cz/events/donnie-darko-ttiot-themayrevolution/"),
    ],
    20: [  # Sobota
        ("Tři sestry & Trautenberk", "19:00", "O2 Arena", "Praha", "https://www.o2arena.cz/en/events/tri-sestry-trautenberk-2/"),
        ("Sám doma in Concert", "19:00", "O2 Universum", "Praha", "https://www.o2universum.cz/en/events/sam-doma-in-concert-2/"),
        ("Vánoční koncert Michala Prokopa & Framus Five", "19:00", "Forum Karlín", "Praha", "https://www.forumkarlin.cz/en/event/vanocni-koncert-michala-prokopa-framus-five-s-hosty"),
        ("DNB WEDNIGHT: CHRISTMAS SPECIAL", "23:00", "Roxy", "Praha", "https://goout.net/cs/listky/dnb-wednight-christmas-special/mhqib/"),
        ("Lollipopz slaví 10 let", "17:00", "Lucerna Velký sál", "Praha", "https://www.lucpra.com/index.php/cz/programs/eventdetail/997/lollipopz-slavi-10-let"),
        ("Pop 80's & 90's video party", "21:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/pop-80s-90s-video-party-dj-jirka-neumann-869/"),
        ("HUDBA PRAHA", "21:00", "Vagon", "Praha", "http://www.hudbaprahaband.cz"),
        ("Green Monster (26th birthday)", "19:00", "Rock Café", "Praha", "https://rockcafe.cz/en/program/green-monster-26-narozeniny-hoste-twisted-rod-the-rusty-cans/"),
        ("KASTA /RU", "20:00", "Palác Akropolis", "Praha", "https://palacakropolis.cz/work/33298?event_id=40395"),
        ("Acoustic Needles", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-20/acoustic-needles/9355484"),
        ("E!E * host: Pod stolem", "20:00", "Divadlo Pod lampou", "Plzeň", "https://podlampou.cz/events/ee-3/"),
        ("KEČUP – 40 let", "20:00", "Šeříkovka", "Plzeň", "https://www.serikovka.cz/koncerty/83-20-12-2025-kecup-40-let"),
    ],
    21: [  # Neděle
        ("Ben Cristovao, Sofian Medjmedj – Khaosan & Denpasar show", "20:00", "O2 Universum", "Praha", "https://www.o2universum.cz/en/events/ben-cristovao-sofian-medjmedj-khaosan-denpasar-show-2-show-en/"),
        ("HELENA tour 25", "19:00", "Lucerna Velký sál", "Praha", "https://www.lucpra.com/index.php/cz/programs/eventdetail/1008/helena-tour-25"),
        ("Blue Effect & The Matadors", "18:30", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/vzpominka-na-radima-hladika-blue-effect-the-matadors/"),
        ("Riot Zone: Razor Instead of Tongue, Trýzeň, Aparath", "18:00", "Rock Café", "Praha", "https://rockcafe.cz/en/program/riot-zone-razor-instead-of-tongue-tryzen-aparath-berhelven-antistress/"),
        ("Kristina Barta Quartet", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-21/kristina-barta-quartet/9355497"),
        ("Marie TILŠAROVÁ", "20:00", "Buena Vista Club", "Plzeň", "https://www.buenavistaclub.cz/program-klubu.aspx"),
    ],
    22: [  # Pondělí
        ("Ben Cristovao, Sofian Medjmedj – Khaosan & Denpasar show", "20:00", "O2 Universum", "Praha", "https://www.o2universum.cz/en/events/ben-cristovao-sofian-medjmedj-khaosan-denpasar-show-en/"),
        ("Eva Urbanová & Miroslav Donutil", "19:00", "Lucerna Velký sál", "Praha", "https://www.lucpra.com/index.php/cz/programs/eventdetail/1035/spolecne-a-vanocne-eva-urbanova-miroslav-donutil"),
        ("PAVEL SEDLÁČEK & CADILLAC", "19:30", "Vagon", "Praha", "http://www.cadillacband.cz/Cadillac/Home.html"),
    ],
    23: [  # Úterý
        ("Eva Urbanová & Miroslav Donutil", "19:00", "Lucerna Velký sál", "Praha", "https://www.lucpra.com/index.php/cz/programs/eventdetail/1036/spolecne-a-vanocne-eva-urbanova-miroslav-donutil"),
    ],
    25: [  # Čtvrtek (Vánoce)
        ("HOLLY BASS", "22:00", "Cross Club", "Praha", "https://www.crossclub.cz/cs/program/8346-holly-bass/"),
        ("V3Ska – Boží Hot party vol. 14", "20:00", "Divadlo Pod lampou", "Plzeň", "https://podlampou.cz/events/v3ska-5/"),
    ],
    26: [  # Pátek
        ("Pop 80's & 90's video party", "21:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/pop-80s-90s-video-party-dj-jirka-neumann-870/"),
        ("METALLICA CZECH TRIBUTE BAND", "21:00", "Vagon", "Praha", "https://www.facebook.com/profile.php?id=61576334550722"),
        ("DRUM & BELLS w/ MC COPPA & 5HA5H", "22:00", "Cross Club", "Praha", "https://www.crossclub.cz/cs/program/8344-drum-bells-w-mc-coppa-5ha5h/"),
    ],
    27: [  # Sobota
        ("Pop 80's & 90's video party", "21:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/pop-80s-90s-video-party-dj-jirka-neumann-871/"),
        ("NIRVANA Revival Praha", "21:00", "Vagon", "Praha", "https://www.facebook.com/nirvanapraha"),
        ("COCO CROSS", "22:00", "Cross Club", "Praha", "https://www.crossclub.cz/cs/program/8345-coco-cross/"),
        ("Groove It", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-27/groove-it/9423137"),
        ("Tony Rocky Horror Vinyl Show Xmas special vol.4", "20:00", "Divadlo Pod lampou", "Plzeň", "https://podlampou.cz/events/danzhun/"),
        ("BRUTUS", "20:00", "Šeříkovka", "Plzeň", "https://www.serikovka.cz/koncerty/77-27-12-2025-brutus"),
    ],
    28: [  # Neděle
        ("Kamil Střihavka & The Leaders! + Petr Janda", "19:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/kamil-strihavka-the-leaders-8/"),
        ("U2 Revival.cz", "21:00", "Vagon", "Praha", "https://www.u2-revival.cz"),
        ("Unissono Groove & Patricie", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-28/unissono-groove-patricie/9423139"),
    ],
    29: [  # Pondělí
        ("The Universe of John Williams", "19:00", "O2 Universum", "Praha", "https://www.o2universum.cz/en/events/the-universe-of-john-williams-2025-en/"),
        ("VELVET UNDERGROUND REVIVAL BAND", "21:00", "Vagon", "Praha", "http://www.youtube.com/watch?v=2sOketWSny4"),
        ("Duende", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-29/duende/9303032"),
    ],
    30: [  # Úterý
        ("BOX Lucerna", "18:00", "Lucerna Velký sál", "Praha", "https://www.lucpra.com/index.php/cz/programs/eventdetail/1040/box-lucerna"),
        ("TONY DUCHÁČEK & GARAGE", "21:00", "Vagon", "Praha", "https://www.facebook.com/garagetonyduchacek"),
        ("Bio Trio", "20:00", "U Staré Paní", "Praha", "https://ustarepani.club/en/2025-12-30/bio-trio/9415862"),
        ("TURBO", "20:00", "Šeříkovka", "Plzeň", "https://www.serikovka.cz/koncerty/76-30-12-2025-turbo"),
    ],
    31: [  # Středa (Silvestr)
        ("New Year's Eve 2025: Gold Rush", "22:00", "Roxy", "Praha", "https://goout.net/cs/listky/new-year-s-eve-2025-gold-rush/jhqib/"),
        ("Silvestrovská Pop 80's & 90's", "21:00", "Lucerna Music Bar", "Praha", "https://musicbar.cz/en/program/silvestrovska-pop-80s-90s-video-party-dj-jirka-neumann-9/"),
        ("PROFESSOR (New Year's Eve)", "21:00", "Vagon", "Praha", "http://www.imagine.cz/"),
    ],
}

# Day names in Czech
day_names = {
    0: "Pondělí", 1: "Úterý", 2: "Středa", 3: "Čtvrtek",
    4: "Pátek", 5: "Sobota", 6: "Neděle"
}

def get_day_name(day):
    """Get Czech day name for December 2025."""
    date = datetime(2025, 12, day)
    return day_names[date.weekday()]

def generate_html():
    """Generate the HTML file."""

    total_events = sum(len(events) for events in events_data.values())

    html_content = f'''<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Program koncertů - Prosinec 2025</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #1a5f2a 0%, #c41e3a 100%);
            min-height: 100vh;
        }}

        .container {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}

        h1 {{
            text-align: center;
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #1a5f2a 0%, #c41e3a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .stats {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}

        .date-section {{
            background: #f8f9fa;
            margin: 20px 0;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .date-section:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        }}

        .date-header {{
            font-size: 1.4em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 3px solid;
            border-image: linear-gradient(90deg, #1a5f2a 0%, #c41e3a 100%) 1;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .event-count {{
            font-size: 0.7em;
            color: #7f8c8d;
            font-weight: normal;
        }}

        .event {{
            margin: 15px 0;
            padding: 15px;
            background: white;
            border-left: 5px solid #1a5f2a;
            border-radius: 8px;
            transition: all 0.2s;
        }}

        .event:hover {{
            border-left-color: #c41e3a;
            transform: translateX(5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}

        .event-name {{
            font-weight: 600;
            color: #2c3e50;
            font-size: 1.1em;
            margin-bottom: 8px;
        }}

        .event-details {{
            color: #555;
            font-size: 0.95em;
            line-height: 1.6;
        }}

        .venue {{
            color: #e74c3c;
            font-weight: 500;
        }}

        .city {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            margin-left: 10px;
            font-weight: 500;
        }}

        .praha {{
            background: linear-gradient(135deg, #1a5f2a 0%, #2d8f4e 100%);
            color: white;
        }}

        .plzen {{
            background: linear-gradient(135deg, #c41e3a 0%, #e74c3c 100%);
            color: white;
        }}

        .time {{
            color: #16a085;
            font-weight: 600;
            font-size: 1.05em;
        }}

        .sold-out {{
            display: inline-block;
            background: #e74c3c;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            margin-left: 8px;
        }}

        a {{
            color: #1a5f2a;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }}

        a:hover {{
            color: #c41e3a;
            text-decoration: underline;
        }}

        .filter-bar {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .filter-bar label {{
            font-weight: 600;
            color: #2c3e50;
        }}

        .filter-bar select, .filter-bar input {{
            padding: 8px 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.2s;
        }}

        .filter-bar select:focus, .filter-bar input:focus {{
            outline: none;
            border-color: #1a5f2a;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            .container {{
                padding: 15px;
            }}

            h1 {{
                font-size: 1.8em;
            }}

            .date-header {{
                font-size: 1.2em;
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎄 Program koncertů - Prosinec 2025</h1>
        <div class="stats">{total_events}+ koncertů | 18 klubů | Praha & Plzeň</div>

        <div class="filter-bar">
            <label>Filtr:</label>
            <select id="cityFilter">
                <option value="all">Všechna města</option>
                <option value="praha">Praha</option>
                <option value="plzen">Plzeň</option>
            </select>
            <input type="text" id="searchInput" placeholder="Hledat umělce nebo klub...">
        </div>

'''

    # Generate events for each day
    for day in sorted(events_data.keys()):
        events = events_data[day]
        day_name = get_day_name(day)

        html_content += f'''        <div class="date-section">
            <div class="date-header">
                <span>{day_name} {day}. prosince 2025</span>
                <span class="event-count">{len(events)} akcí</span>
            </div>
'''

        for event in events:
            name = html.escape(event[0])
            time = event[1]
            venue = html.escape(event[2])
            city = event[3]
            url = event[4]
            sold_out = len(event) > 5 and event[5] == "VYPRODÁNO"

            city_class = "praha" if city == "Praha" else "plzen"
            sold_out_tag = ' <span class="sold-out">VYPRODÁNO</span>' if sold_out else ''

            time_str = f'<span class="time">{time}</span> | ' if time else ''

            html_content += f'''            <div class="event">
                <div class="event-name">{name}{sold_out_tag}</div>
                <div class="event-details">
                    {time_str}<span class="venue">{venue}</span><span class="city {city_class}">{city}</span><br>
                    <a href="{url}" target="_blank">Více informací</a>
                </div>
            </div>
'''

        html_content += '''        </div>

'''

    html_content += '''    </div>

    <script>
        document.getElementById('cityFilter').addEventListener('change', function(e) {
            const city = e.target.value;
            const events = document.querySelectorAll('.event');

            events.forEach(event => {
                if (city === 'all') {
                    event.style.display = 'block';
                } else {
                    const hasCity = event.querySelector('.city.' + city);
                    event.style.display = hasCity ? 'block' : 'none';
                }
            });
        });

        document.getElementById('searchInput').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const events = document.querySelectorAll('.event');

            events.forEach(event => {
                const text = event.textContent.toLowerCase();
                event.style.display = text.includes(searchTerm) ? 'block' : 'none';
            });
        });
    </script>
</body>
</html>'''

    return html_content

if __name__ == "__main__":
    html_output = generate_html()
    with open("program_prosinec_2025.html", "w", encoding="utf-8") as f:
        f.write(html_output)
    print(f"Generated program_prosinec_2025.html")
