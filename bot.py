import twitter
from PIL import Image
import urllib
import io
from picture_pallet import Palette

api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')


def get_last():
    with open('last.txt', 'r+') as f:
        last = f.readline().strip()
    return last


def reply_to(m):
    fd = urllib.urlopen(m['media'][0]['media_url_https'])
    image_file = io.BytesIO(fd.read())
    im = Image.open(image_file).convert('RGB')

    fd = urllib.urlopen(m['media'][1]['media_url_https'])
    image_file = io.BytesIO(fd.read())
    im2 = Image.open(image_file).convert('RGB')

    palette = Palette(im, im2).generate_picture()

    api.PostMedia('@%s' % m['user']['screen_name'], palette, in_reply_to_status_id=m['id'])


def start():
    last = get_last()

    mentions = api.GetMentions(10, since_id=last)

    print "{0:d} mentions.".format(len(mentions))

    for mention in mentions:
        asdict = mention.AsDict()
        print 'replying to %s' % asdict['user']['screen_name']
        reply_to(asdict)
        with open('last.txt', 'w') as f:
            f.write(str(asdict['id']))
        print 'replied to %s' % asdict['user']['screen_name']

start()
