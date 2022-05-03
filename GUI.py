import ipywidgets as widgets

from Turbofan_Engine import TurboFanEngine, Atmosphere

flight_mach_number_tbox = widgets.FloatText(
    value   = 0.85,
    min     = 0.5,
    max     = 5.0,
    step    = 0.01
)

flight_altitude_slider  = widgets.FloatSlider(
    value   = 12.0,
    min     =  8.0,
    max     = 15.0,
    step    =  0.1,
    readout_format = '.1f'
    # orientation = 'vertical'
)

flight_conditions_grid = widgets.GridspecLayout(2, 3)

flight_conditions_grid[0, 0] = widgets.Label('Flight Mach Number', layout = widgets.Layout(display="flex", justify_content="flex-end"))
flight_conditions_grid[0, 1] = flight_mach_number_tbox

flight_conditions_grid[1, 0] = widgets.Label('Flight Altitude', layout = widgets.Layout(display="flex", justify_content="flex-end"))
flight_conditions_grid[1, 1] = flight_altitude_slider
flight_conditions_grid[1, 2] = widgets.Label('km')

compressor_compression_ratio_slider = widgets.FloatSlider(
	value	= 35.0,
	min		=  1.0,
	max		= 75.0,
	step	= 0.01
)

fan_compression_ratio_slider = widgets.FloatSlider(
	value	=  1.5,
	min		=  1.0,
	max		=  5.0,
	step	= 0.01
)

bypass_ratio_slider = widgets.FloatSlider(
	value	=  8.0,
	min		=  0.0,
	max		= 20.0,
	step	= 0.01
)

engine_design_grid = widgets.GridspecLayout(3, 3)

engine_design_grid[2, 0] = widgets.Label('Bypass Ratio', layout = widgets.Layout(display="flex", justify_content="flex-end"))
engine_design_grid[2, 1] = bypass_ratio_slider

engine_design_grid[0, 0] = widgets.Label('Compressor Compression Ratio', layout = widgets.Layout(display="flex", justify_content="flex-end"))
engine_design_grid[0, 1] = compressor_compression_ratio_slider

engine_design_grid[1, 0] = widgets.Label('Fan Compression Ratio', layout = widgets.Layout(display="flex", justify_content="flex-end"))
engine_design_grid[1, 1] = fan_compression_ratio_slider

tech_level_dropdown = widgets.Dropdown(
	options = [
		('1945 - 1965', 0),
		('1965 - 1985', 1),
		('1985 - 2005', 2),
		('2005 - 2025', 3),
		('2025 - 2045', 4)
	],
	value 	= 3
)

diffuser_pressure_ratio_tbox = widgets.FloatText(
	value	= 0.995,
	min		= 0.0,
	max		= 1.0,
	step	= 0.001
)

compressor_efficiency_tbox = widgets.FloatText(
	value	= 0.9,
	min		= 0.0,
	max		= 1.0,
	step	= 0.001
)

fan_efficiency_tbox = widgets.FloatText(
	value	= 0.89,
	min		= 0.0,
	max		= 1.0,
	step	= 0.001
)

burner_pressure_ratio_tbox = widgets.FloatText(
	value	= 0.95,
	min		= 0.0,
	max		= 1.0,
	step	= 0.001
)

burner_efficiency_tbox = widgets.FloatText(
	value	= 0.999,
	min		= 0.0,
	max		= 1.0,
	step	= 0.001
)

turbine_efficiency_tbox = widgets.FloatText(
	value	= 0.90,
	min		= 0.0,
	max		= 1.0,
	step	= 0.001
)

mechanical_shaft_efficiency_tbox = widgets.FloatText(
	value	= 0.97,
	min		= 0.0,
	max		= 1.0,
	step	= 0.001
)

nozzle_pressure_ratio_tbox = widgets.FloatText(
	value	= 0.995,
	min		= 0.0,
	max		= 1.0,
	step	= 0.001
)

turbine_temperature_tbox = widgets.FloatText(
	value	= 2000,
	min		=  800,
	max		= 3000,
	step	=   10,
	readout_format = '.1f'
)

component_performance_grid_box = widgets.GridspecLayout(10, 4)

component_performance_grid_box[0, 0] = widgets.Label('Level of Technology', layout = widgets.Layout(display="flex", justify_content="flex-end"))
component_performance_grid_box[0, 1] = tech_level_dropdown

component_performance_grid_box[1, 1] = widgets.Label('--or--')

component_performance_grid_box[2, 0] = widgets.Label('Design Limit')

component_performance_grid_box[3, 0] = widgets.Label('Turbine Inlet Total Temperature', layout = widgets.Layout(display="flex", justify_content="flex-end"))
component_performance_grid_box[3, 1] = turbine_temperature_tbox
component_performance_grid_box[3, 2] = widgets.Label('kelvin', layout = widgets.Layout(display="flex", justify_content="flex-start"))

component_performance_grid_box[4, 0] = widgets.Label('Component Efficiencies')

component_performance_grid_box[5, 0] = widgets.Label('Maximum Diffuser Pressure Drop', layout = widgets.Layout(display="flex", justify_content="flex-end"))
component_performance_grid_box[5, 1] = diffuser_pressure_ratio_tbox

component_performance_grid_box[6, 0] = widgets.Label('Compressor Polytropic Efficiency', layout = widgets.Layout(display="flex", justify_content="flex-end"))
component_performance_grid_box[6, 1] = compressor_efficiency_tbox
component_performance_grid_box[6, 2] = widgets.Label('Fan Polytropic Efficiency', layout = widgets.Layout(display="flex", justify_content="flex-end"))
component_performance_grid_box[6, 3] = fan_efficiency_tbox

component_performance_grid_box[7, 0] = widgets.Label('Burner Pressure Drop', layout = widgets.Layout(display="flex", justify_content="flex-end"))
component_performance_grid_box[7, 1] = burner_pressure_ratio_tbox
component_performance_grid_box[7, 2] = widgets.Label('Burner Efficiency', layout = widgets.Layout(display="flex", justify_content="flex-end"))
component_performance_grid_box[7, 3] = burner_efficiency_tbox

component_performance_grid_box[8, 0] = widgets.Label('Mechanical Shaft Efficiency', layout = widgets.Layout(display="flex", justify_content="flex-end"))
component_performance_grid_box[8, 1] = mechanical_shaft_efficiency_tbox
component_performance_grid_box[8, 2] = widgets.Label('Turbine Polytropic Efficiency', layout = widgets.Layout(display="flex", justify_content="flex-end"))
component_performance_grid_box[8, 3] = turbine_efficiency_tbox

component_performance_grid_box[9, 0] = widgets.Label('Nozzle Pressure Drop', layout = widgets.Layout(display="flex", justify_content="flex-end"))
component_performance_grid_box[9, 1] = nozzle_pressure_ratio_tbox

tech_level_dict = {
	'pi_d_max'	:	(0.9,	0.95,	0.98,	0.955,	0.999),
	'e_c'		:	(0.8,	0.84,	0.88,	0.90,	0.92),
	'e_f'		:	(0.78,	0.82,	0.86,	0.89,	0.90),
	'pi_b'		:	(0.9,	0.92,	0.94,	0.95,	0.99),
	'eta_b'		:	(0.85,	0.91,	0.98,	0.99,	0.99),
	'eta_m'		:	(0.9,	0.92,	0.95,	0.97,	0.98),
	'e_t'		:	(0.8,	0.85,	0.89,	0.90,	0.92),
	'pi_n'		:	(0.95,	0.97,	0.98,	0.995,	0.998),
	'T_t4'		:	(1110,	1390,	1780,	2000,	2200)
}

def on_tech_level_select(change) :

	i = change['new']

	turbine_temperature_tbox.value = tech_level_dict['T_t4'][i]

	diffuser_pressure_ratio_tbox.value = tech_level_dict['pi_d_max'][i]

	compressor_efficiency_tbox.value = tech_level_dict['e_c'][i]
	fan_efficiency_tbox.value = tech_level_dict['e_f'][i]

	burner_efficiency_tbox.value = tech_level_dict['eta_b'][i]
	burner_pressure_ratio_tbox.value = tech_level_dict['pi_b'][i]

	mechanical_shaft_efficiency_tbox.value = tech_level_dict['eta_m'][i]
	turbine_efficiency_tbox.value = tech_level_dict['e_t'][i]

	nozzle_pressure_ratio_tbox.value = tech_level_dict['pi_n'][i]

	pass

tech_level_dropdown.observe(on_tech_level_select, names='value')

fuel_dropdown = widgets.Dropdown(
	options = [
		('JP - 1', 0)
	],
	value = 0
)

fuel_info_dict = {
	'h_PR'		:	(42.7984E6),
	'c_pt'		:	(1155.5568),
	'gamma_t'	:	(1.33)
}

fuel_heating_value_tbox = widgets.FloatText(
	value	= 42.7984,
	step	= 0.1,
	min		= 0.0
)

combustion_products_heat_capacity_tbox = widgets.FloatText(
	value	= 1155.5568,
	min		= 0.0,
	step	= 0.1
)

combustion_products_gamma_tbox = widgets.FloatText(
	value	= 1.33,
	min		= 0.0,
	step	= 0.01,
)

fuel_gridbox = widgets.GridspecLayout(7, 3)

fuel_gridbox[0, 0] = widgets.Label('Fuel', layout = widgets.Layout(display="flex", justify_content="flex-end"))
fuel_gridbox[0, 1] = fuel_dropdown

fuel_gridbox[1, 1] = widgets.Label('--or--')

fuel_gridbox[2, 0] = widgets.Label('Fuel')

fuel_gridbox[3, 0] = widgets.Label('Heating Value', layout = widgets.Layout(display="flex", justify_content="flex-end"))
fuel_gridbox[3, 1] = fuel_heating_value_tbox
fuel_gridbox[3, 2] = widgets.Label('MJ / kg')

fuel_gridbox[4, 0] = widgets.Label('Combustion Product Gases')

fuel_gridbox[5, 0] = widgets.Label('Heat Capacity', layout = widgets.Layout(display="flex", justify_content="flex-end"))
fuel_gridbox[5, 1] = combustion_products_heat_capacity_tbox
fuel_gridbox[5, 2] = widgets.Label('J / kg - K')

fuel_gridbox[6, 0] = widgets.Label('gamma', layout = widgets.Layout(display="flex", justify_content="flex-end"))
fuel_gridbox[6, 1] = combustion_products_gamma_tbox

def on_fuel_select(change) :

	i = change['new']

	fuel_heating_value_tbox.value = fuel_info_dict['h_PR'][i]

	combustion_products_heat_capacity_tbox.value = fuel_info_dict['c_pt'][i]
	combustion_products_gamma_tbox.value = fuel_info_dict['gamma_t'][i]

	pass

fuel_dropdown.observe(on_fuel_select, names='value')
fuel_dropdown = widgets.Dropdown(
	options = [
		('JP - 1', 0)
	],
	value = 0
)

fuel_info_dict = {
	'h_PR'		:	(42.7984E6),
	'c_pt'		:	(1155.5568),
	'gamma_t'	:	(1.33)
}

fuel_heating_value_tbox = widgets.FloatText(
	value	= 42.7984,
	step	= 0.1,
	min		= 0.0
)

combustion_products_heat_capacity_tbox = widgets.FloatText(
	value	= 1155.5568,
	min		= 0.0,
	step	= 0.1
)

combustion_products_gamma_tbox = widgets.FloatText(
	value	= 1.33,
	min		= 0.0,
	step	= 0.01,
)

fuel_gridbox = widgets.GridspecLayout(7, 3)

fuel_gridbox[0, 0] = widgets.Label('Fuel', layout = widgets.Layout(display="flex", justify_content="flex-end"))
fuel_gridbox[0, 1] = fuel_dropdown

fuel_gridbox[1, 1] = widgets.Label('--or--')

fuel_gridbox[2, 0] = widgets.Label('Fuel')

fuel_gridbox[3, 0] = widgets.Label('Heating Value', layout = widgets.Layout(display="flex", justify_content="flex-end"))
fuel_gridbox[3, 1] = fuel_heating_value_tbox
fuel_gridbox[3, 2] = widgets.Label('MJ / kg')

fuel_gridbox[4, 0] = widgets.Label('Combustion Product Gases')

fuel_gridbox[5, 0] = widgets.Label('Heat Capacity', layout = widgets.Layout(display="flex", justify_content="flex-end"))
fuel_gridbox[5, 1] = combustion_products_heat_capacity_tbox
fuel_gridbox[5, 2] = widgets.Label('J / kg - K')

fuel_gridbox[6, 0] = widgets.Label('gamma', layout = widgets.Layout(display="flex", justify_content="flex-end"))
fuel_gridbox[6, 1] = combustion_products_gamma_tbox

def on_fuel_select(change) :

	i = change['new']

	fuel_heating_value_tbox.value = fuel_info_dict['h_PR'][i]

	combustion_products_heat_capacity_tbox.value = fuel_info_dict['c_pt'][i]
	combustion_products_gamma_tbox.value = fuel_info_dict['gamma_t'][i]

	pass

fuel_dropdown.observe(on_fuel_select, names='value')

def setUpEngine(engine : TurboFanEngine) :

	engine.setFuelProperties(
		fuel_heating_value_tbox.value * 1E6,
		combustion_products_gamma_tbox.value,
		combustion_products_heat_capacity_tbox.value
	)

	engine.setInletOutletProperties(
		diffuser_pressure_ratio_tbox.value,
		nozzle_pressure_ratio_tbox.value,
		nozzle_pressure_ratio_tbox.value
	)

	engine.setBurnerProperties(
		burner_pressure_ratio_tbox.value,
		burner_efficiency_tbox.value
	)

	engine.setCompressorProperties(
		compressor_compression_ratio_slider.value,
		compressor_efficiency_tbox.value
	)

	engine.setFanProperties(
		fan_compression_ratio_slider.value,
		fan_efficiency_tbox.value
	)

	engine.setTurbineProperties(
		turbine_temperature_tbox.value,
		turbine_efficiency_tbox.value,
		mechanical_shaft_efficiency_tbox.value
	)

	engine.setBypassRatio(bypass_ratio_slider.value)
	
	engine.initializeProblem()

	flight_conditions = Atmosphere(flight_altitude_slider.value)
	flight_speed = flight_mach_number_tbox.value * flight_conditions.speed_of_sound

	engine.performAnalysis(flight_speed, flight_conditions)

	pass