#Car tracker median

Will allow webasto on/off from mobile app. Webasto has a v-bus line, that can be connected with microcontroller.
Embedded system with STM32, HM-10(BLE), U-box GNSS, IMU, and NEOWAY M590(SMS, GPRS) will be installed to car.
Raspberry pi will be in control of Projector(SANYO PLC-WXU700A) in car. Projector can be controller through ethernet.

Microcontroller keeps track of 2 leisure batteries from analong pin. These batteries are connected to cars main battery in parralel. 
When car charges main battery, also leisure batteries are being charged. One relay is required between main and leisure batteries.
This will shut down connection to main battery when car is not running.

Knowing battery voltage is essential. When battery voltage goes under 12.3V microcontroller will tell raspberry pi to shutdown projector. Once projector is shutdown, raspberry pi will turn it self off and microconroller turns of all unnecessary processes. 
Unnecessary processes such as:
- GPRS, SMS needs to stay on to report position if car moves
- Bluetooth
- More.. once projec goes forward

##References
1. https://docs.docker.com/compose/django/
2. https://www.django-rest-framework.org/tutorial/quickstart/