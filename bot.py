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


def get_image(mention_media):
    fd = urllib.urlopen(mention_media['media_url_https'])
    image_file = io.BytesIO(fd.read())
    return Image.open(image_file).convert('RGB')


def reply_to(m):
    if len(m['media']) < 2:
        api.PostUpdate('Sorry @%s! I need two pictures!', in_reply_to_status_id=m['id'])
        return

    im = get_image(m['media'][0])
    im2 = get_image(m['media'][1])

    palette = Palette(im, im2).generate_picture()

    api.PostMedia('@%s' % m['user']['screen_name'], palette, in_reply_to_status_id=m['id'])


def start():
    last = get_last()

    mentions = api.GetMentions(10, since_id=last)

    print "{0:d} mentions.".format(len(mentions))

    for mention in mentions:
        as_dict = mention.AsDict()
        print 'replying to %s' % as_dict['user']['screen_name']
        reply_to(as_dict)

        # keep track of the last mention replied to so we don't reply to someone twice
        with open('last.txt', 'w') as f:
            f.write(str(as_dict['id']))
        print 'replied to %s' % as_dict['user']['screen_name']

if __name__ == '__main__':
    start()
