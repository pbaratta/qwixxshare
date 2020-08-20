import django
import json
import pytest
import asyncio
from django.test import override_settings
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter

import qwixx.routing

async def create_ws_connex(room_name):
	url = f"/ws/qwixx/{room_name}/"

	routed = URLRouter(qwixx.routing.websocket_urlpatterns)
	communicator = WebsocketCommunicator(routed, url)
	connected, _ = await communicator.connect()
	assert connected
	return communicator


@pytest.mark.asyncio
async def test_qwixx_game_consumer_connex():
	ROOM_NAME = "UNCOMMON_WORD_HERE"
	USER_NAME = 'UNCOMMON_NAME_HERE'
	NUM_DICE = 6
	SIDES = 6

	communicator = await create_ws_connex(ROOM_NAME)

	json_ask = {
		'event': 'roll_ask',
		'user_source': USER_NAME,
		'num_dice': NUM_DICE,
	}

	await communicator.send_to(text_data=json.dumps(json_ask))

	response = await communicator.receive_from()
	json_resp = json.loads(response)

	assert json_resp['event'] == 'roll_broadcast'
	assert json_resp['user_source'] == USER_NAME
	assert json_resp['sides'] == SIDES
	assert json_resp['num_dice'] == NUM_DICE

	roll = json_resp['roll']
	assert len(roll) == NUM_DICE
	assert all(1 <= dice <= SIDES for dice in roll)

	await communicator.disconnect()


@pytest.mark.asyncio
async def test_qwixx_game_consumer_huge_num_dice():
	ROOM_NAME = "UNCOMMON_WORD_HERE"
	USER_NAME = 'UNCOMMON_NAME_HERE'
	HUGE_NUM_DICE = 1000000

	communicator = await create_ws_connex(ROOM_NAME)

	json_ask = {
		'event': 'roll_ask',
		'user_source': USER_NAME,
		'num_dice': HUGE_NUM_DICE,
	}

	await communicator.send_to(text_data=json.dumps(json_ask))

	response = await communicator.receive_from()
	json_resp = json.loads(response)

	assert json_resp['num_dice'] < HUGE_NUM_DICE  # should we test that it's only 100??
	assert len(json_resp['roll']) == json_resp['num_dice']

	await communicator.disconnect()
