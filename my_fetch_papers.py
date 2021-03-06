"""
Queries arxiv API and downloads papers (the query is a parameter).
The script is intended to enrich an existing database pickle (by default db.p),
so this file will be loaded first, and then new results will be added to it.
"""

import os
import time
import pickle
import random
import argparse
import urllib.request
from  urllib.request import urlopen,Request
import feedparser

from utils import Config, safe_pickle_dump






def encode_feedparser_dict(d):
  """ 
  helper function to get rid of feedparser bs with a deep copy. 
  I hate when libs wrap simple things in their own classes.
  """
  if isinstance(d, feedparser.FeedParserDict) or isinstance(d, dict):
    j = {}
    for k in d.keys():
      j[k] = encode_feedparser_dict(d[k])
    return j
  elif isinstance(d, list):
    l = []
    for k in d:
      l.append(encode_feedparser_dict(k))
    return l
  else:
    return d

def parse_arxiv_url(url):
  """ 
  examples is http://arxiv.org/abs/1512.08756v2
  we want to extract the raw id and the version
  """
  ix = url.rfind('/')
  idversion = url[ix+1:] # extract just the id (and the version)
  parts = idversion.split('v')
  assert len(parts) == 2, 'error parsing url ' + url
  return parts[0], int(parts[1])

if __name__ == "__main__":

  # parse input arguments
  parser = argparse.ArgumentParser()

  # when there's hyphen in author's name, the - symbol should be replaced by its html code &#45; see https://www.ascii.cl/htmlcodes.htm for help
  # already added authors: Zhenghan Wang, Liang Kong, Davide Gaiotto, Jurgen Fuchs, Maissam Barkeshli, Meng Cheng, Iris Cong, Guifre Vidal, Yidun Wan, Xiao-Gang Wen, Ling-Yan Hung,  Edward Witten, Mironov or Morozov, Juven Wang, Bais and Slingerland, kirillov, 

  # to be added:Victor Kac, Zheng-Cheng Gu, Robert C Myers, T S Yau, Cumrun Vafa, Juan Maldacena, Eric Rowell, Paul Bruillard, Coquereaux, Frank Verstraete

  # (to do) filter out math/physics by subject category

  # title to contain: PT, anti-PT, classification, modular invariant
  # title added: topological entanglement, entanglement entropy, topological order, area law, topological phase, modular tensor category, non-Hermitian, exceptional point, parity-time, frobenius algebra,
  parser.add_argument('--search-query', type=str,
                      # specify authors
                      #default='au:kong_liang+OR+au:wang_zhenghan',
                      #default='au:verstraete_frank',
                      
                      #default='ti:"fermion+condensation"',
                      #default='ti:"topological+phase"',

                      default='id:1708.00006',

                      # specify title keywords
                      help='query used for arxiv API. See http://arxiv.org/help/api/user-manual#detailed_examples')



  
  parser.add_argument('--start-index', type=int, default=0,#cn.arxiv.org is one day later than arxiv.org
                      help='0 = most recent API result')
  parser.add_argument('--max-index', type=int, default=2000, help='upper bound on paper index we will fetch')
                                              # maximal number of papers to have in the server. not the number to download this run
  parser.add_argument('--results-per-iteration', type=int, default=100, help='passed to arxiv API')
  parser.add_argument('--wait-time', type=float, default=5.0, help='lets be gentle to arxiv API (in number of seconds)')
  parser.add_argument('--break-on-no-added', type=int, default=1, help='break out early if all returned query papers are already in db? 1=yes, 0=no')
  args = parser.parse_args()

  # misc hardcoded variables
  base_url = 'http://export.arxiv.org/api/query?' # base api query url
  myheaders={}
  myheaders["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"

  print('Searching arXiv for %s' % (args.search_query, ))

  # lets load the existing database to memory
  try:
    db = pickle.load(open(Config.db_path, 'rb'))
  except Exception as e:
    print('error loading existing database:')
    print(e)
    print('starting from an empty database')
    db = {}

  # -----------------------------------------------------------------------------
  # main loop where we fetch the new results
  print('database has %d entries at start' % (len(db), ))
  num_added_total = 0
  inject_count = 10
  #offset=len(db) - inject_count
  offset=0
  for i in range(args.start_index, args.max_index, args.results_per_iteration):

    print("Results \033[31m%i - %i\033[0m" % (i,i+args.results_per_iteration))
    query = 'search_query=%s&sortBy=lastUpdatedDate&start=%i&max_results=%i' % (args.search_query,
                                                         i+offset, args.results_per_iteration)
    # with urllib.request.urlopen(base_url+query) as url:
    #   response = url.read()
    with urllib.request.urlopen(Request(base_url+query,None,myheaders)) as url:
      response = url.read()
    parse = feedparser.parse(response)
    num_added = 0
    num_skipped = 0
    for e in parse.entries:
      #print("\n\n\n",e,"\n\n\n")
      j = encode_feedparser_dict(e)

      # extract just the raw arxiv id and version for this paper
      rawid, version = parse_arxiv_url(j['id'])
      j['_rawid'] = rawid
      j['_version'] = version

      # add to our database if we didn't have it before, or if this is a new version
      #if not rawid in db or j['_version'] > db[rawid]['_version']:
      if not rawid in db:
        # save a big dictionary j to the database
        db[rawid] = j
        #print(j['tags'])
        print('Updated %s added %s' % (j['updated'].encode('utf-8'), j['title'].encode('utf-8')))
        num_added += 1
        num_added_total += 1
      else:
        num_skipped += 1

    # print some information
    print('Added %d papers, already had %d.' % (num_added, num_skipped))

    if len(parse.entries) == 0:
      print('Received no results from arxiv. Rate limiting? Exiting. Restart later maybe.')
      print(response)
      break
    if num_added == 0 and args.break_on_no_added == 1:
      print('No new papers were added. Assuming no new papers exist. Exiting.')
      break

    print('Sleeping for %i seconds' % (args.wait_time , ))
    time.sleep(args.wait_time + random.uniform(0, 3))

  # save the database before we quit, if we found anything new
  if num_added_total > 0:
    print('Saving database with %d papers to %s' % (len(db), Config.db_path))
    safe_pickle_dump(db, Config.db_path)

#http://export.arxiv.org/api/query?search_query=cat:hep-th&sortBy=lastUpdatedDate&start=1&max_results=5



