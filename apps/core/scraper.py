import scrapy
from scrapy import FormRequest

from .models import Friend, Account


class FriendsLocSpider(scrapy.Spider):

    def __init__(self, *args, **kwargs):
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.name = 'Friends Location Spider'
        self.facebook = 'https://mbasic.facebook.com'
        self.start_urls = [self.facebook]
        super().__init__(*args, **kwargs)

    def clean_url(self, url):
        url = url[:(url.find('?refid'))]
        url = url[:(url.find('&fref'))]
        # url = url[:(url.find('%3Amf'))]
        url = url[:(url.find('?fref'))]
        url = url[:(url.find('?ref'))]
        if url != '':
            if self.facebook in url:
                return url
            else:
                return self.facebook + url
        else:
            return ''

    def get_element(self, element):
        if element == []:
            return ''
        else:
            return element[0]

    def parse(self, response):
        # prompt for username and password, then login
        # email = input('enter email of fb account: ')
        # password = input('enter password: ')
        return FormRequest.from_response(
            response,
            formxpath='//form[contains(@action, "login")]',
            formdata={
                'email': self.email, 'pass': self.password
            },
            callback=self.parse_home
            )

    def parse_home(self, response):
        # goes through the 'save device' part by not saving device
        if response.xpath("//div/a[contains(@href,'save-device')]"):
            self.logger.info('"save-device" checkpoint. redirecting...')
            return FormRequest.from_response(
                response,
                formdata={'name_action_selected': 'dont_save'},
                callback=self.parse_home
            )
        profile_url = self.get_element(response.xpath(
            '//a[contains(text(), "Profile")]/@href').extract())
        friends_url = self.clean_url(profile_url) + '/friends'
        # if "don't save" is selected, go on to profile page
        return scrapy.Request(
            url=friends_url,
            callback=self.parse_profile,
        )

    def parse_profile(self, response):
        profiles = response.xpath(
            '//td[contains(@style, "vertical-align")]/a/@href').extract()
        # go to every profile
        for x in profiles:
            url = self.facebook + x
            yield scrapy.Request(
                url=url,
                callback=self.get_about,
                meta={'profile_url': url},
            )
        # follow link to see more friends
        if response.xpath('//div[contains(@id, "more_friends")]'):
            see_more = self.facebook + self.get_element(response.xpath(
                '//div[contains(@id, "more_friends")]/a/@href'
            ).extract())
            yield scrapy.Request(url=see_more, callback=self.parse_profile)

    def get_about(self, response):
        about_url = self.facebook + self.get_element(response.xpath(
            '//a[contains(text(), "bout")]/@href'
        ).extract())
        yield scrapy.Request(
            url=about_url,
            callback=self.parse_info,
            meta={'profile_url': response.meta.get('profile_url'),}
        )

    def parse_info(self, response):
        url = response.meta.get('profile_url')
        name = self.get_element(response.xpath(
            '//div/span/strong[string-length(@class) = 2]/text()'
        ).extract())
        current_city = self.get_element(response.xpath(
            '//div[contains(@title, "Current City")]//a/text()'
        ).extract())
        hometown = self.get_element(response.xpath(
            '//div[contains(@title, "Hometown")]//a/text()'
        ).extract())
        this_account = Account.objects.get(email=self.email)
        new_friend = Friend(
            name=name, profile_url=url, current_city=current_city,
            hometown=hometown, friend_of=this_account,
        )
        new_friend.save()
