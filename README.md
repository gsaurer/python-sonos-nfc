SONOS HTTP API
==============

** Beta is no more, master is up to date with the beta now! **

**This application requires node 4.0.0 or higher!**

**This should now work on Node 6+, please let me know if you have issues**

A simple http based API for controlling your Sonos system.

There is a simple sandbox at /docs (incomplete atm)

USAGE
-----

Start by fixing your dependencies. Invoke the following command:

`npm install --production`

This will download the necessary dependencies if possible.

start the server by running

`npm start`

Now you can control your system by invoking the following commands:

	http://localhost:5005/zones
	http://localhost:5005/lockvolumes
	http://localhost:5005/unlockvolumes
	http://localhost:5005/pauseall[/{timeout in minutes}]
	http://localhost:5005/resumeall[/{timeout in minutes}]
	http://localhost:5005/preset/{JSON preset}
	http://localhost:5005/preset/{predefined preset name}
	http://localhost:5005/reindex
	http://localhost:5005/{room name}/sleep/{timeout in seconds or "off"}
	http://localhost:5005/{room name}/sleep/{timeout in seconds or "off"}
	http://localhost:5005/{room name}/{action}[/{parameter}]

Example:
