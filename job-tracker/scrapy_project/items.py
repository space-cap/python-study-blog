import scrapy

class JobPostingItem(scrapy.Item):
    company_name = scrapy.Field()
    job_title = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    applicant_count = scrapy.Field()
    requirements = scrapy.Field()
    preferred_qualifications = scrapy.Field()
    location = scrapy.Field()
    source_url = scrapy.Field()