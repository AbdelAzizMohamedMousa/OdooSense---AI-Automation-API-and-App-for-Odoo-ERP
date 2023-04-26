import requests
from odoo import models, fields, api
from odoo.http import request

class OdooSenseChatbot(models.Model):
    _name = 'odoosense.chatbot'
    _description = 'OdooSense Chatbot'

    name = fields.Char(string='Bot Name', required=True)
    api_key = fields.Char(string='API Key', required=True)
    conversation_history = fields.Html(string='Conversation History', readonly=True)
    chatbot_response = fields.Html(string='Chatbot Response', readonly=True)
    context = fields.Char(string='Chatbot Context')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('trained', 'Trained'),
    ], default='draft')

    @staticmethod
    def send_message(message, api_key, context):
        # Send a message to the chatbot and return the response
        url = 'https://your-chatbot-api-url.com'
        data = {
            'message': message,
            'api_key': api_key,
            'context': context,
            'webhook_url': request.httprequest.host_url + 'odoosense_chatbot/webhook',
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        return response_data['response'], response_data.get('context')

    def stop_conversation(self):
        self.state = 'trained'
        self.conversation_history += '<p>Chatbot: Goodbye! Have a nice day.</p>'
        self.context = None

    @staticmethod
    def webhook(**post):
        # Handle incoming messages from the chatbot API
        message = post.get('message')
        chatbot = request.env['odoosense.chatbot'].sudo().search([], limit=1)
        chatbot.conversation_history += '<p>Chatbot: ' + message + '</p>'
        response, context = OdooSenseChatbot.send_message(message, chatbot.api_key, chatbot.context)
        chatbot.chatbot_response = '<p>Chatbot: ' + response + '</p>'
        chatbot.context = context
        return 'OK'