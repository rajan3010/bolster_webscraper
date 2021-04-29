from flask import Flask
#from pymongo import MongoClient
from flask_restful import Api, Resource, reqparse
from fullstack_ex import Solution

'''cluster=MongoClient('mongodb+srv://ranbazh:SonofGod@3012@cluster0.wzfr6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db=cluster['bolster_app']
collection=db['scraped_info']'''
app= Flask(__name__)
api=Api(app)

class Bolster(Resource):
    def get(self, url):
        #Call the functions from each class and update the resultant json
        
        url="https://"+url
        print(url)
        res={}
        url_obj=Solution(url)
        
        #Currently I am not returning the image in the API but I am just saving it in the local directory
        url_obj.take_screenshot('screenshot.png')
        url_obj.extract_ip()
        url_obj.find_redirected()
        url_obj.extract_ASN()
        url_obj.extract_certifications()
        url_obj.extract_source()

        res['ip']=url_obj.ip_address
        if url_obj.is_redirected:
            res['dst_url']=url_obj.destination_url
        res['src_url']=url_obj.source_url
        res['asn']=url_obj.asn_result
        if url_obj.is_https:
            res['cert']=[url_obj.cert_issuer,url_obj.cert_subject]
        res['src_html']=url_obj.source_html
        res['src_text']=url_obj.source_text

        print(res)
        return res

api.add_resource(Bolster, '/bolster/<string:url>')

if __name__=="__main__":
    app.run(debug=True)