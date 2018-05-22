import pandas as pd
import requests as r
import json
from sqlalchemy import create_engine, inspect, Table, Column
import numpy as np
import asyncio
import sys
import math as m
from aiohttp import ClientSession, TCPConnector, BasicAuth
from ilxutils.args_reader import read_args
from collections import defaultdict, namedtuple
import ilxutils.dictlib as dictlib
from ilxutils.interlex_sql import interlex_sql
from pathlib import Path as p

'''
Get functions need a list of term ids
Post functions need a list of dictionaries with their needed/optional keys & values

identifierSearches          (identifierSearches(self, ids=None, HELP=False, LIMIT=50)
updateTerms                 (self, data, HELP=False, LIMIT=50, sql=False)
addTerms                    (self, data, HELP=False, LIMIT=50, sql=False)
addAnnotations              (self, data, HELP=False, LIMIT=50, sql=False)
getAnnotations_via_tid      (self, tids, HELP=False, LIMIT=50)
getAnnotations_via_id       (self, annotation_ids, HELP=False, LIMIT=50)
updateAnntationValues       (self, data, HELP=False, LIMIT=50)
updateAnntationType         (self, data, HELP=False, LIMIT=50)
deleteAnnotations           (self, annotation_ids, HELP=False, LIMIT=50)
addRelationship             (self, data, HELP=False, LIMIT=50)
'''
class scicrunch():

    def __init__(self, api_key, base_path, db_url, auth=('None','None')):
        self.key = api_key
        self.base_path = base_path
        self.auth = BasicAuth(auth)
        self.sql = interlex_sql(db_url=db_url)

    def crawl_get(self, urls):
        outputs = {}
        for url in urls:
            auth = ('scicrunch', 'perl22(query)') # needed for test2.scicrunch.org
            headers = {'Content-type': 'application/json'}
            req = r.get(url, headers=headers, auth=auth)

            if req.raise_for_status():
                print(url.split('?key=')[0]); sys.exit(req)
            try: #sometimes will return an odd error not from the servers list
                output = req.json()['data']
            except:
                print(req.text); sys.exit('Failed to convert to json')
            if output.get('errormsg'): #error from the servers list
                print(url.split('?key=')[0]); sys.exit(output['errormsg'])
            try:
                output={int(output['id']):output} #terms
            except:
                output={int(output[0]['tid']):output} #annotations
            outputs.update(output)
        return outputs

    def crawl_post(self, total_data, _print, debug):
        outputs = []
        for i, tupdata in enumerate(total_data):
            url, data = tupdata
            params = {**{'key':self.key}, **data} #**{'batch-elastic':'True'}}
            auth = ('scicrunch', 'perl22(query)') # needed for test2.scicrunch.org
            headers = {'Content-type': 'application/json'}
            req = r.post(url, data=json.dumps(params), headers=headers, auth=auth)

            if req.raise_for_status():
                print(data); sys.exit(req.text)
            try:
                output = req.json()
            except:
                print(req.text); sys.exit('Could not convert to json')
            if output['data'].get('errormsg'):
                print(data); sys.exit(output['data']['errormsg'])
            if debug:
                return [output]
            output = output['data']
            if _print:
                try:
                    print(i, output['label'])
                except:
                    print(i, output['id'])
            outputs.append(output)
        return outputs

    def get(self, urls, LIMIT=50, action='Getting Info', _print=True, crawl=False, debug=False):
        if crawl:
            return self.crawl_get(urls)

        async def get_single(url, session, auth):
            async with session.get(url) as response:
                if response.status not in [200, 201]:
                    try:
                        output = await response.json()
                    except:
                        output = await response.text()
                    problem = str(output)
                    sys.exit(str(problem)+' with status code ['+str(response.status)+']')
                output = await response.json()
                if debug:
                    return output
                try:
                    try:
                        output={int(output['data']['id']):output['data']} #terms
                    except:
                        output={int(output['data'][0]['tid']):output['data']} #annotations
                except:
                    return {url:None}
                return output

        async def get_all(urls, connector, loop):
            if _print: print('=== {0} ==='.format(action))
            tasks = []
            auth = BasicAuth('scicrunch', 'perl22(query)')
            async with ClientSession(connector=connector, loop=loop, auth=auth) as session:
                for i, url in enumerate(urls):
                    task = asyncio.ensure_future(get_single(url, session, auth))
                    tasks.append(task)
                return (await asyncio.gather(*tasks))

        connector = TCPConnector(limit=LIMIT) # rate limiter; should be between 20 and 80; 100 maxed out server
        loop = asyncio.get_event_loop() # event loop initialize
        future = asyncio.ensure_future(get_all(urls, connector, loop)) # tasks to do; data is in json format [{},]
        outputs = loop.run_until_complete(future) # loop until done
        return {k:v for keyval in outputs for k, v in keyval.items()}

    def post(self, data, LIMIT=50, action='Pushing Info', _print=True, crawl=False, debug=False):
        if crawl:
            return self.crawl_post(data, _print=_print, debug=debug)

        async def post_single(url, data, session, i):
            params = {**{'key':self.key}, **data} #**{'batch-elastic':'True'}}
            headers = {'Content-type': 'application/json'}
            async with session.post(url, data=json.dumps(params), headers=headers) as response:

                """ While using post for ilx/add """

                post_ilx = await response.json()
                limit = 0 #BUG; server needs to breath sometimes while generating ilx ids
                while post_ilx.get('errormsg') == 'could not generate ILX identifier' and limit < 100:
                    async with session.post(url, data=json.dumps(params), headers=headers) as response:
                        post_ilx = await response.json()
                        limit+=1

                if response.status not in [200, 201]:
                    try:
                        output = await response.json()
                    except:
                        output = await response.text()
                    problem = str(output)
                    sys.exit(str(problem)+' with status code ['+str(response.status)+'] with params:'+str(params))
                output = await response.json()
                if debug:
                    return output
                if _print:
                    try:
                        print(i, output['data']['label'])
                    except:
                        print(i, output['data'])
                return output['data']

        async def post_all(total_data, connector, loop):
            tasks = []
            auth = BasicAuth('scicrunch', 'perl22(query)')
            async with ClientSession(connector=connector, loop=loop, auth=auth) as session:
                if _print:
                    print('=== {0} ==='.format(action))
                for i, tupdata in enumerate(total_data):
                    url, data = tupdata
                    task = asyncio.ensure_future(post_single(url, data, session, i)) #FIXME had to copy to give new address
                    tasks.append(task)
                return (await asyncio.gather(*tasks))

        connector = TCPConnector(limit=LIMIT) # rate limiter; should be between 20 and 80; 100 maxed out server
        loop = asyncio.get_event_loop() # event loop initialize
        future = asyncio.ensure_future(post_all(data, connector, loop)) # tasks to do; data is in json format [{},]
        outputs = loop.run_until_complete(future) # loop until done
        return outputs

    def identifierSearches(self, ids=None, LIMIT=50, _print=True, crawl=False, debug=False):
        """parameters( data = "list of term_ids" )"""
        url_base = self.base_path + '/api/1/term/view/{id}' + '?key=' + self.key
        urls = [url_base.format(id=str(_id)) for _id in ids]
        return self.get(urls=urls, LIMIT=LIMIT, action='Searching For Terms', _print=_print, debug=debug)

    def updateTerms(self, data, LIMIT=50, _print=True, crawl=False, debug=False):
        """
            need:
                    term           <str>
            options:
                    definition      <str> #bug with qutations
                    superclasses    [{'id':<int>}]
                    type            term, cde, anntation, or relationship <str>
                    synonym         {'literal':<str>}
                    existing_ids    {'iri':<str>,'curie':<str>','change':<bool>, 'delete':<bool>}
        """
        old_data = self.identifierSearches([d['id'] for d in data], _print=_print, crawl=crawl)
        url_base = self.base_path + '/api/1/term/edit/{id}'
        merged_data = []
        for d in data:
            url = url_base.format(id=str(d['id']))
            merged = dictlib.merge(new=d, old=old_data[int(d['id'])])
            merged = dictlib.superclasses_bug_fix(merged) #BUG
            merged_data.append((url, merged))
        return self.post(merged_data, LIMIT=LIMIT, action='Updating Terms', _print=_print, crawl=crawl, debug=debug)

    def addTerms(self, data, LIMIT=50, _print=True, crawl=False, debug=False):
        """
            need:
                    term           <str>
            options:
                    definition      <str> #bug with qutations
                    superclasses    [{'id':<int>}]
                    type            term, cde, anntation, or relationship <str>
                    synonym         {'literal':<str>}
                    existing_ids    {'iri':<str>,'curie':<str>','change':<bool>, 'delete':<bool>}
        """
        url_base = self.base_path + '/api/1/ilx/add'
        terms = []
        for d in data:
            terms.append((url_base, d))
        ilx = self.post(terms, action='Priming Terms', LIMIT=LIMIT, _print=_print, crawl=crawl)
        ilx = {d['term']:d for d in ilx}

        url_base = self.base_path + '/api/1/term/add'
        terms = []
        for d in data:
            d['label'] = d.pop('term')
            d = dictlib.superclasses_bug_fix(d)
            try:
                d.update({'ilx':ilx[d['label']]['ilx']})
            except:
                d.update({'ilx':ilx[d['label']]['fragment']})
            terms.append((url_base, d))

        return self.post(terms, action='Adding Terms', LIMIT=LIMIT, _print=_print, crawl=crawl, debug=debug)

    def addAnnotations(self, data, LIMIT=50, _print=True, crawl=False, debug=False):
        """{'tid':'', 'annotation_tid':'', 'value':''}"""
        url_base = self.base_path + '/api/1/term/add-annotation'
        annotations = []
        for annotation in data:
            annotation.update({
                'term_version':'1',
                'annotation_term_version':'1',
                'batch-elastic':'True',
            })
            annotations.append((url_base, annotation))
        return self.post(annotations, LIMIT=LIMIT, action='Adding Annotations', _print=_print, crawl=crawl, debug=debug)

    def getAnnotations_via_tid(self, tids, LIMIT=50, _print=True, crawl=False, debug=False):
        """tids = list of strings or ints that are the ids of the terms that possess the annoations"""
        url_base = self.base_path + '/api/1/term/get-annotations/{tid}?key=' + self.key
        urls = [url_base.format(tid=str(tid)) for tid in tids]
        return self.get(urls, LIMIT=LIMIT, _print=_print, crawl=crawl, debug=debug)

    def getAnnotations_via_id(self, annotation_ids, LIMIT=50, _print=True, crawl=False, debug=False):
        """tids = list of strings or ints that are the ids of the annotations themselves"""
        url_base = self.base_path + '/api/1/term/get-annotation/{id}?key=' + self.key
        urls = [url_base.format(id=str(annotation_id)) for annotation_id in annotation_ids]
        return self.get(urls, LIMIT=LIMIT, _print=_print, crawl=crawl, debug=debug)

    def updateAnnotations(self, data, LIMIT=50, _print=True, crawl=False, debug=False):
        """data = list of dict {"tid","annotation_tid","value"}"""
        url_base = self.base_path + '/api/1/term/edit-annotation/{id}' # id of annotation not term id
        annotations = self.getAnnotations_via_id([d['id'] for d in data], _print=_print, crawl=crawl)
        annotations_to_update = []
        for d in data:
            annotation = annotations[int(d['id'])]
            annotation.update({**d})
            url = url_base.format(id=annotation['id'])
            annotations_to_update.append((url, annotation))
        self.post(annotations_to_update, LIMIT=LIMIT, _print=_print, crawl=crawl, debug=debug)

    def deleteAnnotations(self, annotation_ids, LIMIT=50,  _print=True, crawl=False, debug=False):
        """data = list of tids"""
        url_base = self.base_path + '/api/1/term/edit-annotation/{annotation_id}' # id of annotation not term id; thx past troy!
        annotations = self.getAnnotations_via_id(annotation_ids,  _print=_print, crawl=crawl)
        annotations_to_delete = []
        for annotation_id in annotation_ids:
            annotation = annotations[int(annotation_id)]
            params = {
                'value':' ', #for delete
                'annotation_tid':' ', #for delete
                'tid':' ', #for delete
                'term_version':'1',
                'annotation_term_version':'1',
            }
            url = url_base.format(annotation_id=annotation_id)
            annotation.update({**params})
            annotations_to_delete.append((url, annotation))
        self.post(annotations_to_delete, LIMIT=LIMIT, _print=_print, crawl=crawl, debug=debug)

    def addRelationship(self, data, HELP=False, LIMIT=50,  _print=True, crawl=False, debug=False):
        """data = [{"term_1_id", "term_2_id", "relationship_tid"}]"""
        url_base = self.base_path + '/api/1/term/add-relationship'
        relationships = []
        for relationship in data:
            relationship.update({
                'term1_version':'1',
                'term2_version':'1',
                'relationship_term_version':'1'
            })
            relationships.append((url_base, relationship))
        return self.post(relationships, LIMIT=LIMIT, action='Adding Relationships', _print=True, crawl=False, debug=False)

    def deleteTerms(self, ilx_ids, LIMIT=50, _print=True, crawl=True):
        """ilx_ids = list of interlex ids."""
        url = self.base_path + '/api/1/term/elastic/delete/{ilx_id}?key=' + self.key
        data = [(url.format(ilx_id=str(ilx_id)), {}) for ilx_id in ilx_ids]
        return self.post(data, LIMIT=LIMIT,  _print=_print, crawl=crawl)

def main():
    #args = read_args(api_key= p.home() / 'keys/beta_api_scicrunch_key.txt', db_url= p.home() / 'keys/beta_engine_scicrunch_key.txt', beta=True)
    args = read_args(api_key= p.home() / 'keys/production_api_scicrunch_key.txt', db_url= p.home() / 'keys/production_engine_scicrunch_key.txt', production=True)
    sql = interlex_sql(db_url=args.db_url)
    sci = scicrunch(api_key=args.api_key, base_path=args.base_path, db_url=args.db_url)
    #example term is troysincomb 38918 tmp_0138415
    #https://test2.scicrunch.org/scicrunch/interlex/view/tmp_0138415?searchTerm=troysincomb
    #https://test2.scicrunch.org/api/1/ilx/search/identifier/tmp_0138415?key=

    annotations_to_delete = [2109347, 2109346, 2109348, 2109349,   48685,   48689,   48690,
         48693,   48695,   48697,   48698,   48688,   48687,   48691,
         48686,   48694,   48692,   48696,   48699]

    terms = [{
        #'term':'troysincomb',
        'id':38918,
        'existing_ids':[{
            'tid':38918,
            'curie':'ILX:0003',
            'iri':'http://t3db.org/toxins/T3D0002',
            'preferred':0,
            'change':False
        }],
        'definition':'employee',
        'synonyms':[{'literal':'trenton'}],
        'superclasses': [{
            'id': '146',
            #'ilx': 'tmp_0100145',
            #'label': 'A1 neuron',
            #'definition': 'Any abdominal neuron (FBbt_00001987) that is part of some larval abdominal segment 1 (FBbt_00001748).',
            #'status': '0'
        }],
    }]
    #annotations = [{'tid':38918,'annotation_tid':15034,'value':'testvaluess'}]
    #sci.addTerms(terms)
    #annotations = sci.getAnnotations([38918])
    #terms = json.load(open('../test.json', 'r'))
    #terms = sci.addTerms(terms, sql=False, _print=False)
    #sci.updateAnntationValues(annotations)
    #print(terms)
    #json.dump(terms, open('../elastic_testing.json', 'w'), indent=4)
    #sci.deleteAnnotations([annotations_to_delete[0]], crawl=True)
    sci.deleteAnnotations(annotations_to_delete)
    #output = sci.getAnnotations_via_id([2109347], crawl=True)
    #print(output)

if __name__ == '__main__':
    main()
