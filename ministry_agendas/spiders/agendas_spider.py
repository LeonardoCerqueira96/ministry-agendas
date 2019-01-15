# Developed by: Leonardo Cesar Cerqueira

import scrapy
import datetime

class AgendasSpider(scrapy.Spider):
    name = "agendas"

    def __init__(self, date_override=None, *args, **kwargs):
        super(AgendasSpider, self).__init__(*args, **kwargs)
        self.date_override = date_override

    def start_requests(self):
        main_url = "http://www.economia.gov.br/Economia/agendas/gabinete-do-ministro/ministro-da-economia-paulo-guedes/"

        date_start = datetime.datetime.strptime("2019-01-01", "%Y-%m-%d")
        
        # Use today's date if not overriden
        if self.date_override:
            date_end = datetime.datetime.strptime(self.date_override, "%Y-%m-%d")
        else:
            date_end = datetime.datetime.today()

        # Adds 1 day to the date end, for use in a range function
        date_end += datetime.timedelta(days=1)

        # Builds the list of urls to check for events
        date_list = [date_start + datetime.timedelta(days=x) for x in range(0, (date_end - date_start).days)]
        url_list = [main_url + datetime.datetime.strftime(date, "%Y-%m-%d") for date in date_list]

        for index, url in enumerate(url_list):
            yield scrapy.Request(url=url, meta={"index": index})

    # Extracts data from the page and builds dict objects for each event of the day
    # Creates an unique id from the timestamp of the event 
    def parse(self, response):
        ministry_name = response.css(".agenda-orgao::text").extract_first().strip()
        minister_name = response.css(".agenda-autoridade::text").extract_first().strip()

        events = response.css(".item-compromisso")
        for event in events:
            event_date = event.css(".comprimisso-inicio::attr(datetime)").extract_first().strip()
            event_date = datetime.datetime.strptime(event_date, "%Y-%m-%d %H:%M")
            
            # Discards the label tag and its contents from the extracted data
            event_title = event.css(".comprimisso-titulo::text").extract_first().strip()
            event_location = event.css(".comprimisso-local").re_first(r"</label>\s*(.*)</p>$").strip()
            
            # Removes traling spaces and '-' characters
            # Removes "Participantes:" and empty strings from the list, if present
            event_participants = event.css(".comprimisso-participantes::text").extract()
            event_participants = [p.strip(" -\r\t") for p in event_participants]
            event_participants = [p for p in event_participants if p and ':' not in p]

            # Builds the dict object
            event_dict = dict()
            event_dict["_id"] = int(event_date.timestamp())
            event_dict["MinistryName"] = ministry_name
            event_dict["MinisterName"] = minister_name
            event_dict["EventDate"] = event_date
            event_dict["EventTitle"] = event_title
            event_dict["EventLocation"] = event_location
            event_dict["EventParticipants"] = event_participants
            
            yield event_dict