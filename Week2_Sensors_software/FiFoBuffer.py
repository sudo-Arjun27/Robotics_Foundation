import time
import random
from collections import deque

# -------------------------
# MOTOR (PLANT)
# -------------------------
class Motor:
    def __init__(self):
        self.speed = 0.0  # RPM

    def update(self, pwm):
        # simple first-order motor model
        self.speed += 0.1 * (pwm - self.speed)
        return self.speed


# -------------------------
# ENCODER (NOISY SENSOR)
# -------------------------
class Encoder:
    def __init__(self, noise_std=1.0):
        self.noise_std = noise_std

    def read(self, true_speed):
        noise = random.gauss(0, self.noise_std)
        return true_speed + noise


# -------------------------
# MOVING AVERAGE FILTER
# -------------------------
class MovingAverageFilter:
    def __init__(self, window_size=5):
        self.window = deque(maxlen=window_size)

    def filter(self, value):
        self.window.append(value)
        return sum(self.window) / len(self.window)


# -------------------------
# MEASUREMENT DELAY (FIFO)
# -------------------------
class MeasurementDelay:
    def __init__(self, delay_steps=5):
        self.buffer = deque(maxlen=delay_steps)

    def apply(self, value):
        self.buffer.append(value)

        # until buffer is full, output oldest available
        if len(self.buffer) < self.buffer.maxlen:
            return self.buffer[0]

        return self.buffer.popleft()


# -------------------------
# SETUP
# -------------------------
motor = Motor()
encoder = Encoder(noise_std=1.0)
filter = MovingAverageFilter(window_size=5)

delay = MeasurementDelay(delay_steps=5)  # 👈 CHANGE THIS

desired_speed = 120.0  # RPM

kp, ki, kd = 0.6, 0.05, 0.1
integral = 0.0
prev_error = 0.0

MAX_PWM = 100
MIN_PWM = -100

dt = 0.2  # control loop timestep


# -------------------------
# CONTROL LOOP
# -------------------------
for step in range(60):

    # --- Sensor pipeline ---
    measured_speed = encoder.read(motor.speed)
    filtered_speed = filter.filter(measured_speed)
    delayed_speed = delay.apply(filtered_speed)

    # --- PID ---
    error = desired_speed - delayed_speed
    derivative = (error - prev_error) / dt
    integral_candidate = integral + error * dt

    raw_control = (
        kp * error +
        ki * integral_candidate +
        kd * derivative
    )

    # --- Actuator saturation ---
    control = max(min(raw_control, MAX_PWM), MIN_PWM)

    # --- Anti-windup ---
    if control == raw_control:
        integral = integral_candidate

    # --- Apply control ---
    motor.update(control)

    prev_error = error

    print(
        f"Step {step:02d} | "
        f"True: {motor.speed:7.2f} | "
        f"Meas: {measured_speed:7.2f} | "
        f"Filt: {filtered_speed:7.2f} | "
        f"Delay: {delayed_speed:7.2f} | "
        f"Ctrl: {control:7.2f}"
    )

    time.sleep(dt)
