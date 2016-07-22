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

#def make_request(url):
    #request = urllib2.Request(url)
    #request.add_header('User-Agent', 'LegoSrchBot/1.0 +http://iizs.net/legosrch')

def item_number(request, num):
    resp = {}
    resp['item_number'] = num
    #opener = urllib2.build_opener()
    #body = opener.open(request).read()
    return HttpResponse(json.dumps(resp, indent=2), content_type="application/json")
