import re
import json
from datetime import datetime as dt
import argparse


def extract_sensor_metadata(file_content: str, num_sensors):
    # section entire preboxup log into just the final selftest
    # selftest starts with either "a" command or "i s" command
    search_string1 = "> a"
    search_string2 = "> i s"
    search_string_opt = "> o d"

    # search entire file for those commands
    # after these two statements,file_content is only selftest
    if search_string_opt in file_content:
        _, _, opt_content = file_content.partition(search_string_opt)
    if search_string1 in file_content:
        _, _, file_content = file_content.partition(search_string1)
    elif search_string2 in file_content:
        _, _, file_content = file_content.partition(search_string2)

    # -----------------VARIABLE CREATION -------------
    # General variables
    # entering as none first so they can be changed later

    datetime = None
    frmwr = None
    apfid = None

    # CTD variables
    ct_serno = None
    ctd_frmwr = None
    ctd_model = None
    ctd_manufac = None
    t_cal_date = None
    p_cal_date = None
    p_serno = None

    # Optode variables
    opt_serno = None
    opt_frmwr = None
    opt_model = None
    opt_manufac = None
    opt_cal_date = None
    opt_manu_date = None

    # Dura (pH) varibles
    dura_serno = None # same as isus serno
    dura_frmwr = None
    dura_model = None
    dura_manufac = None
    dura_cal_date = None
    dura_sensor_serno = None #pH sensor specific number

    # ISUS (Nitrate) variables
    isus_serno = None # same as dura serno
    isus_frmwr = None
    isus_model = None
    isus_manufac = None
    isus_cal_date = None
    # other sensors and variables may be added here as we know more about MSC3

    # FLBB variables
    flbb_serno = None
    flbb_frmwr = None
    flbb_model = None
    flbb_manufac = None
    flbb_cal_date = None

    # OCR variables
    ocr_serno = None
    ocr_frmwr = None
    ocr_model = None
    ocr_manufac = None
    ocr_cal_date = None

    platform = 'APEXapf11'

    # build structure ONCE, before the loop
    structure = {
        "add_date": datetime,
        "platform_model": platform,
        "platform_serial_no": apfid,
        "platform_firmware": frmwr,
        "platform_manufacture_date": None,
        "platform_comments": None,
        "sensors": [{

            # Temperature sensor information (index 0)
            "add_date": datetime,
            "sensor_type": "CTD_TEMP",
            "sensor_model": ctd_model,
            "sensor_serial_no": ct_serno,
            "sensor_manufacturer": ctd_manufac,
            "sensor_firmware": ctd_frmwr,
            "sensor_manufacture_date": None,
            "sensor_comments": None,
            "calibrations": [{
                "add_date": datetime,
                "calibration_date": t_cal_date,
                "parameter_type": "TEMP",
                "provided_to_customer": True,
                "calibration_type": "PRE_DEPLOYMENT",
                "parameter_accuracy": None,
                "parameter_resolution": None,
                "calibration_comments": None,
                "calibration_coefficients": {},
                "calibration_metadata": None
                }] 
           },
          # Conductivity sensor information (index 1)
          {"add_date": datetime,
            "sensor_type": "CTD_CNDC",
            "sensor_model": ctd_model,
            "sensor_serial_no": ct_serno,
            "sensor_manufacturer": ctd_manufac,
            "sensor_firmware": ctd_frmwr,
            "sensor_manufacture_date": None,
            "sensor_comments": None,
            "calibrations": [{
                "add_date": datetime,
                "calibration_date": t_cal_date,
                "parameter_type": "CNDC",
                "provided_to_customer": True,
                "calibration_type": "PRE_DEPLOYMENT",
                "parameter_accuracy": None,
                "parameter_resolution": None,
                "calibration_comments": None,
                "calibration_coefficients": {},
                "calibration_metadata": None
                            }]
          },
          # Pressure sensor information (index 2)
          {"add_date": datetime,
            "sensor_type": "CTD_PRESS",
            "sensor_model": ctd_model,
            "sensor_serial_no": p_serno,
            "sensor_manufacturer": ctd_manufac,
            "sensor_firmware": ctd_frmwr,
            "sensor_manufacture_date": None,
            "sensor_comments": None,
            "calibrations": [{
              "add_date": datetime,
              "calibration_date": p_cal_date,
              "parameter_type": "PRESS",
              "provided_to_customer": True,
              "calibration_type": "PRE_DEPLOYMENT",
              "parameter_accuracy": None,
              "parameter_resolution": None,
              "calibration_comments": None,
              "calibration_coefficients": {},
              "calibration_metadata": None
                            }]
            },

        # Optode sensor information (index 3)
            {"add_date": datetime,
            "sensor_type": "Optode",
            "sensor_model": opt_model,
            "sensor_serial_no": opt_serno,
            "sensor_manufacturer": opt_manufac,
            "sensor_firmware": opt_frmwr,
            "sensor_manufacture_date": opt_manu_date,
            "sensor_comments": None,
            "calibrations": [{
                "add_date": datetime,
                "calibration_date": opt_cal_date,
                "parameter_type": "Oxygen",
                "provided_to_customer": True,
                "calibration_type": "PRE_DEPLOYMENT",
                "parameter_accuracy": None,
                "parameter_resolution": None,
                "calibration_comments": None,
                "calibration_coefficients": {},
                "calibration_metadata": None
                            }]
            }, 
        # pH sensor information (index 4)
            {"add_date": datetime,
            "sensor_type": "DURA",
            "sensor_model": dura_model,
            "sensor_serial_no": dura_serno,
            "sensor_manufacturer": dura_manufac,
            "sensor_firmware": dura_frmwr,
            "sensor_manufacture_date": None,
            "sensor_comments": None,
            "calibrations": [{
                "add_date": datetime,
                "calibration_date": dura_cal_date,
                "parameter_type": "pH",
                "provided_to_customer": True,
                "calibration_type": "PRE_DEPLOYMENT",
                "parameter_accuracy": None,
                "parameter_resolution": None,
                "calibration_comments": None,
                "calibration_coefficients": {},
                "calibration_metadata": None
                            }] 
            }, 
        # Nitrate sensor information (index 5)
            {"add_date": datetime,
            "sensor_type": "Nitrate",
            "sensor_model": isus_model,
            "sensor_serial_no": isus_serno,
            "sensor_manufacturer": isus_manufac,
            "sensor_firmware": isus_frmwr,
            "sensor_manufacture_date": None,
            "sensor_comments": None,
            "calibrations": [{
                "add_date": datetime,
                "calibration_date": isus_cal_date,
                "parameter_type": "Nitrate",
                "provided_to_customer": True,
                "calibration_type": "PRE_DEPLOYMENT",
                "parameter_accuracy": None,
                "parameter_resolution": None,
                "calibration_comments": None,
                "calibration_coefficients": {},
                "calibration_metadata": None
                            }]
            }, 
        # FLBB sensor information (index 6)
            {"add_date": datetime,
            "sensor_type": "FLBB",
            "sensor_model": flbb_model,
            "sensor_serial_no": flbb_serno,
            "sensor_manufacturer": flbb_manufac,
            "sensor_firmware": flbb_frmwr,
            "sensor_manufacture_date": None,
            "sensor_comments": None,
            "calibrations": [{
                "add_date": datetime,
                "calibration_date": flbb_cal_date,
                "parameter_type": "Fluorescence",
                "provided_to_customer": True,
                "calibration_type": "PRE_DEPLOYMENT",
                "parameter_accuracy": None,
                "parameter_resolution": None,
                "calibration_comments": None,
                "calibration_coefficients": {},
                "calibration_metadata": None
                            }]
            },
            {"add_date": datetime,
            "sensor_type": "Radiometer",
            "sensor_model": ocr_model,
            "sensor_serial_no": ocr_serno,
            "sensor_manufacturer": ocr_manufac,
            "sensor_firmware": ocr_frmwr,
            "sensor_manufacture_date": None,
            "sensor_comments": None,
            "calibrations": [{
                "add_date": datetime,
                "calibration_date": ocr_cal_date,
                "parameter_type": "irradiance",
                "provided_to_customer": True,
                "calibration_type": "PRE_DEPLOYMENT",
                "parameter_accuracy": None,
                "parameter_resolution": None,
                "calibration_comments": None,
                "calibration_coefficients": {},
                "calibration_metadata": None
                            }]
            }

    ]}
    # run through every line of the selftest
    for line in file_content.splitlines():

        # update fields in structure here...
        if datetime is None and "(" in line and ")" in line:
            raw_dt = line.split("(", 1)[1].split(")", 1)[0]
            datetime = raw_dt.split(",", 1)[0].strip()

            # add date for whole json file and for each sensor and sensor calibration 
            for i in range(num_sensors):
                structure["add_date"] = datetime
                structure["sensors"][i]["add_date"] = datetime
                structure["sensors"][i]["calibrations"][0]["add_date"] = datetime

        # if float firmware type isnt already recorded, its done here
        if frmwr is None:
            match = re.search(r"FwRev\s+(\d+)", line)
            if match:
                frmwr = match.group(1)
                structure["platform_firmware"] = frmwr

        # if apfid isnt already recorded, its done here
        if apfid is None and "ApfId" in line:
            apfid = line.split('ApfId', 1)[1].split(".")[0].strip()
            structure["platform_serial_no"] = apfid

        # use "SBE41cp" to search for specific lines that only have the serial number for easier spliceing
        if "SBE41cp" in line:
            ctd_model = "Sbe41cp"
            ctd_manufac = "SBE"
            structure['sensors'][0]["sensor_model"] = ctd_model
            structure['sensors'][1]["sensor_model"] = ctd_model
            structure['sensors'][2]["sensor_model"] = ctd_model
            structure['sensors'][0]["sensor_manufacturer"] = ctd_manufac
            structure['sensors'][1]["sensor_manufacturer"] = ctd_manufac
            structure['sensors'][2]["sensor_manufacturer"] = ctd_manufac

            # search for serial number of CT,  and add it to those sensor sections
            match = re.search(r"serno[:\s]*([0-9a-fx]+)", line, re.IGNORECASE)
            if match:
                ct_serno = match.group(1)
                structure["sensors"][0]["sensor_serial_no"] = ct_serno
                structure["sensors"][1]["sensor_serial_no"] = ct_serno

        # add ctd type to the platform model
        if platform == "APEXapf11":
            platform = platform + "Sbe41cp"
            structure["platform_model"] = platform

        # find temperature calibration date and add it to temp sensor block
        if "temperature:" in line:
            t_cal_date = line.split("temperature:", 1)[1].strip()
            structure["sensors"][0]["calibrations"][0]["calibration_date"] = t_cal_date

        # find conductivity calibration date and add it to cndc sensor block
        if "conductivity:" in line:
            c_cal_date = line.split("conductivity:", 1)[1].strip()
            structure["sensors"][1]["calibrations"][0]["calibration_date"] = c_cal_date

        # find pressure calibration date and add it to press sensor block
        if "pressure" in line:

            p_cal_date = line.split(":")[-1].strip()
            structure['sensors'][2]["calibrations"][0]["calibration_date"] = p_cal_date

            # in same line of selftest, look for pressure sensor specific serial number
            match = re.search(r"S/N\s*=\s*(\d+)", line)
            if match:
                p_serno = match.group(1)
                structure['sensors'][2]["sensor_serial_no"] = p_serno

        # go through each ctd information line, and find firmware and calibration vals
        if "Sbe41cpLogCal()" in line:
            # look for a pattern that shows firmware number
            match = re.search(r"V\s+([\d.]+)", line)
            # if code finds that pattern 
            if match:
                version = match.group(1)

                # update firmware for temp, cndc and press sensors
                structure["sensors"][0]["sensor_firmware"] = version
                structure["sensors"][1]["sensor_firmware"] = version
                structure["sensors"][2]["sensor_firmware"] = version

            # look for pattern of all calibration coefficients for temp
            t_matches = re.findall(r"(TA\d)\s*=\s*([-+0-9.eE]+)", line)
            for key, val in t_matches:
                # add all temp cal coefs to dictionary
                structure['sensors'][0]['calibrations'][0]['calibration_coefficients'][key] = float(val)

            # look for pattern of all calibration coefficients for cndc
            c_matches = re.findall(r"\b(G|H|I|J|CTCOR|CPCOR|CWBOTC)\s*=\s*([-+0-9.eE]+)", line)
            for key, val in c_matches:
                # add all cndc cal coefs to dictionary
                structure['sensors'][1]['calibrations'][0]['calibration_coefficients'][key] = float(val)

            # look for pattern of all calibration coefficients for temp
            p_matches = re.findall(r'(P[A-Z0-9]+)\s*=\s*([-+0-9.eE]+)', line)
            for key, val in p_matches:
                # add all press cal coefs to dictionary
                structure['sensors'][2]['calibrations'][0]['calibration_coefficients'][key] = float(val)

        # go throgh all dura/ph lines to find necessary values
        if "DuraConfigLog_()" in line:
            # either seabird or MBARI - is there a way to tell???
            structure['sensors'][4]['sensor_manufacturer'] = "MBARI"

            # go through lines to get serial number
            if "SN" in line:
                match_msc_num = re.search(r"SN:([-+0-9.eE]+)", line)
                if match_msc_num:
                    structure['sensors'][4]["sensor_serial_no"] = match_msc_num.group(1)
            # go through lines to get manufacture date
            if "App Build" in line:
                match_date = re.search(r'([A-Za-z]{3}\s+\d{1,2}\s+\d{4},\s+\d{2}:\d{2}:\d{2})', line)
                if match_date:
                    structure['sensors'][4]['sensor_manufacture_date'] = match_date.group(1)
            # go through lines to get firmware and model (data on the same line)
            if "Application" in line:
                match_msc_frmwr = re.search(r'([A-Za-z]+\s+v\d+\.\d+\.\d+)', line)
                if match_msc_frmwr:
                    structure["sensors"][4]['sensor_firmware'] = match_msc_frmwr.group(1)
                match_msc_model = re.search(r'(MSC\d+\s*\d+)', line)
                if match_msc_model:
                    structure['sensors'][4]['sensor_model'] = match_msc_model.group(1)

        # SEARCH LINES FOR ISUSCONFIGLOG() FOR ALL ISUS VARIABLES
        if "IsusConfigLog_()" in line:
            structure['sensors'][5]['sensor_manufacturer'] = "MBARI"

            if platform == "APEXapf11Sbe41cp":
                platform = platform + "IsusDura"
                structure["platform_model"] = platform

            if "SN" in line:
                match_msc_num = re.search(r"SN:([-+0-9.eE]+)", line)
                if match_msc_num:
                    structure['sensors'][5]["sensor_serial_no"] = match_msc_num.group(1)
            if "App Build" in line:
                match_date = re.search(r'([A-Za-z]{3}\s+\d{1,2}\s+\d{4},\s+\d{2}:\d{2}:\d{2})', line)
                if match_date:
                    structure['sensors'][5]['sensor_manufacture_date'] = match_date.group(1)
            if "Application" in line:
                match_msc_frmwr = re.search(r'([A-Za-z]+\s+v\d+\.\d+\.\d+)', line)
                if match_msc_frmwr:
                    structure["sensors"][5]['sensor_firmware'] = match_msc_frmwr.group(1)
                match_msc_model = re.search(r'(MSC\d+\s*\d+)', line)
                if match_msc_model:
                    structure['sensors'][5]['sensor_model'] = match_msc_model.group(1)
            if "Zeiss" in line:
                match = re.search(r"Zeiss Coefficient Vals,(.*)", line)
                if match:
                    coeffs = match.group(1).split(",")  # split by comma
                    coeffs = [c.strip() for c in coeffs if c.strip()]  # clean blanks
                    coeffs = [float(c) for c in coeffs]  # convert to floats

                    # load into ISUS calibration coefficients dict
                    structure['sensors'][5]['calibrations'][0]['calibration_coefficients']["Zeiss"] = coeffs
        
        # go through lines to get calibration coefficients and cal date
        if "MscCalFile_()" in line:
            if "pH_CalFile" in line:
                match_caldate = re.search(r'(\d{8})', line)
                if match_caldate:
                    date_str = match_caldate.group(1)
                    caldate_obj = dt.strptime(date_str, '%Y%m%d')
                    caldate_formated = caldate_obj.strftime('%B-%d-%y')
                    structure['sensors'][4]['calibrations'][0]['calibration_date'] = caldate_formated

            ph_matches = re.findall(r'.*?\s([A-Za-z0-9_\[\]]+)\s*=\s*([-+0-9.eE]+)\s*$', line)
            for key, val in ph_matches:
                structure['sensors'][4]['calibrations'][0]['calibration_coefficients'][key] = float(val) 
        if "H," in line:
            match = re.search(r'(\d{2}/\d{2}/\d{4})', line)
            if match:
                structure['sensors'][5]['calibrations'][0]['calibration_date'] = match.group(1)
            
        if "WaveLen," in line:
            content = line.split("MscCalFile_()", 1)[1].strip()
            # make into list and drop the first element
            coeff_names = [x.strip() for x in content.split(",")[1:]]

            for str in coeff_names:
                structure['sensors'][5]['calibrations'][0]['calibration_coefficients'][str] = []
        if "E," in line:
            content_val = line.split("MscCalFile_()", 1)[1].strip()
            values = [x.strip() for x in content_val.split(",")[1:]]  # drop "E"

    # Append each value to the right coefficient list
            for name, val in zip(coeff_names, values):
                structure['sensors'][5]['calibrations'][0]['calibration_coefficients'][name].append(val)


    # FLBB VARIABLE STRUCTURE GOES HERE - VARIOUS SEARCH PARAMETERS
        if "FLBB" in line:
            structure['sensors'][6]["sensor_manufacturer"] = "SBE"

            match_fl_serno = re.search(r"SerNo:\s*(\d+)", line)

            if match_fl_serno:
                structure['sensors'][6]['sensor_serial_no'] = match_fl_serno.group(1)

            if "FwRev" in line:
                match_fl_frmwr = re.search(r"\[(.*?)\]", line)
                if match_fl_frmwr:
                    structure["sensors"][6]['sensor_firmware'] = match_fl_frmwr.group(1)
            
            if "wavelengths:" in line:
                match_flbb_cals = re.search(r"Fl\[(\d+)\]\s*Bb\[(\d+)\]", line)
                if match_flbb_cals:
                    fl_val, bb_val = match_flbb_cals.groups()
                    structure['sensors'][6]['calibrations'][0]['calibration_coefficients'] = {
                    "FL": [fl_val],
                    "BB": [bb_val]}

                    if len(structure['sensors'][6]['calibrations'][0]['calibration_coefficients']['FL']) == 2:
                        structure['sensors'][6]['sensor_model'] = "FLBB2-FL"
                        if platform != "APEXapf11Sbe41cpIsusDuraFLBB2":
                            platform = "APEXapf11Sbe41cpIsusDuraFLBB2"
                            structure["platform_model"] = platform
                    else:
                        structure['sensors'][6]['sensor_model'] = "FLBB-FL"
                        if platform != "APEXapf11Sbe41cpIsusDuraFLBB":
                            platform = "APEXapf11Sbe41cpIsusDuraFLBB"
                            structure["platform_model"] = platform
        if "SelfTest()" in line:
            if "Ocr504" in line:
                structure["sensors"][7]['sensor_model'] = "OCR504"
                match_ocr_frmwr = re.search(r"\[(.*?)\]", line)
                if match_ocr_frmwr:
                    structure["sensors"][7]['sensor_firmware'] = match_ocr_frmwr.group(1)
        
        if "Ocr504LogConfig()" in line:
            structure['sensors'][7]["sensor_manufacturer"] = "SBE"
            
            if "serial number:" in line:
                match_ocr_serno = re.search(r"serial number:\s*(\d+)", line)
                if match_ocr_serno:
                    structure['sensors'][7]['sensor_serial_no'] = match_ocr_serno.group(1)
            
            # Initialize calibration_coefficients if not exists
            if 'calibrations' not in structure['sensors'][7]:
                structure['sensors'][7]['calibrations'] = [{}]
            if 'calibration_coefficients' not in structure['sensors'][7]['calibrations'][0]:
                structure['sensors'][7]['calibrations'][0]['calibration_coefficients'] = {}
            
            # Parse optical channel headers and initialize structure
            if "optical channel" in line and ":" in line:
                match_opt_channel = re.search(r"optical channel (\d+):", line)
                if match_opt_channel:
                    channel_num = match_opt_channel.group(1)
                    channel_key = f"optical_channel_{channel_num}"
                    if channel_key not in structure['sensors'][7]['calibrations'][0]['calibration_coefficients']:
                        structure['sensors'][7]['calibrations'][0]['calibration_coefficients'][channel_key] = {}
            
            # Parse calibration coefficients (a0, a1, im)
            coeff_match = re.search(r"\s+(a0|a1|im):([0-9.-]+(?:e[+-]?\d+)?)", line)
            if coeff_match:
                coeff_name = coeff_match.group(1)
                coeff_value = coeff_match.group(2)
                
                # Find the current optical channel by looking for the most recent channel definition
                # This assumes the coefficients appear after the channel header
                coeffs = structure['sensors'][7]['calibrations'][0]['calibration_coefficients']
                if coeffs:
                    # Get the last added channel (most recent)
                    last_channel = list(coeffs.keys())[-1]
                    coeffs[last_channel][coeff_name] = coeff_value


        
        



        # OPTODE SECTION - TWO DIFFERENT MODELS AND DIFFERENT FILE FOR CAL COEFFICIENTS

        # Aanderaa optode sensor info if applicable
        if "Optode" in line:
            structure["sensors"][3]["sensor_manufacturer"] = "Aanderaa"
            # update platform model to include optode
            if platform != "APEXapf11Sbe41cpOptodeIsusDuraFLBB" or platform != "APEXapf11Sbe41cpOptodeIsusDuraFLBB2" :
                
                if platform == "APEXapf11Sbe41cpIsusDuraFLBB":
                    platform = "APEXapf11Sbe41cpOptodeIsusDuraFLBB"
                    structure["platform_model"] = platform
                else:
                    platform = "APEXapf11Sbe41cpOptodeIsusDuraFLBB2"
                    structure["platform_model"] = platform

            # match line pattern to look for optode serial number
            match_opt_serno = re.search(r"SerNo:\s*(\d+)", line)
            if match_opt_serno:
                # if there is a match, update optode serial number
                structure['sensors'][3]["sensor_serial_no"] = match_opt_serno.group(1)

            #
            match_opt_frmwr = re.search(r"accepted:\s*\[([\d.]+)\]", line)
            if match_opt_frmwr:
                structure['sensors'][3]["sensor_firmware"] = match_opt_frmwr.group(1)

    # run through every line of the optode configuration       
    for line in opt_content.splitlines():
        if "Oxygen Optode" in line:
            match = re.search(r'Product Name\s+(\d+)', line)
            if match:
                opt_model = match.group(1)
                structure['sensors'][3]["sensor_model"] = opt_model

        if "Production Date" in line:
            match = re.search(r'(\d{4}-\d{2}-\d{2})$', line)
            if match:
                opt_manu_date = match.group(1)
                structure['sensors'][3]['sensor_manufacture_date'] = opt_manu_date

        # optode SBE83 sensor info if applicable
        if "Sbe83LogConfig()" in line:
            structure["sensors"][3]["sensor_manufacturer"] = "SBE"

            if platform != "APEXapf11Sbe41cpSbe83IsusDuraFLBB" or platform != "APEXapf11Sbe41cpSbe83IsusDuraFLBB2" :
                
                if platform == "APEXapf11Sbe41cpIsusDuraFLBB":
                    platform = "APEXapf11Sbe41cpSbe83IsusDuraFLBB"
                    structure["platform_model"] = platform
                else:
                    platform = "APEXapf11Sbe41cpSbe83IsusDuraFLBB2"
                    structure["platform_model"] = platform

            # UPDATE ALL OF THIS EVENTUALLY AFTER I KNOW THIS FORMAT

        # Aanderaa optode sensor info if applicable
        if "Optode" in line:
            structure["sensors"][3]["sensor_manufacturer"] = "Aanderaa"

            # match line pattern to look for optode serial number
            match_opt_serno = re.search(r"SerNo:\s*(\d+)", line)
            if match_opt_serno:
                # if there is a match, update optode serial number
                structure['sensors'][3]["sensor_serial_no"] = match_opt_serno.group(1)

            #
            match_opt_frmwr = re.search(r"accepted:\s*\[([\d.]+)\]", line)
            if match_opt_frmwr:
                structure['sensors'][3]["sensor_firmware"] = match_opt_frmwr.group(1)

    # run through every line of the optode configuration       
    for line in opt_content.splitlines():
        if "Oxygen Optode" in line:
            match = re.search(r'Product Name\s+(\d+)', line)
            if match:
                opt_model = match.group(1)
                structure['sensors'][3]["sensor_model"] = opt_model

        if "Production Date" in line:
            match = re.search(r'(\d{4}-\d{2}-\d{2})$', line)
            if match:
                opt_manu_date = match.group(1)
                structure['sensors'][3]['sensor_manufacture_date'] = opt_manu_date

        if "OptodeLogConfig()" in line:
        # Split after OptodeLogConfig() and strip extra spaces
            parts = line.split("OptodeLogConfig()")[1].strip().split()
            if len(parts) < 4:
                continue  # skip lines that don’t have enough data
            key = parts[0]  # coefficient name
            try:
                value = [float(x) for x in parts[3:]]
            except ValueError:
            # if any value is non-numeric (like FoilID 2310M), keep as string
                value = parts[3:]
        
            structure['sensors'][3]['calibrations'][0]['calibration_coefficients'][key] = value

    return structure

def prebox_to_json(preboxup_log, num_sensors, output_file):
    with open(preboxup_log, 'r', encoding="latin-1") as file:
        file_content = file.read()

        # find variable in Selftest format
        data = extract_sensor_metadata(file_content, num_sensors + 1)

        # Convert dict → JSON string
        json_string = json.dumps(data, indent=2)

        # Print to screen
        #print(json_string)

    with open(output_file, "w", encoding="latin-1", errors='ignore') as f:
        json.dump(data, f, indent=2)  # indent=2 makes it pretty-printed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Preboxup log to JSON")
    parser.add_argument("file_path", help="Path to the log file")
    parser.add_argument("num_sensors", type=int, help="Number of sensors")
    parser.add_argument("output_file", help="Output JSON filename")

    args = parser.parse_args()

    prebox_to_json(args.file_path, args.num_sensors, args.output_file)