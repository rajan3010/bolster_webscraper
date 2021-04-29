from playwright.sync_api import sync_playwright
import socket
#Stage 2
from ipwhois.net import Net
from ipwhois.asn import IPASN
from pprint import pprint
import ssl, socket

class Solution:
    def __init__(self, url):
        #1.a
        self.user_given_url = url
        self.is_https = None
        self.domain_name = None
        #1.b
        self.ip_address = None
        #1.c
        self.is_redirected = None
        self.source_url = None
        self.destination_url = None

        #2.a
        self.asn_result = {}
        #2.b
        self.cert_subject = {}
        self.cert_issuer = {}

        #2.c
        self.source_html = None
        self.source_text = []

        self.strip_url()

    def debug(self):
        print("given URL: ",self.user_given_url)
        print("is https: ",self.is_https)
        print("domain name: ",self.domain_name)
        print("ip address: ",self.ip_address)

    def strip_url(self):
        if "https" in self.user_given_url:
            self.is_https = True
        else:
            self.is_https = False
        
        ping_this = (self.user_given_url.split("://")[1]).split('/')[0]
        ping_this = ping_this.strip('/')
        if 'www.' not in ping_this:
            ping_this = "www."+ping_this
        self.domain_name = ping_this

    def take_screenshot(self, filename):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(self.user_given_url)
            page.screenshot(path=filename)
            browser.close()

    def extract_ip(self):
        self.ip_address = socket.gethostbyname(self.domain_name)
    
    def find_redirected(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            response = page.goto(self.user_given_url)
            if response.request.redirected_from and not response.request.redirected_from.redirected_to.url == self.user_given_url:
                self.source_url = self.user_given_url
                self.destination_url = response.url
                self.is_redirected = True
            else:
                self.is_redirected = False
            browser.close()

    def extract_ASN(self):
        net = Net(self.ip_address)
        obj = IPASN(net)
        res = obj.lookup()
        self.asn_result = res
    
    def extract_certifications(self):
        if self.is_https:
            hostname = self.domain_name.split("www.")[1]
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
                s.connect((hostname, 443))
                cert = s.getpeercert()

            subject = dict(x[0] for x in cert['subject'])
            issuer = dict(x[0] for x in cert['issuer'])
            self.cert_issuer = issuer
            self.cert_subject = subject

    def extract_source(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(self.user_given_url)
            page_source = page.inner_html('html')
            source_text_page = page.query_selector_all('p')
            source_text = []
            for s in source_text:
                text = s.inner_text()
                if len(text) > 0:
                    source_text.append(text.strip('\n '))
            self.source_html = page_source
            self.source_text = source_text
            browser.close()

filename = "screenshot.png"
basic_url = "https://google.com"
url = "https://playwright.dev/"
phase1 = Solution(basic_url)
#1.a
#phase1.take_screenshot(filename)
#1.b
phase1.extract_ip()
#1.c
phase1.find_redirected()
#2.a
phase1.extract_ASN()
#2.b
phase1.extract_certifications()
#3.a
phase1.extract_source()
#phase1.debug()