"""
Python client for relate IQ

VERY EXPERIMENTAL
"""

import requests

class RelateObject:
    API_PROTO = 'https'
    API_PORT = '443'
    API_HOST = 'app.relateiq.com'
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

    def __init__(self, api_key=None, api_secret=None, list_id=None, debug=False):
        self.API_KEY = api_key or RELATE_API_KEY
        self.API_SECRET = api_secret or RELATE_API_SECRET
        self.LIST_ID = list_id
        self.DEBUG = debug

    def _build_request_path(self, endpoint):
        path = "%s://%s/api/%s/%s" % (
            self.API_PROTO,
            self.API_HOST,
            self.API_VERSION,
            endpoint)
        return path

    def add_relationship(self, data, list_id=None):
        """
        This is an api v1 method that has been deprecated
        
        Add a relationship to the given list
        data format:
        {
            'firstName': "Matt",
            'email': "matt@sendwithus.com",
            'phone': '123-456-7890',
            'Status': 'New',
            'source': 'Landing'
        }

        expected response:
        {
            result: ["Created a contact", "Added a member"]
            success: true
        }
        """

        if not data:
            data = {}

        if not 'firstName' in data:
            raise Exception('firstName is a required parameter')

        if not 'email' in data:
            raise Exception('Email must be set')

        return self._api_request(self.HTTP_POST, 'addrelationship',
                list_id=list_id, data=data)

    def search_relationship(self, name, list_id=None):
        """searches for a relationship in the given list, by name"""

        if not name:
            raise Exception("name is required")

        return self._api_request(self.HTTP_GET, 'search', list_id=list_id,
                data={'name': name})

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

        if (http_method == self.HTTP_POST):
            r = requests.post(path, data=data,
                auth=(self.API_KEY, self.API_SECRET),
                headers=headers)
        elif (http_method == self.HTTP_PUT):
            r = requests.put(path, data=data,
                auth=(self.API_KEY, self.API_SECRET),
                headers=headers)
        elif (http_method == self.HTTP_GET):
            r = requests.get(path, params=data,
                auth=(self.API_KEY, self.API_SECRET),
                headers=headers)

        if r.status_code not in [200, 204]:
            if r.status_code not in self.API_STATUS_CODES:
                msg = "UNKNOWN STATUS CODE"
            else:
                msg = self.API_STATUS_CODES[r.status_code]

            raise Exception('Request failed: %s\n%s\n\n%s' % (r.status_code,
                msg, r.text))

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

    @classmethod
    def get_all(cls):
        data = cls.get(cls.ENDPOINT)
        return data['objects']

    @classmethod
    def get_by_id(cls, contact_id):
        endpoint = '%s/%s' % (cls.ENDPOINT, contact_id)
        data = cls.get(endpoint, contact_id)
        account = cls.from_dict(data)
        return account

    @classmethod
    def from_dict(cls, data):
        contact = cls()
        contact.update_from_dict(data)
        return contact

    def update_from_dict(self, data):
        self.id = data['id']
        self.modified_date = data['modifiedDate']
        self.name = data['properties']['name'][0]['value']
        self.email = data['properties']['email'][0]['value']
        self.phone = data['properties']['phone'][0]['value']
        self.address = data['properties']['address'][0]['value']
        self.company = data['properties']['company'][0]['value']
        self.title = data['properties']['title'][0]['value']

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

    @classmethod
    def get_all(cls):
        data = cls.get(cls.ENDPOINT)
        return data['objects']

    @classmethod
    def get_by_id(cls, account_id):
        endpoint = '%s/%s' % (cls.ENDPOINT, account_id)
        data = cls.get(endpoint)
        account = cls.from_dict(data)
        return account

    @classmethod
    def from_dict(cls, data):
        account = cls()
        account.update_from_dict(data)
        return account

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
    def get_by_id(cls, list_id, get_items=False):
        data = cls.get('%s/%s' % (cls.ENDPOINT, list_id))
        r_list = cls.from_dict(data)

        if get_items:
            r_list.get_items()

        return r_list

    @classmethod
    def from_dict(cls, data):
        r_list = cls()
        r_list.update_from_dict(data)
        return r_list

    @classmethod
    def get_all(cls):
        """Gets all lists"""
        data = cls.get(cls.ENDPOINT)
        return data['objects']

    def update_from_dict(self, data):
        self.id = data['id']
        self.modified_date = data['modifiedDate']
        self.list_type = data['listType']
        self.fields = data['fields']

        self.fields_dict = {}

        for field in self.fields:
            self.fields_dict[field['id']] = field['name']

        self.raw_data = data

    def get_items(self, start=0, limit=20):
        """Get all items in this list"""

        data = {'_start': start, '_limit': limit}
        endpoint = '%s/%s/listitems' % (self.ENDPOINT, self.id)

        response = self.get(endpoint, data=data)

        self.items = [RelateListItem(self, item) for item in response['objects']]

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
    ENDPOINT = RelateList.ENDPOINT + '/%s/listitems/%s'

    id = None
    modified_date = None
    created_date = None
    list_id = None
    account_id = None
    contact_ids = []
    name = None

    field_values = {}
    field_dict = {}
    fields = {}

    def __init__(self, r_list, data=None):
        self.list_id = r_list.id
        self.fields_dict = r_list.fields_dict

        if data:
            self.update_from_dict(data)

    @classmethod
    def get_by_id(cls, list_id, item_id):
        endpoint = cls.ENDPOINT % (list_id, item_id)
        data = cls.get(endpoint)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data):
        item = cls()
        item.update_from_dict(data)
        return item

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

        for key, value in self.field_dict.iteritems():
            self.fields[value] = self.field_values[key][0]['raw']

    def to_dict(self):
        fieldValues = {}

        for key, value in self.field_dict.iteritems():
            fieldValues[key] = [{"raw": self.fields[value]}]

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
        if self.id:
            # update
            endpoint = self.ENDPOINT % (self.list_id, self.id)
            data = self.put(endpoint, self.to_dict())
            self.update_from_dict(data)
        else:
            #create
            endpoint = self.ENDPOINT
            data = self.post(endpoint, self.to_dict())
            self.update_from_dict(data)

        return data


class RelateEvent(RelateObject):
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
