# midjourney/receiver.py

import requests
import json
import pandas as pd
import os
import re
from datetime import datetime
from django.conf import settings

class Receiver:
    def __init__(self, params_path='midjourney/sender_params.json', local_path='assets'):
        self.params = params_path
        self.local_path = local_path
        self.processed_ids = set()

        self.sender_initializer()
        self.df = pd.DataFrame(columns=['prompt', 'url', 'filename', 'is_downloaded'])
        self.awaiting_list = pd.DataFrame(columns=['prompt', 'status'])

        # Ensure the local_path exists
        if not os.path.isdir(self.local_path):
            os.makedirs(self.local_path, exist_ok=True)
            print(f"Created directory: {self.local_path}")

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

        if not self.channelid or not self.authorization:
            raise ValueError("Missing 'channelid' or 'authorization' in the parameters file.")

        self.headers = {'authorization': self.authorization}

    def retrieve_messages(self, limit=10):
        url = f'https://discord.com/api/v10/channels/{self.channelid}/messages?limit={limit}'
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching messages: {e}")
            return []

    def collect_latest_message(self):
        message_list = self.retrieve_messages(limit=10)  # Fetch last 10 messages to ensure catching new ones
        status = "downloading"

        for message in message_list:
            message_id = message.get('id')
            if not message_id or message_id in self.processed_ids:
                continue  # Skip already processed messages

            author = message.get('author', {}).get('username', '')
            content = message.get('content', '')
            attachments = message.get('attachments', [])

            if author != 'Midjourney Bot' or '**' not in content:
                continue  # Skip irrelevant messages

            self.processed_ids.add(message_id)

            if attachments:
                attachment = attachments[0]
                filename = attachment.get('filename', '')
                url = attachment.get('url', '')

                if filename.endswith('.png') or '(Open on website for full quality)' in content:
                    prompt = self.extract_prompt(content)
                    if prompt:
                        self.df.loc[message_id] = [prompt, url, filename, 0]
                else:
                    prompt = self.extract_prompt(content)
                    if prompt:
                        self.awaiting_list.loc[message_id] = [prompt, status]
            else:
                prompt = self.extract_prompt(content)
                if prompt:
                    self.awaiting_list.loc[message_id] = [prompt, status]

    def extract_prompt(self, content):
        try:
            return content.split('**')[1].split(' --')[0].strip()
        except IndexError:
            return None

    def download_latest_image(self):
        processed_prompts = []
        for message_id, row in self.df[self.df['is_downloaded'] == 0].iterrows():
            try:
                response = requests.get(row['url'])
                response.raise_for_status()
                filename = os.path.join(self.local_path, row['filename'])
                with open(filename, "wb") as file:
                    file.write(response.content)
                self.df.loc[message_id, 'is_downloaded'] = 1
                processed_prompts.append(row['prompt'])
            except requests.exceptions.RequestException as e:
                print(f"Error downloading {row['url']}: {e}")

        if processed_prompts:
            print(f"{datetime.now().strftime('%H:%M:%S')} - Processed prompts: {processed_prompts}")
            print('=========================================')

    def get_latest_image_path(self):
        if self.df.empty:
            return None
        latest_entry = self.df.iloc[0]
        print(latest_entry)
        return os.path.join(self.local_path, latest_entry['filename'])

    def process_latest_message(self):
        self.collect_latest_message()
        self.download_latest_image()
        return self.get_latest_image_path()
