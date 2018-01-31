"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- addressing.py --

@author: Informed Solutions
"""
import ast

import requests
import json
from django.conf import settings


class AddressHelper:

    @staticmethod
    def issue_postcode_search(postcode):
        """
        Helper method for building a select list of addresses with a count at the top.
        :param postcode: the postcode on which a search will be made (issued to Addressing Service API)
        :return: list of addresses formatted for a ChoiceField
        """
        headers = {"content-type": "application/json"}
        response = requests.get(settings.ADDRESSING_URL + postcode + '/', headers=headers, verify=False)
        address_matches = json.loads(response.text)
        results = address_matches['results']
        count = address_matches['count']
        results_no = str(count) + ' addresses found'
        addresses = [(None, results_no)]
        for address in results:
            one_line = address['combinedAddress']
            elements = {
                'line1': address['line1'],
                'line2': address['line2'],
                'townOrCity': address['townOrCity'],
                'postcode': address['postcode']
            }
            addresses.append((elements, one_line))
        return addresses

    @staticmethod
    def get_posted_address(form, field_name):
        """
        Gets a dictionary representation of an address that has been posted in a form
        :param field_name: the name of a POST body field to be queried for an address submission
        :return: a dictionary response object representing a chosen addresss
        """
        selected_address = form.data.get(field_name)
        return ast.literal_eval(selected_address)