refer to https://arxiv.org/help/api/user-manual





base_url + query

 base_url = 'http://export.arxiv.org/api/query?'



### query

query = '**search_query**=%s &**sortBy**=lastUpdatedDate &**start**=%i &**max_results**=%i ' % (args.search_query, i+offset, args.results_per_iteration)



#### add specific papers with their id in a list

query = '**id_list**=%s '

e.g.  http://export.arxiv.org/api/query?id_list=1809.10275,1706.09464,1903.12246 can be realized by  `query = 'id_list=%s' %list`    where the string `list = "1809.10275,1706.09464,1903.12246"`  



##### add papers by a specific author

```bash
http://export.arxiv.org/api/query?search_query=au:wang_zhenghan&sortBy=lastUpdatedDate&max_results=30
```

 retrieves the recent 30 papers by Zhenghan Wang

```bash
http://export.arxiv.org/api/query?search_query=au:wang_juven&sortBy=lastUpdatedDate&max_results=30
```

gives recent 30 papers by Juven Wang



##### search_query

ti:  title

au: author

abs: abstract

cat: subject category

all: all of the above



###### author

```bash
http://export.arxiv.org/api/query?search_query=au:del_maestro+AND+ti:checkerboard
```

 gives the (last 10) papers of Del Maestro whose titles contain checkerboard



when there's hyphen in author's name, the - symbol should be replaced by its html code `&#45;` see https://www.ascii.cl/htmlcodes.htm for help

```bash
http://export.arxiv.org/api/query?search_query=au:wen_xiao&#45;gang
```

  to extract papers from Xiao-Gang Wen



###### title

title include "topological entanglement", the space between words should be replaced by a `+` 

```bash
http://export.arxiv.org/api/query?search_query=ti:"topological+entanglement"&sortBy=lastUpdatedDate&sortOrder=ascending
```