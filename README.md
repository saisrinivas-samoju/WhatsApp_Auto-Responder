## WhatsApp Auto-Responder

### Description

  You can add your custom patterns and responses in the intents.json file, run the train.py file after installing required libraries to train the model for auto-responses.
  Once the model is trained, it will replace the existing data.pth file, this file can then be used for responding your WhatsApp messages.
  Finally, Open WhatsApp web in your local system in light mode, and run the main.py file.

### How does it work?

  While the code is running, it will keep on checking for new unread messages, and unanswered messages which are opened in the main page. Once, it finds a message unread or not responded, It will copy the message, process it, and posts the response.

### Demo
