# WashingMachineNotifier
[![Python](https://img.shields.io/badge/python-3-brightgreen.svg)]() [![Donate](https://img.shields.io/badge/donate-PayPal-brightgreen.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5654A67GA3GHA)

Get Pushover messages when washing machine has ended using FRITZ!DECT 200

**You need a Pushover account, Pushover App for desired plattform and FRITZ!DECT 200 along with Fritzbox!**

*This python script sends push messages using Pushover when your laundry is done. FRITZ!DECT 200 and Fritzbox is needed as hardware. Tested on Raspberry Pi 3.*

## Setup
Install Python 3 and required libraries, register Pushover account, install according app, then modify configuration on top of script. Power threshold must be given in mW, poll frequency in seconds. Device AIN can be seen in Fritzbox web interface, please only use number without dashes etc.
Please run a wash cycle first and log your values in Fritzbox web interface - they can be different from machine to machine!