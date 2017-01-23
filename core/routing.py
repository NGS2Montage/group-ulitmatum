from channels.routing import route, include
from anagrams.consumers import anagrams_add, anagrams_message, anagrams_disconnect

anagrams_routing = [
    route("websocket.connect", anagrams_add),
    route("websocket.receive", anagrams_message),
    route("websocket.disconnect", anagrams_disconnect),
]

channel_routing = [
    # You can use a string import path as the first argument as well.
    include(anagrams_routing, path=r"^/anagrams"),
]
