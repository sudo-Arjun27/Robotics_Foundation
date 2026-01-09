import time

class Motor:
    def __init__(self):
        self.speed = 0.0  # RPM

    def update(self, pwm):
        # simple motor model
        self.speed += 0.1 * (pwm - self.speed)
        return self.speed
    
class Encoder:
    def __init__(self):
        self.ticks = 0

    def update(self, speed):
        self.ticks += int(speed * 0.5)
        return self.ticks


motor = Motor()
encoder = Encoder()


for _ in range(20):
    speed = motor.update(pwm=100)
    ticks = encoder.update(speed)
    print(f"Speed: {speed:.2f} RPM | Encoder ticks: {ticks}")
    time.sleep(0.2)

desired_speed = 120  # RPM

for _ in range(30):
    speed = motor.update(pwm=desired_speed)
    error = desired_speed - speed
    print(f"Speed: {speed:.2f} | Error: {error:.2f}")
    time.sleep(0.2)

kp, ki, kd = 0.6, 0.05, 0.1
integral = 0
prev_error = 0

motor = Motor()

for _ in range(40):
    error = desired_speed - motor.speed
    integral += error
    derivative = error - prev_error

    control = kp*error + ki*integral + kd*derivative
    motor.update(control)

    prev_error = error
    print(f"Speed: {motor.speed:.2f} | Control: {control:.2f}")
    time.sleep(0.2)
