import time
import random
from collections import deque

# MOTOR (PLANT)

class Motor:
    def __init__(self):
        self.speed = 0.0  # RPM

    def update(self, pwm):
        # simple first-order motor model
        self.speed += 0.1 * (pwm - self.speed)
        return self.speed

# ENCODER (NOISY SENSOR)

class Encoder:
    def __init__(self, noise_std=1.0):
        self.noise_std = noise_std

    def read(self, true_speed):
        noise = random.gauss(0, self.noise_std)
        return true_speed + noise


# MOVING AVERAGE FILTER
class MovingAverageFilter:
    def __init__(self, window_size=5):
        self.window = deque(maxlen=window_size)

    def filter(self, value):
        self.window.append(value)
        return sum(self.window) / len(self.window)

# SETUP
motor = Motor()
encoder = Encoder(noise_std=1.0)
filter = MovingAverageFilter(window_size=5)

desired_speed = 120.0  # RPM

kp, ki, kd = 0.6, 0.05, 0.1
integral = 0.0
prev_error = 0.0

MAX_PWM = 100
MIN_PWM = -100

dt = 0.2  # control loop time step



# CONTROL LOOP
for step in range(50):

    measured_speed = encoder.read(motor.speed)
    filtered_speed = filter.filter(measured_speed)

    error = desired_speed - filtered_speed
    derivative = (error - prev_error) / dt
    integral_candidate = integral + error * dt

    raw_control = (
        kp * error +
        ki * integral_candidate +
        kd * derivative
    )

    control = max(min(raw_control, MAX_PWM), MIN_PWM)\
         
    if control == raw_control:
        integral = integral_candidate

    motor.update(control)

    prev_error = error

    print(
        f"Step {step:02d} | "
        f"True Speed: {motor.speed:7.2f} | "
        f"Measured: {measured_speed:7.2f} | "
        f"Filtered: {filtered_speed:7.2f} | "
        f"Control: {control:7.2f}"
    )

    time.sleep(dt)
