import scrapy

class TicketsSpider(scrapy.Spider):
  name = "tickets"
  start_urls = [
    'http://www.atgtickets.com/shows/bloc-productions-presents-chitty-chitty-bang-bang/bristol-hippodrome/'
  ]
  download_delay = 1
  
  def parse(self, response):
    for i, show_href in enumerate(response.xpath('//a[text()="Buy Tickets"]/@href').extract()):
      yield response.follow(show_href, meta={'cookiejar': i}, callback=self.parse_show)

  def parse_show(self, response):
    for section in response.css('div.item-box-item-details select.form-control').xpath('//option/@value').extract():
      yield scrapy.FormRequest.from_response(
        response,
        formdata={'BOset::WSmap::seatmap::screen_id' : section},
        meta={'cookiejar': response.meta['cookiejar']},
        callback=self.parse_seats,
        formname='mapSelect'
      )

  def parse_seats(self, response):
    total_seats = len(response.css('div#svg_map_section_inner svg g#seatGroup circle'))
    unavailable_seats = len(response.css('div#svg_map_section_inner svg g#seatGroup circle[data-status="U"]'))
    yield {
      "show": response.css('span.performance-date::text').extract_first(),
      "seat_block": response.css('div.item-box-item-details select.form-control option:checked::text').extract_first(),
      "total_seats": total_seats,
      "available_seats": total_seats - unavailable_seats,
      "sold_seats": unavailable_seats,
      "proportion_sold": unavailable_seats / total_seats
    }
