import logging
import json
import openai
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class OdooSenseController(http.Controller):
    
    @http.route('/odoosense/handle_message', type='json', auth='public')
    def handle_message(self, **kw):
        message = kw.get('message')
        _logger.info(f"Incoming message: {message}")

        # Check if the OpenAI API key is set
        openai_api_key = request.env['odoosense.odoosense'].search([], limit=1).openai_api_key
        if not openai_api_key:
            _logger.warning("OpenAI API key is missing. Please set the key in the OdooSense settings.")
            return {'message': 'OdooSense is not configured. Please contact your system administrator.'}

        try:
            # Call the OpenAI API to generate a response to the message
            response = self.generate_response(message, openai_api_key)
            _logger.info(f"Generated response: {response}")
        except openai.error.APIError as api_error:
            _logger.error("An error occurred while processing the message: %s", str(api_error))
            return {'message': 'An error occurred while processing your request. Please try again later.'}
        except Exception as e:
            _logger.error("An unexpected error occurred while processing the message: %s", str(e))
            return {'message': 'An unexpected error occurred while processing your request. Please contact your system administrator.'}

        return {'message': response}

    def generate_response(self, message, api_key):
        try:
            # Call the OpenAI API to generate a response based on the message
            openai.api_key = api_key
            model_engine = 'davinci' # or 'curie', 'babbage', 'ada', etc.
            prompt = f"Message: {message}\nResponse: "
            response = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return response.choices[0].text.strip()
        except openai.error.APIError as api_error:
            raise api_error
        except Exception as e:
            raise e