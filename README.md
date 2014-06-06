very basic python wrapper for relateiq.com

Based on API here: https://github.com/relateiq/riqapi/blob/master/resources/entitylists.md

Should note that as the relateiq API is alpha, this package could break at any time

## Usage:

### Setup
```python
RELATE_API_KEY = 'API_KEY'
RELATE_API_SECRET = 'API_SECRET'

from pyrelate import RelateContact, \
    RelateAccount, \
    RelateList, \
    RelateListItem
```

### Lists
```python

# get all lists
lists = RelatList.get_all()

# get a list by id
my_list = RelateList.get_by_id('my--list-id')

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
items = my_list.items

type items[0]
# RelateListItem

# Assume we have a field called "value"
# we can now do
print items[0].fields['value']

# what's really cool, if we update this field
# and save it
# it will be pushed to relate!
items[0].fields['value'] = 500
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
