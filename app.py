import streamlit as st
import pandas as pd
import io

# Page configuration
st.set_page_config(page_title="Trailer Quotation System", layout="wide")

# Load Excel data
@st.cache_data
def load_data():
    excel_file = 'Quote-Tempelate.xlsx'
    
    # Load all sheets
    lights_df = pd.read_excel(excel_file, sheet_name='LIGHTS')
    axles_df = pd.read_excel(excel_file, sheet_name='AXLES')
    tires_df = pd.read_excel(excel_file, sheet_name='TIRES')
    specoptions_df = pd.read_excel(excel_file, sheet_name='SPECOPTIONS')
    chassis_df = pd.read_excel(excel_file, sheet_name='CHASSIS')
    
    return lights_df, axles_df, tires_df, specoptions_df, chassis_df

try:
    lights_df, axles_df, tires_df, specoptions_df, chassis_df = load_data()
    data_loaded = True
except:
    data_loaded = False
    st.warning("Excel file not found. Using default values.")

# Initialize session state for prices
if 'line_items' not in st.session_state:
    st.session_state.line_items = []

# Title
st.title("🚛 Trailer Quotation System")

# Sidebar for quote information
with st.sidebar:
    st.header("Quote Information")
    quote_number = st.text_input("Quote #")
    quote_date = st.date_input("Date")
    dealer = st.text_input("Dealer")
    contact = st.text_input("Contact")
    model = st.selectbox("Model", ["End Dump 4x", "End Dump 3x", "End Dump 5x"])
    st.divider()
    discount_percent = st.number_input("Discount %", min_value=0.0, max_value=100.0, value=4.0, step=0.5)

# Main content tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Body Specs", "Chassis", "Axles", "Tires & Rims", "Lights", "Paint", "Summary"
])

# Initialize pricing dictionary
prices = {}

# TAB 1: TRAILER BODY SPECIFICATION
with tab1:
    st.header("Trailer Body Specification")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dimensions")
        full_body_polish = st.selectbox("Full Body Polish", ["STANDARD", "YES", "NO"])
        
        # Trailer Length with pricing
        trailer_length_options = ["40'", "41'", "42'", "43'", "44'", "45'", "46'", "47'", "48'"]
        trailer_length = st.selectbox("Trailer Length", trailer_length_options, index=6)
        if data_loaded:
            length_prices = {
                "40'": 0, "41'": 0, "42'": 0, "43'": 0, "44'": 0, "45'": 0, "46'": 1000, "47'": 1000, "48'": 1000
            }
            prices['trailer_length'] = length_prices.get(trailer_length, 0)
        else:
            prices['trailer_length'] = 1000 if trailer_length == "46'" else 0
        
        trailer_width = st.selectbox("Trailer Width", ["96 INCHES", "102 INCHES", "104 INCHES"])
        
        # Wall Height with pricing
        wall_height_options = ['60"', '62"', '64"', '66"', '68"', '70"', '72"', '74"', '76"', '78"', '80"', '82"', '84"']
        wall_height = st.selectbox("Trailer Wall Height", wall_height_options, index=1)
        wall_height_prices = {
            '60"': 0, '62"': 500, '64"': 600, '66"': 700, '68"': 800, 
            '70"': 900, '72"': 1000, '74"': 1100, '76"': 1200, '78"': 1300, '80"': 1400, '82"': 1500, '84"': 1600
        }
        prices['wall_height'] = wall_height_prices.get(wall_height, 0)
        
        # Board Height with pricing
        board_height_options = ["NONE", '6" Board', '8" Board', '10" Board', '12" Board']
        board_height = st.selectbox("Board Height", board_height_options, index=2)
        board_prices = {"NONE": 0, '6" Board': 0, '8" Board': 0, '10" Board': 0, '12" Board': 0}
        prices['board_height'] = board_prices.get(board_height, 0)
        
        box_height = st.text_input("Box Height", value='70"')
        
    with col2:
        st.subheader("Wall & Floor")
        wall_panels = st.selectbox("Wall Panels", ['6061  2.25" PANELS', '6061  3.0" PANELS'])
        inner_wall = st.selectbox("Inner Wall", ["1/8 Inner wall", "3/16 Inner wall", "NONE"])
        side_placement = st.selectbox("Side Placement", ["OUTSET SMOOTH SIDE PANEL", "INSET PANEL"])
        body_hold_down = st.selectbox("Body Hold Down", ["NO", "YES"])
        box_liner = st.selectbox("Box Liner", ["NONE", "YES"])
        top_rail = st.selectbox("Top Rail", ["6061 ALUMINUM EXTRUSION - POLISHED", "PAINTED"])
        
        # Floor with pricing
        floor = st.selectbox("Floor", ['1/4" THICKNESS', '3/8" THICKNESS'])
        floor_prices = {'1/4" THICKNESS': 0, '3/8" THICKNESS': 1000}
        prices['floor'] = floor_prices.get(floor, 0)
        
        crossmember = st.selectbox("Crossmember(s)", [
            '4 INCH EXTRUDED C CHANNELS - STANDARD (12" CENTER)',
            '4 INCH EXTRUDED C CHANNELS (10" CENTER)'
        ])
        
        # Tow Motor Package with pricing
        tow_motor = st.selectbox("Tow Motor Package", ["NO", "YES"])
        prices['tow_motor'] = 0 if tow_motor == "NO" else 500
        
        vibrator = st.selectbox("Vibrator", ["NONE", "YES"])
        
        # Rear Side Wall Steps with pricing
        rear_steps_options = ["D/S IN AND OUT", "P/S IN AND OUT", "P/S IN", "NONE"]
        rear_steps = st.selectbox("Rear Side Wall Steps", rear_steps_options, index=1)
        rear_steps_prices = {"D/S IN AND OUT": 0, "P/S IN AND OUT": 0, "P/S IN": 0, "NONE": 0}
        prices['rear_steps'] = rear_steps_prices.get(rear_steps, 0)
    
    st.subheader("Bulkhead")
    col3, col4 = st.columns(2)
    with col3:
        bulkhead_type = st.selectbox("Trailer Bulkhead Type", [
            '3/16" 5083 ALUMINUM - RADIUS CORNERS',
            '1/4" 5083 ALUMINUM - RADIUS CORNERS'
        ])
        
        # Shovel Holder with pricing
        shovel_holder = st.selectbox("Shovel Holder", [
            "YES -DRIVER SIDE @DOGHOUSE",
            "YES -DRIVER SIDE @UNDERNEATH BOX",
            "NONE"
        ])
        shovel_prices = {
            "YES -DRIVER SIDE @DOGHOUSE": 50,
            "YES -DRIVER SIDE @UNDERNEATH BOX": 50,
            "NONE": 0
        }
        prices['shovel_holder'] = shovel_prices.get(shovel_holder, 0)
        
        hoist = st.selectbox("Recommended Hoist", ["HYVA", "WESTEEL"])
        hose = st.selectbox("9' Hydraulic Hose", ['1" X 108" HOSE W/WING FITTING (4-WIRE HOSE)'])
    
    with col4:
        # Man Door with pricing
        man_door_options = ["NONE", "YES - DRIVER SIDE W/GRAB HANDLE", "YES - PASSENGER SIDE W/GRAB HANDLE"]
        man_door = st.selectbox("Man Door", man_door_options)
        man_door_prices = {"NONE": 0, "YES - DRIVER SIDE W/GRAB HANDLE": 1300, "YES - PASSENGER SIDE W/GRAB HANDLE": 1300}
        prices['man_door'] = man_door_prices.get(man_door, 0)
        
        # Bulkhead Steps with pricing
        bulkhead_steps = st.selectbox("Bulkhead Steps", ["NONE", "DRIVER SIDE AND 1 BELOW MANDOOR", "PASSENGER SIDE AND 1 BELOW MANDOOR"])
        bulkhead_steps_prices = {"NONE": 0, "DRIVER SIDE AND 1 BELOW MANDOOR": 0, "PASSENGER SIDE AND 1 BELOW MANDOOR": 0}
        prices['bulkhead_steps'] = bulkhead_steps_prices.get(bulkhead_steps, 0)
    
    st.subheader("Tailgate")
    col5, col6 = st.columns(2)
    with col5:
        # Tailgate Slope with pricing
        tailgate_slope = st.selectbox("Tailgate Slope", ["STRAIGHT", "85 DEGREE SLOPE"])
        tailgate_slope_prices = {"STRAIGHT": 0, "85 DEGREE SLOPE": 0}
        prices['tailgate_slope'] = tailgate_slope_prices.get(tailgate_slope, 0)
        
        tailgate_type = st.selectbox("Tailgate Type", ["OVERSLUNG ONLY", "UNDERSLUNG"])
        rear_seal = st.selectbox("Rear Tailgate Seal", ["STANDARD RUBBER W/ ALL TRAILERS"])
        
        # Gate Operation with pricing
        gate_operation = st.selectbox("Gate Operation", [
            "ELECTRIC OVER AIR BOOSTER",
            "ELECTRIC OVER AIR CYLINDER",
            "MANUAL LOCKING"
        ])
        gate_operation_prices = {
            "ELECTRIC OVER AIR BOOSTER": 0,
            "ELECTRIC OVER AIR CYLINDER": 0,
            "MANUAL LOCKING": 0
        }
        prices['gate_operation'] = gate_operation_prices.get(gate_operation, 0)
    
    with col6:
        winder_locks = st.selectbox("Winder Locks", ['4 (2 BOTTOM, 1 EACH SIDE @ 45 Degree Angle)', '6 LOCKS'])
        angle_top = st.selectbox("Angle on Top of Gate", ["NONE", "YES"])
        spreader_chains = st.selectbox("Spreader Chains", ["NONE", "YES"])
        gate_steps = st.selectbox("Gate Steps", ["NONE", "YES"])
        
        # Coal/Grain Chute with pricing
        coal_chute = st.selectbox("Coal/Grain Chute", ['3 DOORS 24"', '1 DOOR 24"', "NONE"])
        coal_chute_prices = {'3 DOORS 24"': 1500, '1 DOOR 24"': 1000, "NONE": 0}
        prices['coal_chute'] = coal_chute_prices.get(coal_chute, 0)
        
        # Sock Adaptor with pricing
        sock_adaptor = st.selectbox("Sock Adaptor", ["NONE", "YES- Driver Side", "YES- Passenger Side"])
        sock_prices = {"NONE": 0, "YES- Driver Side": 0, "YES- Passenger Side": 0}
        prices['sock_adaptor'] = sock_prices.get(sock_adaptor, 0)
        
        tarp_hooks = st.selectbox("Tarp Hooks", ["NONE", "YES"])

# TAB 2: CHASSIS SPECIFICATION
with tab2:
    st.header("Chassis Specification")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Main Chassis")
        chassis_model = st.selectbox("Model", ["3 Axle", "4 Axle", "5 Axle"], index=1)
        wear_pad = st.selectbox("Wear Pad", ["YES, 5/16 INCH FRAME RUBBER ILO CM PADS", "NO"])
        cylinder_pin = st.selectbox("Cylinder Pin", ["STANDARD/ YES, 1 SOLID PIN", "2 PINS"])
        
        # Chassis Type with pricing
        chassis_type = st.selectbox("Chassis", [
            "ALUMINUM (Polished)",
            "ALUMINUM (Non Polished)",
            "STEEL"
        ])
        chassis_prices = {
            "ALUMINUM (Polished)": 4500,
            "ALUMINUM (Non Polished)": 1500,
            "STEEL": 0
        }
        prices['chassis'] = chassis_prices.get(chassis_type, 0)
        
        chassis_length = st.text_input("Chassis Length", value='45\' 3"')
        
        # Gooseneck with pricing
        gooseneck = st.selectbox("Gooseneck", ["NONE", 'YES - 12"'])
        gooseneck_prices = {"NONE": 0, 'YES - 12"': 0}
        prices['gooseneck'] = gooseneck_prices.get(gooseneck, 0)
        
        rear_overhang = st.text_input("Rear Overhang", value='9"')
        king_pin_setting = st.text_input("King Pin Setting", value='16"')
        fifth_wheel = st.selectbox("Fifth Wheel Pick Up Plate", ['5/16" , GALVANIZED'])
        king_pin_height = st.text_input("King Pin Height", value='49"')
        
    with col2:
        st.subheader("Additional Components")
        hoist_mount = st.selectbox("Hoist and Mount Style", ['DOUBLE 3" X 6" X 3/8"'])
        front_mudflaps = st.selectbox("Front Mudflaps", ["BOX CORNERS", "FULL WIDTH"])
        steer_mudflap = st.selectbox("Steer Axle Mudflap", ["FRONT AND REAR", "NONE"])
        
        # Ride Axle Mudflap with pricing
        ride_mudflap = st.selectbox("Ride Axle Mudflap", [
            "FRONT OF ALL AXLES",
            "FRONT OF 1ST RIDE ONLY"
        ])
        ride_mudflap_prices = {"FRONT OF ALL AXLES": 0, "FRONT OF 1ST RIDE ONLY": 0}
        prices['ride_mudflap'] = ride_mudflap_prices.get(ride_mudflap, 0)
        
        center_splash = st.selectbox("Center Splash Panel", ["NONE", "YES"])
        rear_mudflaps = st.selectbox("Rear Mudflaps", ["FULL WIDTH", "STANDARD"])
        fenders_front = st.selectbox("Fenders on Front", ["NONE", "YES"])
        load_indicator = st.selectbox("Load Level Indicator", ["NO", "YES"])
        
        # Tire Carrier with pricing
        tire_carrier = st.selectbox("Tire Carrier", ["YES", "NONE"])
        tire_carrier_price = st.number_input("Tire Carrier Price (TBD)", min_value=0, value=0, step=100)
        prices['tire_carrier'] = tire_carrier_price if tire_carrier == "YES" else 0
        
        air_tanks = st.selectbox("Air Tanks", ["ALUMINUM", "STEEL"])
        tow_hooks = st.selectbox("Tow Hooks", ["YES, IN REAR PIVOTS", "NO"])
        
        # Landing Gear with pricing
        landing_gear = st.selectbox("Landing Gear", [
            "STEEL - SAF HOLLAND",
            "ALUMINUM - JOST AX150"
        ])
        landing_gear_prices = {"STEEL - SAF HOLLAND": 0, "ALUMINUM - JOST AX150": 0}
        prices['landing_gear'] = landing_gear_prices.get(landing_gear, 0)
        
        shims = st.selectbox("Shims", ["STAINLESS STEEL", "GALVANIZED"])
        enclosure = st.selectbox("Enclosure for Switches", ["YES - STAINLESS STEEL (STANDARD)"])
        air_gauge = st.selectbox("Air Gauge/System", ['YES, IN FRONT (45 Degree Angle)'])

# TAB 3: AXLE CONFIGURATION
with tab3:
    st.header("Axle Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("General")
        # Brakes with pricing
        brakes_type = st.selectbox("Brakes", ["DRUM", "DISC"])
        brakes_prices = {"DRUM": 0, "DISC": 0}
        prices['brakes'] = brakes_prices.get(brakes_type, 0)
        
        suspension_control = st.selectbox("Suspension Control", [
            "ELECTRIC W/ MANUAL BALL VALVE IN CONTROL BOX (Electric on Aux cord)"
        ])
        abs = st.selectbox("ABS", ["2S1M MERITOR/WABCO"])
        suspension_hangers = st.selectbox("Suspension Hangers", ["GALVANIZED", "PAINTED"])
    
    with col2:
        st.subheader("Ride Axle")
        qty_ride = st.number_input("Quantity of Ride Only Axles", min_value=0, max_value=5, value=1)
        ride_spacing = st.number_input("Axles Spacing", min_value=60, max_value=100, value=72)
        ride_suspension = st.selectbox("Suspension for Ride Axles", ["HEND. INTRAAX AAT-30K W/HXL-3"])
        ride_axle = st.selectbox("Axle", ["HENDRICKSON INTRAAX"])
        ride_brakes = st.selectbox("Brakes (Ride)", ['DRUMS, 7 IN XL, W/ 30-30 CHAMBERS'])
        ride_hubs = st.selectbox("Hubs and Drums", ['CAST W/STEEL HUB HP 10 STUD TP, LS, 7 IN'])
        ride_lubrication = st.selectbox("Axles Lubrication", ["HXL, SYNTHETIC SEMI-FLUID GREASE 3 YEAR"])
        ride_slacks = st.selectbox("Slacks", ["AUTOMATIC"])
    
    with col3:
        st.subheader("Lift Axle")
        # Lift Axle Quantity with pricing
        qty_lift = st.number_input("Quantity of Lift Axles", min_value=0, max_value=3, value=1)
        lift_prices_map = {0: 0, 1: 1000, 2: 2000, 3: 3000}
        prices['lift_axle'] = lift_prices_map.get(qty_lift, 0)
        
        lift_spacing = st.number_input("Axles Spacing (Lift)", min_value=60, max_value=100, value=72)
        lift_option = st.selectbox("Lift", [
            "HEND. INTRAAX AAT WITH UBL-102 LIFT",
            "HEND. INTRAAX AAL WITH UBL-102 HIGH LIFT"
        ])
        lift_axle = st.selectbox("Axle (Lift)", ["HENDRICKSON INTRAAX"])
        lift_position = st.selectbox("Position", ["1 -FRONT", "2 -MIDDLE", "3 -MIDDLE", "4 -REAR"])
    
    st.subheader("Steer Axle")
    col4, col5 = st.columns(2)
    with col4:
        # Steer Axle Quantity with pricing
        qty_steer = st.number_input("Quantity of Steer Axles", min_value=0, max_value=2, value=1)
        steer_qty_prices = {0: 0, 1: 7000, 2: 14000}
        prices['steer_axle'] = steer_qty_prices.get(qty_steer, 0)
        
        steer_spacing = st.number_input("Steer Axle Spacing", min_value=80, max_value=120, value=100)
        steer_suspension = st.selectbox("Suspension for Steer/Lift Axle", ["IMT DEXTER 25K"])
        steer_axles = st.selectbox("Steer Axles", ["IMT DEXTER"])
    
    with col5:
        steer_brakes = st.selectbox("Brakes (Steer)", ['DRUMS, 7 IN XL, W/ 30-30 CHAMBERS'])
        lift_kit = st.selectbox("Lift Kit", ["INTEGRATED WITH AXLE"])
        lift_control = st.selectbox("Lift Control", ["REVERSE-A-MATIC"])
        steer_hubs = st.selectbox("Hubs and Drums (Steer)", ['CAST W/STEEL HUB HP 10 STUD TP, LS, 7 IN'])
        proportioning = st.selectbox("Proportioning Valve", ["YES", "NO"])

# TAB 4: RIMS AND TIRES
with tab4:
    st.header("Rims and Tires")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tire Configuration")
        tire_size = st.selectbox("Tire Size Selection", ["22.5", "24.5"])
        ride_tire_type = st.selectbox("Ride Tire Selection", ["DUAL TIRES", "SINGLE TIRES"])
        steer_tire_type = st.selectbox("Steer Tire Selection", ["DUAL TIRES", "SINGLE TIRES"])
        
        st.subheader("Ride Configuration")
        ride_rim_selection = st.selectbox("Ride Rim Selection", [
            "HIGH POLISH x ALL RIMS",
            "DURABRITE x ALL RIMS",
            "HIGH POLISH INSIDE AND DURABRITE OUTSIDE"
        ])
        
        if data_loaded and tire_size == "22.5" and ride_tire_type == "DUAL TIRES":
            ride_rim_prices = {
                "HIGH POLISH x ALL RIMS": 1500,
                "DURABRITE x ALL RIMS": 4500,
                "HIGH POLISH INSIDE AND DURABRITE OUTSIDE": 2250
            }
            prices['ride_tires'] = ride_rim_prices.get(ride_rim_selection, 0)
        else:
            prices['ride_tires'] = 1500
        
        ride_tires_model = st.selectbox("Tires (Ride)", [
            "CONTINENTAL HSR3 11R22.5 16 PLY",
            "CONTINENTAL HSR3 11R24.5 16 PLY"
        ])
        
        if ride_rim_selection == "HIGH POLISH x ALL RIMS":
            ride_rims_model = "ALUMINUM 22.5X8.25 - ALCOA High Polish"
        elif ride_rim_selection == "DURABRITE x ALL RIMS":
            ride_rims_model = "ALUMINUM 22.5X8.25 - ALCOA Durabrite Polish"
        else:
            ride_rims_model = "ALUMINUM 22.5X8.25 - ALCOA Durabrite Outside and High Polish Inside"
        
        st.text(f"Rims (Ride): {ride_rims_model}")
    
    with col2:
        st.subheader("Steer Configuration")
        steer_rim_selection = st.selectbox("Steer Rim Selection", [
            "DURABRITE x ALL RIMS",
            "HIGH POLISH x ALL RIMS",
            "HIGH POLISH INSIDE AND DURABRITE OUTSIDE"
        ], index=0)
        
        if data_loaded and tire_size == "22.5" and steer_tire_type == "DUAL TIRES":
            steer_rim_prices = {
                "DURABRITE x ALL RIMS": 1000,
                "HIGH POLISH x ALL RIMS": 500,
                "HIGH POLISH INSIDE AND DURABRITE OUTSIDE": 750
            }
            prices['steer_tires'] = steer_rim_prices.get(steer_rim_selection, 0)
        else:
            prices['steer_tires'] = 500
        
        steer_tires_model = st.selectbox("Tires (Steer)", [
            "CONTINENTAL HSR3 11R22.5 16 PLY",
            "CONTINENTAL HSR3 11R24.5 16 PLY"
        ])
        
        if steer_rim_selection == "DURABRITE x ALL RIMS":
            steer_rims_model = "ALUMINUM 22.5X8.25 - ALCOA Durabrite Polish"
        elif steer_rim_selection == "HIGH POLISH x ALL RIMS":
            steer_rims_model = "ALUMINUM 22.5X8.25 - ALCOA High Polish"
        else:
            steer_rims_model = "ALUMINUM 22.5X8.25 - ALCOA Durabrite Outside and High Polish Inside"
        
        st.text(f"Rims (Steer): {steer_rims_model}")
        
        st.subheader("Additional Options")
        tire_inflation = st.selectbox("Tire Inflation System", ["NONE", "YES"])
        chrome_hats = st.selectbox("Chrome Top Hats", ["NONE", "YES"])

# TAB 5: LIGHTS
with tab5:
    st.header("Lights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Light Type with pricing
        light_type = st.selectbox("Light Type", [
            "GROTE L.E.D. STANDARD - GROMMET MOUNT",
            "GROTE L.E.D. STANDARD - FLANGE MOUNT"
        ])
        light_type_prices = {
            "GROTE L.E.D. STANDARD - GROMMET MOUNT": 0,
            "GROTE L.E.D. STANDARD - FLANGE MOUNT": 0
        }
        prices['light_type'] = light_type_prices.get(light_type, 0)
        
        light_panel = st.selectbox("Light Panel", ["(3) LARGE - (3) LARGE", "(2) LARGE - (2) LARGE"])
        license_plate = st.selectbox("License Plate Panel", ["STANDARD WITH 5 SMALL LIGHTS"])
        light_shield = st.selectbox("Light Shield", ["LIGHT SHIELD STANDARD"])
        marker_bottom = st.selectbox("Marker Lights Bottom Rail", ["(5) EACH SIDE", "(6) EACH SIDE", "(7) EACH SIDE"])
        
        # Additional Marker Lights with pricing
        additional_markers = st.number_input("Additional Marker Lights - Each Side", min_value=0, max_value=50, value=30)
        # Price calculation: $120 per additional light for grommet
        if "GROMMET" in light_type:
            prices['additional_lights'] = additional_markers * 120 if additional_markers > 5 else 0
        else:
            prices['additional_lights'] = additional_markers * 140 if additional_markers > 5 else 0
    
    with col2:
        backup_lights = st.selectbox("Back Up Lights", ["NONE", "YES"])
        tarp_shield_lights = st.selectbox("Tarp Shield Lights", ["NONE", "YES"])
        mid_turns = st.selectbox("Mid Turns", ["(1) PAIR LED (UNDER THE BOX)", "NONE"])
        auxiliary_cable = st.selectbox("Auxillary Cable", [
            "7 WAY (ISO) (GLADHANDS 7 WAY SOCKETS MOUNTED ON D/S AREA)"
        ])
        rear_pocket = st.selectbox("Rear Pocket Lights", ["NONE", "YES"])

# TAB 6: PAINT
with tab6:
    st.header("Paint")
    
    col1, col2 = st.columns(2)
    
    with col1:
        chassis_finish = st.selectbox("Chassis Finish", ["NOT POLISHED", "POLISHED"])
        paint_color = st.selectbox("Paint Color", ["GALVANIZED", "BLACK", "WHITE", "RED", "BLUE"])
    
    with col2:
        sideboard_color = st.selectbox("Side Board Color", ["BLACK", "GALVANIZED", "WHITE", "RED"])
        document_holder = st.selectbox("Document Holder", ["STANDARD (ROUND) HOLDER", "RECTANGULAR"])
    
    st.subheader("Special Notes / Additional Requests")
    special_notes = st.text_area("Enter any special requirements", height=100)
    
    steel_galvanized = st.checkbox("All Steel Parts Galvanized", value=True)

# TAB 7: SUMMARY & PRICING
with tab7:
    st.header("Quote Summary")
    
    # Calculate base price from all options
    base_price = sum(prices.values())
    
    # Display itemized pricing
    st.subheader("Itemized Pricing")
    
    pricing_data = []
    for item, price in prices.items():
        if price > 0:
            pricing_data.append({
                "Item": item.replace('_', ' ').title(),
                "Price": f"${price:,.2f}"
            })
    
    if pricing_data:
        pricing_df = pd.DataFrame(pricing_data)
        st.dataframe(pricing_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Final pricing calculations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Additional Items")
        
        # Additional line items
        alcoa_rims_add = st.number_input("ALCOA Rims Additional", min_value=0, value=2000, step=100)
        grain_sock_add = st.number_input("Grain Sock", min_value=0, value=500, step=50)
        
        # Custom line items
        st.write("Add Custom Items:")
        custom_item_name = st.text_input("Item Name")
        custom_item_price = st.number_input("Item Price", min_value=0, value=0, step=100)
        if st.button("Add Custom Item") and custom_item_name:
            st.session_state.line_items.append({
                "name": custom_item_name,
                "price": custom_item_price
            })
            st.success(f"Added {custom_item_name}")
        
        if st.session_state.line_items:
            st.write("Custom Items:")
            for idx, item in enumerate(st.session_state.line_items):
                col_a, col_b, col_c = st.columns([3, 2, 1])
                with col_a:
                    st.write(item['name'])
                with col_b:
                    st.write(f"${item['price']:,.2f}")
                with col_c:
                    if st.button("Remove", key=f"remove_{idx}"):
                        st.session_state.line_items.pop(idx)
                        st.rerun()
    
    with col2:
        st.subheader("Final Pricing")
        
        # Calculate totals
        subtotal = base_price
        discount_amount = subtotal * (discount_percent / 100)
        discounted_price = subtotal - discount_amount
        
        additional_items_total = alcoa_rims_add + grain_sock_add + sum([item['price'] for item in st.session_state.line_items])
        final_total = discounted_price + additional_items_total
        
        # Display pricing
        st.metric("Base Price", f"${subtotal:,.2f}")
        st.metric(f"Discount ({discount_percent}%)", f"-${discount_amount:,.2f}")
        st.metric("Discounted Price", f"${discounted_price:,.2f}")
        st.metric("Additional Items", f"${additional_items_total:,.2f}")
        st.metric("**TOTAL PRICE**", f"**${final_total:,.2f}**")
    
    st.divider()
    
    # Generate Quote Document
    st.subheader("Generate Quote Document")
    
    if st.button("📄 Generate PDF Quote", type="primary"):
        st.info("PDF generation would be implemented here using reportlab or similar library")
    
    # Export to Excel
    if st.button("📊 Export to Excel"):
        # Create export data
        export_data = {
            "Quote Information": {
                "Quote #": quote_number,
                "Date": str(quote_date),
                "Dealer": dealer,
                "Contact": contact,
                "Model": model
            },
            "Specifications": {
                "Trailer Length": trailer_length,
                "Wall Height": wall_height,
                "Chassis Type": chassis_type,
                "Tire Size": tire_size,
            },
            "Pricing": {
                "Base Price": subtotal,
                f"Discount ({discount_percent}%)": -discount_amount,
                "Discounted Price": discounted_price,
                "Additional Items": additional_items_total,
                "TOTAL": final_total
            }
        }
        
        st.success("Excel export functionality ready!")
        st.json(export_data)
    
    # Signature section
    st.divider()
    col_sig1, col_sig2 = st.columns(2)
    with col_sig1:
        st.write("**Customer Signature:**")
        st.write("")
        st.write("_" * 40)
    with col_sig2:
        st.write("**Sales Representative:**")
        st.write("")
        st.write("_" * 40)

# Footer
st.divider()
st.caption(f"Quote Generated: {quote_date} | Discount Applied: {discount_percent}% | Total: ${sum(prices.values()):,.2f}")
