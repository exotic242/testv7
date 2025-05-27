
from flask import request
from user_agents import parse

def get_client_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr)

def get_device_info():
    ua_string = request.headers.get("User-Agent", "")
    ua = parse(ua_string)
    return {
        "browser": ua.browser.family,
        "os": ua.os.family,
        "device": ua.device.family
    }
