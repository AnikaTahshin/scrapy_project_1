import scrapy


class AMAZON_API(scrapy.Spider):
    name = "amaze"
    start_urls = [
        'https://www.amazon.com/s?i=specialty-aps&bbn=16225009011&rh=n%3A%2116225009011%2Cn%3A172541&ref=nav_em__nav_desktop_sa_intl_headphones_0_2_5_8',
    ]
    def parse(self, response):
        another_page_links = response.css('h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-4 > a')
        yield from response.follow_all(another_page_links, self.parse_next)

        next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator ::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    
    def parse_next(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'brand': extract_with_css('tr.a-spacing-small.po-brand td.a-span9 > span.a-size-base::text'),
            'model': extract_with_css('tr.a-spacing-small.po-model_name td.a-span9 > span.a-size-base::text'),
            'color': extract_with_css('tr.a-spacing-small.po-color td.a-span9 > span.a-size-base::text'),
            'form-factor': extract_with_css('tr.a-spacing-small.po-headphones_form_factor td.a-span9 > span.a-size-base::text'),
            'connectivity': extract_with_css('tr.a-spacing-small.po-connectivity_technology td.a-span9 > span.a-size-base::text'),
            'price' : extract_with_css('span.a-price-whole::text'),
            'rating' : extract_with_css('span.a-icon-alt::text'),
        }

        

















# import scrapy


# class QuotesSpider(scrapy.Spider):
#     name = "amaze"
#     start_urls = [
#         'https://www.amazon.com/s?i=specialty-aps&bbn=16225009011&rh=n%3A%2116225009011%2Cn%3A172541&ref=nav_em__nav_desktop_sa_intl_headphones_0_2_5_8',
#     ]

#     def parse(self, response):
#         for amaze in response.css('div.a-section.a-spacing-base'):
#             yield {
#                 'image': amaze.css('div.a-section.aok-relative.s-image-square-aspect > img::attr(src)').get(),
#                 'title': amaze.css('span.a-size-base-plus.a-color-base.a-text-normal::text').get(),
#                 'rating': amaze.css('span.a-size-base::text').get(),
#                 'price': amaze.css('span.a-price-whole::text').get(),
#                 'reviews': amaze.css('span.a-size-base.s-underline-text::text').get(),
#                 'previous-price': amaze.css('span.a-offscreen::text').get(),
#   }

#         next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator ::attr(href)').get()
#         if next_page is not None:
#             next_page = response.urljoin(next_page)
#             yield scrapy.Request(next_page, callback=self.parse)