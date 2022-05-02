import ipywidgets as widgets

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

flight_conditions_grid[0, 0] = widgets.Label('Flight Mach Number')
flight_conditions_grid[0, 1] = flight_mach_number_tbox

flight_conditions_grid[1, 0] = widgets.Label('Flight Altitude')
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

engine_design_grid[2, 0] = widgets.Label('Bypass Ratio')
engine_design_grid[2, 1] = bypass_ratio_slider

engine_design_grid[0, 0] = widgets.Label('Compressor Compression Ratio')
engine_design_grid[0, 1] = compressor_compression_ratio_slider

engine_design_grid[1, 0] = widgets.Label('Fan Compression Ratio')
engine_design_grid[1, 1] = fan_compression_ratio_slider
