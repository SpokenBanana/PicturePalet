import twitter
from PIL import Image
import urllib
import io
from picture_pallet import Palette

last = None
with open('last.txt', 'r+') as f:
    last = f.readline().strip()

api = twitter.Api(consumer_key='faqiNoOyUonfihuaxeT7Grd94',
                  consumer_secret='QLBEHu2lqJqzcgREF9HwQswevKRZ7j86uErwiTQ0El4SGCKYAj',
                  access_token_key='3478266803-RLjVpSVpUfs4GvnlE7MEizMfS94zdbSIc1bVdGd',
                  access_token_secret='llSbkP6PP63PaWkHQOeT9A0BkpmQKbeSoyVSU8xp8MfNr')


def reply_to(m):
    fd = urllib.urlopen(m['media'][0]['media_url_https'])
    image_file = io.BytesIO(fd.read())
    im = Image.open(image_file).convert('RGB')

    fd = urllib.urlopen(m['media'][1]['media_url_https'])
    image_file = io.BytesIO(fd.read())
    im2 = Image.open(image_file).convert('RGB')

    palette = Palette(im, im2).generate_picture()

    api.PostMedia('@%s' % m['user']['screen_name'], palette, in_reply_to_status_id=m['id'])

mentions = api.GetMentions(10, since_id=last)

print "{0:d} mentions.".format(len(mentions))

for mention in mentions:
    asdict = mention.AsDict()
    print 'replying to %s' % asdict['user']['screen_name']
    reply_to(asdict)
    with open('last.txt', 'w') as f:
        f.write(str(asdict['id']))
    print 'replied to %s' % asdict['user']['screen_name']
