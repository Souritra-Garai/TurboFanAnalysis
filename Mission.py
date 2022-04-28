import numpy as np

from Aircraft import Aircraft
from Turbofan_Engine import TurboFanEngine

speed_takeoff = 150 # m / s
speed_landing = 150 # m / s

ratio_ascent    = 3.0
ratio_descent   = 3.0

class Mission :

    def __init__(self) -> None:
        
        self.distance   = 0.0   # m
        self.altitude   = 0.0   # m
        
        self.speed      = 0.0   # m / s

        self.flag = True
        self.time_flight = 0.0      # s
        self.fuel_consumed = 0.0    # kg
        
        pass

    def takeoff(self, aircraft:Aircraft, engine:TurboFanEngine, delta_t = 1.0) :

        time_takeoff = self.altitude * np.sqrt(ratio_ascent**2 + 1.0) / speed_takeoff

        num_iter = np.max(time_takeoff / delta_t)

        delta_t = time_takeoff / num_iter

        altitude = 0.0

        for i in range(num_iter) :

            initial_fuel_level = aircraft.mass_fuel

            self.flag = np.bitwise_and(aircraft.fly_aircraft(delta_t, speed_takeoff, altitude, engine, 'takeoff'), self.flag)

            altitude = altitude + speed_takeoff * delta_t / np.sqrt(ratio_ascent**2 + 1.0)

            final_fuel_level = aircraft.mass_fuel

            self.fuel_consumed = initial_fuel_level - final_fuel_level

            self.time_flight = self.time_flight + delta_t

        return self.flag

    def landing(self, aircraft:Aircraft, engine:TurboFanEngine, delta_t = 1.0) :

        time_landing = self.altitude * np.sqrt(ratio_descent**2 + 1.0) / speed_landing

        num_iter = np.max(time_landing / delta_t)

        delta_t = time_landing / num_iter

        altitude = 0.0

        for i in range(num_iter) :

            initial_fuel_level = aircraft.mass_fuel

            self.flag = np.bitwise_and(aircraft.fly_aircraft(delta_t, speed_landing, altitude, engine, 'landing'), self.flag)

            altitude = altitude + speed_landing * delta_t / np.sqrt(ratio_descent**2 + 1.0)

            final_fuel_level = aircraft.mass_fuel

            self.fuel_consumed = initial_fuel_level - final_fuel_level

            self.time_flight = self.time_flight + delta_t

        return self.flag

    def landing(self, aircraft:Aircraft, engine:TurboFanEngine, delta_t = 1.0) :

        time_landing = self.altitude * np.sqrt(ratio_descent**2 + 1.0) / speed_landing

        num_iter = np.max(time_landing / delta_t)

        delta_t = time_landing / num_iter

        altitude = 0.0

        for i in range(num_iter) :

            initial_fuel_level = aircraft.mass_fuel

            self.flag = np.bitwise_and(aircraft.fly_aircraft(delta_t, speed_landing, altitude, engine, 'landing'), self.flag)

            altitude = altitude + speed_landing * delta_t / np.sqrt(ratio_descent**2 + 1.0)

            final_fuel_level = aircraft.mass_fuel

            self.fuel_consumed = initial_fuel_level - final_fuel_level

            self.time_flight = self.time_flight + delta_t

        return self.flag

    