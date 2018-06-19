import scrapy


class TouristAttractionSpider(scrapy.Spider):
    name = "tourist_attraction"

    start_urls=['http://www.srilanka.travel/tourist-attractions?page=1']

    for i in range(1, 16):
        start_urls.append("http://www.srilanka.travel/tourist-attractions?page=" + str(i))

    def parse(self, response):
        for place in response.css('body > div.lt-attrs-wpouter > div > div > div.lt-attr-places.clearfix > div'):
            article= place.css('div>div');
            href=article.css('a::attr(href)')[0];

            yield response.follow(href, self.parsePage)

    def parsePage(self,response):
        # x='12'
        title=response.css('html body div.lt-attrs-wpouter div.lt-attrs-wpinner.container div.lt-attrs.clearfix div.lt-attr-content.pull-left div.lt-attr-info.place h1::text').extract_first()

        town=title.split('|')[0].strip();
        place=title.split('|')[1].strip();

        paragraphs=response.css('html body div.lt-attrs-wpouter div.lt-attrs-wpinner.container div.lt-attrs.clearfix div.lt-attr-content.pull-left div.lt-attr-info.place div p::text').extract();

        paragraph_text='';

        for para in paragraphs:
            paragraph_text+=para;

        replace_text=['\n','\r','\t','\xa0'];

        for t in replace_text:
            paragraph_text=paragraph_text.replace(t,'')

        yield {
            'town':town,
            'place':place,
            'description':paragraph_text
        }



