import base64
import io
import requests
from odoo import http, _
from odoo.http import request
from PIL import Image
from .main import OdooSenseChatbot


class OdooSense_Chatbot(OdooSenseChatbot):
    @http.route('/odoosense_chatbot/get_response', type='json', auth='public', methods=['POST'])
    def get_response(self, query, is_image=False):
        if is_image:
            # Convert data URL to image
            image_string = query.split(',')[1]
            image_bytes = io.BytesIO(base64.b64decode(image_string))
            image = Image.open(image_bytes)

            # Process image and get response
            response = self.process_image(image)
        elif ',' in query:
            # Parse latitude and longitude from query
            latitude, longitude = map(float, query.split(','))
            
            # Process location data and get response
            response = self.process_location(latitude, longitude)
        else:
            # Process text query and get response
            response = self.process_text(query)
        
        return response

    def process_text(self, query):
        # Process text query and return response
        # This is an example implementation that just echoes the user's query back to them
        return _('You said: %s') % query

    def process_image(self, image):
        # Process image and return response
        # This is an example implementation that just returns a fixed response
        return _('I see a picture!')

    