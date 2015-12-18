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
    with open('last.txt', 'r+') as last_file:
        last = last_file.readline().strip()
    return last


def get_image(mention_media):
    fd = urllib.urlopen(mention_media['media_url_https'])
    image_file = io.BytesIO(fd.read())
    return Image.open(image_file).convert('RGB')


def reply_to(mention):
    if len(mention['media']) < 2:
        api.PostUpdate('Sorry @%s! I need two pictures!',
                       in_reply_to_status_id=mention['id'])
        return

    im = get_image(mention['media'][0])
    im2 = get_image(mention['media'][1])

    palette = Palette(im, im2).generate_picture()

    api.PostMedia('@%s' % mention['user']['screen_name'], palette,
                  in_reply_to_status_id=mention['id'])


def start():
    last = get_last()

    mentions = api.GetMentions(1, since_id=last)

    print "{0:d} mentions.".format(len(mentions))

    for mention in mentions:
        as_dict = mention.AsDict()
        print 'replying to %s' % as_dict['user']['screen_name']
        reply_to(as_dict)

        # keep track of the last mention replied to
        with open('last.txt', 'w') as last_file:
            last_file.write(str(as_dict['id']))

        print 'replied to %s' % as_dict['user']['screen_name']


if __name__ == '__main__':
    start()
