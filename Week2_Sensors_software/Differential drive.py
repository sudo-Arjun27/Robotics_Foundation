import time
import random
from collections import deque
import math

# -------------------------
# MOTOR (PLANT)
# -------------------------
class Motor:
    def __init__(self):
        self.speed = 0.0  # RPM

    def update(self, pwm):
        self.speed += 0.1 * (pwm - self.speed)
        return self.speed


# -------------------------
# ENCODER (NOISY SENSOR)
# -------------------------
class Encoder:
    def __init__(self, noise_std=1.0):
        self.noise_std = noise_std

    def read(self, true_speed):
        return true_speed + random.gauss(0, self.noise_std)


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
# MEASUREMENT DELAY
# -------------------------
class MeasurementDelay:
    def __init__(self, delay_steps=3):
        self.buffer = deque(maxlen=delay_steps)

    def apply(self, value):
        self.buffer.append(value)
        if len(self.buffer) < self.buffer.maxlen:
            return self.buffer[0]
        return self.buffer.popleft()


# -------------------------
# PID CONTROLLER
# -------------------------
class PID:
    def __init__(self, kp, ki, kd, max_out):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_out = max_out
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, target, measured, dt):
        error = target - measured
        derivative = (error - self.prev_error) / dt
        integral_candidate = self.integral + error * dt

        raw = (
            self.kp * error +
            self.ki * integral_candidate +
            self.kd * derivative
        )

        output = max(min(raw, self.max_out), -self.max_out)

        if output == raw:  # anti-windup
            self.integral = integral_candidate

        self.prev_error = error
        return output


# -------------------------
# ROBOT PARAMETERS
# -------------------------
WHEEL_RADIUS = 0.05     # meters
WHEEL_BASE = 0.3        # meters
RPM_PER_MPS = 60 / (2 * math.pi * WHEEL_RADIUS)

dt = 0.1
MAX_PWM = 100

# -------------------------
# ROBOT SETUP
# -------------------------
left_motor = Motor()
right_motor = Motor()

left_encoder = Encoder(noise_std=1.0)
right_encoder = Encoder(noise_std=1.0)

left_filter = MovingAverageFilter(5)
right_filter = MovingAverageFilter(5)

left_delay = MeasurementDelay(3)
right_delay = MeasurementDelay(3)

left_pid = PID(0.6, 0.05, 0.1, MAX_PWM)
right_pid = PID(0.6, 0.05, 0.1, MAX_PWM)


# -------------------------
# COMMAND: LINEAR & ANGULAR VELOCITY
# -------------------------
v = 0.6     # m/s (forward)
omega = 0.8 # rad/s (turn)

# Convert (v, ω) → wheel RPM
left_target_rpm = RPM_PER_MPS * (v - (omega * WHEEL_BASE / 2))
right_target_rpm = RPM_PER_MPS * (v + (omega * WHEEL_BASE / 2))


# -------------------------
# CONTROL LOOP
# -------------------------
for step in range(80):

    # --- Left wheel sensing ---
    l_meas = left_encoder.read(left_motor.speed)
    l_filt = left_filter.filter(l_meas)
    l_delay = left_delay.apply(l_filt)

    # --- Right wheel sensing ---
    r_meas = right_encoder.read(right_motor.speed)
    r_filt = right_filter.filter(r_meas)
    r_delay = right_delay.apply(r_filt)

    # --- PID control ---
    l_pwm = left_pid.compute(left_target_rpm, l_delay, dt)
    r_pwm = right_pid.compute(right_target_rpm, r_delay, dt)

    # --- Apply control ---
    left_motor.update(l_pwm)
    right_motor.update(r_pwm)

    print(
        f"Step {step:02d} | "
        f"L RPM: {left_motor.speed:7.2f} | "
        f"R RPM: {right_motor.speed:7.2f}"
    )

    time.sleep(dt)
