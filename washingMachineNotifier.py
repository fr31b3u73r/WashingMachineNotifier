#!/usr/bin/python3

from xml.etree.ElementTree import parse
from urllib.request import urlopen
from pushover import Pushover
import hashlib
import time

# configuration
FRITZBOX_PASSWORD = ''
FRITZBOX_BASE_URL = ''
DEVICE_AIN = ''
PUSHOVER_USER_KEY = ''
PUSHOVER_APP_KEY = ''
POWER_THRESHOLD = 1500
POLL_FREQUENCY = 30
POLL_TIMES = 4
MESSAGE_TITLE_WASH_CYCLE_STARTED = 'Washing machine turned on'
MESSAGE_TEXT_WASH_CYCLE_STARTED = 'Your laundry will be washed'
MESSAGE_TITLE_WASH_CYCLE_ENDED = 'Wash cycle ended'
MESSAGE_TEXT_WASH_CYCLE_ENDED = 'Please grab your laundry'

# global vars
is_running = False
counter = 0


def get_sid():
	fb = urlopen(FRITZBOX_BASE_URL + 'login_sid.lua')
	dom = parse(fb)
	sid = dom.findtext('./SID')
	challenge = dom.findtext('Challenge')
	if sid == '0000000000000000':
		md5 = hashlib.md5()
		md5.update(challenge.encode('utf-16le'))
		md5.update('-'.encode('utf-16le'))
		md5.update(FRITZBOX_PASSWORD.encode('utf-16le'))
		response = challenge + '-' + md5.hexdigest()
		url = FRITZBOX_BASE_URL + 'login_sid.lua?&response=' + response
		fb = urlopen(url)
		dom = parse(fb)
		sid = dom.findtext('./SID')

	if sid == '0000000000000000':
		raise PermissionError('access denied')

	return sid

def get_power():
	global sid
	main_url = FRITZBOX_BASE_URL + "webservices/homeautoswitch.lua?sid="
	url = main_url + sid + '&switchcmd=getswitchpower&ain=' + DEVICE_AIN
	fb = urlopen(url)
	power = str(fb.read())
	#cut off 'b' at start and '\n' on end of power
	power = power[2:-3]
	return power

po = Pushover(PUSHOVER_APP_KEY)
po.user(PUSHOVER_USER_KEY)
sid = get_sid()

while True:
	power = get_power()

	if is_running == False and int(power) > POWER_THRESHOLD:
		msg = po.msg(MESSAGE_TEXT_WASH_CYCLE_STARTED)
		msg.set("title", MESSAGE_TITLE_WASH_CYCLE_STARTED)
		po.send(msg)
		is_running = True

	if is_running == True and int(power) < POWER_THRESHOLD:
		counter += 1

	if is_running == True and int(power) > POWER_THRESHOLD:
		counter = 0

	if counter == POLL_TIMES:
		msg = po.msg(MESSAGE_TEXT_WASH_CYCLE_ENDED)
		msg.set("title", MESSAGE_TITLE_WASH_CYCLE_ENDED)
		po.send(msg)
		is_running = False
		counter = 0

	time.sleep(POLL_FREQUENCY)