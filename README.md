# Car tracker median
## Brief/Idea
Allows webasto on/off from mobile app. Webasto has a v-bus line, that can be connected with microcontroller.
Embedded system with STM32, HM-10(BLE), U-box GNSS, IMU, and NEOWAY M590(SMS, GPRS) will be installed to car.
Raspberry pi will be in control of Projector(SANYO PLC-WXU700A) in car. Projector can be controller through ethernet.

Microcontroller keeps track of 2 leisure batteries from analong pin. These batteries are connected to cars main battery in parralel. 
When car charges main battery, also leisure batteries are being charged. One relay is required between main and leisure batteries.
This will shut down connection to main battery when car is not running.

Knowing battery voltage is essential. When battery voltage goes under 12.3V microcontroller will tell raspberry pi to shutdown projector. Once projector is shutdown, raspberry pi will turn it self off and microconroller turns of all unnecessary processes. If projector is terminated while lamp is warm/projecting, this can cause permanent damage to lamp. Lamp neads to be cooled down in controlled manner.

### Low power mode, shut following:
- GPRS. !SMS needs to stay on to report position if car moves
- Bluetooth.
- More.. once projec goes forward.

Server is hosted on AWS EC2 instance.

## Test log
    600W inverter is powerfull enough to start projector.
    600W inverter is not powerfull enough to start car fridge -> need seperate and more powerfull inverter for fridge

## References
1. https://docs.docker.com/compose/django/
2. https://www.django-rest-framework.org/tutorial/quickstart/
3. https://www.freertos.org/
4. https://www.st.com/en/embedded-software/stm32-standard-peripheral-libraries.html
5. https://aws.amazon.com/ec2/instance-types/
