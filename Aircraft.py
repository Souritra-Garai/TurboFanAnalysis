import numpy as np

from Turbofan_Engine import TurboFanEngine
from ambiance import Atmosphere, CONST

class Aircraft :

    def __init__(self) -> None:
        
        self.area_inlet     = 0.0 # m2
        self.area_wing      = 0.0 # m2

        self.mass_structure = 0.0 # kg
        self.mass_payload   = 0.0 # kg
        self.mass_fuel      = 0.0 # kg

        self.C_D0   = 0.0
        self.k_1    = 0.0
        self.k_2    = 0.0

        self.load_factor = {
            'cruise'    : 1.0,
            'takeoff'   : 1.0,
            'landing'   : 1.0
        }
        
        pass

    def getMass(self) :

        return self.mass_fuel + self.mass_payload + self.mass_structure

    def getDragCoefficient(self, C_L) :

        return self.C_D0 + self.k_1 * (C_L**2) + self.k_2 * C_L

    def getLift(self, speed, air:Atmosphere, flight_mode = 'cruise') :

        return self.load_factor[flight_mode] * self.getMass() * air.grav_accel

    def fly_aircraft(self, time, speed, altitude, engine:TurboFanEngine, flight_mode = 'cruise') :

        air = Atmosphere(altitude)
        
        engine.performAnalysis(speed, air)

        TSFC = engine.getSpecificFuelConsumtionRates()[..., 1]

        dynamic_pressure = 0.5 * air.density * (speed ** 2)

        C_L = self.getLift(speed, air, flight_mode) / (dynamic_pressure * self.area_wing)

        C_D = self.getDragCoefficient(C_L)

        self.mass_fuel = self.mass_fuel - self.getMass() * (1.0 - np.exp(- C_L * air.grav_accel * time / (C_D * TSFC)))

        return 0.5 * C_D * dynamic_pressure * self.area_wing <= engine.getSpecificThrusts()[..., 0] * air.density * speed * self.area_inlet

if __name__ == '__main__' :

    aircraft = Aircraft()

    aircraft.area_inlet = np.pi * ((2.5 / 2) ** 2)  # m2
    aircraft.area_wing  = 102.0 # m2

    aircraft.mass_fuel = 21.685E3       # kg
    aircraft.mass_payload = 20.882E3    # kg
    aircraft.mass_structure = 41.145E3  # kg

    aircraft.C_D0 = 0.024
    aircraft.k_1 = 0.0366

    aircraft.load_factor['takeoff'] = 3.04
    aircraft.load_factor['landing'] = 1.2
    
    engine = TurboFanEngine()

    engine.setFuelProperties(42.7984E6, 1.33, 1155.5568)
    engine.setInletOutletProperties(0.99, 0.99, 0.99)
    engine.setBurnerProperties(0.96, 0.99)
    engine.setCompressorProperties(36, 0.9)
    engine.setFanProperties(1.7, 0.89)
    engine.setTurbineProperties(1666.67, 0.89, 0.99)
    engine.setBypassRatio(8)
    engine.setExitPressureRatios(0.9, 0.9)

    engine.initializeProblem()

    flight_conditions = Atmosphere(12E3)
    flight_speed = 0.8 * flight_conditions.speed_of_sound

    print(aircraft.fly_aircraft(10, flight_speed, 12E3, engine, 'cruise'))