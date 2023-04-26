import logging
import openai
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class OdooSense(models.Model):
    _name = 'odoosense.odoosense'
    _description = 'OdooSense AI Chatbot'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    suggestion = fields.Text(string='Suggestion', readonly=True)
    openai_api_key = fields.Char(string='OpenAI API Key', required=True)

    @api.onchange('description')
    def generate_suggestion(self):
        if self.description:
            # Call the OpenAI API to generate a suggestion based on the description
            suggestion = self.generate_suggestion_from_openai(self.description, self.openai_api_key)
            self.suggestion = suggestion

    def generate_suggestion_from_openai(self, description, api_key):
        try:
            # Call the OpenAI API to generate a suggestion based on the description
            openai.api_key = api_key
            model_engine = 'davinci' # or 'curie', 'babbage', 'ada', etc.
            prompt = f"Description: {description}\nSuggestion: "
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
            _logger.error("An error occurred while generating suggestion from OpenAI: %s", str(api_error))
            return "An error occurred while generating suggestion."
        except Exception as e:
            _logger.error("An unexpected error occurred while generating suggestion from OpenAI: %s", str(e))
            return "An unexpected error occurred while generating suggestion."