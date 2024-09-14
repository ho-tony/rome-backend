# midjourney/views.py

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from midjourney.receiver import Receiver
from midjourney.sender import Sender
import json
import os
import time
from split_image import split_image
from rembg import remove
from PIL import Image
from resizeimage import resizeimage

def split_image(image):
    split_image(image[0], 2, 2, False, False, output_path="rome_backend/images")

    obj = {}

    for i in range(4):
        input_path = f'rome_backend/images/{image[1]}_{i}'
        output_path = f'rome_backend/images/output_{i}'

        with open(input_path, 'rb') as i:
            with open(output_path, 'wb') as o:
                input = i.read()
                output = remove(input)
                o.write(output)
                obj[f'img_{i}'] = o.read()
    
    return obj

@csrf_exempt
def index(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('text', '').strip()
            if not prompt:
                return JsonResponse({'error': 'No prompt provided.'}, status=400)

            sender = Sender()
            sender.send(prompt)

            # Optional: Wait for a short duration to allow Discord to process the prompt
            time.sleep(45)  # Adjust as needed based on Discord's response time

            receiver = Receiver()
            image= receiver.process_latest_message()

            if image[0] and os.path.exists(image[0]):
                return HttpResponse(json.dumps(split_image(image)))
                # with open(image[0], 'rb') as image_file:
                #    return HttpResponse(image_file.read(), content_type='image/png')
            else:
                return JsonResponse({'error': 'Image not found or not downloaded yet.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)

