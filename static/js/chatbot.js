odoo.define('odoosense_chatbot.chatbot', function (require) {
    'use strict';

    var ajax = require('web.ajax');

    var Chatbot = function (options) {
        this.conversation_history = '';
        this.chatbot_response = '';
        this.options = options || {};
    };

    Chatbot.prototype.get_response = function (query) {
        var self = this;

        ajax.jsonRpc('/odoosense_chatbot/get_response', 'call', {
            query: query,
        }).then(function (response) {
            self.update_chatbot_response(response);
        }).fail(function () {
            self.update_chatbot_response('Oops! Something went wrong. Please try again later.');
        });

        // Display user query in conversation history
        this.conversation_history += '<div class="user-query"><strong>You:</strong> ' + query + '</div>';
        this.update_conversation_history();
    };

    Chatbot.prototype.update_chatbot_response = function (response) {
        // Display chatbot response in conversation history
        this.chatbot_response = '<div class="chatbot-response"><strong>Chatbot:</strong> ' + response + '</div>';
        this.conversation_history += this.chatbot_response;
        this.update_conversation_history();
    };

    Chatbot.prototype.update_conversation_history = function () {
        var $conversation_history = this.$('.media-body');
        $conversation_history.html(this.conversation_history);

        // Add clear button if conversation history is not empty
        if (this.conversation_history) {
            var $clear_button = $('<button>', {
                class: 'btn btn-default btn-xs clear-chatbot-history',
                text: 'Clear history',
            }).click(function () {
                this.clear_conversation_history();
            }.bind(this));
            $conversation_history.append($('<div>', {
                class: 'text-center',
            }).append($clear_button));
        }
    };

    Chatbot.prototype.clear_conversation_history = function () {
        this.conversation_history = '';
        this.chatbot_response = '';
        this.update_conversation_history();
    };

    return Chatbot;
});