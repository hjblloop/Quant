class Car:
    def __init__(self, p = 0.0, v = 0.0, a=0.0):
        self.p = p
        self.v = v
        self.a = a
    
    def update(self, dt):
        self.p += self.v * dt + 0.5 * self.a * dt**2
        self.v += self.a * dt
    
    def __str__(self):
        return f"Position: {self.p:.2f} m, Velocity: {self.v:.2f} m/s"