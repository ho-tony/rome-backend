# midjourney/views.py

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from midjourney.receiver import Receiver
from midjourney.sender import Sender
import json
import os
import time
import base64

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from split_image import split_image
from rembg import remove
from PIL import Image
from resizeimage import resizeimage

# def get_images(image):
#     split_image(image[0], 2, 2, False, False)

#     obj = []

#     for i in range(4):
#         input_path = f'{image[1][:len(image[1])-4]}_{i}.png'
#         output_path = f'output_{i}.png'
#         print(input_path)
#         print(output_path)
#         with open(input_path, 'rb') as in_f:
#             with open(output_path, 'wb') as o:
#                 input = in_f.read()
#                 output = remove(input)
#                 o.write(output)
#         print(f'removed background {i}')
#         with open(output_path, 'r+b') as f:
#             with Image.open(f) as image:
#                 cover = resizeimage.resize_contain(image, [24, 24])
#                 cover.save(output_path, image.format)
#         print(f'resized {i}')
#         # with open(output_path, 'rb') as o:
#         #    obj.append({f'img_{i}' : o.read()})
#     print(obj)
#     return obj

def get_images(image):
    split_image(image[0], 2, 2, False, False)

    obj = {}

    for i in range(4):
        input_path = f'{image[1][:len(image[1])-4]}_{i}.png'
        output_path = f'output_{i}.png'
        print(f"Processing: Input: {input_path}, Output: {output_path}")
        
        try:
            # Remove background
            with open(input_path, 'rb') as in_f:
                input_data = in_f.read()
                output_data = remove(input_data)
            
            with open(output_path, 'wb') as out_f:
                out_f.write(output_data)
            
            print(f'Removed background for image {i}')
            
            # Resize image
            with Image.open(output_path) as img:
                cover = resizeimage.resize_contain(img, [24, 24])
                cover.save(output_path, img.format)
            
            print(f'Resized image {i}')
            
            # Read the processed image and encode it as base64
            with open(output_path, 'rb') as o:
                img_data = base64.b64encode(o.read()).decode('utf-8')
                obj[f'img_{i}'] = img_data
            
            print(f'Added image {i} to obj')
        
        except Exception as e:
            print(f"Error processing image {i}: {str(e)}")
    
    print(f"Processed {len(obj)} images")
    return obj


@csrf_exempt
def get_assets(request):
    if request.method == 'POST':
        print("hit post")
        print(request)
        
        data = json.loads(request.body)
        print(data)
        prompt = data.get('enemies', '').strip()
        if not prompt:
            return JsonResponse({'error': 'No prompt provided.'}, status=400)

        sender = Sender()
        sender.send(prompt)

        # Optional: Wait for a short duration to allow Discord to process the prompt
        time.sleep(45)  # Adjust as needed based on Discord's response time

        receiver = Receiver()
        image = receiver.process_latest_message()

        if image[0] and os.path.exists(image[0]):
            print("generated img")
            processed_images = get_images(image)
            return JsonResponse({'images': processed_images}, status=200)
        else:
            return JsonResponse({'error': 'Image not found or not downloaded yet.'}, status=404)

       

    return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)


