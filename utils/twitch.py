import re
import urllib.parse

def obter_slug(link_clip: str):
    '''
    Analisa input de link de um clip, obtendo o seu id
    '''
    if 'twitch' in link_clip:
        padrao_clip = [
        r"^(?P<slug>[A-Za-z0-9]+(?:-[A-Za-z0-9_-]{16})?)$",
        r"^(https://www.)?twitch.tv/\w+/clip/(?P<slug>[A-Za-z0-9]+(?:-[A-Za-z0-9_-]{16})?)(\?.+)?$",
        r"^https://(www.)?twitch.tv/\w+/clip/(?P<slug>[A-Za-z0-9]+(?:-[A-Za-z0-9_-]{16})?)(\?.+)?$",
        r"^(https://)?clips.twitch.tv/(?P<slug>[A-Za-z0-9]+(?:-[A-Za-z0-9_-]{16})?)(\?.+)?$",
        r"^https://clips.twitch.tv/(?P<slug>[A-Za-z0-9]+(?:-[A-Za-z0-9_-]{16})?)(\?.+)?$"]
        for padrao in padrao_clip:
            match = re.match(padrao, link_clip)
            if match:
                return match.group('slug')
            
def encodar_string(string):
    encoded_string = string.encode('utf-8')
    return urllib.parse.quote_plus(encoded_string)

