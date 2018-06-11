import twitter
from PIL import Image
import urllib
import io
import os
from picture_pallet import Palette
from firebase import firebase
from apscheduler.schedulers.blocking import BlockingScheduler

api = twitter.Api(consumer_key=os.environ['TWITTER_KEY'],
                  consumer_secret=os.environ['TWITTER_SECRET'],
                  access_token_key=os.environ['TWITTER_TOKEN'],
                  access_token_secret=os.environ['TWITTER_TOKEN_SECRET'])
cursor = firebase.FirebaseApplication(os.environ['FIREBASE_URL'])
sched = BlockingScheduler()


def get_last():
    last = cursor.get('', 'last', connection=None)
    return last if last else None


def get_image(mention_media):
    fd = urllib.request.urlopen(mention_media['media_url_https'])
    image_file = io.BytesIO(fd.read())
    return Image.open(image_file).convert('RGB')


def reply_to(mention):
    if len(mention['media']) < 2:
        api.PostUpdate('Sorry @{}, I need two pictures!'.format(
            mention['user']['screen_name']),
            in_reply_to_status_id=mention['id'])
        return

    im = get_image(mention['media'][0])
    im2 = get_image(mention['media'][1])

    palette = Palette(im, im2).generate_picture(
        file_name='{}.jpg'.format(mention['id']))

    api.PostUpdate('@{}'.format(mention['user']['screen_name']),
                   in_reply_to_status_id=mention['id'], media=palette)


@sched.scheduled_job('interval', minutes=10)
def start():
    last = get_last()
    mentions = api.GetMentions(since_id=last)

    print("{0:d} mentions.".format(len(mentions)))

    for mention in mentions:
        as_dict = mention.AsDict()
        print('replying to {}'.format(as_dict['user']['screen_name']))
        reply_to(as_dict)
        print('replied to {}'.format(as_dict['user']['screen_name']))

    # keep track of the last mention replied to
    if len(mentions):
        cursor.put('', 'last', str(mentions[0].id), connection=None)


if __name__ == '__main__':
    sched.start()
