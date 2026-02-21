"""
WebFetch Data Storage
====================
Manually collected WebFetch results for JavaScript-heavy sites.

To update:
1. Use Claude Code WebFetch tool on venue URL
2. Copy the formatted output here
3. Run scrape_concerts.py to parse all venues
"""

# Rock Café - November 2025
ROCK_CAFE_NOV_2025 = """
1. **01.11.2025 | 20:00**
   Eddie Fresco (M) + support: DJ Starvin Marvin
   https://rockcafe.cz/en/program/eddie-fresco-m-support-dj-starvin-marvin/

2. **02.11.2025 | 19:00** [CANCELED]
   Lonely Spring (DE) + support
   https://rockcafe.cz/en/program/lonely-spring-de-support/

3. **04.11.2025 | 20:00**
   Pavel Čadek a Úcellová skupina – KŘEST ALBA CELLEM VPŘED
   https://rockcafe.cz/en/program/pavel-cadek-a-ucellova-skupina-krest-alba-cellem-vpred/

4. **05.11.2025 | 20:00**
   Fource presents: Marc Scibilia (USA)
   https://rockcafe.cz/en/program/fource-presents-marc-scibilia-usa/

5. **06.11.2025 | 18:30**
   Prague Music Week 2025: Rat Boy (UK), Venus Grrrls (UK), Tracy De Sa (FR) + others
   https://rockcafe.cz/en/program/prague-music-week-2025-rat-boy-uk-venus-grrrls-uk-tracy-de-sa-fr-a-dalsi/

6. **07.11.2025 | 18:30**
   Prague Music Week 2025: Slow Crush (BE), Ebbb (UK), Vianova (DE) + others
   https://rockcafe.cz/en/program/prague-music-week-2025-slow-crush-be-ebbb-uk-vianova-de-a-dalsi/

7. **08.11.2025 | 20:00** [MOVED]
   Fource presents: Everything Everything (UK)
   https://rockcafe.cz/en/program/fource-presents-everything-everything-uk/

8. **11.11.2025 | 20:00**
   Live Nation presents: Sadie Jean (USA)
   https://rockcafe.cz/en/program/live-nation-presents-sadie-jean-usa/

9. **14.11.2025 | 20:00**
   Fource presents: Modestep (UK) + support: Akira
   https://rockcafe.cz/en/program/fource-presents-modestep-uk/

10. **15.11.2025 | 19:00**
    Rock for People presents: Deafheaven (USA), Portrayal of Guilt (USA), Zeruel (USA)
    https://rockcafe.cz/en/program/rock-for-people-presents-deafheaven-usa-portrayal-of-guilt-usa-zeruel-usa/

11. **17.11.2025 | 14:30**
    Korzo Národní: Osobnost Plus naživo
    https://rockcafe.cz/en/program/korzo-narodni-osobnost-plus-nazivo/

12. **18.11.2025 | 20:00**
    My Ugly Clementine (AT) + support
    https://rockcafe.cz/en/program/my-ugly-clementine-at-support/

13. **19.11.2025 | 20:00**
    Vasilův Rubáč a Kohout Plaší Smrt
    https://rockcafe.cz/en/program/vasiluv-rubac-a-kohout-plasi-smrt/

14. **20.11.2025 | 20:00**
    Fource presents: ROYA (DK)
    https://rockcafe.cz/en/program/fource-presents-roya-dk/

15. **21.11.2025 | 19:00**
    Ikkimel (DE)
    https://rockcafe.cz/en/program/ikkimel-de/

16. **22.11.2025 | 19:30**
    D Smack U presents: Sophie and the Giants (UK)
    https://rockcafe.cz/en/program/d-smack-u-presents-sophie-and-the-giants-uk/

17. **23.11.2025 | 19:00**
    Austin Giorgio (USA)
    https://rockcafe.cz/en/program/austin-giorgio-usa/

18. **24.11.2025 | 20:00**
    DRUHEJ PLÁN ve zhovadilých časech: Proč bychom se netěšili
    https://rockcafe.cz/en/program/druhej-plan-ve-zhovadilych-casech-proc-bychom-se-netesili/

19. **25.11.2025 | 20:00**
    Chiki Liki Tu-a (SK) + guest: B.D.H.S. (SK)
    https://rockcafe.cz/en/program/chiki-liki-tu-a-sk-2/

20. **26.11.2025 | 19:00**
    Obscure presents: MONO (JAP) + support: Delfíni v brnění (CZ)
    https://rockcafe.cz/en/program/obscure-presents-mono-jap/

21. **27.11.2025 | 20:25**
    PLEXISovjanka + special guest: Just Wär
    https://rockcafe.cz/en/program/plexisovjanka-special-guest-just-war/

22. **28.11.2025 | 20:00**
    POST-IT
    https://rockcafe.cz/en/program/post-it/

23. **29.11.2025 | 20:00**
    Live Nation presents: MICO (CAN)
    https://rockcafe.cz/en/program/live-nation-presents-mico-can/
"""


def get_webfetch_data(venue_name: str, month: int, year: int) -> str:
    """
    Get WebFetch data for a venue

    Args:
        venue_name: Name of the venue
        month: Month number
        year: Year

    Returns:
        WebFetch data string or empty string if not available
    """
    if venue_name == "Rock Café" and month == 11 and year == 2025:
        return ROCK_CAFE_NOV_2025

    # Add more venues here

    return ""
