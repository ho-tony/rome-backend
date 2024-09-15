# midjourney/views.py

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from midjourney.receiver import Receiver
from midjourney.sender import Sender
import json
import os
import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



# @csrf_exempt
# def index(request):

#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             prompt = data.get('text', '').strip()
#             if not prompt:
#                 return JsonResponse({'error': 'No prompt provided.'}, status=400)

#             sender = Sender()
#             sender.send(prompt)

#             # Optional: Wait for a short duration to allow Discord to process the prompt
#             time.sleep(45)  # Adjust as needed based on Discord's response time

#             receiver = Receiver()
#             image_path = receiver.process_latest_message()

#             if image_path and os.path.exists(image_path):
#                 with open(image_path, 'rb') as image_file:
#                     return HttpResponse(image_file.read(), content_type='image/png')
#             else:
#                 return JsonResponse({'error': 'Image not found or not downloaded yet.'}, status=404)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)


def index(request):
    sender = Sender()
    sender.send(f"Can you generate me an image of Link from the Legend of Zelda. ")
    receiver = Receiver()
    receiver.main()
    return render(request, "../frontend/index.html")

@api_view(['POST'])
def get_assets(request):

    if request.content_type == 'text/plain':
        form_data = request.body.decode('utf-8')
    else:
        form_data = request.data  

    assets = [
        {"id": 1, "name": "Asset 1", "value": 100},
        {"id": 2, "name": "Asset 2", "value": 200},
    ]
    return Response(assets, status=status.HTTP_200_OK)

