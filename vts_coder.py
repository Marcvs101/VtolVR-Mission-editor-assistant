class VtsCoder():
    sub_tokens = ["CustomScenario","UNITS","PATHS","WAYPOINTS","UNITGROUPS","TimedEventGroups","TRIGGER_EVENTS","OBJECTIVES","OBJECTIVES_OPFOR","StaticObjects","Conditionals","ConditionalActions","EventSequences","BASES","GlobalValues","Briefing","Briefing_B"]

    # vts -> dict
    def decode(vts_text):
        result = dict()

        # Prime result structure
        result["CustomScenario"] = dict()
        result["CustomScenario"]["UNITS"] = list()
        result["CustomScenario"]["PATHS"] = list()
        result["CustomScenario"]["WAYPOINTS"] = dict()
        result["CustomScenario"]["WAYPOINTS"]["bullseyeID"] = ""
        result["CustomScenario"]["WAYPOINTS"]["waypoint_list"] = list()
        result["CustomScenario"]["UNITGROUPS"] = dict()
        result["CustomScenario"]["TimedEventGroups"] = list()
        result["CustomScenario"]["TRIGGER_EVENTS"] = list()
        result["CustomScenario"]["OBJECTIVES"] = list()
        result["CustomScenario"]["OBJECTIVES_OPFOR"] = list()
        result["CustomScenario"]["StaticObjects"] = list()
        result["CustomScenario"]["Conditionals"] = list()
        result["CustomScenario"]["ConditionalActions"] = list()
        result["CustomScenario"]["EventSequences"] = list()
        result["CustomScenario"]["BASES"] = list()
        result["CustomScenario"]["GlobalValues"] = list()
        result["CustomScenario"]["Briefing"] = list()
        result["CustomScenario"]["Briefing_B"] = list()

        # Split major tokens
        vts_split = dict()

        last_token = ""
        for sub_token in VtsCoder.sub_tokens:
            local_split = vts_text.split(sub_token,1)
            vts_split[last_token] = (local_split[0].replace("\t","").strip())
            vts_text = local_split[1].replace("\t","").replace("\n{","{").strip()
            last_token = sub_token
        vts_split[last_token] = vts_text
    

        # Decode UNITS list
        target = vts_split["UNITS"]
        for split_elem in target.split("UnitSpawner"):
            elem_struct = VtsCoder.decode_recursive("UnitSpawner"+split_elem)
            if "UnitSpawner" in elem_struct:
                elem_struct = elem_struct["UnitSpawner"]
            if elem_struct != {}:
                result["CustomScenario"]["UNITS"].append(elem_struct)
        

        # Decode PATHS list
        target = vts_split["PATHS"]
        for split_elem in target.split("PATH"):
            elem_struct = VtsCoder.decode_recursive("PATH"+split_elem)
            if "PATH" in elem_struct:
                elem_struct = elem_struct["PATH"]
            if elem_struct != {}:
                result["CustomScenario"]["PATHS"].append(elem_struct)


        # waypoint bullseye
        target = vts_split["WAYPOINTS"]
        bullseye = target[target.find("=")+1:]
        bullseye = bullseye[:bullseye.find("\n")]
        result["CustomScenario"]["WAYPOINTS"]["bullseyeID"] = bullseye.strip()
        target = target[target.find(bullseye)+1:]


        # Decode WAYPOINT list
        for split_elem in target.split("WAYPOINT"):
            elem_struct = VtsCoder.decode_recursive("WAYPOINT"+split_elem)
            if "WAYPOINT" in elem_struct:
                elem_struct = elem_struct["WAYPOINT"]
            if elem_struct != {}:
                result["CustomScenario"]["WAYPOINTS"]["waypoint_list"].append(elem_struct)


        # Decode UNITGROUPS list
        target = vts_split["UNITGROUPS"]
        elem_struct = VtsCoder.decode_recursive("DUMMY"+target)
        if "DUMMY" in elem_struct:
            elem_struct = elem_struct["DUMMY"]
        if elem_struct != {}:
            result["CustomScenario"]["UNITGROUPS"] = elem_struct


        # Decode TimedEventGroups list
        target = vts_split["TimedEventGroups"]
        for event_group in target.split("TimedEventGroup"):
            info_split = event_group.split("TimedEventInfo")
            temp_struct = VtsCoder.decode_recursive("TimedEventGroup"+info_split[0]+"}}")
            if "TimedEventGroup" in temp_struct:
                temp_struct = temp_struct["TimedEventGroup"]
            elem_struct = temp_struct
            elem_struct["TimedEventInfo_list"] = list()
            info_split.pop(0)

            for event_info in info_split:
                event_info_struct = VtsCoder.parse_event(event_info)
                if event_info_struct != dict():
                    elem_struct["TimedEventInfo_list"].append(event_info_struct)

            if elem_struct != {"TimedEventInfo_list":[]}:
                result["CustomScenario"]["TimedEventGroups"].append(elem_struct)
            

        # Decode TRIGGER_EVENTS list
        target = vts_split["TRIGGER_EVENTS"]
        for event_group in target.split("TriggerEvent"):
            info_split = event_group.split("EventInfo")
            temp_struct = VtsCoder.decode_recursive("TriggerEvent"+info_split[0]+"}}")
            if "TriggerEvent" in temp_struct:
                temp_struct = temp_struct["TriggerEvent"]
            elem_struct = temp_struct
            elem_struct["EventInfo_list"] = list()
            info_split.pop(0)

            for event_info in info_split:
                event_info_struct = VtsCoder.parse_event(event_info)
                if event_info_struct != dict():
                    elem_struct["EventInfo_list"].append(event_info_struct)

            if elem_struct != {"EventInfo_list":[]}:
                result["CustomScenario"]["TRIGGER_EVENTS"].append(elem_struct)
            

        # Decode OBJECTIVES list
        target = vts_split["OBJECTIVES"]
        for objective in target.split("Objective{"):
            if objective.strip() != "{" and objective.strip() != "{\n}":
                data_fields = objective.split("startEvent")[0]+"\nfields"+objective.split("fields")[1]
                start_event = objective.split("startEvent")[1].split("failEvent")[0]
                fail_event = objective.split("failEvent")[1].split("completeEvent")[0]
                complete_event = objective.split("completeEvent")[1].split("fields")[0]

                temp_struct = VtsCoder.decode_recursive("Data"+data_fields+"}}")
                if "Data" in temp_struct:
                    temp_struct = temp_struct["Data"]
                data_struct = temp_struct

                elem_struct = data_struct
                elem_struct["start"] = list()
                elem_struct["fail"] = list()
                elem_struct["complete"] = list()

                for event_info in start_event.split("EventInfo{"):
                    event_info_struct = VtsCoder.parse_event(event_info)
                    if event_info_struct != dict():
                        elem_struct["start"].append(event_info_struct)
                
                for event_info in fail_event.split("EventInfo{"):
                    event_info_struct = VtsCoder.parse_event(event_info)
                    if event_info_struct != dict():
                        elem_struct["fail"].append(event_info_struct)

                for event_info in complete_event.split("EventInfo{"):
                    event_info_struct = VtsCoder.parse_event(event_info)
                    if event_info_struct != dict():
                        elem_struct["complete"].append(event_info_struct)

                result["CustomScenario"]["OBJECTIVES"].append(elem_struct)

            
        # Decode OBJECTIVES_OPFOR list
        target = vts_split["OBJECTIVES_OPFOR"]
        for objective in target.split("Objective{"):
            if objective.strip() != "{" and objective.strip() != "{\n}":
                data_fields = objective.split("startEvent")[0]+"\nfields"+objective.split("fields")[1]
                start_event = objective.split("startEvent")[1].split("failEvent")[0]
                fail_event = objective.split("failEvent")[1].split("completeEvent")[0]
                complete_event = objective.split("completeEvent")[1].split("fields")[0]

                temp_struct = VtsCoder.decode_recursive("Data"+data_fields+"}}")
                if "Data" in temp_struct:
                    temp_struct = temp_struct["Data"]
                data_struct = temp_struct

                elem_struct = data_struct
                elem_struct["start"] = list()
                elem_struct["fail"] = list()
                elem_struct["complete"] = list()

                for event_info in start_event.split("EventInfo{"):
                    event_info_struct = VtsCoder.parse_event(event_info)
                    if event_info_struct != dict():
                        elem_struct["start"].append(event_info_struct)
                
                for event_info in fail_event.split("EventInfo{"):
                    event_info_struct = VtsCoder.parse_event(event_info)
                    if event_info_struct != dict():
                        elem_struct["fail"].append(event_info_struct)

                for event_info in complete_event.split("EventInfo{"):
                    event_info_struct = VtsCoder.parse_event(event_info)
                    if event_info_struct != dict():
                        elem_struct["complete"].append(event_info_struct)

                result["CustomScenario"]["OBJECTIVES_OPFOR"].append(elem_struct)

            
        # Decode StaticObjects list
        target = vts_split["StaticObjects"]
        for split_elem in target.split("StaticObject"):
            elem_struct = VtsCoder.decode_recursive("StaticObject"+split_elem)
            if "StaticObject" in elem_struct:
                elem_struct = elem_struct["StaticObject"]
            if elem_struct != {}:
                result["CustomScenario"]["StaticObjects"].append(elem_struct)
            

        # Decode Conditionals list
            

        # Decode ConditionalActions list
        target = vts_split["ConditionalActions"]
        for base_action in target.split("ConditionalAction{"):
            if base_action.strip() != "{":
                generic_info = base_action.split("BASE_BLOCK{")[0]
                block_info = base_action.split("BASE_BLOCK{")[1].split("CONDITIONAL")[0]
                conditional_text = base_action.split("CONDITIONAL{")[1].split("ACTIONS")[0]
                actions_text = base_action.split("ACTIONS{")[1].split("ELSE_ACTIONS")[0]
                else_text = base_action.split("ELSE_ACTIONS{")[1]

                temp_struct = VtsCoder.decode_recursive("Info"+generic_info+"\n"+block_info+"}}")
                if "Info" in temp_struct:
                    temp_struct = temp_struct["Info"]
                elem_struct = temp_struct

                elem_struct["actions"] = VtsCoder.parse_event(actions_text)
                elem_struct["else_actions"] = VtsCoder.parse_event(else_text)

                if elem_struct != {"EventInfo_list":[]}:
                    result["CustomScenario"]["ConditionalActions"].append(elem_struct)
    

        # Decode EventSequences list
        target = vts_split["EventSequences"]
        for sequence in target.split("SEQUENCE"):
            event_split = sequence.split("EVENT")
            temp_struct = VtsCoder.decode_recursive("TriggerEvent"+event_split[0]+"}}")
            if "TriggerEvent" in temp_struct:
                temp_struct = temp_struct["TriggerEvent"]
            elem_struct = temp_struct
            elem_struct["Event_list"] = list()
            event_split.pop(0)

            for event in event_split:
                event_struct = VtsCoder.parse_event(event)
                if event_struct != dict():
                    new_event_struct = dict()
                    for key in event_struct:
                        if key == "EventInfo":
                            for subkey in event_struct[key]:
                                new_event_struct[subkey] = event_struct[key][subkey]
                        else:
                            new_event_struct[key] = event_struct[key]
                    elem_struct["Event_list"].append(new_event_struct)

            if elem_struct != {"Event_list":[]}:
                result["CustomScenario"]["EventSequences"].append(elem_struct)
            

        # Decode BASES list
        target = vts_split["BASES"]
        for split_elem in target.split("BaseInfo"):
            elem_struct = VtsCoder.decode_recursive("BaseInfo"+split_elem)
            if "BaseInfo" in elem_struct:
                elem_struct = elem_struct["BaseInfo"]
            if elem_struct != {}:
                result["CustomScenario"]["BASES"].append(elem_struct)


        # Decode GlobalValues list
        target = vts_split["GlobalValues"]
        for split_elem in target.split("gv"):
            elem_struct = VtsCoder.decode_recursive("gv"+split_elem)
            if "gv" in elem_struct:
                elem_struct = elem_struct["gv"]
            if elem_struct != {}:
                result["CustomScenario"]["GlobalValues"].append(elem_struct)


        # Decode Briefing list
        target = vts_split["Briefing"]
        for split_elem in target.split("BRIEFING_NOTE"):
            elem_struct = VtsCoder.decode_recursive("BRIEFING_NOTE"+split_elem)
            if "BRIEFING_NOTE" in elem_struct:
                elem_struct = elem_struct["BRIEFING_NOTE"]
            if elem_struct != {}:
                result["CustomScenario"]["Briefing"].append(elem_struct)

        target = vts_split["Briefing_B"]
        for split_elem in target.split("BRIEFING_NOTE"):
            elem_struct = VtsCoder.decode_recursive("BRIEFING_NOTE"+split_elem)
            if "BRIEFING_NOTE" in elem_struct:
                elem_struct = elem_struct["BRIEFING_NOTE"]
            if elem_struct != {}:
                result["CustomScenario"]["Briefing_B"].append(elem_struct)

        return result
    

    def parse_event(event_info_string):
        event_info_struct = dict()

        target_split = event_info_string.split("EventTarget")
        temp_struct = VtsCoder.decode_recursive("TimedEventInfo"+target_split[0]+"}}")
        if "TimedEventInfo" in temp_struct:
            temp_struct = temp_struct["TimedEventInfo"]
        event_struct = temp_struct
        event_struct["EventTarget_list"] = list()
        target_split.pop(0)

        for event_target in target_split:
            param_split = event_target.split("ParamInfo")
            temp_struct = VtsCoder.decode_recursive("EventTarget"+param_split[0]+"}}")
            if "EventTarget" in temp_struct:
                temp_struct = temp_struct["EventTarget"]
            target_struct = temp_struct
            target_struct["ParamInfo_list"] = list()
            param_split.pop(0)

            event_struct["EventTarget_list"].append(target_struct)

            for event_param in param_split:
                param_attr_split = event_param.split("ParamAttrInfo")
                temp_struct = VtsCoder.decode_recursive("ParamInfo"+param_attr_split[0]+"}}")
                if "ParamInfo" in temp_struct:
                    temp_struct = temp_struct["ParamInfo"]
                param_struct = temp_struct
                param_struct["ParamAttrInfo"] = list()
                param_attr_split.pop(0)

                target_struct["ParamInfo_list"].append(param_struct)

                for event_param_attr in param_attr_split:
                    temp_struct = VtsCoder.decode_recursive("ParamAttrInfo"+event_param_attr+"}}")
                    if "ParamAttrInfo" in temp_struct:
                        temp_struct = temp_struct["ParamAttrInfo"]
                    param_struct["ParamAttrInfo"].append(temp_struct)

        if event_struct != {"EventTarget_list":list()}:
            event_info_struct = event_struct

        return event_info_struct


    def decode_recursive(text):
        result = dict()

        skip_block = 0
        rolling_text = text

        for line in text.split("\n"):
            rolling_text = rolling_text[rolling_text.find("\n")+1:]

            if "}" in line:
                if skip_block > 0:
                    skip_block = skip_block - 1
                else:
                    return result
            elif "{" in line:
                if skip_block == 0:
                    key = line.replace("{","").strip()
                    result[key] = VtsCoder.decode_recursive(rolling_text)
                skip_block = skip_block + 1
            elif "=" in line:
                if skip_block == 0:
                    key = line.split("=")[0].strip()
                    value = line.split("=")[1].strip()

                    result[key] = value

        return result




#"""
import json

f = open(file="mission/01 - Resolution.vts")
content = f.read()
f.close()

result = VtsCoder.decode(content)
f = open(file="test_out.json",mode="w")
f.write(json.dumps(result,indent=4,sort_keys=False))
f.close
#"""