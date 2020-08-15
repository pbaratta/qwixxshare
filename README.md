# QuixxShare

> A quick, shared online implementation for a quick game

Quixx is a 15 minute dice game for 2-5 players. Players take turns rolling 6 dice and marking points on their scoresheets.

Playing this game over a video chat remotely is quite doable, but one camera has to be dedicated on the dice rolls, and only the associated party has any control of that input. This project solves one specific problem: letting any remote player control the dice, with all players seeing the results.

## Use Case
- Everyone has a paper scoresheet and a pencil
- Remote players connect via videochat and also the quixxshare server
- Players identify themselves
- Players take turns hitting the "Roll" button
- Everyone can see the results of the roll

Not extremely useful, but this provides the framework to share any gameplay between any number of remote clients. I needed a practice programming project, and this is the first idea I came up with.

## Install
My implementation is run on a django asgi server. It uses the channels package with a redis channel layer to pass messages between the different client connections. On the front-end it is pretty simple javascript for now.

To get the server up-and-running:

1. clone git repo (`git clone https://github.com/pbaratta/quixxshare.git`)
1. optional: create a new virtual environment (`python3 -m venv venv` and `source venv/bin/activate`)
1. install pip requirements (`pip install -r requirements.txt`)
1. [install docker](https://docs.docker.com/engine/install/ubuntu/), then download and run redis (`docker run -p 6379:6379 -d redis:5`)
1. run the webserver (`python manage.py runserver 0.0.0.0:8000` or `daphne -b 0.0.0.0 -p 8000 mysite.asgi:application`)
1. load "localhost:8000/quixx/"
