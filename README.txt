A simple script to indicate when one or more users is connected to a local Mumble server.

Change the gpio_pin and mumble_port variables at the top of main based on your setup.

An attached LED will turn on/off once per second if at least one user is connected. The script will also log the IPs of all users connected to the server whenever the set of users changes.
