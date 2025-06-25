from car import Car

car1 = Car(p=0, v=0, a=10)
car2 = Car(p=0, v=10, a=10)

dt=0.1
for t in range(10):
    car1.update(dt)
    car2.update(dt)
    print(f"t={t*dt:.1f}s | Car1: {car1} | Car2: {car2}")

