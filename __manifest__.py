{
    'name': 'OdooSense Chatbot',
    'version': '1.0',
    'summary': 'Integrate a chatbot into your Odoo instance',
    'description': 'Integrate a chatbot into your Odoo instance using the OdooSense API',
    'category': 'Uncategorized',
    'author': 'Your Name',
    'depends': ['base', 'web'],
    'data': [
        'views/odoosense_chatbot_conversation.xml',
    ],
    'qweb': [
        'static/src/xml/odoosense_chatbot_conversation.xml',
    ],
    'external_dependencies': {
        'python': ['requests'],
        'js': ['https://code.jquery.com/jquery-3.6.0.min.js', 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.min.js'],
        'css': ['https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/css/bootstrap.min.css'],
    },
}