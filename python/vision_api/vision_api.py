#!/usr/bin/env python
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This class uses the Vision API's detection capabilities to find labels/text/logos/safe search params based on an image's content.

To run the example, install the necessary libraries by running:

    pip install -r requirements.txt

Import this module and use the VisionAPI class to detect labels/text/logo's from given images, E.g.:

"""

import argparse
import base64
import httplib2

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

class VisionAPI(object):
    """ Class to interact witht eh Google Vision API services. """

    def __init__(self):
        self.service = discovery.build('vision', 'v1',
                credentials=GoogleCredentials.get_application_default(),
                discoveryServiceUrl=DISCOVERY_URL)

    def label_image(self, image, max_results=1):
        """ Use the Vison API to label the image given. """
        detection_type = 'LABEL_DETECTION'
        api_request = self.generate_request(image, detection_type, max_results)
        service_request = self.service.images().annotate(body=api_request)
        response = service_request.execute()
        print(response)
        label = response['responses'][0]['labelAnnotations']
        return label

    def detect_text(self, image):
        """ Use the Vison API to detect text in the image given. """
        detection_type = 'TEXT_DETECTION'
        api_request = self.generate_request(image, detection_type)
        service_request = self.service.images().annotate(body=api_request)
        response = service_request.execute()
        print(response)
        label = response['responses'][0]['textAnnotations']
        return label

    def detect_logo(self, image, max_results=1):
        """ Use the Vison API to detect logo in the image given. """
        detection_type = 'LOGO_DETECTION'
        api_request = self.generate_request(image, detection_type, max_results)
        service_request = self.service.images().annotate(body=api_request)
        response = service_request.execute()
        print(response)
        label = response['responses'][0]['logoAnnotations']
        return label

    def safe_search(self, image):
        """ Use te Vision API to get safe search annotations for image. """
        detection_type = 'SAFE_SEARCH_DETECTION'
        api_request = self.generate_request(image, detection_type)
        service_request = self.service.images().annotate(body=api_request)
        response = service_request.execute()
        print(response)
        label = response['responses'][0]['safeSearchAnnotation']
        return label

    @staticmethod
    def generate_request(image, detection_type=None, max_results=1):
        """ """
        request_list = []
        image_content = base64.b64encode(image.read())
        image.seek(0)
        content_json = {'content': image_content.decode('UTF-8')}
        feature_json = []
        feature_json.append({
            'type': detection_type,
            'maxResults': max_results
            })
        request_list.append({
            'features': feature_json,
            'image': content_json
            })
        return {'requests': request_list}

