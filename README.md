very basic python wrapper for relateiq.com

Based on API here: https://github.com/relateiq/riqapi/blob/master/resources/entitylists.md

Should note that as the relateiq API is alpha, this package could break at any time

Usage:
```
from pyrelate import RelateAPI

api = RelateAPI('API_TOKEN')

# add a relationship
api.add_relationship({
    'firstName': 'User',
    'email': : ''
}, list_id='LIST_ID')

# search for a relationship in a list
api.search_relationship('name', list_id='LIST_ID')
```
