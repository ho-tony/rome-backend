# midjourney/sender.py

import requests
import json
import re
import asyncio
import aiohttp
from django.conf import settings

class Sender:
    def __init__(self, params_path='midjourney/sender_params.json'):
        self.params = params_path
        self.sender_initializer()

    def sender_initializer(self):
        try:
            with open(self.params, "r") as json_file:
                params = json.load(json_file)
        except FileNotFoundError:
            print(f"Parameters file not found: {self.params}")
            raise
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the parameters file: {self.params}")
            raise

        self.channelid = params.get('channelid')
        self.authorization = params.get('authorization')
        self.application_id = params.get('application_id')
        self.guild_id = params.get('guild_id')
        self.session_id = params.get('session_id')
        self.version = params.get('version')
        self.id = params.get('id')
        self.flags = params.get('flags')

        if not all([self.channelid, self.authorization, self.application_id, self.guild_id,
                    self.session_id, self.version, self.id, self.flags]):
            raise ValueError("Missing one or more required parameters in the parameters file.")

    async def send_async(self, prompt):
        headers = {
            'authorization': self.authorization,
            'Content-Type': 'application/json'
        }

        # Clean the prompt
        prompt = prompt.replace('_', ' ')
        prompt = " ".join(prompt.split())
        prompt = re.sub(r'[^a-zA-Z0-9\s]+', '', prompt)
        prompt = prompt.lower()

        payload = {
            'type': 2,
            'application_id': self.application_id,
            'guild_id': self.guild_id,
            'channel_id': self.channelid,
            'session_id': self.session_id,
            'data': {
                'version': self.version,
                'id': self.id,
                'name': 'imagine',
                'type': 1,
                'options': [{'type': 3, 'name': 'prompt', 'value': f"{prompt} {self.flags}"}],
                'attachments': []
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post('https://discord.com/api/v9/interactions', json=payload, headers=headers) as response:
                if response.status == 204:
                    print(f'Prompt [{prompt}] successfully sent!')
                else:
                    resp_text = await response.text()
                    print(f"Failed to send prompt [{prompt}]. Status: {response.status}, Response: {resp_text}")

    def send(self, prompt):
        asyncio.run(self.send_async(prompt))
