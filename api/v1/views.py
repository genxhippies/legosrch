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

class ItemNotFoundException(Exception):
    pass

def _make_request(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'LegoSrchBot/1.0 +http://iizs.net/legosrch')
    return request

def _get_set_info(opener, num):
    request = _make_request('http://lego.wikia.com/api/v1/Articles/List/?category=Sets_by_item_number&limit=100')
    body = opener.open(request).read()

    all_cate = json.loads(body)
    candidate = None
    candidate_match_len = 0
    for i in all_cate['items']:
        set_name = i['title'].lower().replace(' sets', '')
        if len(num) != len(set_name):
            continue
        for j in range(0,len(num)):
            if num[j] != set_name[j]:
                break
        if j > candidate_match_len:
            candidate = i
            candidate_match_len = j

    if candidate == None:
        raise ItemNotFoundException('Unable to guess proper Sets, which contains \'{n}\''.format(n=str(num)) )

    return candidate

def _get_set_list(opener, set_info, limit=100, offset=None):
    url = 'http://lego.wikia.com/api/v1/Articles/List/?category={c}&limit={l}&namespaces=0&{offsetparam}'.format(
        c = set_info['url'].replace('/wiki/Category:', ''),
        l = str(limit),
        offsetparam = 'offset={o}'.format(o=offset) if offset != None else '',
    )
    request = _make_request(url)
    body = opener.open(request).read()
    set_list = json.loads(body)
    return set_list

def _get_from_wikia(opener, num):
    set_info = _get_set_info(opener, num)

    candidates = []
    offset = None
    num_int = int(num)
    # XXX: limit maximum paging to maximum 100 page. 
    # if a set has items more than 100 page, this can be a problem
    for i in range(0,100):
        list_items = _get_set_list(opener, set_info, offset=offset)
        for i in list_items['items']:
            n, remain = i['title'].split(' ', 1)
            try:
                n_int = int(n)
                if n_int == num_int:
                    candidates.append(i)
                elif n_int > num_int:
                    break
            except ValueError:
                # List document does not starts with item number and causes ValueError
                pass
        if 'offset' not in list_items:
            # End of list
            break
        offset=list_items['offset']

    id_list = []
    for c in candidates:
        id_list.append(str(c['id']))
    ids = ','.join(id_list)
    url = 'http://lego.wikia.com/api/v1/Articles/Details/?ids={ids}'.format(
        ids=ids,
    )
    request = _make_request(url)
    body = opener.open(request).read()

    item_details = json.loads(body)

    # convert wikia data to legisrch api response
    resp = []
    for i in item_details['items']:
        d = {}
        d['title'] = item_details['items'][i]['title']
        d['image'] = item_details['items'][i]['thumbnail']
        resp.append(d)

    return resp

def item_number(request, num):
    resp = {}
    resp['item_number'] = num

    opener = urllib2.build_opener()
    try:
        resp['items'] = _get_from_wikia(opener, num)
    except KeyError, ItemNotFoundException:
        resp['items'] = []
    except Exception:
        # XXX: logging required
        resp['items'] = []

    return HttpResponse(json.dumps(resp, indent=2), content_type="application/json")