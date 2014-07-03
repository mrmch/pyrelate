Basic API client for: https://api.relateiq.com/#/

## Usage:

### Setup
```python
import pyrelate

pyrelate.settings.RELATE_API_KEY = 'API_KEY'
pyrelate.settings.RELATE_API_SECRET = 'API_SECRET'
```

### Types
```python
# List
pyrelate.RelateList

# List Item
pyrelate.RelateListItem

# Account
pyrelate.RelateAccount

# Contacts
pyrelate.RelateContact

# Users
pyrelate.RelateUser

# Events
# @TODO: Not complete yet
pyrelate.RelateEvent
```

### Standard Methods

Every object has 3 standard methods

#### get_by_id

Gets a single item of that type by id

```python
RelateList.get_by_id('my-list-id')
```

#### all

Gets all items of that type

Optional parameters:
- `fetch_all` (default False) gets all items by doing multiple requests
- `start` (default 0) if not fetching all, sets a start item
- `limit` (default 20) sets the limit (or count) of objects to pull
- `transform` (default True), returns Object type instead of raw values

```python
# gets all
RelateList.all()

# optional parameter fetch_all
RelateList.all(fetch_all=True)
```

#### save

Saves the object to relateiq
@TODO: Not completed

```python
obj.save()
```


### Lists
```python

# get all lists
lists = RelatList.all()

# get a list by id
my_list = RelateList.get_by_id('my-list-id')

# optionally, retreive all list items at the same time
my_list_with_items = RelateList.get_by_id('my-list-id', get_items=True)

# we can always fetch the items later
my_list.get_items()

# check what fields we have
print my_list.fields_dict
# {"0": "Name", "1": "Source"}
```

### List Items
```python
# back to my_list from above example
# get the list items
item = my_list.items[0]

type item
# RelateListItem

# Assume we have a field called "value"
# we can now do
print item.get_field('Status')
# u'Interested'

# You can also get the raw value of a field
print item.get_field('value', raw=True)

# set a field
item.set_field('value', 100)

# what's really cool, if we update this field
# and save it, will be pushed to relate!
items[0].save()

# we have a few handy list methods as well
# get_item_by_name searches list items by name 
awesome_deal = my_list.get_item_by_name("My awesome Deal")

# Let's get a filtered set of items
# based on having a field "value" of 500
value_500_items = my_list.filter_items("value", "500")

# Now let's get items that have the opposite (not value 500)
not_500_items = my_list_filter_items("value", "500", include=False)

# create a new item
item = RelateListItem(my_list)
item.name = "My awesome Item"
item.fields['value'] = 500
item.save()
```
