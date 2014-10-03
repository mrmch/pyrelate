"""
Python client for relate IQ

VERY EXPERIMENTAL
"""

import json
import requests

import settings


class RelateObject(object):
    API_PROTO = 'https'
    API_PORT = '443'
    API_HOST = 'api.relateiq.com'
    API_VERSION = 'v2'

    API_STATUS_CODES = {
        200: "Ok - normal successful request",
        400: "Bad Request - normally a missing or malformatted parameter",
        401: "Unauthorized - missing credentials",
        403: "Forbidden - provided key does not have access for that method",
        404: "Not Found - requested object does not exist",
        422: "Unprocessable Entity - often the posted object is malformatted",
        429: "Too Many Requests - exceeded rate limits",
        500: "Internal Server Error - an unexpected error on the RelateIQ side",
        503: "Service Unavailable - likely a deploy is occuring, wait 2 minutes and retry"
    }

    HTTP_POST = 'post'
    HTTP_PUT = 'put'
    HTTP_GET = 'get'

    DEFAULT_LIMIT = 20

    DEBUG = False

    def __init__(self, api_key=None, api_secret=None, debug=True):
        self.API_KEY = api_key or settings.RELATE_API_KEY
        self.API_SECRET = api_secret or settings.RELATE_API_SECRET

        self.DEBUG = debug

    def _build_request_path(self, endpoint):
        path = "%s://%s/%s/%s" % (
            self.API_PROTO,
            self.API_HOST,
            self.API_VERSION,
            endpoint)
        return path

    @classmethod
    def all(cls, start=0, limit=None, fetch_all=False, transform=True):
        """Gets all the objects of this type
        optionally transforms as well"""

        if not limit:
            limit = cls.DEFAULT_LIMIT

        obj = cls()

        results = []

        while True:
            data = {'_start': start, '_limit': limit}

            response = obj.get(cls.ENDPOINT, data=data)

            if len(response['objects']) == 0:
                break

            if transform:
                results += [cls.from_dict(item) for item in response['objects']]
            else:
                results += response['objects']

            start += limit

            if not fetch_all:
                break

        return results

    @classmethod
    def get_by_id(cls, object_id):
        obj = cls()
        endpoint = '%s/%s' % (cls.ENDPOINT, object_id)
        data = obj.get(endpoint)
        obj.update_from_dict(data)
        return obj

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        obj.update_from_dict(data)
        return obj

    def post(self, endpoint, data):
        return self._api_request(self.HTTP_POST, endpoint, data=data)

    def put(self, endpoint, data):
        return self._api_request(self.HTTP_PUT, endpoint, data=data)

    def get(self, endpoint, data=None):
        return self._api_request(self.HTTP_GET, endpoint, data=data)

    def _api_request(self, http_method, endpoint, data=None):
        """Private method for api requests"""

        path = self._build_request_path(endpoint)

        if self.DEBUG:
            print '%s\n' % path
            print 'data:\n%s\n' % data

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        r = None
        auth = requests.auth.HTTPBasicAuth(self.API_KEY, self.API_SECRET)

        if (http_method == self.HTTP_POST):
            r = requests.post(path, data=json.dumps(data), auth=auth, headers=headers)
        elif (http_method == self.HTTP_PUT):
            r = requests.put(path, data=json.dumps(data), auth=auth, headers=headers)
        elif (http_method == self.HTTP_GET):
            r = requests.get(path, params=data, auth=auth, headers=headers)

        if r.status_code not in [200, 204]:
            extra = ""

            if r.status_code not in self.API_STATUS_CODES:
                msg = "UNKNOWN STATUS CODE"
            else:
                msg = self.API_STATUS_CODES[r.status_code]

                if self.DEBUG:
                    extra = "RELATE_API_KEY: %s\nRELATE_API_SECRET: %s" % (
                        self.API_KEY, self.API_SECRET
                    )

            raise Exception("""
                Request failed: %s
                Path: %s
                Method: %s
                Response Msg: %s
                Extra:
                %s
                
                Response Body
                %s""" % (r.status_code, path, http_method, msg, extra,
                            r.text))

        return r.json()


class RelateContact(RelateObject):
    ENDPOINT = 'contacts'

    id = None
    modified_date = None
    properties = None

    # current supported contact properties
    # ----
    name = None
    email = None
    phone = None
    address = None
    company = None
    title = None

    def update_from_dict(self, data):
        self.id = data['id']
        self.modified_date = data['modifiedDate']

        self.properties = []

        for prop, val in data['properties'].items():
            if hasattr(self, prop):
                self.properties.append(prop)
                setattr(self, prop, val[0]['value'])

    def to_dict(self):
        data = {
            'id': self.id,
            'modifiedDate': self.modified_date,
            'properties': {
                'name': [{'value': self.name}],
                'email': [{'value': self.email}],
                'phone': [{'value': self.phone}],
                'address': [{'value': self.address}],
                'company': [{'value': self.company}],
                'title': [{'value': self.title}]
            }
        }

        return data

    def save(self):
        if self.id and self.modified_date:
            # update
            endpoint = '%s/%s' % (self.ENDPOINT, self.id)
            data = self.put(endpoint, self.to_dict())
            self.update_from_dict(data)
        else:
            #create
            endpoint = self.ENDPOINT
            data = self.post(endpoint, self.to_dict())
            self.update_from_dict(data)

        return data


class RelateUser(RelateObject):
    ENDPOINT = 'users'

    id = None
    modified_date = None
    properties = None

    # current supported contact properties
    # ----
    name = None
    email = None
    phone = None
    address = None
    company = None
    title = None

    def update_from_dict(self, data):
        self.id = data['id']
        self.modified_date = data['modifiedDate']

        self.properties = []

        for prop, val in data['properties'].items():
            if hasattr(self, prop):
                self.properties.append(prop)
                setattr(self, prop, val[0]['value'])

    def to_dict(self):
        data = {
            'id': self.id,
            'modifiedDate': self.modified_date,
            'properties': {
                'name': [{'value': self.name}],
                'email': [{'value': self.email}],
                'phone': [{'value': self.phone}],
                'address': [{'value': self.address}],
                'company': [{'value': self.company}],
                'title': [{'value': self.title}]
            }
        }

        return data

    def save(self):
        if self.id and self.modified_date:
            # update
            endpoint = '%s/%s' % (self.ENDPOINT, self.id)
            data = self.put(endpoint, self.to_dict())
            self.update_from_dict(data)
        else:
            #create
            endpoint = self.ENDPOINT
            data = self.post(endpoint, self.to_dict())
            self.update_from_dict(data)

        return data


class RelateAccount(RelateObject):
    ENDPOINT = 'accounts'

    id = None
    modified_date = None
    name = None

    def update_from_dict(self, data):
        self.id = data['id']
        self.modified_date = data['modifiedDate']
        self.name = data['name']

    def to_dict(self):
        data = {
            'id': self.id,
            'modifiedDate': self.modified_date,
            'name': self.name
        }
        return data

    def save(self):
        if self.id and self.modified_date:
            # update
            endpoint = '%s/%s' % (self.ENDPOINT, self.id)
            data = self.put(endpoint, self.to_dict())
            self.update_from_dict(data)
        else:
            #create
            endpoint = self.ENDPOINT
            data = self.post(endpoint, self.to_dict())
            self.update_from_dict(data)

        return data


class RelateList(RelateObject):
    ENDPOINT = 'lists'

    id = None
    modified_date = None
    title = None
    list_type = None
    fields = []
    fields_dict = {}
    items = []

    raw_data = None

    @classmethod
    def get_by_id(cls, list_id, get_items=False, fetch_all=False):
        obj = cls()
        data = obj.get('%s/%s' % (cls.ENDPOINT, list_id))
        obj.update_from_dict(data)

        if get_items:
            obj.get_items(fetch_all=fetch_all)

        return obj

    def update_from_dict(self, data):
        self.id = data['id']
        self.modified_date = data['modifiedDate']
        self.list_type = data['listType']
        self.fields = data['fields']
        self.title = data['title']

        self.fields_dict = {field['id']: field for field in self.fields}

        self.raw_data = data

    def get_items(self, start=1, limit=20, fetch_all=False, clear_items=False):
        """Get all items in this list"""

        endpoint = '%s/%s/listitems' % (self.ENDPOINT, self.id)

        if clear_items:
            self.items = []

        while True:
            data = {'_start': start, '_limit': limit}

            response = self.get(endpoint, data=data)

            if len(response['objects']) == 0:
                break

            self.items += [RelateListItem(self, item) for item in response['objects']]

            start += limit

            if not fetch_all:
                break

        return self.items

    def filter_items(self, field, value, include=True):
        """Returns a filtered set of items. include defaults to true,
        so it will include items that have a field equaling value.
        To exclude items with field=value, set include false"""
        matches = []

        for item in self.items:
            if item.fields[field] == value and include:
                matches.append(item)
            elif item.fields[field] != value and not include:
                matches.append(item)

        return matches

    def get_item_by_name(self, name):
        for item in self.items:
            if item.name == name:
                return item

        return None


class RelateListItem(RelateObject):
    ENDPOINT = RelateList.ENDPOINT + '/%s/listitems'

    id = None
    modified_date = None
    created_date = None
    list_id = None
    account_id = None
    contact_ids = []
    name = None

    fields_data = {}
    field_values = {}
    fields_dict = {}
    fields_dict_reversed = {}
    fields = {}

    def __init__(self, r_list=None, list_id=None, data=None, **kwargs):
        super(RelateListItem, self).__init__(**kwargs)
        if r_list:
            self.list_id = r_list.id
            self.fields_dict = r_list.fields_dict
            self.fields_dict_reversed = {v['name']: k for k, v in r_list.fields_dict.items()}
            self.fields_data = r_list.fields
        else:
            self.list_id = list_id

        if data:
            self.update_from_dict(data)

    @classmethod
    def get_by_id(cls, list_id, item_id):
        obj = cls(list_id=list_id)
        endpoint = (cls.ENDPOINT % list_id) + ('/%s' % item_id)
        data = obj.get(endpoint)
        obj.update_from_dict(data)

        return obj

    def get_field(self, name, raw=False):
        if name in self.fields_dict_reversed:
            if raw:
                return self.fields[self.fields_dict_reversed[name]]
            else:
                field_key = self.fields_dict_reversed[name]
                raw_val = self.fields[field_key]
                field = self.fields_dict[field_key]

                if field['dataType'] == 'Text':
                    return raw_val
                elif field['dataType'] == 'User':
                    return RelateUser.get_by_id(raw_val)
                elif field['dataType'] == 'DateTime':
                    # @TODO: impl parse library to create dt object
                    return raw_val
                elif field['dataType'] == 'Numeric':
                    return raw_val
                elif field['dataType'] == 'List':
                    for item in field['listOptions']:
                        if item['id'] == raw_val:
                            return item['display']
                else:
                    raise Exception('Unknown data type: %s' % field)

        raise Exception('Invalid field for list: %s' % name)

    def set_field(self, name, val):
        if name in self.fields_dict_reversed:
            self.fields[self.fields_dict_reversed[name]] = val
        else:
            raise Exception('Invalid field for list: %s' % name)

    def update_from_dict(self, data):
        self.id = data['id']
        self.modified_date = data['modifiedDate']
        self.created_date = data['createdDate']
        self.list_id = data['listId']
        self.name = data['name']
        self.field_values = data['fieldValues']
        self.account_id = data['accountId']
        self.contact_ids = data['contactIds']

        self.fields = {}

        for key, value in self.fields_dict.iteritems():
            if key in self.field_values:
                self.fields[key] = self.field_values[key][0]['raw']
            else:
                self.fields[key] = ''

    def to_dict(self):
        fieldValues = {}

        for key in self.fields:
            fieldValues[key] = [{"raw": self.fields[key]}]

        data = {
            "listId": self.list_id,
            "accountId": self.account_id,
            "contactIds": self.contact_ids,
            "name": self.name,
            "fieldValues": fieldValues
        }

        if self.id:
            data['id'] = self.id

        if self.modified_date:
            data['modifiedDate'] = self.modified_date

        if self.created_date:
            data['createdDate'] = self.created_date

        return data

    def save(self):
        endpoint = self.ENDPOINT % (self.list_id)
        if self.id:
            # update
            endpoint += '/%s' % self.id
            data = self.put(endpoint, self.to_dict())
            self.update_from_dict(data)
        else:
            #create
            data = self.post(endpoint, self.to_dict())
            self.update_from_dict(data)

        return data


class RelateEvent(RelateObject):
    # @TODO: RelateEvent is not completed
    PARTICIPANT_TYPES = ["email", "phone"]
    ENDPOINT = 'events'

    subject = None
    body = None
    participants = []

    def __init__(self, subject, body, participants=None):
        if not participants:
            participants = []

        for participant in participants:
            self.participants.append(participant)

        self.subject = subject
        self.body = body

    def add_participant(self, participant_type, value):
        if participant_type not in self.PARTICIPANT_TYPES:
            raise Exception("Particpant type `%s` is not valid, must be one of %s" % (
                participant_type, self.PARTICIPANT_TYPES
                ))

        data = {
            "type": participant_type,
            "value": value
        }

        self.participants.append(data, value)

    def to_dict(self):
        data = {
            "subject": self.subject,
            "body": self.body,
            "participantIds": self.participants
        }

        return data

    def save(self):
        self.put(self.ENDPOINT, data=self.to_dict())
