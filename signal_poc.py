from django.db.models.signals import post_save
from django.dispatch import receiver


import django.dispatch
pizza_done = django.dispatch.Signal(providing_args=["toppings", "size"])

# http://127.0.0.1:8080/signal_poc/
# 1. This file define the customized signal and the receiver
# 2. the handler for url signal_poc send the signal
def callback(sender, **kwargs):
    print("In the callback to test the customize signal")
    print(sender, kwargs)
pizza_done.connect(callback)
# You can also specify the sender in connect()
# from app01.views import signal_poc
# pizza_done.connect(callback, sender=signal_poc)

