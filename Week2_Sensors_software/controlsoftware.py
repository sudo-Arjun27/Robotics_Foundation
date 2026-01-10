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


# -------------------------
# SETUP
# -------------------------
motor = Motor()
encoder = Encoder()

MAX_PWM = 100        # actuator saturation limits
MIN_PWM = -100

dt = 0.2             # control loop timestep


# -------------------------
# OPEN LOOP TEST
# -------------------------
for _ in range(20):
    speed = motor.update(pwm=100)
    ticks = encoder.update(speed)
    print(f"Speed: {speed:.2f} RPM | Encoder ticks: {ticks}")
    time.sleep(dt)


# -------------------------
# CLOSED LOOP WITH PID
# -------------------------
desired_speed = 120  # RPM

kp, ki, kd = 0.6, 0.05, 0.1
integral = 0.0
prev_error = 0.0

motor = Motor()   # reset motor


for _ in range(40):
    error = desired_speed - motor.speed

    # --- Anti-windup: only integrate if NOT saturated ---
    integral_candidate = integral + error * dt

    derivative = (error - prev_error) / dt

    # raw PID output (what controller WANTS)
    raw_control = kp*error + ki*integral_candidate + kd*derivative

    # --- Actuator saturation ---
    control = max(min(raw_control, MAX_PWM), MIN_PWM)

    # apply anti-windup condition
    if control == raw_control:
        integral = integral_candidate

    motor.update(control)

    prev_error = error

    print(
        f"Speed: {motor.speed:.2f} | "
        f"Control: {control:.2f} | "
        f"Error: {error:.2f}"
    )

    time.sleep(dt)
