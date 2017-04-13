#!/usr/bin/python
import psycopg2
import psycopg2.extensions

import json

from tornado.httpserver import HTTPServer
from tornado.web import *
from tornado.ioloop import IOLoop

import momoko

import logging

SESSION_DURATION_SEC = 60*60*8
PING_TIME = 10
VERSION = "2015-02-19, v2"


# dsn = 'user=root password=qwerty host=localhost port=5433 dbname=production sslmode=disable'
dsn = 'user=postgres password=123  port=5432 dbname=production sslmode=disable'
conn = psycopg2.connect(dsn)
# conn = psycopg2.connect('user=root password=qwerty port=5433 dbname=production sslmode=disable')
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

DATA_ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(DATA_ROOT, 'listener_py.log')


user_online = {}
user_times = {}
user_notification = {}
event_id = None


logging.basicConfig(filename=LOG_FILE,
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S')

logger = logging.getLogger(__name__)

def listen(ch):
    '''Listenes to a channel.'''

    logger.info("==============Starting==============\n")
    logger.info("Listener version {0} started".format(VERSION))
    curs = conn.cursor()
    curs.execute("LISTEN %s;" % ch)


@gen.coroutine
def notification_receiver(fd, events):
    '''Receives a notify message from the channel we are listening.
    Selects certain event for certain user(according to notification) from database and returnes it.
    '''
    state = conn.poll()
    if state == psycopg2.extensions.POLL_OK:
        if conn.notifies:
            notify = conn.notifies.pop()
            a = notify.payload.split()
            if len(a) != 2:
                pass
            else:
                user_id = int(a[0])
                global event_id
                event_id = a[1]

                curs = conn.cursor()
                curs.execute("SELECT events->>'{0}' FROM FEEDS WHERE USER_ID = '{1}' AND events is NOT NULL".format(event_id, user_id))
                events_found = curs.fetchall()

                global user_notification
                user_notification[user_id] = str(events_found[0][0])

class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db


class InternetEventHandler(BaseHandler):
    """
    Checks if API-TOKEN from POST request coincides with any valid token in database.
    If certain api-token is found in database, adds user object to the list of all users in dictionary.
    """
    @asynchronous
    def get(self):
        api_token = self.request.headers.get("API-TOKEN")
        self.db.execute("SELECT user_id, updated_at FROM sessions WHERE sessions.token= '{0}'".format(api_token), callback=self._done)

        self.set_header("Content-Type", "text/event-stream")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")

    def _done(self, cursor, error=None):

        user_found = cursor.fetchone()

        if user_found:
            user_id = user_found[0]
            user_time = user_found[1]

            user_agent, user_ip = get_user_info(self.request)

            logger.info("New client added: [{0}] User IP: '{1}' User-Agent: '{2}'".format(user_id, user_ip, user_agent))

            if not user_online.get(user_id):
                user_online[int(user_id)] = []

            start_session_time = time.mktime(user_time.timetuple())
            ping_queue = 1
            user_online[int(user_id)].append({'writer': self, 'timestamp': time.time(),
                                              'start_session_time': start_session_time,
                                             'user_start_time': time.time(), 'user_ip': user_ip,
                                             'user_agent': user_agent, 'online': 'true', 'ping_queue': ping_queue})

            ping = str("1" + "ping"*256)
            data = json.dumps({"ping":ping})
            self.write("event: 1111111111\ndata: {0}\n".format(data))
            #self.write("ping\n")
            self.flush()


            logger.info("Clients count: {0}\n".format(len(user_online)))

            friends_list = check_for_friends_in_db(user_id)
            write_notification_online_status(user_id, friends_list, 'true')

        else:
            logger.info("Token not found!\n")

            self.write('Token not found\n')
            self.finish()


def get_user_info(request):
    user_agent = request.headers.get("User-Agent")

    client_ip = request.headers.get("CLIENT_IP") \
                or request.headers.get("X-Real-IP") \
                or request.headers.get("Host")\
                or request.remote_ip
    return user_agent, client_ip


def write():
    """
    Parses hash with notifications. Writes notification to corresponding user, than removes notification.
    :return:
    """
    for_removing = []
    for user_id in user_notification.keys():
        if user_online.get(user_id):
            event = user_notification[user_id]
            for_removing.append(user_id)
            for user_session in user_online[user_id]:
                writer = user_session['writer']

                writer.set_header("Content-Type", "text/event-stream")
                writer.set_header("Cache-Control", "no-cache")
                writer.set_header("Connection", "keep-alive")

                writer.write("event: {0}\ndata: {1}\n\n".format(event_id, event))

                logger.info("Event for user {0} received\n".format(user_id))

                writer.flush()
    for user_id in for_removing:
        del user_notification[user_id]


def ping():
    """
    Sends 'ping' to user every predefined period of time(PING_TIME).
    :return:
    """
    current_time = int(time.time())
    for user_id, user_list in user_online.items():
        for user_sample_hash in user_list:
            time_delta = current_time - user_sample_hash['timestamp']
            if time_delta > PING_TIME:
                user_sample_hash['timestamp'] = time.time()
                writer = user_sample_hash['writer']
                if writer.request.connection.stream.closed():
                    user_list.remove(user_sample_hash)
                    if not user_online[user_id]:
                        friends_list = check_for_friends_in_db(user_id)
                        write_notification_online_status(user_id, friends_list, 'false')
                        del user_online[user_id]
                        logger.info("User {0} session finished\n".format(user_id))

                else:
                    writer.set_header("Content-Type", "text/event-stream")
                    writer.set_header("Cache-Control", "no-cache")
                    writer.set_header("Connection", "keep-alive")

                    user_sample_hash['ping_queue'] += 1
                    ping = str(str(user_sample_hash['ping_queue']) + "ping"*256)
                    data = json.dumps({"ping":ping})
                    writer.write("event: 1111111111\ndata: {0}\n".format(data))

                    #writer.write('ping\n')

                    writer.flush()


def check_for_friends_in_db(user_id):
    """
    Checks what approved frendship connections does user have.
    :param user_id:
    :return: <list> of ID's of friends
    """
    curs = conn.cursor()
    curs.execute("SELECT user_id FROM friendships "
     " WHERE friendships.approved = TRUE AND friendships.friend_id = {0}".format(user_id))
    user_found_first = curs.fetchall()
    curs.execute("SELECT friend_id FROM friendships "
     " WHERE friendships.approved = TRUE AND friendships.user_id = {0}".format(user_id))
    user_found_second = curs.fetchall()
    users_online_list = list(user_found_first + user_found_second)
    friends_list = [element[0] for element in users_online_list]
    logger.debug("For user [{0}] found {1} friends\n".format(user_id, len(friends_list)))
    return friends_list



def write_notification_online_status(user_id, friends_list, status):
    """
    Sends notification to friends about status online of user.
    :param user_id:
    :param friends_list: list of ID`s of friends
    :param status: online: 'true' or 'false'
    """
    if not friends_list:
        logger.debug("Empty friend list for user with ID [{0}]. Checking skipped.".format(user_id))
    else:
        logger.debug("Processing friends list of user [{0}]. Friends list: {1}".format(user_id, friends_list))
        for friend_user_id in friends_list:
            if friend_user_id in user_online.keys():
                for user_hash in user_online[friend_user_id]:
                    logger.debug("User data: {0}\n".format(user_hash))

                    writer = user_hash['writer']

                    user_finish_data = json.dumps({"users_status": {"id": user_id, "online": status}})

                    if not user_hash['user_agent']:
                        data = "event: {0}\ndata: {1}\n".format(int(time.time()), user_finish_data)
                    else:
                        ios_user_agent = user_hash['user_agent'].find("Darwin")
                        if ios_user_agent != -1:
                            data = "event: {0}\ndata: {1}\n".format(int(time.time()), user_finish_data)
                        else:
                            data = "event: {0}\ndata: {1}\n\n".format(int(time.time()), user_finish_data)

                    writer.set_header("Content-Type", "text/event-stream")
                    writer.set_header("Cache-Control", "no-cache")
                    writer.set_header("Connection", "keep-alive")

                    writer.write(data)
                    writer.flush()
                    logger.debug(data)
            else:
                logger.debug("Friend user ID [{0}]not in user_online.keys\n".format(friend_user_id))



def scan():
    current_time = int(time.time())
    for user_id, user_list in user_online.items():
        for item in user_list:
            if current_time - item['start_session_time'] > SESSION_DURATION_SEC:
                self = item['writer']
                connection_to_be_closed, user_update_time = need_to_be_closed(self)
                if connection_to_be_closed:

                    logger.info("User {0} session expired\n".format(user_id))

                    friends_list = check_for_friends_in_db(user_id)
                    write_notification_online_status(user_id, friends_list, 'false')

                    self.finish()
                    user_list.remove(item)

                    if not user_online[user_id]:
                        del user_online[user_id]

                else:
                    item['start_session_time'] = user_update_time


def need_to_be_closed(self):
    current_time = int(time.time())
    api_token = self.request.headers.get("API-TOKEN")
    curs = conn.cursor()
    curs.execute("SELECT user_id, updated_at FROM sessions WHERE sessions.token= '{0}'".format(api_token))
    user_found = curs.fetchone()
    if user_found:
        user_time = user_found[1]
        user_update_time = time.mktime(user_time.timetuple())
        return current_time - user_update_time > SESSION_DURATION_SEC, user_update_time


class ControlEventHandler(BaseHandler):
    """
    Writes current info, such as: user ID, user IP, time when user joined, time when session updated,
    time delta between the beginning of the session and it`s update. Output appears in the form of table on
    url: /control
    """
    def get(self):
        self.write("version: {0}".format(VERSION))
        if user_online:
            for i, user_id in enumerate(user_online.keys()):
                if i == 0:
                    self.write('<table border="1"></tr><th>User ID</th><th>User IP</th><th>Time when joined/ Duration</th>'
                    '<th>Session updated at (from db)</th><th>User-Agent</th><th>OS</th></tr>')
                for user_hash in user_online[user_id]:

                    if user_hash['user_agent'] == None:
                        os = "Android"
                    else:
                        ios_user_agent = user_hash['user_agent'].find("Darwin")
                        if ios_user_agent != -1:
                            os = "IOS"
                        else:
                            os = "Android"

                    user_start_time = (datetime.datetime.fromtimestamp(user_hash['user_start_time'])).strftime("%Y-%m-%d %H:%M:%S")

                    user_start_delta = (datetime.datetime.fromtimestamp(time.time()) - datetime.datetime.fromtimestamp(user_hash['user_start_time']))
                    start_delta = time_delta_formatting(user_start_delta)

                    session_updated_at = (datetime.datetime.fromtimestamp(user_hash['start_session_time'])).strftime("%Y-%m-%d %H:%M:%S")
                    session_update_delta = (datetime.datetime.fromtimestamp(time.time()) - datetime.datetime.fromtimestamp(user_hash['start_session_time']))
                    session_delta = time_delta_formatting(session_update_delta)

                    self.write('<tr><td>{0}</td> <td>{1}</td> <td>{2} ({3})</td> <td>{4} ({5})</td><td>{7}</td><td>{8}</td></tr>'.format(user_id,
                                user_hash['user_ip'], user_start_time, start_delta, session_updated_at, session_delta,
                                start_delta, user_hash['user_agent'], os))
        self.write('</table><p>Users online: {0}</p>'.format(str(len(user_online))))


def time_delta_formatting(td):
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    seconds = td.seconds % 60
    time_delta = '%s:%s:%s' % (hours, minutes, seconds)
    return time_delta

@gen.engine
def main_cycle():
    ping()
    write()
    scan()
    time.sleep(0.001)

    IOLoop.instance().add_callback(main_cycle)


#--- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

if __name__ == '__main__':
    listen("feed")
    io_loop = tornado.ioloop.IOLoop.instance()

    application = Application([(r'/index', InternetEventHandler),
                               (r'/control', ControlEventHandler)], debug=True)

    application.db = momoko.Pool(dsn=dsn, size=1)

    io_loop.add_handler(conn.fileno(), notification_receiver, io_loop.READ)

    io_loop.add_callback(main_cycle)

    http_server = HTTPServer(application)
    http_server.listen(8887, '0.0.0.0')
    # http_server.listen(8001, 'localhost')

    io_loop.start()



