from vts_coder import VtsCoder
#import plotly.express as px
from pyvis.network import Network

f = open(file="mission/01 - Resolution.vts")
mission_file = f.read()
f.close()

mission_dict = VtsCoder.decode(mission_file)["CustomScenario"]

# Get units and coordinates
unit_dict = dict()
for unit in mission_dict["UNITS"]:
    unit_struct = dict()
    unit_struct["name"] = unit["unitName"]
    unit_struct["allied"] = ("allied" in unit["unitID"].lower())
    text_coords = unit["lastValidPlacement"].replace("(","").replace(")","").split(",")
    unit_struct["x"] = float(text_coords[0].strip())
    unit_struct["y"] = float(text_coords[1].strip())
    unit_struct["z"] = float(text_coords[2].strip())

    unit_dict[unit["unitInstanceID"]] = unit_struct

"""
fig = px.scatter(text=[i["name"] for i in unit_dict.values()], 
                 x=[i["x"] for i in unit_dict.values()], 
                 y=[i["z"] for i in unit_dict.values()],
                 color=[i["allied"] for i in unit_dict.values()]
                )
fig.show()
"""





# Get Event Graph
net = Network(height="930px",width="100%",directed=True)


# Get nodes from objectives
objective_dict = dict()
for objective in mission_dict["OBJECTIVES"]:
    objective_struct = dict()
    objective_struct["name"] = objective["objectiveName"]
    objective_struct["start"] = list()
    objective_struct["fail"] = list()
    objective_struct["complete"] = list()

    for event in objective["start"]:
        for target in event["EventTarget_list"]:
            if target["targetType"] == "Trigger_Events":
                if target["methodName"] == "Trigger":
                    objective_struct["start"].append({"type":"trigger","method":"trigger","target":target["targetID"]})
                elif target["methodName"] == "Enable":
                    objective_struct["start"].append({"type":"trigger","method":"enable","target":target["targetID"]})
                elif target["methodName"] == "Disable":
                    objective_struct["start"].append({"type":"trigger","method":"disable","target":target["targetID"]})
            
            elif target["targetType"] == "Timed_Events":
                if target["methodName"] == "Begin":
                    objective_struct["start"].append({"type":"timed","method":"begin","target":target["targetID"]})
                elif target["methodName"] == "Stop":
                    objective_struct["start"].append({"type":"timed","method":"stop","target":target["targetID"]})
            
            elif target["targetType"] == "Event_Sequences":
                if target["methodName"] == "Begin":
                    objective_struct["start"].append({"type":"sequence","method":"begin","target":target["targetID"]})
                elif target["methodName"] == "Stop":
                    objective_struct["start"].append({"type":"sequence","method":"stop","target":target["targetID"]})
                elif target["methodName"] == "Restart":
                    objective_struct["start"].append({"type":"sequence","method":"restart","target":target["targetID"]})

            elif target["targetType"] == "System":
                if target["methodName"] == "FireConditionalAction":
                    for event_info in target["ParamInfo_list"]:
                        if event_info["type"] == "ConditionalActionReference":
                            objective_struct["start"].append({"type":"conditional_action","method":"trigger","target":event_info["value"]})

            elif target["targetType"] == "Objective":
                if target["methodName"] == "BeginObjective":
                    objective_struct["start"].append({"type":"objective","method":"begin","target":target["targetID"]})
                elif target["methodName"] == "CompleteObjective":
                    objective_struct["start"].append({"type":"objective","method":"complete","target":target["targetID"]})
                elif target["methodName"] == "FailObjective":
                    objective_struct["start"].append({"type":"objective","method":"fail","target":target["targetID"]})
                elif target["methodName"] == "ResetObjective":
                    objective_struct["start"].append({"type":"objective","method":"reset","target":target["targetID"]})
                elif target["methodName"] == "CancelObjective":
                    objective_struct["start"].append({"type":"objective","method":"camcel","target":target["targetID"]})

    for event in objective["fail"]:
        for target in event["EventTarget_list"]:
            if target["targetType"] == "Trigger_Events":
                if target["methodName"] == "Trigger":
                    objective_struct["fail"].append({"type":"trigger","method":"trigger","target":target["targetID"]})
                elif target["methodName"] == "Enable":
                    objective_struct["fail"].append({"type":"trigger","method":"enable","target":target["targetID"]})
                elif target["methodName"] == "Disable":
                    objective_struct["fail"].append({"type":"trigger","method":"disable","target":target["targetID"]})
            
            elif target["targetType"] == "Timed_Events":
                if target["methodName"] == "Begin":
                    objective_struct["fail"].append({"type":"timed","method":"begin","target":target["targetID"]})
                elif target["methodName"] == "Stop":
                    objective_struct["fail"].append({"type":"timed","method":"stop","target":target["targetID"]})
            
            elif target["targetType"] == "Event_Sequences":
                if target["methodName"] == "Begin":
                    objective_struct["fail"].append({"type":"sequence","method":"begin","target":target["targetID"]})
                elif target["methodName"] == "Stop":
                    objective_struct["fail"].append({"type":"sequence","method":"stop","target":target["targetID"]})
                elif target["methodName"] == "Restart":
                    objective_struct["fail"].append({"type":"sequence","method":"restart","target":target["targetID"]})

            elif target["targetType"] == "System":
                if target["methodName"] == "FireConditionalAction":
                    for event_info in target["ParamInfo_list"]:
                        if event_info["type"] == "ConditionalActionReference":
                            objective_struct["fail"].append({"type":"conditional_action","method":"trigger","target":event_info["value"]})

            elif target["targetType"] == "Objective":
                if target["methodName"] == "BeginObjective":
                    objective_struct["fail"].append({"type":"objective","method":"begin","target":target["targetID"]})
                elif target["methodName"] == "CompleteObjective":
                    objective_struct["fail"].append({"type":"objective","method":"complete","target":target["targetID"]})
                elif target["methodName"] == "FailObjective":
                    objective_struct["fail"].append({"type":"objective","method":"fail","target":target["targetID"]})
                elif target["methodName"] == "ResetObjective":
                    objective_struct["fail"].append({"type":"objective","method":"reset","target":target["targetID"]})
                elif target["methodName"] == "CancelObjective":
                    objective_struct["fail"].append({"type":"objective","method":"camcel","target":target["targetID"]})

    for event in objective["complete"]:
        for target in event["EventTarget_list"]:
            if target["targetType"] == "Trigger_Events":
                if target["methodName"] == "Trigger":
                    objective_struct["complete"].append({"type":"trigger","method":"trigger","target":target["targetID"]})
                elif target["methodName"] == "Enable":
                    objective_struct["complete"].append({"type":"trigger","method":"enable","target":target["targetID"]})
                elif target["methodName"] == "Disable":
                    objective_struct["complete"].append({"type":"trigger","method":"disable","target":target["targetID"]})
            
            elif target["targetType"] == "Timed_Events":
                if target["methodName"] == "Begin":
                    objective_struct["complete"].append({"type":"timed","method":"begin","target":target["targetID"]})
                elif target["methodName"] == "Stop":
                    objective_struct["complete"].append({"type":"timed","method":"stop","target":target["targetID"]})
            
            elif target["targetType"] == "Event_Sequences":
                if target["methodName"] == "Begin":
                    objective_struct["complete"].append({"type":"sequence","method":"begin","target":target["targetID"]})
                elif target["methodName"] == "Stop":
                    objective_struct["complete"].append({"type":"sequence","method":"stop","target":target["targetID"]})
                elif target["methodName"] == "Restart":
                    objective_struct["complete"].append({"type":"sequence","method":"restart","target":target["targetID"]})

            elif target["targetType"] == "System":
                if target["methodName"] == "FireConditionalAction":
                    for event_info in target["ParamInfo_list"]:
                        if event_info["type"] == "ConditionalActionReference":
                            objective_struct["complete"].append({"type":"conditional_action","method":"trigger","target":event_info["value"]})

            elif target["targetType"] == "Objective":
                if target["methodName"] == "BeginObjective":
                    objective_struct["complete"].append({"type":"objective","method":"begin","target":target["targetID"]})
                elif target["methodName"] == "CompleteObjective":
                    objective_struct["complete"].append({"type":"objective","method":"complete","target":target["targetID"]})
                elif target["methodName"] == "FailObjective":
                    objective_struct["complete"].append({"type":"objective","method":"fail","target":target["targetID"]})
                elif target["methodName"] == "ResetObjective":
                    objective_struct["complete"].append({"type":"objective","method":"reset","target":target["targetID"]})
                elif target["methodName"] == "CancelObjective":
                    objective_struct["complete"].append({"type":"objective","method":"camcel","target":target["targetID"]})

    objective_dict[objective["objectiveID"]] = objective_struct
    net.add_node("o"+objective["objectiveID"],objective_struct["name"]+" ("+objective["objectiveID"]+")",color="#00ffff",shape="star")


# Get nodes from trigger events
trigger_event_dict = dict()
for event in mission_dict["TRIGGER_EVENTS"]:
    event_struct = dict()
    event_struct["name"] = event["eventName"]

    event_struct["triggered_events_triggered"] = list()
    event_struct["triggered_events_disabled"] = list()
    event_struct["triggered_events_enabled"] = list()
    
    event_struct["timed_events_stop"] = list()
    event_struct["timed_events_start"] = list()
    
    event_struct["event_sequences_start"] = list()
    event_struct["event_sequences_stop"] = list()
    event_struct["event_sequences_restart"] = list()

    event_struct["conditional_actions_trigger"] = list()
    
    event_struct["objectives_begin"] = list()
    event_struct["objectives_completed"] = list()
    event_struct["objectives_failed"] = list()
    event_struct["objectives_reset"] = list()
    event_struct["objectives_cancel"] = list()

    for event_info in event["EventInfo_list"]:
        for event_target in event_info["EventTarget_list"]:
            if event_target["targetType"] == "Trigger_Events":
                if event_target["methodName"] == "Trigger":
                    event_struct["triggered_events_triggered"].append(event_target["targetID"])
                elif event_target["methodName"] == "Disable":
                    event_struct["triggered_events_disabled"].append(event_target["targetID"])
                elif event_target["methodName"] == "Enable":
                    event_struct["triggered_events_enabled"].append(event_target["targetID"])

            elif event_target["targetType"] == "Timed_Events":
                if event_target["methodName"] == "Stop":
                    event_struct["timed_events_stop"].append(event_target["targetID"])
                elif event_target["methodName"] == "Begin":
                    event_struct["timed_events_start"].append(event_target["targetID"])

            elif event_target["targetType"] == "Event_Sequences":
                if event_target["methodName"] == "Stop":
                    event_struct["event_sequences_stop"].append(event_target["targetID"])
                elif event_target["methodName"] == "Begin":
                    event_struct["event_sequences_start"].append(event_target["targetID"])
                elif event_target["methodName"] == "Restart":
                    event_struct["event_sequences_restart"].append(event_target["targetID"])

            elif event_target["targetType"] == "System":
                if event_target["methodName"] == "FireConditionalAction":
                    for event_info in event_target["ParamInfo_list"]:
                        if event_info["type"] == "ConditionalActionReference":
                            event_struct["conditional_actions_trigger"].append(event_info["value"])

            elif event_target["targetType"] == "Objective":
                if event_target["methodName"] == "BeginObjective":
                    event_struct["objectives_begin"].append(event_target["targetID"])
                elif event_target["methodName"] == "CompleteObjective":
                    event_struct["objectives_completed"].append(event_target["targetID"])
                elif event_target["methodName"] == "FailObjective":
                    event_struct["objectives_failed"].append(event_target["targetID"])
                elif event_target["methodName"] == "ResetObjective":
                    event_struct["objectives_reset"].append(event_target["targetID"])
                elif event_target["methodName"] == "CancelObjective":
                    event_struct["objectives_cancel"].append(event_target["targetID"])

    trigger_event_dict[event["id"]] = event_struct
    net.add_node("t"+event["id"],event_struct["name"]+" ("+event["id"]+")",color="#ffff00")


# Get nodes from timed events
timed_event_dict = dict()
for event in mission_dict["TimedEventGroups"]:
    event_struct = dict()
    event_struct["name"] = event["groupName"]
    event_struct["triggered_events_triggered"] = list()
    event_struct["triggered_events_disabled"] = list()
    event_struct["triggered_events_enabled"] = list()
    
    event_struct["timed_events_stop"] = list()
    event_struct["timed_events_start"] = list()
    
    event_struct["event_sequences_start"] = list()
    event_struct["event_sequences_stop"] = list()
    event_struct["event_sequences_restart"] = list()

    event_struct["conditional_actions_trigger"] = list()
    
    event_struct["objectives_begin"] = list()
    event_struct["objectives_completed"] = list()
    event_struct["objectives_failed"] = list()
    event_struct["objectives_reset"] = list()
    event_struct["objectives_cancel"] = list()

    for event_info in event["TimedEventInfo_list"]:
        for event_target in event_info["EventTarget_list"]:
            if event_target["targetType"] == "Trigger_Events":
                if event_target["methodName"] == "Trigger":
                    event_struct["triggered_events_triggered"].append(event_target["targetID"])
                elif event_target["methodName"] == "Disable":
                    event_struct["triggered_events_disabled"].append(event_target["targetID"])
                elif event_target["methodName"] == "Enable":
                    event_struct["triggered_events_enabled"].append(event_target["targetID"])
            
            elif event_target["targetType"] == "Timed_Events":
                if event_target["methodName"] == "Stop":
                    event_struct["timed_events_stop"].append(event_target["targetID"])
                elif event_target["methodName"] == "Begin":
                    event_struct["timed_events_start"].append(event_target["targetID"])

            elif event_target["targetType"] == "Event_Sequences":
                if event_target["methodName"] == "Stop":
                    event_struct["event_sequences_stop"].append(event_target["targetID"])
                elif event_target["methodName"] == "Begin":
                    event_struct["event_sequences_start"].append(event_target["targetID"])
                elif event_target["methodName"] == "Restart":
                    event_struct["event_sequences_restart"].append(event_target["targetID"])

            elif event_target["targetType"] == "System":
                if event_target["methodName"] == "FireConditionalAction":
                    for event_info in event_target["ParamInfo_list"]:
                        if event_info["type"] == "ConditionalActionReference":
                            event_struct["conditional_actions_trigger"].append(event_info["value"])

            elif event_target["targetType"] == "Objective":
                if event_target["methodName"] == "BeginObjective":
                    event_struct["objectives_begin"].append(event_target["targetID"])
                elif event_target["methodName"] == "CompleteObjective":
                    event_struct["objectives_completed"].append(event_target["targetID"])
                elif event_target["methodName"] == "FailObjective":
                    event_struct["objectives_failed"].append(event_target["targetID"])
                elif event_target["methodName"] == "ResetObjective":
                    event_struct["objectives_reset"].append(event_target["targetID"])
                elif event_target["methodName"] == "CancelObjective":
                    event_struct["objectives_cancel"].append(event_target["targetID"])

    timed_event_dict[event["groupID"]] = event_struct
    net.add_node("tt"+event["groupID"],event_struct["name"]+" ("+event["groupID"]+")",color="#555500",shape="triangle")


# Get nodes from event sequences
event_sequence_dict = dict()
event_sequence_nodes_dict = dict()
for event in mission_dict["EventSequences"]:
    squence_struct = dict()
    squence_struct["name"] = event["sequenceName"]
    squence_struct["id"] = event["id"]

    squence_struct["nodes"] = list()

    sequential_node_id = 0

    for event_info in event["Event_list"]:

        event_struct = dict()
        event_struct["name"] = event_info["nodeName"]
        event_struct["id"] = event["id"]+"-"+str(sequential_node_id)

        event_struct["triggered_events_triggered"] = list()
        event_struct["triggered_events_disabled"] = list()
        event_struct["triggered_events_enabled"] = list()
        
        event_struct["timed_events_stop"] = list()
        event_struct["timed_events_start"] = list()

        event_struct["event_sequences_start"] = list()
        event_struct["event_sequences_stop"] = list()
        event_struct["event_sequences_restart"] = list()

        event_struct["conditional_actions_trigger"] = list()
        
        event_struct["objectives_begin"] = list()
        event_struct["objectives_completed"] = list()
        event_struct["objectives_failed"] = list()
        event_struct["objectives_reset"] = list()
        event_struct["objectives_cancel"] = list()

        for event_target in event_info["EventTarget_list"]:
            if event_target["targetType"] == "Trigger_Events":
                if event_target["methodName"] == "Trigger":
                    event_struct["triggered_events_triggered"].append(event_target["targetID"])
                elif event_target["methodName"] == "Disable":
                    event_struct["triggered_events_disabled"].append(event_target["targetID"])
                elif event_target["methodName"] == "Enable":
                    event_struct["triggered_events_enabled"].append(event_target["targetID"])
            
            elif event_target["targetType"] == "Timed_Events":
                if event_target["methodName"] == "Stop":
                    event_struct["timed_events_stop"].append(event_target["targetID"])
                elif event_target["methodName"] == "Begin":
                    event_struct["timed_events_start"].append(event_target["targetID"])

            elif event_target["targetType"] == "Event_Sequences":
                if event_target["methodName"] == "Stop":
                    event_struct["event_sequences_stop"].append(event_target["targetID"])
                elif event_target["methodName"] == "Begin":
                    event_struct["event_sequences_start"].append(event_target["targetID"])
                elif event_target["methodName"] == "Restart":
                    event_struct["event_sequences_restart"].append(event_target["targetID"])

            elif event_target["targetType"] == "System":
                if event_target["methodName"] == "FireConditionalAction":
                    for event_info in event_target["ParamInfo_list"]:
                        if event_info["type"] == "ConditionalActionReference":
                            event_struct["conditional_actions_trigger"].append(event_info["value"])

            elif event_target["targetType"] == "Objective":
                if event_target["methodName"] == "BeginObjective":
                    event_struct["objectives_begin"].append(event_target["targetID"])
                elif event_target["methodName"] == "CompleteObjective":
                    event_struct["objectives_completed"].append(event_target["targetID"])
                elif event_target["methodName"] == "FailObjective":
                    event_struct["objectives_failed"].append(event_target["targetID"])
                elif event_target["methodName"] == "ResetObjective":
                    event_struct["objectives_reset"].append(event_target["targetID"])
                elif event_target["methodName"] == "CancelObjective":
                    event_struct["objectives_cancel"].append(event_target["targetID"])

        squence_struct["nodes"].append(event_struct)

        event_sequence_nodes_dict[event["id"]+"-"+str(sequential_node_id)] = event_struct
        net.add_node("esn"+event["id"]+"-"+str(sequential_node_id),event_struct["name"]+" ("+event["id"]+"-"+str(sequential_node_id)+")",color="#7f7f7f")

        sequential_node_id = sequential_node_id + 1

    event_sequence_dict[event["id"]] = squence_struct
    net.add_node("es"+event["id"],squence_struct["name"]+" ("+event["id"]+")",color="#7f7f7f")


# Get nodes from conditional event
conditional_event_dict = dict()
for event in mission_dict["ConditionalActions"]:
    conditional_struct = dict()
    conditional_struct["name"] = event["name"]
    conditional_struct["id"] = event["id"]
    
    conditional_struct["true_actions"] = dict()

    conditional_struct["true_actions"]["triggered_events_triggered"] = list()
    conditional_struct["true_actions"]["triggered_events_disabled"] = list()
    conditional_struct["true_actions"]["triggered_events_enabled"] = list()
    
    conditional_struct["true_actions"]["timed_events_stop"] = list()
    conditional_struct["true_actions"]["timed_events_start"] = list()

    conditional_struct["true_actions"]["event_sequences_start"] = list()
    conditional_struct["true_actions"]["event_sequences_stop"] = list()
    conditional_struct["true_actions"]["event_sequences_restart"] = list()
    
    conditional_struct["true_actions"]["conditional_actions_trigger"] = list()
    
    conditional_struct["true_actions"]["objectives_begin"] = list()
    conditional_struct["true_actions"]["objectives_completed"] = list()
    conditional_struct["true_actions"]["objectives_failed"] = list()
    conditional_struct["true_actions"]["objectives_reset"] = list()
    conditional_struct["true_actions"]["objectives_cancel"] = list()

    conditional_struct["false_actions"] = dict()

    conditional_struct["false_actions"]["triggered_events_triggered"] = list()
    conditional_struct["false_actions"]["triggered_events_disabled"] = list()
    conditional_struct["false_actions"]["triggered_events_enabled"] = list()
    
    conditional_struct["false_actions"]["timed_events_stop"] = list()
    conditional_struct["false_actions"]["timed_events_start"] = list()
    
    conditional_struct["false_actions"]["event_sequences_start"] = list()
    conditional_struct["false_actions"]["event_sequences_stop"] = list()
    conditional_struct["false_actions"]["event_sequences_restart"] = list()
    
    conditional_struct["false_actions"]["conditional_actions_trigger"] = list()
    
    conditional_struct["false_actions"]["objectives_begin"] = list()
    conditional_struct["false_actions"]["objectives_completed"] = list()
    conditional_struct["false_actions"]["objectives_failed"] = list()
    conditional_struct["false_actions"]["objectives_reset"] = list()
    conditional_struct["false_actions"]["objectives_cancel"] = list()

    for event_target in event["actions"]["EventTarget_list"]:
        if event_target["targetType"] == "Trigger_Events":
            if event_target["methodName"] == "Trigger":
                conditional_struct["true_actions"]["triggered_events_triggered"].append(event_target["targetID"])
            elif event_target["methodName"] == "Disable":
                conditional_struct["true_actions"]["triggered_events_disabled"].append(event_target["targetID"])
            elif event_target["methodName"] == "Enable":
                conditional_struct["true_actions"]["triggered_events_enabled"].append(event_target["targetID"])
        
        elif event_target["targetType"] == "Timed_Events":
            if event_target["methodName"] == "Stop":
                conditional_struct["true_actions"]["timed_events_stop"].append(event_target["targetID"])
            elif event_target["methodName"] == "Begin":
                conditional_struct["true_actions"]["timed_events_start"].append(event_target["targetID"])

        elif event_target["targetType"] == "Event_Sequences":
            if event_target["methodName"] == "Stop":
                conditional_struct["true_actions"]["event_sequences_stop"].append(event_target["targetID"])
            elif event_target["methodName"] == "Begin":
                conditional_struct["true_actions"]["event_sequences_start"].append(event_target["targetID"])
            elif event_target["methodName"] == "Restart":
                conditional_struct["true_actions"]["event_sequences_restart"].append(event_target["targetID"])

        elif event_target["targetType"] == "System":
            if event_target["methodName"] == "FireConditionalAction":
                for event_info in event_target["ParamInfo_list"]:
                    if event_info["type"] == "ConditionalActionReference":
                        conditional_struct["true_actions"]["conditional_actions_trigger"].append(event_info["value"])

        elif event_target["targetType"] == "Objective":
            if event_target["methodName"] == "BeginObjective":
                conditional_struct["true_actions"]["objectives_begin"].append(event_target["targetID"])
            elif event_target["methodName"] == "CompleteObjective":
                conditional_struct["true_actions"]["objectives_completed"].append(event_target["targetID"])
            elif event_target["methodName"] == "FailObjective":
                conditional_struct["true_actions"]["objectives_failed"].append(event_target["targetID"])
            elif event_target["methodName"] == "ResetObjective":
                conditional_struct["true_actions"]["objectives_reset"].append(event_target["targetID"])
            elif event_target["methodName"] == "CancelObjective":
                conditional_struct["true_actions"]["objectives_cancel"].append(event_target["targetID"])

    for event_target in event["else_actions"]["EventTarget_list"]:
        if event_target["targetType"] == "Trigger_Events":
            if event_target["methodName"] == "Trigger":
                conditional_struct["false_actions"]["triggered_events_triggered"].append(event_target["targetID"])
            elif event_target["methodName"] == "Disable":
                conditional_struct["false_actions"]["triggered_events_disabled"].append(event_target["targetID"])
            elif event_target["methodName"] == "Enable":
                conditional_struct["false_actions"]["triggered_events_enabled"].append(event_target["targetID"])
        
        elif event_target["targetType"] == "Timed_Events":
            if event_target["methodName"] == "Stop":
                conditional_struct["false_actions"]["timed_events_stop"].append(event_target["targetID"])
            elif event_target["methodName"] == "Begin":
                conditional_struct["false_actions"]["timed_events_start"].append(event_target["targetID"])

        elif event_target["targetType"] == "Event_Sequences":
            if event_target["methodName"] == "Stop":
                conditional_struct["false_actions"]["event_sequences_stop"].append(event_target["targetID"])
            elif event_target["methodName"] == "Begin":
                conditional_struct["false_actions"]["event_sequences_start"].append(event_target["targetID"])
            elif event_target["methodName"] == "Restart":
                conditional_struct["false_actions"]["event_sequences_restart"].append(event_target["targetID"])

        elif event_target["targetType"] == "System":
            if event_target["methodName"] == "FireConditionalAction":
                for event_info in event_target["ParamInfo_list"]:
                    if event_info["type"] == "ConditionalActionReference":
                        conditional_struct["false_actions"]["conditional_actions_trigger"].append(event_info["value"])

        elif event_target["targetType"] == "Objective":
            if event_target["methodName"] == "BeginObjective":
                conditional_struct["false_actions"]["objectives_begin"].append(event_target["targetID"])
            elif event_target["methodName"] == "CompleteObjective":
                conditional_struct["false_actions"]["objectives_completed"].append(event_target["targetID"])
            elif event_target["methodName"] == "FailObjective":
                conditional_struct["false_actions"]["objectives_failed"].append(event_target["targetID"])
            elif event_target["methodName"] == "ResetObjective":
                conditional_struct["false_actions"]["objectives_reset"].append(event_target["targetID"])
            elif event_target["methodName"] == "CancelObjective":
                conditional_struct["false_actions"]["objectives_cancel"].append(event_target["targetID"])

    conditional_event_dict[event["id"]] = conditional_struct
    net.add_node("ce"+event["id"],"Conditional Event ("+event["id"]+")",color="#550055",shape="diamond")







# build links from objectives
for objective_id in objective_dict:
    objective_struct = objective_dict[objective_id]
    for target in objective_struct["start"]:
        if target["type"] == "trigger":
            if target["method"] == "trigger":
                net.add_edge("o"+objective_id,"t"+target["target"],arrows="to,middle",color="#0000ff",title=target["method"])
            elif target["method"] == "enable":
                net.add_edge("o"+objective_id,"t"+target["target"],arrows="to",color="#000055",title=target["method"])
            elif target["method"] == "disable":
                net.add_edge("o"+objective_id,"t"+target["target"],arrows="to",dashes=True,color="#000055",title=target["method"])
        
        elif target["type"] == "timed":
            if target["method"] == "begin":
                net.add_edge("o"+objective_id,"tt"+target["target"],arrows="to",color="#000055",title=target["method"])
            elif target["method"] == "stop":
                net.add_edge("o"+objective_id,"tt"+target["target"],arrows="to",dashes=True,color="#000055",title=target["method"])
        
        elif target["type"] == "sequence":
            if target["method"] == "begin":
                net.add_edge("o"+objective_id,"es"+target["target"],arrows="to",color="#000055",title=target["method"])
            elif target["method"] == "stop":
                net.add_edge("o"+objective_id,"es"+target["target"],arrows="to",dashes=True,color="#000055",title=target["method"])
            elif target["method"] == "restart":
                net.add_edge("o"+objective_id,"es"+target["target"],arrows="to,middle",color="#000055",title=target["method"])
        
        elif target["type"] == "conditional_action":
            if target["method"] == "trigger":
                net.add_edge("o"+objective_id,"ce"+target["target"],arrows="to",color="#000055",title=target["method"])
        
        elif target["type"] == "objective":
            if target["method"] == "begin":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to",color="#0000ff",title=target["method"])
            elif target["method"] == "complete":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to,middle",color="#000055",title=target["method"])
            elif target["method"] == "fail":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to,middle",dashes=True,color="#000055",title=target["method"])
            elif target["method"] == "reset":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to",dashes=True,color="#000055",title=target["method"])
            elif target["method"] == "cancel":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to,middle",dashes=True,color="#000055",title=target["method"])

    for target in objective_struct["fail"]:
        if target["type"] == "trigger":
            if target["method"] == "trigger":
                net.add_edge("o"+objective_id,"t"+target["target"],arrows="to,middle",color="#ff0000",title=target["method"])
            elif target["method"] == "enable":
                net.add_edge("o"+objective_id,"t"+target["target"],arrows="to",color="#550000",title=target["method"])
            elif target["method"] == "disable":
                net.add_edge("o"+objective_id,"t"+target["target"],arrows="to",dashes=True,color="#550000",title=target["method"])
        
        elif target["type"] == "timed":
            if target["method"] == "begin":
                net.add_edge("o"+objective_id,"tt"+target["target"],arrows="to",color="#550000",title=target["method"])
            elif target["method"] == "stop":
                net.add_edge("o"+objective_id,"tt"+target["target"],arrows="to",dashes=True,color="#550000",title=target["method"])
        
        elif target["type"] == "sequence":
            if target["method"] == "begin":
                net.add_edge("o"+objective_id,"es"+target["target"],arrows="to",color="#550000",title=target["method"])
            elif target["method"] == "stop":
                net.add_edge("o"+objective_id,"es"+target["target"],arrows="to",dashes=True,color="#550000",title=target["method"])
            elif target["method"] == "restart":
                net.add_edge("o"+objective_id,"es"+target["target"],arrows="to,middle",color="#550000",title=target["method"])
        
        elif target["type"] == "conditional_action":
            if target["method"] == "trigger":
                net.add_edge("o"+objective_id,"ce"+target["target"],arrows="to",color="#550000",title=target["method"])
        
        elif target["type"] == "objective":
            if target["method"] == "begin":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to",color="#ff0000",title=target["method"])
            elif target["method"] == "complete":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to,middle",color="#550000",title=target["method"])
            elif target["method"] == "fail":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to,middle",dashes=True,color="#550000",title=target["method"])
            elif target["method"] == "reset":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to",dashes=True,color="#550000",title=target["method"])
            elif target["method"] == "cancel":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to,middle",dashes=True,color="#550000",title=target["method"])

    for target in objective_struct["complete"]:
        if target["type"] == "trigger":
            if target["method"] == "trigger":
                net.add_edge("o"+objective_id,"t"+target["target"],arrows="to,middle",color="#00ff00",title=target["method"])
            elif target["method"] == "enable":
                net.add_edge("o"+objective_id,"t"+target["target"],arrows="to",color="#005500",title=target["method"])
            elif target["method"] == "disable":
                net.add_edge("o"+objective_id,"t"+target["target"],arrows="to",dashes=True,color="#005500",title=target["method"])
        
        elif target["type"] == "timed":
            if target["method"] == "begin":
                net.add_edge("o"+objective_id,"tt"+target["target"],arrows="to",color="#005500",title=target["method"])
            elif target["method"] == "stop":
                net.add_edge("o"+objective_id,"tt"+target["target"],arrows="to",dashes=True,color="#005500",title=target["method"])
        
        elif target["type"] == "sequence":
            if target["method"] == "begin":
                net.add_edge("o"+objective_id,"es"+target["target"],arrows="to",color="#005500",title=target["method"])
            elif target["method"] == "stop":
                net.add_edge("o"+objective_id,"es"+target["target"],arrows="to",dashes=True,color="#005500",title=target["method"])
            elif target["method"] == "restart":
                net.add_edge("o"+objective_id,"es"+target["target"],arrows="to,middle",color="#005500",title=target["method"])
        
        elif target["type"] == "conditional_action":
            if target["method"] == "trigger":
                net.add_edge("o"+objective_id,"ce"+target["target"],arrows="to",color="#005500",title=target["method"])
        
        elif target["type"] == "objective":
            if target["method"] == "begin":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to",color="#00ff00",title=target["method"])
            elif target["method"] == "complete":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to,middle",color="#005500",title=target["method"])
            elif target["method"] == "fail":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to,middle",dashes=True,color="#005500",title=target["method"])
            elif target["method"] == "reset":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to",dashes=True,color="#005500",title=target["method"])
            elif target["method"] == "cancel":
                net.add_edge("o"+objective_id,"o"+target["target"],arrows="to,middle",dashes=True,color="#005500",title=target["method"])


# Build links from trigger events
for event_id in trigger_event_dict:
    event_struct = trigger_event_dict[event_id]
    for target in event_struct["triggered_events_triggered"]:
        net.add_edge("t"+event_id,"t"+target,arrows="to,middle",color="#7f7f7f",title="trigger")
    for target in event_struct["triggered_events_disabled"]:
        net.add_edge("t"+event_id,"t"+target,arrows="to",color="#555555",title="disable")
    for target in event_struct["triggered_events_enabled"]:
        net.add_edge("t"+event_id,"t"+target,arrows="to",color="#7f7f00",title="enable")

    for target in event_struct["timed_events_stop"]:
        net.add_edge("t"+event_id,"tt"+target,arrows="to",color="#555555",title="stop")
    for target in event_struct["timed_events_start"]:
        net.add_edge("t"+event_id,"tt"+target,arrows="to",color="#7f7f00",title="start")    

    for target in event_struct["event_sequences_stop"]:
        net.add_edge("t"+event_id,"es"+target,arrows="to",color="#555555",title="stop")
    for target in event_struct["event_sequences_start"]:
        net.add_edge("t"+event_id,"es"+target,arrows="to",color="#7f7f00",title="start")    
    for target in event_struct["event_sequences_restart"]:
        net.add_edge("t"+event_id,"es"+target,arrows="to,middle",color="#7f7f00",title="restart")    

    for target in event_struct["conditional_actions_trigger"]:
        net.add_edge("t"+event_id,"ce"+target,arrows="to",color="#555555",title="trigger")

    for target in event_struct["objectives_begin"]:
        net.add_edge("t"+event_id,"o"+target,arrows="to",color="#7f7f7f",title="begin")
    for target in event_struct["objectives_completed"]:
        net.add_edge("t"+event_id,"o"+target,arrows="to,middle",color="#7f7f7f",title="complete")
    for target in event_struct["objectives_failed"]:
        net.add_edge("t"+event_id,"o"+target,arrows="to,middle",color="#555555",dashes=True,title="fail")
    for target in event_struct["objectives_reset"]:
        net.add_edge("t"+event_id,"o"+target,arrows="to,middle",color="#555555",dashes=True,title="reset")
    for target in event_struct["objectives_cancel"]:
        net.add_edge("t"+event_id,"o"+target,arrows="to,middle",color="#555555",dashes=True,title="cancel")


# Build links from timed events
for event_id in timed_event_dict:
    event_struct = timed_event_dict[event_id]
    for target in event_struct["triggered_events_triggered"]:
        net.add_edge("tt"+event_id,"t"+target,arrows="to,middle",color="#7f7f7f",title="trigger")
    for target in event_struct["triggered_events_disabled"]:
        net.add_edge("tt"+event_id,"t"+target,arrows="to",color="#555555",title="disable")
    for target in event_struct["triggered_events_enabled"]:
        net.add_edge("tt"+event_id,"t"+target,arrows="to",color="#7f7f00",title="enable")

    for target in event_struct["timed_events_stop"]:
        net.add_edge("tt"+event_id,"tt"+target,arrows="to",color="#555555",title="stop")
    for target in event_struct["timed_events_start"]:
        net.add_edge("tt"+event_id,"tt"+target,arrows="to",color="#7f7f00",title="start")

    for target in event_struct["event_sequences_stop"]:
        net.add_edge("tt"+event_id,"es"+target,arrows="to",color="#555555",title="stop")
    for target in event_struct["event_sequences_start"]:
        net.add_edge("tt"+event_id,"es"+target,arrows="to",color="#7f7f00",title="start")    
    for target in event_struct["event_sequences_restart"]:
        net.add_edge("tt"+event_id,"es"+target,arrows="to,middle",color="#7f7f00",title="restart")    

    for target in event_struct["conditional_actions_trigger"]:
        net.add_edge("tt"+event_id,"ce"+target,arrows="to",color="#555555",title="trigger")

    for target in event_struct["objectives_begin"]:
        net.add_edge("tt"+event_id,"o"+target,arrows="to",color="#7f7f7f",title="begin")
    for target in event_struct["objectives_completed"]:
        net.add_edge("tt"+event_id,"o"+target,arrows="to,middle",color="#7f7f7f",title="complete")
    for target in event_struct["objectives_failed"]:
        net.add_edge("tt"+event_id,"o"+target,arrows="to,middle",color="#555555",dashes=True,title="fail")
    for target in event_struct["objectives_reset"]:
        net.add_edge("tt"+event_id,"o"+target,arrows="to,middle",color="#555555",dashes=True,title="reset")
    for target in event_struct["objectives_cancel"]:
        net.add_edge("tt"+event_id,"o"+target,arrows="to,middle",color="#555555",dashes=True,title="cancel")


# Build links from event sequences
for sequence_id in event_sequence_dict:
    sequence_struct = event_sequence_dict[sequence_id]

    last_node_id = ""
    for node in sequence_struct["nodes"]:
        node_id = node["id"]
        if last_node_id == "":
            net.add_edge("es"+sequence_id,"esn"+node_id,arrows="to",color="#7f7f7f",title="next_node")
        else:
            net.add_edge("esn"+last_node_id,"esn"+node_id,arrows="to",color="#7f7f7f",title="next_node")
        last_node_id = node_id


# Build links from event sequences nodes
for event_id in event_sequence_nodes_dict:
    event_struct = event_sequence_nodes_dict[event_id]
    for target in event_struct["triggered_events_triggered"]:
        net.add_edge("esn"+event_id,"t"+target,arrows="to,middle",color="#7f7f7f",title="trigger")
    for target in event_struct["triggered_events_disabled"]:
        net.add_edge("esn"+event_id,"t"+target,arrows="to",color="#555555",title="disable")
    for target in event_struct["triggered_events_enabled"]:
        net.add_edge("esn"+event_id,"t"+target,arrows="to",color="#7f7f00",title="enable")

    for target in event_struct["timed_events_stop"]:
        net.add_edge("esn"+event_id,"tt"+target,arrows="to",color="#555555",title="stop")
    for target in event_struct["timed_events_start"]:
        net.add_edge("esn"+event_id,"tt"+target,arrows="to",color="#7f7f00",title="start")

    for target in event_struct["event_sequences_stop"]:
        net.add_edge("esn"+event_id,"es"+target,arrows="to",color="#555555",title="stop")
    for target in event_struct["event_sequences_start"]:
        net.add_edge("esn"+event_id,"es"+target,arrows="to",color="#7f7f00",title="start")    
    for target in event_struct["event_sequences_restart"]:
        net.add_edge("esn"+event_id,"es"+target,arrows="to,middle",color="#7f7f00",title="restart")    

    for target in event_struct["conditional_actions_trigger"]:
        net.add_edge("esn"+event_id,"ce"+target,arrows="to",color="#555555",title="trigger")

    for target in event_struct["objectives_begin"]:
        net.add_edge("esn"+event_id,"o"+target,arrows="to",color="#7f7f7f",title="begin")
    for target in event_struct["objectives_completed"]:
        net.add_edge("esn"+event_id,"o"+target,arrows="to,middle",color="#7f7f7f",title="complete")
    for target in event_struct["objectives_failed"]:
        net.add_edge("esn"+event_id,"o"+target,arrows="to,middle",color="#555555",dashes=True,title="fail")
    for target in event_struct["objectives_reset"]:
        net.add_edge("esn"+event_id,"o"+target,arrows="to,middle",color="#555555",dashes=True,title="reset")
    for target in event_struct["objectives_cancel"]:
        net.add_edge("esn"+event_id,"o"+target,arrows="to,middle",color="#555555",dashes=True,title="cancel")


# Build links from conditional event
for event_id in conditional_event_dict:
    event_struct = conditional_event_dict[event_id]

    for target in event_struct["true_actions"]["triggered_events_triggered"]:
        net.add_edge("ce"+event_id,"t"+target,arrows="to,middle",color="#007f00",title="trigger")
    for target in event_struct["true_actions"]["triggered_events_disabled"]:
        net.add_edge("ce"+event_id,"t"+target,arrows="to",color="#005500",title="disable")
    for target in event_struct["true_actions"]["triggered_events_enabled"]:
        net.add_edge("ce"+event_id,"t"+target,arrows="to",color="#007f00",title="enable")

    for target in event_struct["true_actions"]["timed_events_stop"]:
        net.add_edge("ce"+event_id,"tt"+target,arrows="to",color="#005500",title="stop")
    for target in event_struct["true_actions"]["timed_events_start"]:
        net.add_edge("ce"+event_id,"tt"+target,arrows="to",color="#007f00",title="start")

    for target in event_struct["true_actions"]["event_sequences_stop"]:
        net.add_edge("ce"+event_id,"es"+target,arrows="to",color="#005500",title="stop")
    for target in event_struct["true_actions"]["event_sequences_start"]:
        net.add_edge("ce"+event_id,"es"+target,arrows="to",color="#007f00",title="start")    
    for target in event_struct["true_actions"]["event_sequences_restart"]:
        net.add_edge("ce"+event_id,"es"+target,arrows="to,middle",color="#007f00",title="restart")    

    for target in event_struct["true_actions"]["conditional_actions_trigger"]:
        net.add_edge("ce"+event_id,"ce"+target,arrows="to",color="#005500",title="trigger")

    for target in event_struct["true_actions"]["objectives_begin"]:
        net.add_edge("ce"+event_id,"o"+target,arrows="to",color="#007f00",title="begin")
    for target in event_struct["true_actions"]["objectives_completed"]:
        net.add_edge("ce"+event_id,"o"+target,arrows="to,middle",color="#007f00",title="complete")
    for target in event_struct["true_actions"]["objectives_failed"]:
        net.add_edge("ce"+event_id,"o"+target,arrows="to,middle",color="#005500",dashes=True,title="fail")
    for target in event_struct["true_actions"]["objectives_reset"]:
        net.add_edge("ce"+event_id,"o"+target,arrows="to,middle",color="#005500",dashes=True,title="reset")
    for target in event_struct["true_actions"]["objectives_cancel"]:
        net.add_edge("ce"+event_id,"o"+target,arrows="to,middle",color="#005500",dashes=True,title="cancel")


    for target in event_struct["false_actions"]["triggered_events_triggered"]:
        net.add_edge("ce"+event_id,"t"+target,arrows="to,middle",color="#7f0000",title="trigger")
    for target in event_struct["false_actions"]["triggered_events_disabled"]:
        net.add_edge("ce"+event_id,"t"+target,arrows="to",color="#550000",title="disable")
    for target in event_struct["false_actions"]["triggered_events_enabled"]:
        net.add_edge("ce"+event_id,"t"+target,arrows="to",color="#7f0000",title="enable")

    for target in event_struct["false_actions"]["timed_events_stop"]:
        net.add_edge("ce"+event_id,"tt"+target,arrows="to",color="#550000",title="stop")
    for target in event_struct["false_actions"]["timed_events_start"]:
        net.add_edge("ce"+event_id,"tt"+target,arrows="to",color="#7f0000",title="start")

    for target in event_struct["false_actions"]["event_sequences_stop"]:
        net.add_edge("ce"+event_id,"es"+target,arrows="to",color="#550000",title="stop")
    for target in event_struct["false_actions"]["event_sequences_start"]:
        net.add_edge("ce"+event_id,"es"+target,arrows="to",color="#7f0000",title="start")    
    for target in event_struct["false_actions"]["event_sequences_restart"]:
        net.add_edge("ce"+event_id,"es"+target,arrows="to,middle",color="#7f0000",title="restart")    

    for target in event_struct["false_actions"]["conditional_actions_trigger"]:
        net.add_edge("ce"+event_id,"ce"+target,arrows="to",color="#550000",title="trigger")
    
    for target in event_struct["false_actions"]["objectives_begin"]:
        net.add_edge("ce"+event_id,"o"+target,arrows="to",color="#7f0000",title="begin")
    for target in event_struct["false_actions"]["objectives_completed"]:
        net.add_edge("ce"+event_id,"o"+target,arrows="to,middle",color="#7f0000",title="complete")
    for target in event_struct["false_actions"]["objectives_failed"]:
        net.add_edge("ce"+event_id,"o"+target,arrows="to,middle",color="#550000",dashes=True,title="fail")
    for target in event_struct["false_actions"]["objectives_reset"]:
        net.add_edge("ce"+event_id,"o"+target,arrows="to,middle",color="#550000",dashes=True,title="reset")
    for target in event_struct["false_actions"]["objectives_cancel"]:
        net.add_edge("ce"+event_id,"o"+target,arrows="to,middle",color="#550000",dashes=True,title="cancel")






net.set_edge_smooth('dynamic')
net.show("mission.html", notebook=False)