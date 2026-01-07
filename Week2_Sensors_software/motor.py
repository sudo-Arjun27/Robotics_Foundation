class motor:
    def __init__(self):
        self.speed = 0

    def speedinput(self):
        x=int(input("Enter the speed of the motor:"))
        return x

    def update(self, speed):
        self.speed = speed

        print(f"Motor speed set to {self.speed}")

m = motor()
speed = m.speedinput()
m.update(speed)


    