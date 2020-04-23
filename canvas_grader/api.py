import os
from canvasapi import Canvas
import json

def GetCurrentUser(domain, token):
    return GetUserByUserId(domain, token, "self")

def GetUserByUserId(domain, token, user_id):
    canvas = GetCanvas(domain, token)
    user = canvas.get_user(user_id)
    return user

def GetCanvas(domain, token):
    if not domain.startswith("https://"):
        domain = "https://" + domain
    domain = os.path.join(domain, "api", "v1")
    canvas = Canvas(domain, token)
    return canvas

