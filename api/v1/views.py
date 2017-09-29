# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
#from django.views.decorators.csrf import csrf_exempt
#from django.db import IntegrityError, transaction
#from django.db.models import Q
#from django.utils.datastructures import MultiValueDictKeyError
#from django.core import serializers

import json
import urllib2
import re

from api.models import LegoProduct, LegoProductImage, LegoProductSku

class ItemNotFoundException(Exception):
    pass

def _make_request(url):
    request = urllib2.Request(url)
    #request.add_header('User-Agent', 'LegoSrchBot/1.0 +http://iizs.net/legosrch')
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    return request

def _get_from_lego_dot_com(opener, num):
    request = _make_request('https://sp1004f1fe.guided.ss-omtrdc.net/?do=json-db&callback=json&count=18&q={query}&cc=us&lang=en&jsonp=jsonCallback'.format(query=num))

    # If Referer omitted, result does not comes out.
    request.add_header('Referer', 'https://search2.lego.com/en-US/{query}'.format(query=num))

    body = opener.open(request).read()

    # removes "jsonCallback( .. )"
    # request url에서 jsonp=jsonCallback query parameter를 제거해도 같은 효과이지만, 웹 페이지에서 부르는 것와 패턴을 맞추기 위해서 살려둠
    body = re.sub( ' \)', '', re.sub( 'jsonCallback\(', '', body), re.M )

    srch_result = json.loads(body)

    # TODO: make resp dict more reliable, reusable
    resp = []
    for i in srch_result['results']:
        if i['product_code'] == num:
            d = {}
            d['product_id'] = i['seo_path']     # seems to be a nomalized ascii name
            d['title'] = i['name_html'] # contains special characters
            d['image'] = [ i['media'] ]
            d['product_code'] = i['product_code']
            d['piece_count'] = i['piece_count']
            d['skus'] = []
            for l in i['skus']:
                s = {}
                s['sku_number'] = l['sku_number']
                s['price'] = l['list_price']   # can be null
                #s['list_price_formatted'] = l['list_price_formatted']
                s['site'] = 'lego.com (US)'
                s['shop_url'] = 'https://shop.lego.com/en-US/{seo_id}'.format(seo_id=d['product_id'])
                s['currency'] = srch_result['currency_code']
                d['skus'].append(s)
            resp.append(d)
    return resp

def _get_from_db(num):
    result = LegoProduct.objects.filter(product_code = num)

    if len(result) == 0:
        return None

    resp = []
    for i in result:
        d = {}
        d['product_id'] = i.product_id
        d['title'] = i.title
        d['product_code'] = str(i.product_code)
        d['piece_count'] = i.piece_count
        d['datetime_updated'] = str(i.datetime_updated)
        d['image'] = []
        images = LegoProductImage.objects.filter( lego_product = i )
        for img in images:
            d['image'].append( img.img_url )
        d['skus'] = []
        skus = LegoProductSku.objects.filter( lego_product = i )
        for sku in skus:
            s = {}
            s['sku_number'] = sku.sku_number
            s['price'] = sku.price
            #s['list_price_formatted'] = l['list_price_formatted']
            s['shop_url'] = sku.product_url
            s['currency'] = sku.currency
            s['site'] = sku.site
            d['skus'].append(s)
        resp.append(d)
    
    return resp

def _put_to_db(num, items):
    for i in items:
        product = LegoProduct(
            product_id = i['product_id'],
            title = i['title'],
            product_code = i['product_code'],
            piece_count = i['piece_count'],
        )
        product.save()

        for img in i['image']:
            image = LegoProductImage(
                lego_product = product,
                img_url = img,
            )
            image.save()

        for s in i['skus']:
            sku = LegoProductSku(
                lego_product = product,
                site = s['site'],
                sku_number = s['sku_number'],
                price = s['price'],
                currency = s['currency'],
                product_url = s['shop_url'],
            )
            sku.save()
    return

def item_number(request, num):
    resp = {}
    resp['item_number'] = num

    resp['items'] = _get_from_db(num)
    if resp['items'] == None:
        opener = urllib2.build_opener()
        try:
            resp['items'] = _get_from_lego_dot_com(opener, num)
            _put_to_db(num, resp['items'])
        except (KeyError, ItemNotFoundException) as e:
            print e
            resp['items'] = []
        except Exception as e:
            # XXX: logging required
            print e
            resp['items'] = []

    return HttpResponse(json.dumps(resp, indent=2), content_type="application/json")
