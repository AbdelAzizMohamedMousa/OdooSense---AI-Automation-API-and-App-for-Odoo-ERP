import openai
from odoo import api, fields, models

class OdooSense(models.Model):
    _name = 'odoosense.odoosense'
    _description = 'OdooSense Chatbot'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    suggestion = fields.Text(string='Suggestion')
    openai_api_key = fields.Char(string='OpenAI API Key', required=True)
    conversation = fields.Many2one('odoosense.conversation', string='Conversation')
    message = fields.Text(string='User Message', required=True)
    response = fields.Text(string='Chatbot Response', readonly=True)

    @api.onchange('openai_api_key')
    def _onchange_openai_api_key(self):
        openai.api_key = self.openai_api_key

    def send_message(self):
        prompt = f"{self.suggestion.strip()} {self.message.strip()}"
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7
        )

        self.response = response.choices[0].text.strip()
    
        self.conversation.history += f"User: {self.message}\nBot: {self.response}\n"