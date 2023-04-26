import openai
from odoo import api, fields, models, _

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
        if not self.conversation:
            self.conversation = self.env['odoosense.conversation'].create({'history': ''})
        prompt = f"{self.conversation.history}\nUser: {self.message}\nBot:"
        try:
            # Call the OpenAI API to generate a response based on the prompt
            response = openai.Completion.create(
                engine='davinci',
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            ).choices[0].text.strip()
        except openai.error.APIError as api_error:
            # Log the error message and set the response field to an error message
            _logger.error("An error occurred while processing the message: %s", str(api_error))
            self.write({'response': _('An error occurred while processing your request. Please try again later.')})
            return
        except Exception as e:
            # Log the error message and set the response field to an error message
            _logger.error("An unexpected error occurred while processing the message: %s", str(e))
            self.write({'response': _('An unexpected error occurred while processing your request. Please contact your system administrator.')})
            return

        self.conversation.write({'history': prompt + response + '\n'})
        self.write({'response': response})
        self.env.cr.commit()