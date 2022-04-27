from time import sleep
import numpy as np

from shutil import ExecError
from ambiance import CONST, Atmosphere

def getGasConstant(gamma, c_p) :
	'''Enter c_p in J / kg - K'''
	return (gamma - 1.0) * c_p / gamma

def getHeatCapacity(gamma, R) :
	'''Enter R in J / kg - K'''
	return gamma * R / (gamma - 1.0)

def getSonicSpeed(gamma, gas_constant, temperature) :
	'''Enter gas_constant in J / kg - K and temperature in kelvin'''
	return np.sqrt(gamma * gas_constant * temperature)

def getStagnationTemperatureRatio(gamma, mach_number) :

	return 1.0 + 0.5 * (gamma - 1.0) * (mach_number**2)

def getStagnationPressureRatio(gamma, mach_number) :

	return np.float_power(
		getStagnationTemperatureRatio(gamma, mach_number),
		gamma / (gamma - 1)
	)

def getRamRecovery(mach_number) :
	'''Vectorized for array input.
	   Mach number should be an ndarray.'''
	
	# if mach_number <= 1.0 :

	#     return 1.0

	# elif mach_number <= 5.0 :

	#     return 1.0 - 0.075 * np.float_power((mach_number - 1.0), 1.35)

	# else :

	#     return 800.0 / (np.power(mach_number, 4) + 935.0)

	return  np.where(mach_number <= 1.0,
				1.0,
			# else
				np.where(mach_number <= 5.0,
					1.0 - 0.075 * np.float_power((np.fmax(mach_number, 1.0) - 1.0), 1.35),
				# else
					800.0 / (np.power(mach_number, 4) + 935.0)
				)
			)

class TurboFanEngine :

	def __init__(self) -> None:

		self._initialized = False
		self._analysis_complete = False

		pass

	def setFuelProperties(self, 
		heat_generated_from_combustion,
		gamma_of_combustion_products = CONST.kappa,
		heat_capacity_of_combustion_products = CONST.kappa * CONST.R / (CONST.kappa - 1.0)
	) :
		'''Enter heat in J / kg and heat capacity in J / kg - K'''

		if gamma_of_combustion_products > 0 :

			self._gamma_t = gamma_of_combustion_products
			self._analysis_complete = False

		else :

			raise ValueError('Gamma must be positive. Given value : ' + str(gamma_of_combustion_products))

		if heat_generated_from_combustion > 0 :

			self._h_PR = heat_generated_from_combustion
			self._analysis_complete = False

		else :

			raise ValueError('Heat generated must be positive. Given value : ' + str(heat_generated_from_combustion))

		if heat_capacity_of_combustion_products > 0 :

			self._c_pt = heat_capacity_of_combustion_products
			self._analysis_complete = False

		else :

			raise ValueError('Heat capacity must be positive. Given value : ' + str(heat_capacity_of_combustion_products))

		self._R_t = getGasConstant(self._gamma_t, self._c_pt)

		pass

	def setTurbineProperties(self,
		inlet_total_temperature : np.ndarray,
		polytropic_efficiency = 1.0,
		mechanical_efficiency = 1.0
	) :
		'''Enter temperature in kelvin'''
		if np.all(inlet_total_temperature > 0) :

			self._T_t4 = inlet_total_temperature
			self._analysis_complete = False

		else :

			raise ValueError('Temperature must be positive. Given value : ' + str(inlet_total_temperature))

		if polytropic_efficiency > 0 and polytropic_efficiency <= 1:

			self._e_t = polytropic_efficiency
			self._analysis_complete = False

		else :

			raise ValueError('Efficiency must belong to the interval (0, 1]. Given value : ' + str(polytropic_efficiency))

		if mechanical_efficiency > 0 and mechanical_efficiency <= 1:

			self._eta_m = mechanical_efficiency
			self._analysis_complete = False

		else :

			raise ValueError('Efficiency must belong to the interval (0, 1]. Given value : ' + str(mechanical_efficiency))

		pass

	def setCompressorProperties(self,
		compression_ratio : np.ndarray,
		polytropic_efficiency = 1.0
	) :

		if np.all(compression_ratio >= 1) :

			self._pi_c = compression_ratio
			self._analysis_complete = False

		else :

			raise ValueError('Compression ratio must be greater than or equal to 1. Given value : ' + str(compression_ratio))

		if polytropic_efficiency > 0 and polytropic_efficiency <= 1:

			self._e_c = polytropic_efficiency
			self._analysis_complete = False

		else :

			raise ValueError('Efficiency must belong to the interval (0, 1]. Given value : ' + str(polytropic_efficiency))

		pass

	def setFanProperties(self,
		compression_ratio : np.ndarray,
		polytropic_efficiency = 1.0
	) :

		if np.all(compression_ratio >= 1) :

			self._pi_f = compression_ratio
			self._analysis_complete = False

		else :

			raise ValueError('Compression ratio must be greater than or equal to 1. Given value : ' + str(compression_ratio))

		if polytropic_efficiency > 0 and polytropic_efficiency <= 1:

			self._e_f = polytropic_efficiency
			self._analysis_complete = False

		else :

			raise ValueError('Efficiency must belong to the interval (0, 1]. Given value : ' + str(polytropic_efficiency))

		pass

	def setInletOutletProperties(self,
		diffuser_max_total_pressure_ratio = 1.0,
		fan_nozzle_total_pressure_ratio = 1.0,
		nozzle_total_pressure_ratio = 1.0
	) :

		if diffuser_max_total_pressure_ratio > 0 and diffuser_max_total_pressure_ratio <= 1 :

			self._pi_dmax = diffuser_max_total_pressure_ratio
			self._analysis_complete = False

		else :

			raise ValueError('Pressure ratio must be in the interval (0,1]. Given value : ' + str(diffuser_max_total_pressure_ratio))

		if fan_nozzle_total_pressure_ratio > 0 and fan_nozzle_total_pressure_ratio <= 1 :

			self._pi_fn = fan_nozzle_total_pressure_ratio
			self._analysis_complete = False

		else :

			raise ValueError('Pressure ratio must be in the interval (0,1]. Given value : ' + str(fan_nozzle_total_pressure_ratio))

		if nozzle_total_pressure_ratio > 0 and nozzle_total_pressure_ratio <= 1 :

			self._pi_n = nozzle_total_pressure_ratio
			self._analysis_complete = False

		else :

			raise ValueError('Pressure ratio must be in the interval (0,1]. Given value : ' + str(nozzle_total_pressure_ratio))

		pass

	def setBurnerProperties(self,
		total_pressure_ratio = 1.0,
		efficiency = 1.0
	) :

		if total_pressure_ratio > 0 and total_pressure_ratio <= 1 :

			self._pi_b = total_pressure_ratio
			self._analysis_complete = False

		else :

			raise ValueError('Pressure ratio must be in the interval (0,1]. Given value : ' + str(total_pressure_ratio))

		if efficiency > 0 and efficiency <= 1:

			self._eta_b = efficiency
			self._analysis_complete = False

		else :

			raise ValueError('Efficiency must belong to the interval (0, 1]. Given value : ' + str(efficiency))

		pass

	def setBypassRatio(self, alpha : np.ndarray) :

		if np.all(alpha >= 0) :

			self._alpha = alpha
			self._analysis_complete = False

		else :

			raise ValueError('Mass flow ratio must be greater than or equal to 0. Given value : ' + str(alpha))

		pass

	def setExitPressureRatios(self, P0_by_P9 : np.ndarray, P0_by_P19 : np.ndarray) :

		if np.all(P0_by_P9 > 0) :

			self._P0_by_P9 = P0_by_P9
			self._analysis_complete = False

		else :

			raise ValueError('Pressure ratios (P0 / P9) must be greater than 0. Given value : ' + str(P0_by_P9))

		if np.all(P0_by_P19 > 0) :

			self._P0_by_P19 = P0_by_P19
			self._analysis_complete = False

		else :

			raise ValueError('Pressure ratios (P0 / P19) must be greater than 0. Given value : ' + str(P0_by_P19))

		pass

	def initializeProblem(self) :

		attributes = [
			'_alpha',
			'_eta_b',
			'_pi_b',
			'_pi_n',
			'_pi_fn',
			'_pi_dmax',
			'_e_f',
			'_pi_f',
			'_e_c',
			'_pi_c',
			'_eta_m',
			'_e_t',
			'_T_t4',
			'_c_pt',
			'_h_PR',
			'_gamma_t',
		]

		for attribute in attributes :

			if not hasattr(self, attribute) :

				raise AttributeError(attribute + ' not initialized.')

		self._initialized = True

		pass

	def _initializeRatios(self, M_0, air:Atmosphere) :

		self._tau_r = getStagnationTemperatureRatio(CONST.kappa, M_0)
		self._pi_r  = getStagnationPressureRatio(CONST.kappa, M_0)

		self._pi_d  = self._pi_dmax * getRamRecovery(M_0)
		
		self._tau_l = self._c_pt * self._T_t4 / (getHeatCapacity(CONST.kappa, CONST.R) * air.temperature)

		self._tau_c = np.float_power(self._pi_c, (CONST.kappa - 1.0) / (CONST.kappa * self._e_c))
		self._tau_f = np.float_power(self._pi_f, (CONST.kappa - 1.0) / (CONST.kappa * self._e_f))

		pass

	def _calculateFuelRatio(self, air:Atmosphere) :

		self._f = (self._tau_l - self._tau_r * self._tau_c) / ((self._eta_b * self._h_PR / (getHeatCapacity(CONST.kappa, CONST.R) * air.temperature)) - self._tau_l)

		pass

	def _performTurbineEnergyBalance(self) :

		self._tau_t = 1.0 - (1.0 / (self._eta_m * (1 + self._f))) * (self._tau_r / self._tau_l) * (self._tau_c - 1.0 + self._alpha * (self._tau_f - 1.0))
		self._pi_t  = np.float_power(self._tau_t, self._gamma_t / ((self._gamma_t - 1.0) * self._e_t))

		pass

	def _calculateCoreExitConditions(self, air:Atmosphere) :

		product_pi = self._pi_r * self._pi_d * self._pi_c * self._pi_b * self._pi_t * self._pi_n

		if hasattr(self, '_P0_by_P9') :

			self._P_9 = air.pressure / self._P0_by_P9
			self._M_9 = np.sqrt(
				(2.0 / (self._gamma_t - 1.0)) *
				(np.float_power(product_pi * self._P0_by_P9, (self._gamma_t - 1.0) / self._gamma_t) - 1.0)
			)

		else :

			self._P_9 = air.pressure * product_pi / getStagnationPressureRatio(self._gamma_t, 1.0)

			self._M_9 = np.where(self._P_9 < air.pressure,
							np.sqrt(
								(2.0 / (self._gamma_t - 1.0)) * 
								(np.float_power(product_pi, (self._gamma_t - 1.0) / self._gamma_t) - 1.0)
							),
						# else
							1.0
			)

			self._P_9 = np.where(self._P_9 < air.pressure, air.pressure, self._P_9)
		
		self._T_9 = air.temperature * (self._tau_l * self._tau_t / getStagnationTemperatureRatio(self._gamma_t, self._M_9)) * (getHeatCapacity(CONST.kappa, CONST.R) / self._c_pt)
		self._V_9 = self._M_9 * getSonicSpeed(self._gamma_t, self._R_t, self._T_9)

		pass

	def _calculateFanExitConditions(self, air:Atmosphere) :

		product_pi = self._pi_r * self._pi_d * self._pi_f * self._pi_fn

		if hasattr(self, '_P0_by_P19') :

			self._P_19 = air.pressure / self._P0_by_P19

			self._M_19 = np.sqrt(
				(2.0 / (CONST.kappa - 1.0)) *
				(np.float_power(product_pi * self._P0_by_P19, (CONST.kappa - 1.0) / CONST.kappa) - 1.0)
			)

		else :

			self._P_19 = air.pressure * product_pi / getStagnationPressureRatio(CONST.kappa, 1.0)

			self._M_19 = np.where(self._P_19 < air.pressure,
									np.sqrt(
										(2.0 / (CONST.kappa - 1.0)) * 
										(np.float_power(product_pi, (CONST.kappa - 1.0) / CONST.kappa) - 1.0)
									),
								# else
									1.0
			)

			self._P_19 = np.where(self._P_19 < air.pressure, air.pressure, self._P_19)

		self._T_19 = air.temperature * (self._tau_r * self._tau_f / getStagnationTemperatureRatio(CONST.kappa, self._M_19))
		self._V_19 = self._M_19 * air.speed_of_sound * np.sqrt(self._T_19 / air.temperature)

		pass

	def _calculateThrust(self, V_0, air:Atmosphere) :

		self._ST_core = (1.0 / (1.0 + self._alpha)) * (
			(1.0 + self._f) * self._V_9 - V_0 +
			(1.0 + self._f) * self._R_t * (air.speed_of_sound ** 2) * self._T_9 * (1.0 - (air.pressure / self._P_9)) / (CONST.kappa * CONST.R * air.temperature * self._V_9)
		)

		self._ST_fan = (self._alpha / (1.0 + self._alpha)) * (
			self._V_19 - V_0 +
			(air.speed_of_sound ** 2) * self._T_19 * (1.0 - (air.pressure / self._P_19)) / (CONST.kappa * air.temperature * self._V_19)
		)

		self._ST = self._ST_core + self._ST_fan

		pass

	def _calculateEnergies(self, V_0) :

		self._thrust_power = self._ST * V_0

		self._Delta_KE = 0.5 * (
			(1.0 + self._f) * (self._V_9 ** 2) - (V_0 ** 2) +
			self._alpha * ((self._V_19 ** 2) - (V_0 ** 2))
		) / (1.0 + self._alpha)

		self._thermal_energy = self._f * self._h_PR / (1.0 + self._alpha)

		pass

	def _calculatePerformanceParameters(self) :

		self._TSFC = self._f / ((1.0 + self._alpha) * self._ST)

		self._eta_P = self._thrust_power / self._Delta_KE

		self._eta_T = self._Delta_KE / self._thermal_energy

		pass

	def performAnalysis(self, flight_speed:np.ndarray, flight_conditions:Atmosphere) :

		if np.all(flight_speed > 0) :

			M_0 = flight_speed / flight_conditions.speed_of_sound

		else :

			raise ValueError('Flight speed must be positive. Given value : ' + str(flight_speed))

		if self._initialized :

			self._initializeRatios(M_0, flight_conditions)
			self._calculateFuelRatio(flight_conditions)
			self._performTurbineEnergyBalance()
			self._calculateCoreExitConditions(flight_conditions)
			self._calculateFanExitConditions(flight_conditions)
			self._calculateThrust(flight_speed, flight_conditions)
			self._calculateEnergies(flight_speed)
			self._calculatePerformanceParameters()

			self._analysis_complete = True
			pass
		
		else :

			raise ExecError("Analysis needs to be initialized with initializeProblem()")

	def getSpecificThrusts(self) :

		if self._analysis_complete :

			return np.stack((self._ST, self._ST_core, self._ST_fan), -1)

		else :

			raise ExecError("Value not evaluated yet. Run performAnalysis()")

	def getSpecificFuelConsumtionRates(self) :

		if self._analysis_complete :

			return np.stack((self._TSFC, self._f / (1.0 + self._alpha)), -1)

		else :

			raise ExecError("Value not evaluated yet. Run performAnalysis()")

	def getEfficiencies(self) :

		if self._analysis_complete :

			return np.stack((self._eta_T * self._eta_P, self._eta_P, self._eta_T), -1)

		else :

			raise ExecError("Value not evaluated yet. Run performAnalysis()")

	def getReferenceRatios(self) :

		if self._analysis_complete :

			return np.stack((self._pi_r, self._tau_r), -1)

		else :

			raise ExecError("Value not evaluated yet. Run performAnalysis()")

	def getTurbineOperatingRatios(self) :

		if self._analysis_complete :

			return np.stack((self._pi_t, self._tau_t), -1)

		else :

			raise ExecError("Value not evaluated yet. Run performAnalysis()")

	def getCompressorOperatingRatios(self) :

		if self._analysis_complete :

			return np.stack((self._pi_c, self._tau_c), -1)

		else :

			raise ExecError("Value not evaluated yet. Run performAnalysis()")

	def getFanOperatingRatios(self) :

		if self._analysis_complete :

			return np.stack((self._pi_f, self._tau_f), -1)

		else :

			raise ExecError("Value not evaluated yet. Run performAnalysis()")

	def getCoreExitState(self) :

		if self._analysis_complete :

			return np.stack((self._M_9, self._P_9, self._T_9), -1)

		else :

			raise ExecError("Value not evaluated yet. Run performAnalysis()")

	def getFanExitState(self) :

		if self._analysis_complete :

			return np.stack((self._M_19, self._P_19, self._T_19), -1)

		else :

			raise ExecError("Value not evaluated yet. Run performAnalysis()")
    
	def getBurnerEnthalpyRatio(self) :

		if self._analysis_complete :

			return np.copy(self._tau_l)

		else :

			raise ExecError("Value not evaluated yet. Run performAnalysis()")


if __name__ == '__main__' :

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

	engine.performAnalysis(flight_speed, flight_conditions)

	print(engine.getEfficiencies())
	
	pass