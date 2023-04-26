from odoo import api, fields, models
import requests
from odoo.http import request

class OdooSenseConversation(models.Model):
    _name = 'odoosense.conversation'
    _description = 'OdooSense Conversation'
    _rec_name = 'id'

    history = fields.Text(string='Conversation History', readonly=True)

class OdooSenseChatbot(models.Model):
    _name = 'odoosense.chatbot'
    _description = 'OdooSense Chatbot'

    name = fields.Char(string='Bot Name', required=True)
    api_key = fields.Char(string='API Key', required=True)
    conversation_id = fields.Many2one('odoosense.conversation', string='Conversation')
    context = fields.Char(string='Chatbot Context')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('trained', 'Trained'),
    ], default='draft')

    @api.multi
    def send_message(self, message):
        # Send a message to the chatbot and return the response
        url = 'https://your-chatbot-api-url.com'
        data = {
            'message': message,
            'api_key': self.api_key,
            'context': self.context,
            'webhook_url': request.httprequest.host_url + 'odoosense_chatbot/webhook',
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        conversation_history = self.conversation_id.history or ''
        conversation_history += '<p>User: ' + message + '</p>'
        conversation_history += '<p>Chatbot: ' + response_data['response'] + '</p>'
        self.conversation_id.history = conversation_history
        self.context = response_data.get('context')
        return response_data['response']

    @api.multi
    def stop_conversation(self):
        self.state = 'trained'
        conversation_history = self.conversation_id.history or ''
        conversation_history += '<p>Chatbot: Goodbye! Have a nice day.</p>'
        self.conversation_id.history = conversation_history
        self.context = None

    @api.multi
    def webhook(self, **post):
        # Handle incoming messages from the chatbot API
        message = post.get('message')
        conversation_history = self.conversation_id.history or ''
        conversation_history += '<p>Chatbot: ' + message + '</p>'
        self.conversation_id.history = conversation_history
        response = self.send_message(message)
        conversation_history += '<p>Chatbot: ' + response + '</p>'
        self.conversation_id.history = conversation_history
        return 'OK'