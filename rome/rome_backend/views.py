from django.shortcuts import render
from django.http import HttpResponse
import time
from midjourney.receiver import Receiver
from midjourney.sender import Sender


# Create your views here.
def index(request):
    sender = Sender()
    sender.send(f"Can you generate me an image of Link from the Legend of Zelda. ")
    receiver = Receiver()
    receiver.main()
    return render(request, "../frontend/index.html")
    