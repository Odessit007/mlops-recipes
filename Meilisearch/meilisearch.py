import json
import meilisearch


# Assumes that MEILI_MASTER_KEY environment variable was set.
client = meilisearch.Client('http://localhost:1234')

# Import data from JSON file storing a list of objects, 1 object = 1 document.
# The file can be downloaded from here: https://www.meilisearch.com/movies.json
with open('movies.json', encoding='utf-8') as json_file:
    # Meilisearch will try to guess primary key, but you can also explicitly provide it as `primary_key=KEY_NAME`
    movies = json.load(json_file)


# Requests to the client mostly return asynchronous tasks
# You can use this hack to synchronize them
def run_sync(index_name, method_name, *args, **kwargs):
  index = client.index(index_name)
  task = getattr(index, method_name)(*args, **kwargs)
  uid = task.task_uid
  index.wait_for_task(uid)
  status = client.get_task(uid).status
  assert status == 'succeeded', status
  print(method_name, 'done')


task = client.index('movies').add_documents(movies)

# You can define which fields are used for relevance ranking.
# If more than one value is provided, their order affects the `Attribute` ranking rule.
client.index('movies').update_searchable_attributes(['title'])

# You can add the list of stop words.
client.index('movies').update_stop_words(['the', 'a', 'in', 'of', 'on'])

# You can define synonyms
client.index('movies').update_synonyms({
    'winnie': ['piglet'],
    'piglet': ['winnie'],
    # Synonyms can be one-directional if you want, here only "increased" will be replaced during search
    'increased': ['large', 'elevated', 'high'],  # There can be many synonyms
    'SF': ['San Fransico']  # Synonyms can contain multiple words, but no more than 3
})

# The value of the field configured as a distinct attribute will always be unique among returned documents.
# This means there will never be more than one occurrence of the same value in the distinct attribute field among the returned documents.
client.index('jackets').update_distinct_attribute('product_id')


# Typos
# You can enable/disable typos tolerance (enabled by default)
client.index('movies').update_typo_tolerance({
  'enabled': True
})

# You can define the minimum length of words for which 1 or 2 typos are allowed
client.index('movies').update_typo_tolerance({
  'minWordSizeForTypos': {
    'oneTypo': 5,  # 0 <= oneTypo <= twoTypos; recommended between 2 and 8
    'twoTypos': 9  # oneTypo <= twoTypos <= 255; recommended between 4 and 14
  }
})

# You can forbid typos in specific attributes
client.index('movies').update_typo_tolerance({
  'disableOnAttributes': ['title']
})

# You can forbid typos in specific words
client.index('movies').update_typo_tolerance({
  'disableOnWords': ['shrek']
})


# Search
# client.index('movies').search(query, optional settings)
results_2 = client.index('movies').search(
  'wonder',
  {
    'limit': 5,
    'attributesToHighlight': ['title'],
    'filter': ['id > 1 AND genres = Action']
  }
)
