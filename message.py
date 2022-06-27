import json
import boto3
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
import os
import time
bb={
'989722684664 (989722684664)': 'Glazed frog-989722684664',
'268978774461 (268978774461)': '灵感-268978774461',
'416799389553 (416799389553)': '灵感-416799389553',
'414660254120 (414660254120)': '嘉立创-414660254120',
'484645483170 (484645483170)': '特步-484645483170',
'283966127337 (283966127337)': '瞭风-283966127337',
'121473596124 (121473596124)': '瞭风-121473596124',
'862306272388 (862306272388)': '瞭风-862306272388',
'994840535113 (994840535113)': '赛凌-994840535113',
'306705059054 (306705059054)': '赛凌-306705059054',
'241845836712 (241845836712)': '赛凌-241845836712',
'652673224171 (652673224171)': '赛凌-652673224171',
'626128867451 (626128867451)': '傲雷-626128867451',
'620070690364 (620070690364)': '傲雷-620070690364',
'002107561657 (002107561657)': '傲雷-002107561657',
'853221520929 (853221520929)': '傲雷-853221520929',
'661946724751 (661946724751)': '复娱-661946724751',
'423999433583 (423999433583)': '复娱-423999433583',
'854944865316 (854944865316)': '复娱-854944865316',
'275517379082 (275517379082)': '复娱-275517379082',
'655722529247 (655722529247)': '复娱-655722529247',
'311321910987 (311321910987)': '复娱-311321910987',
'794608515269 (794608515269)': 'Yostar-794608515269',
'593479884953 (593479884953)': 'Yostar-593479884953',
'809501327402 (809501327402)': 'Yostar-809501327402',
'709016922719 (709016922719)': 'Yostar-709016922719',
'067850593054 (067850593054)': 'PingPong-067850593054',
'341268965139 (341268965139)': '心动易玩-341268965139',
'578275272458 (578275272458)': 'XD心动-578275272458',
'857474660237 (857474660237)': 'XD心动-857474660237',
'888986452248 (888986452248)': 'XD心动-888986452248',
'776879703107 (776879703107)': 'XD心动-776879703107',
'602866119124 (602866119124)': 'XD心动-602866119124',
'275930694352 (275930694352)': 'XD心动-275930694352',
'107614576892 (107614576892)': 'XD心动-107614576892',
'552406488846 (552406488846)': 'XD心动-552406488846',
'867836039594 (867836039594)': 'XD心动-867836039594',
'721339760326 (721339760326)': 'XD心动-721339760326',
'330644318382 (330644318382)': 'XD心动-330644318382',
'209852375067 (209852375067)': 'XD心动-209852375067',
'668652987569 (668652987569)': 'XD心动-668652987569',
'410240760002 (410240760002)': '印闪-410240760002',
'643907662836 (643907662836)': '虎趣-643907662836',
'738135835475 (738135835475)': 'Flamingo-738135835475',
'947894009154 (947894009154)': 'BG-947894009154',
'770738614659 (770738614659)': 'BG-770738614659',
'661633860861 (661633860861)': 'BG-661633860861',
'481617506592 (481617506592)': '点众-481617506592',
'402979319347 (402979319347)': '点众-402979319347',
'370726972792 (370726972792)': '点众-370726972792',
'258981937576 (258981937576)': '人人币-258981937576',
'612789561029 (612789561029)': '人人币-612789561029',
'497633604168 (497633604168)': '虎币-497633604168',
'604124905433 (604124905433)': '哈舶互联-604124905433',
'480329292151 (480329292151)': '一图一数-480329292151',
'761809136613 (761809136613)': '一图一数-761809136613',
'004572644932 (004572644932)': '一图一数-004572644932',
'384512081268 (384512081268)': '一图一数-384512081268',
'551484415087 (551484415087)': '一图一数-551484415087',
'221675390729 (221675390729)': '一图一数-221675390729',
'134848474495 (134848474495)': '汉迪-134848474495',
'149870400580 (149870400580)': '汉迪-149870400580',
'462744805499 (462744805499)': '汉迪-462744805499',
'927207885172 (927207885172)': '汉迪-927207885172',
'744330249173 (744330249173)': '汉迪-744330249173',
'757039578059 (757039578059)': '汉迪-757039578059',
'232660966648 (232660966648)': 'Aviagames-232660966648',
'740234844504 (740234844504)': 'Mico-740234844504',
'661642256480 (661642256480)': '币信-661642256480',
'916534085272 (916534085272)': '江娱-916534085272',
'142519756622 (142519756622)': 'Karma-142519756622',
'529393139736 (529393139736)': '炫指-529393139736'
}

def get_message_for_slack(event_details, event_type, affected_accounts, affected_entities, slack_webhook):
    message = ""
    summary = ""
    if slack_webhook == "webhook":
        if len(affected_entities) >= 1:
            affected_entities = "\n".join(affected_entities)
            if affected_entities == "UNKNOWN":
                affected_entities = "All resources\nin region"
        else:
            affected_entities = "All resources\nin region"
        if len(affected_accounts) >= 1:
            affected_accounts = "\n".join(affected_accounts)
        else:
            affected_accounts = "All accounts\nin region"      
        if event_type == "create":
            summary += (
                f":rotating_light:*[NEW] AWS Health reported an issue with the {event_details['successfulSet'][0]['event']['service'].upper()} service in "
                f"the {event_details['successfulSet'][0]['event']['region'].upper()} region.*"
            )
            message = {
                "text": summary,
                "attachments": [
                    {
                        "color": "danger",
                            "fields": [
                                { "title": "Account(s)", "value": affected_accounts, "short": True },
                                { "title": "Resource(s)", "value": affected_entities, "short": True },
                                { "title": "Service", "value": event_details['successfulSet'][0]['event']['service'], "short": True },
                                { "title": "Region", "value": event_details['successfulSet'][0]['event']['region'], "short": True },
                                { "title": "Start Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['startTime']), "short": True },
                                { "title": "Status", "value": event_details['successfulSet'][0]['event']['statusCode'], "short": True },
                                { "title": "Event ARN", "value": event_details['successfulSet'][0]['event']['arn'], "short": False },                          
                                { "title": "Updates", "value": get_last_aws_update(event_details), "short": False }
                            ],
                    }
                ]
            }

        elif event_type == "resolve":
            summary += (
                f":heavy_check_mark:*[RESOLVED] The AWS Health issue with the {event_details['successfulSet'][0]['event']['service'].upper()} service in "
                f"the {event_details['successfulSet'][0]['event']['region'].upper()} region is now resolved.*"
            )
            message = {
                "text": summary,
                "attachments": [
                    {
                        "color": "00ff00",
                            "fields": [
                                { "title": "Account(s)", "value": affected_accounts, "short": True },
                                { "title": "Resource(s)", "value": affected_entities, "short": True },
                                { "title": "Service", "value": event_details['successfulSet'][0]['event']['service'], "short": True },
                                { "title": "Region", "value": event_details['successfulSet'][0]['event']['region'], "short": True },
                                { "title": "Start Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['startTime']), "short": True },
                                { "title": "End Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['endTime']), "short": True },
                                { "title": "Status", "value": event_details['successfulSet'][0]['event']['statusCode'], "short": True },
                                { "title": "Event ARN", "value": event_details['successfulSet'][0]['event']['arn'], "short": False },                                
                                { "title": "Updates", "value": get_last_aws_update(event_details), "short": False }
                            ],
                    }
                ]
            }
    else:
        if len(affected_entities) >= 1:
            affected_entities = "\n".join(affected_entities)
            if affected_entities == "UNKNOWN":
                affected_entities = "All resources\nin region"
        else:
            affected_entities = "All resources in region"
        if len(affected_accounts) >= 1:
            affected_accounts = "\n".join(affected_accounts)
        else:
            affected_accounts = "All accounts in region"      
        if event_type == "create":
            summary += (
                f":rotating_light:*[NEW] AWS Health reported an issue with the {event_details['successfulSet'][0]['event']['service'].upper()} service in "
                f"the {event_details['successfulSet'][0]['event']['region'].upper()} region.*"
            )
            message = {
               "text": summary,
                "accounts": affected_accounts,
                "resources": affected_entities,
                "service": event_details['successfulSet'][0]['event']['service'],
                "region": event_details['successfulSet'][0]['event']['region'],
                "start_time": cleanup_time(event_details['successfulSet'][0]['event']['startTime']),
                "status": event_details['successfulSet'][0]['event']['statusCode'],
                "event_arn": event_details['successfulSet'][0]['event']['arn'],
                "updates": get_last_aws_update(event_details)
            }

        elif event_type == "resolve":
            summary += (
                f":heavy_check_mark:*[RESOLVED] The AWS Health issue with the {event_details['successfulSet'][0]['event']['service'].upper()} service in "
                f"the {event_details['successfulSet'][0]['event']['region'].upper()} region is now resolved.*"
            )
            message = {
                "text": summary,
                "accounts": affected_accounts,
                "resources": affected_entities,                
                "service": event_details['successfulSet'][0]['event']['service'],
                "region": event_details['successfulSet'][0]['event']['region'],
                "start_time": cleanup_time(event_details['successfulSet'][0]['event']['startTime']),
                "status": event_details['successfulSet'][0]['event']['statusCode'],
                "event_arn": event_details['successfulSet'][0]['event']['arn'],
                "updates": get_last_aws_update(event_details)
            }
    
    print("Message sent to Slack: ", message)
    return message

def get_message_for_eventbridge(event_details, event_type, affected_accounts, affected_entities):
    message = ""
    if len(affected_entities) >= 1:
        affected_entities = "\n".join(affected_entities)
        if affected_entities == "UNKNOWN":
            affected_entities = "All resources\nin region"
    else:
        affected_entities = "All resources\nin region"
    if len(affected_accounts) >= 1:
        affected_accounts = "\n".join(affected_accounts)
    else:
        affected_accounts = "All accounts\nin region"       
    if event_type == "create":
        message = {
            "attachments": [
                {
                        "fields": [
                            { "title": "Account(s)", "value": affected_accounts, "short": True },
                            { "title": "Resource(s)", "value": affected_entities, "short": True },
                            { "title": "Service", "value": event_details['successfulSet'][0]['event']['service'], "short": True },
                            { "title": "Region", "value": event_details['successfulSet'][0]['event']['region'], "short": True },
                            { "title": "Start Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['startTime']), "short": True },
                            { "title": "Status", "value": event_details['successfulSet'][0]['event']['statusCode'], "short": True },
                            { "title": "Event ARN", "value": event_details['successfulSet'][0]['event']['arn'], "short": False },
                            { "title": "Updates", "value": get_last_aws_update(event_details), "short": False }
                        ],
                }
            ]
        }

    elif event_type == "resolve":
        message = {
            "attachments": [
                {
                        "fields": [
                            { "title": "Account(s)", "value": affected_accounts, "short": True },
                            { "title": "Resource(s)", "value": affected_entities, "short": True },
                            { "title": "Service", "value": event_details['successfulSet'][0]['event']['service'], "short": True },
                            { "title": "Region", "value": event_details['successfulSet'][0]['event']['region'], "short": True },
                            { "title": "Start Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['startTime']), "short": True },
                            { "title": "End Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['endTime']), "short": True },
                            { "title": "Status", "value": event_details['successfulSet'][0]['event']['statusCode'], "short": True },
                            { "title": "Event ARN", "value": event_details['successfulSet'][0]['event']['arn'], "short": False },
                            { "title": "Updates", "value": get_last_aws_update(event_details), "short": False }
                        ],
                }
            ]
        }
    print("SHD Message generated for EventBridge : ", message)
    return message

def get_org_message_for_eventbridge(event_details, event_type, affected_org_accounts, affected_org_entities):
    message = ""
    if len(affected_org_entities) >= 1:
        affected_org_entities = "\n".join(affected_org_entities)
    else:
        affected_org_entities = "All resources\nin region"
    if len(affected_org_accounts) >= 1:
        affected_org_accounts = "\n".join(affected_org_accounts)
    else:
        affected_org_accounts = "All accounts\nin region"
    if event_type == "create":
        message = {
            "attachments": [
                {
                        "fields": [
                            { "title": "Account(s)", "value": affected_org_accounts, "short": True },
                            { "title": "Resource(s)", "value": affected_org_entities, "short": True },
                            { "title": "Service", "value": event_details['successfulSet'][0]['event']['service'], "short": True },
                            { "title": "Region", "value": event_details['successfulSet'][0]['event']['region'], "short": True },
                            { "title": "Start Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['startTime']), "short": True },
                            { "title": "Status", "value": event_details['successfulSet'][0]['event']['statusCode'], "short": True },
                            { "title": "Event ARN", "value": event_details['successfulSet'][0]['event']['arn'], "short": False },
                            { "title": "Updates", "value": get_last_aws_update(event_details), "short": False }
                        ],
                }
            ]
        }

    elif event_type == "resolve":
        message = {
            "attachments": [
                {
                        "fields": [
                            { "title": "Account(s)", "value": affected_org_accounts, "short": True },
                            { "title": "Resource(s)", "value": affected_org_entities, "short": True },
                            { "title": "Service", "value": event_details['successfulSet'][0]['event']['service'], "short": True },
                            { "title": "Region", "value": event_details['successfulSet'][0]['event']['region'], "short": True },
                            { "title": "Start Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['startTime']), "short": True },
                            { "title": "End Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['endTime']), "short": True },
                            { "title": "Status", "value": event_details['successfulSet'][0]['event']['statusCode'], "short": True },
                            { "title": "Event ARN", "value": event_details['successfulSet'][0]['event']['arn'], "short": False },
                            { "title": "Updates", "value": get_last_aws_update(event_details), "short": False }
                        ],
                }
            ]
        }
    json.dumps(message)
    print("PHD/SHD Message generated for Event Bridge: ", message)
    return message


def get_org_message_for_slack(event_details, event_type, affected_org_accounts, affected_org_entities, slack_webhook):
    message = ""
    summary = ""
    if slack_webhook == "webhook":
        if len(affected_org_entities) >= 1:
            affected_org_entities = "\n".join(affected_org_entities)
        else:
            affected_org_entities = "All resources\nin region"
        if len(affected_org_accounts) >= 1:
            affected_org_accounts = "\n".join(affected_org_accounts)
        else:
            affected_org_accounts = "All accounts\nin region"        
        if event_type == "create":
            summary += (
                f":rotating_light:*[NEW] AWS Health reported an issue with the {event_details['successfulSet'][0]['event']['service'].upper()} service in "
                f"the {event_details['successfulSet'][0]['event']['region'].upper()} region.*"
            )
            message = {
                "text": summary,
                "attachments": [
                    {
                        "color": "danger",
                            "fields": [
                                { "title": "Account(s)", "value": affected_org_accounts, "short": True },
                                { "title": "Resource(s)", "value": affected_org_entities, "short": True },
                                { "title": "Service", "value": event_details['successfulSet'][0]['event']['service'], "short": True },
                                { "title": "Region", "value": event_details['successfulSet'][0]['event']['region'], "short": True },
                                { "title": "Start Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['startTime']), "short": True },
                                { "title": "Status", "value": event_details['successfulSet'][0]['event']['statusCode'], "short": True },
                                { "title": "Event ARN", "value": event_details['successfulSet'][0]['event']['arn'], "short": False },                                  
                                { "title": "Updates", "value": get_last_aws_update(event_details), "short": False }
                            ],
                    }
                ]
            }

        elif event_type == "resolve":
            summary += (
                f":heavy_check_mark:*[RESOLVED] The AWS Health issue with the {event_details['successfulSet'][0]['event']['service'].upper()} service in "
                f"the {event_details['successfulSet'][0]['event']['region'].upper()} region is now resolved.*"
            )
            message = {
                "text": summary,
                "attachments": [
                    {
                        "color": "00ff00",
                            "fields": [
                                { "title": "Account(s)", "value": affected_org_accounts, "short": True },
                                { "title": "Resource(s)", "value": affected_org_entities, "short": True },
                                { "title": "Service", "value": event_details['successfulSet'][0]['event']['service'], "short": True },
                                { "title": "Region", "value": event_details['successfulSet'][0]['event']['region'], "short": True },
                                { "title": "Start Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['startTime']), "short": True },
                                { "title": "End Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['endTime']), "short": True },
                                { "title": "Status", "value": event_details['successfulSet'][0]['event']['statusCode'], "short": True },
                                { "title": "Event ARN", "value": event_details['successfulSet'][0]['event']['arn'], "short": False },                                
                                { "title": "Updates", "value": get_last_aws_update(event_details), "short": False }
                            ],
                    }
                ]
            }
    else:
        if len(affected_org_entities) >= 1:
            affected_org_entities = "\n".join(affected_org_entities)
        else:
            affected_org_entities = "All resources in region"
        if len(affected_org_accounts) >= 1:
            affected_org_accounts = "\n".join(affected_org_accounts)
        else:
            affected_org_accounts = "All accounts in region"        
        if event_type == "create":
            summary += (
                f":rotating_light:*[NEW] AWS Health reported an issue with the {event_details['successfulSet'][0]['event']['service'].upper()} service in "
                f"the {event_details['successfulSet'][0]['event']['region'].upper()} region.*"
            )
            message = {
               "text": summary,
                "accounts": affected_org_accounts,
                "resources": affected_org_entities,
                "service": event_details['successfulSet'][0]['event']['service'],
                "region": event_details['successfulSet'][0]['event']['region'],
                "start_time": cleanup_time(event_details['successfulSet'][0]['event']['startTime']),
                "status": event_details['successfulSet'][0]['event']['statusCode'],
                "event_arn": event_details['successfulSet'][0]['event']['arn'],
                "updates": get_last_aws_update(event_details)
            }

        elif event_type == "resolve":
            summary += (
                f":heavy_check_mark:*[RESOLVED] The AWS Health issue with the {event_details['successfulSet'][0]['event']['service'].upper()} service in "
                f"the {event_details['successfulSet'][0]['event']['region'].upper()} region is now resolved.*"
            )
            message = {
                "text": summary,
                "accounts": affected_org_accounts,
                "resources": affected_org_entities,                
                "service": event_details['successfulSet'][0]['event']['service'],
                "region": event_details['successfulSet'][0]['event']['region'],
                "start_time": cleanup_time(event_details['successfulSet'][0]['event']['startTime']),
                "status": event_details['successfulSet'][0]['event']['statusCode'],
                "event_arn": event_details['successfulSet'][0]['event']['arn'],
                "updates": get_last_aws_update(event_details)
            } 
    json.dumps(message)
    print("Message sent to Slack: ", message)
    return message


def get_message_for_chime(event_details, event_type, affected_accounts, affected_entities):
    message = ""
    if len(affected_entities) >= 1:
        affected_entities = "\n".join(affected_entities)
        if affected_entities == "UNKNOWN":
            affected_entities = "All resources\nin region"
    else:
        affected_entities = "All resources\nin region"
    if len(affected_accounts) >= 1:
        affected_accounts = "\n".join(affected_accounts)
    else:
        affected_accounts = "All accounts\nin region"   
    summary = ""
    if event_type == "create":

        message = str("/md" + "\n" + "**:rotating_light:\[NEW\] AWS Health reported an issue with the " + event_details['successfulSet'][0]['event']['service'].upper() +  " service in " + event_details['successfulSet'][0]['event']['region'].upper() + " region.**" + "\n"
          "---" + "\n"
          "**Account(s)**: " + affected_accounts + "\n"
          "**Resource(s)**: " + affected_entities + "\n"
          "**Service**: " + event_details['successfulSet'][0]['event']['service'] + "\n"
          "**Region**: " + event_details['successfulSet'][0]['event']['region'] + "\n" 
          "**Start Time (UTC)**: " + cleanup_time(event_details['successfulSet'][0]['event']['startTime']) + "\n"
          "**Status**: " + event_details['successfulSet'][0]['event']['statusCode'] + "\n"
          "**Event ARN**: " + event_details['successfulSet'][0]['event']['arn'] + "\n"          
          "**Updates:**" + "\n" + get_last_aws_update(event_details)
          )

    elif event_type == "resolve":

        message = str("/md" + "\n" + "**:heavy_check_mark:\[RESOLVED\] The AWS Health issue with the " + event_details['successfulSet'][0]['event']['service'].upper() +  " service in " + event_details['successfulSet'][0]['event']['region'].upper() + " region is now resolved.**" + "\n"
          "---" + "\n"
          "**Account(s)**: " + affected_accounts + "\n"
          "**Resource(s)**: " + affected_entities + "\n"
          "**Service**: " + event_details['successfulSet'][0]['event']['service'] + "\n"
          "**Region**: " + event_details['successfulSet'][0]['event']['region'] + "\n" 
          "**Start Time (UTC)**: " + cleanup_time(event_details['successfulSet'][0]['event']['startTime']) + "\n"
          "**End Time (UTC)**: " + cleanup_time(event_details['successfulSet'][0]['event']['endTime']) + "\n"
          "**Status**: " + event_details['successfulSet'][0]['event']['statusCode'] + "\n"
          "**Event ARN**: " + event_details['successfulSet'][0]['event']['arn'] + "\n"             
          "**Updates:**" + "\n" + get_last_aws_update(event_details)
        )
    json.dumps(message)
    print("Message sent to Chime: ", message)    
    return message


def get_org_message_for_chime(event_details, event_type, affected_org_accounts, affected_org_entities):
    message = ""
    summary = ""
    if len(affected_org_entities) >= 1:
        affected_org_entities = "\n".join(affected_org_entities)
    else:
        affected_org_entities = "All resources in region"
    if len(affected_org_accounts) >= 1:
        affected_org_accounts = "\n".join(affected_org_accounts)
    else:
        affected_org_accounts = "All accounts in region"
    if event_type == "create":
        
        message = str("/md" + "\n" + "**:rotating_light:\[NEW\] AWS Health reported an issue with the " + event_details['successfulSet'][0]['event']['service'].upper()) +  " service in " + str(event_details['successfulSet'][0]['event']['region'].upper() + " region**" + "\n"
          "---" + "\n"
          "**Account(s)**: " + affected_org_accounts + "\n"
          "**Resource(s)**: " + affected_org_entities + "\n"
          "**Service**: " + event_details['successfulSet'][0]['event']['service'] + "\n"
          "**Region**: " + event_details['successfulSet'][0]['event']['region'] + "\n" 
          "**Start Time (UTC)**: " + cleanup_time(event_details['successfulSet'][0]['event']['startTime']) + "\n"
          "**Status**: " + event_details['successfulSet'][0]['event']['statusCode'] + "\n"
          "**Event ARN**: " + event_details['successfulSet'][0]['event']['arn'] + "\n"             
          "**Updates:**" + "\n" + get_last_aws_update(event_details)
        )

    elif event_type == "resolve":

        message = str("/md" + "\n" + "**:heavy_check_mark:\[RESOLVED\] The AWS Health issue with the " + event_details['successfulSet'][0]['event']['service'].upper()) +  " service in " + str(event_details['successfulSet'][0]['event']['region'].upper() + " region is now resolved.**" + "\n"
          "---" + "\n"
          "**Account(s)**: " + affected_org_accounts + "\n"
          "**Resource(s)**: " + affected_org_entities + "\n"
          "**Service**: " + event_details['successfulSet'][0]['event']['service'] + "\n"
          "**Region**: " + event_details['successfulSet'][0]['event']['region'] + "\n" 
          "**Start Time (UTC)**: " + cleanup_time(event_details['successfulSet'][0]['event']['startTime']) + "\n"
          "**End Time (UTC)**: " + cleanup_time(event_details['successfulSet'][0]['event']['endTime']) + "\n"
          "**Status**: " + event_details['successfulSet'][0]['event']['statusCode'] + "\n"
          "**Event ARN**: " + event_details['successfulSet'][0]['event']['arn'] + "\n"             
          "**Updates:**" + "\n" + get_last_aws_update(event_details)
        )
    print("Message sent to Chime: ", message)
    return message  



def get_message_for_teams(event_details, event_type, affected_accounts, affected_entities):
    message = ""
    if len(affected_entities) >= 1:
        affected_entities = "\n".join(affected_entities)
        if affected_entities == "UNKNOWN":
            affected_entities = "All resources\nin region"
    else:
        affected_entities = "All resources\nin region"
    if len(affected_accounts) >= 1:
        for x in range(len(affected_accounts)):
            try:
                affected_accounts[x] = bb[affected_accounts[x]]
            except Exception as e:
                print(e)
        affected_accounts = "\n".join(affected_accounts)
    else:
        affected_accounts = "All accounts\nin region"      
    summary = ""
    if event_type == "create":
        title = "&#x1F6A8; [NEW] AWS Health reported an issue with the " + event_details['successfulSet'][0]['event'][
            'service'].upper() + " service in the " + event_details['successfulSet'][0]['event'][
                    'region'].upper() + " region."
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "FF0000",
            "summary": "AWS Health Aware Alert",
            "sections": [
                {
                    "activityTitle": str(title),
                    "markdown": False,
                    "facts": [
                        {"name": "Account(s)", "value": affected_accounts},
                        {"name": "Resource(s)", "value": affected_entities},
                        {"name": "Service", "value": event_details['successfulSet'][0]['event']['service']},
                        {"name": "Region", "value": event_details['successfulSet'][0]['event']['region']},
                        {"name": "Start Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['startTime'])},
                        {"name": "Status", "value": event_details['successfulSet'][0]['event']['statusCode']},
                        {"name": "Event ARN", "value": event_details['successfulSet'][0]['event']['arn']},
                        {"name": "Updates", "value": get_last_aws_update(event_details)}
                    ],
                }
            ]
        }

    elif event_type == "resolve":
        title = "&#x2705; [RESOLVED] The AWS Health issue with the " + event_details['successfulSet'][0]['event'][
            'service'].upper() + " service in the " + event_details['successfulSet'][0]['event'][
                    'region'].upper() + " region is now resolved."
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "00ff00",
            "summary": "AWS Health Aware Alert",
            "sections": [
                {
                    "activityTitle": str(title),
                    "markdown": False,
                    "facts": [
                        {"name": "Account(s)", "value": affected_accounts},
                        {"name": "Resource(s)", "value": affected_entities},
                        {"name": "Service", "value": event_details['successfulSet'][0]['event']['service']},
                        {"name": "Region", "value": event_details['successfulSet'][0]['event']['region']},
                        {"name": "Start Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['startTime'])},
                        {"name": "End Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['endTime'])},
                        {"name": "Status", "value": event_details['successfulSet'][0]['event']['statusCode']},
                        {"name": "Event ARN", "value": event_details['successfulSet'][0]['event']['arn']},
                        {"name": "Updates", "value": get_last_aws_update(event_details)}
                    ],
                }
            ]
        }
    print("Message sent to Teams: ", message)
    return message


def get_org_message_for_teams(event_details, event_type, affected_org_accounts, affected_org_entities):
    message = ""
    summary = ""
    if len(affected_org_entities) >= 1:
        affected_org_entities = "\n".join(affected_org_entities)
    else:
        affected_org_entities = "All resources in region"
    if len(affected_org_accounts) >= 1:
        affected_org_accounts = "\n".join(affected_org_accounts)
    else:
        affected_org_accounts = "All accounts in region"
    if event_type == "create":
        title = "&#x1F6A8; [NEW] AWS Health reported an issue with the " + event_details['successfulSet'][0]['event'][
            'service'].upper() + " service in the " + event_details['successfulSet'][0]['event'][
                    'region'].upper() + " region."
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "FF0000",
            "summary": "AWS Health Aware Alert",
            "sections": [
                {
                    "activityTitle": title,
                    "markdown": False,
                    "facts": [
                        {"name": "Account(s)", "value": affected_org_accounts},
                        {"name": "Resource(s)", "value": affected_org_entities},
                        {"name": "Service", "value": event_details['successfulSet'][0]['event']['service']},
                        {"name": "Region", "value": event_details['successfulSet'][0]['event']['region']},
                        {"name": "Start Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['startTime'])},
                        {"name": "Status", "value": event_details['successfulSet'][0]['event']['statusCode']},
                        {"name": "Event ARN", "value": event_details['successfulSet'][0]['event']['arn']},
                        {"name": "Updates", "value": event_details['successfulSet'][0]['eventDescription']['latestDescription']}
                    ],
                }
            ]
        }

    elif event_type == "resolve":
        title = "&#x2705; [RESOLVED] The AWS Health issue with the " + event_details['successfulSet'][0]['event'][
            'service'].upper() + " service in the " + event_details['successfulSet'][0]['event'][
                    'region'].upper() + " region is now resolved."
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "00ff00",
            "summary": "AWS Health Aware Alert",
            "sections": [
                {
                    "activityTitle": title,
                    "markdown": False,
                    "facts": [
                        {"name": "Account(s)", "value": affected_org_accounts},
                        {"name": "Resource(s)", "value": affected_org_entities},
                        {"name": "Service", "value": event_details['successfulSet'][0]['event']['service']},
                        {"name": "Region", "value": event_details['successfulSet'][0]['event']['region']},
                        {"name": "Start Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['startTime'])},
                        {"name": "End Time (UTC)", "value": cleanup_time(event_details['successfulSet'][0]['event']['endTime'])},
                        {"name": "Status", "value": event_details['successfulSet'][0]['event']['statusCode']},
                        {"name": "Event ARN", "value": event_details['successfulSet'][0]['event']['arn']},
                        {"name": "Updates", "value": event_details['successfulSet'][0]['eventDescription']['latestDescription']}
                    ],
                }
            ]
        }
    return message
    print("Message sent to Teams: ", message)


def get_message_for_email(event_details, event_type, affected_accounts, affected_entities):
    if len(affected_entities) >= 1:
        affected_entities = "\n".join(affected_entities)
        if affected_entities == "UNKNOWN":
            affected_entities = "All resources\nin region"
    else:
        affected_entities = "All resources\nin region"
    if len(affected_accounts) >= 1:
        affected_accounts = "\n".join(affected_accounts)
    else:
        affected_accounts = "All accounts\nin region"
    if event_type == "create":
        BODY_HTML = f"""
        <html>
            <body>
                <h>Greetings from AWS Health Aware,</h><br>
                <p>There is an AWS incident that is in effect which may likely impact your resources. Here are the details:<br><br>
                <b>Account(s):</b> {affected_accounts}<br>
                <b>Resource(s):</b> {affected_entities}<br>
                <b>Service:</b> {event_details['successfulSet'][0]['event']['service']}<br>
                <b>Region:</b> {event_details['successfulSet'][0]['event']['region']}<br>
                <b>Start Time (UTC):</b> {cleanup_time(event_details['successfulSet'][0]['event']['startTime'])}<br>                
                <b>Status:</b> {event_details['successfulSet'][0]['event']['statusCode']}<br>
                <b>Event ARN:</b> {event_details['successfulSet'][0]['event']['arn']}<br> 
                <b>Updates:</b> {event_details['successfulSet'][0]['eventDescription']['latestDescription']}<br><br>
                For updates, please visit the <a href=https://status.aws.amazon.com>AWS Service Health Dashboard</a><br>
                If you are experiencing issues related to this event, please open an <a href=https://console.aws.amazon.com/support/home>AWS Support</a> case within your account.<br><br>
                Thanks, <br><br>AHA: AWS Health Aware
                </p>
            </body>
        </html>
    """
    else:
        BODY_HTML = f"""
        <html>
            <body>
                <h>Greetings again from AWS Health Aware,</h><br>
                <p>Good news! The AWS Health incident from earlier has now been marked as resolved.<br><br>
                <b>Account(s):</b> {affected_accounts}<br>
                <b>Resource(s):</b>   {affected_entities}<br>                         
                <b>Service:</b> {event_details['successfulSet'][0]['event']['service']}<br>
                <b>Region:</b> {event_details['successfulSet'][0]['event']['region']}<br>
                <b>Start Time (UTC):</b> {cleanup_time(event_details['successfulSet'][0]['event']['startTime'])}<br>
                <b>End Time (UTC):</b> {cleanup_time(event_details['successfulSet'][0]['event']['endTime'])}<br>
                <b>Status:</b> {event_details['successfulSet'][0]['event']['statusCode']}<br>                
                <b>Event ARN:</b> {event_details['successfulSet'][0]['event']['arn']}<br>                
                <b>Updates:</b> {event_details['successfulSet'][0]['eventDescription']['latestDescription']}<br><br>  
                If you are still experiencing issues related to this event, please open an <a href=https://console.aws.amazon.com/support/home>AWS Support</a> case within your account.<br><br>                
                <br><br>
                Thanks, <br><br>AHA: AWS Health Aware
                </p>
            </body>
        </html>
    """
    print("Message sent to Email: ", BODY_HTML)
    return BODY_HTML


def get_org_message_for_email(event_details, event_type, affected_org_accounts, affected_org_entities):
    if len(affected_org_entities) >= 1:
        affected_org_entities = "\n".join(affected_org_entities)
    else:
        affected_org_entities = "All services related resources in region"
    if len(affected_org_accounts) >= 1:
        affected_org_accounts = "\n".join(affected_org_accounts)
    else:
        affected_org_accounts = "All accounts in region"
    if event_type == "create":
        BODY_HTML = f"""
        <html>
            <body>
                <h>Greetings from AWS Health Aware,</h><br>
                <p>There is an AWS incident that is in effect which may likely impact your resources. Here are the details:<br><br>
                <b>Account(s):</b> {affected_org_accounts}<br>
                <b>Resource(s):</b> {affected_org_entities}<br>
                <b>Service:</b> {event_details['successfulSet'][0]['event']['service']}<br>
                <b>Region:</b> {event_details['successfulSet'][0]['event']['region']}<br>
                <b>Start Time (UTC):</b> {cleanup_time(event_details['successfulSet'][0]['event']['startTime'])}<br>
                <b>Status:</b> {event_details['successfulSet'][0]['event']['statusCode']}<br>                
                <b>Event ARN:</b> {event_details['successfulSet'][0]['event']['arn']}<br>                
                <b>Updates:</b> {event_details['successfulSet'][0]['eventDescription']['latestDescription']}<br><br>                 
                For updates, please visit the <a href=https://status.aws.amazon.com>AWS Service Health Dashboard</a><br>
                If you are experiencing issues related to this event, please open an <a href=https://console.aws.amazon.com/support/home>AWS Support</a> case within your account.<br><br>
                Thanks, <br><br>AHA: AWS Health Aware
                </p>
            </body>
        </html>
    """
    else:
        BODY_HTML = f"""
        <html>
            <body>
                <h>Greetings again from AWS Health Aware,</h><br>
                <p>Good news! The AWS Health incident from earlier has now been marked as resolved.<br><br>
                <b>Account(s):</b> {affected_org_accounts}<br>
                <b>Resource(s):</b> {affected_org_entities}<br>                            
                <b>Service:</b> {event_details['successfulSet'][0]['event']['service']}<br>
                <b>Region:</b> {event_details['successfulSet'][0]['event']['region']}<br>
                <b>Start Time (UTC):</b> {cleanup_time(event_details['successfulSet'][0]['event']['startTime'])}<br>
                <b>End Time (UTC):</b> {cleanup_time(event_details['successfulSet'][0]['event']['endTime'])}<br>
                <b>Status:</b> {event_details['successfulSet'][0]['event']['statusCode']}<br>                
                <b>Event ARN:</b> {event_details['successfulSet'][0]['event']['arn']}<br>
                <b>Updates:</b> {event_details['successfulSet'][0]['eventDescription']['latestDescription']}<br><br>               
                If you are still experiencing issues related to this event, please open an <a href=https://console.aws.amazon.com/support/home>AWS Support</a> case within your account.<br><br>                
                Thanks, <br><br>AHA: AWS Health Aware
                </p>
            </body>
        </html>
    """
    print("Message sent to Email: ", BODY_HTML)
    return BODY_HTML


def cleanup_time(event_time):
    """
    Takes as input a datetime string as received from The AWS Health event_detail call.  It converts this string to a
    datetime object, changes the timezone to EST and then formats it into a readable string to display in Slack.

    :param event_time: datetime string
    :type event_time: str
    :return: A formatted string that includes the month, date, year and 12-hour time.
    :rtype: str
    """
    event_time = datetime.strptime(event_time[:16], '%Y-%m-%d %H:%M')
    return event_time.strftime("%Y-%m-%d %H:%M:%S")


def get_last_aws_update(event_details):
    """
    Takes as input the event_details and returns the last update from AWS (instead of the entire timeline)

    :param event_details: Detailed information about a specific AWS health event.
    :type event_details: dict
    :return: the last update message from AWS
    :rtype: str
    """
    aws_message = event_details['successfulSet'][0]['eventDescription']['latestDescription']
    return aws_message


def format_date(event_time):
    """
    Takes as input a datetime string as received from The AWS Health event_detail call.  It converts this string to a
    datetime object, changes the timezone to EST and then formats it into a readable string to display in Slack.

    :param event_time: datetime string
    :type event_time: str
    :return: A formatted string that includes the month, date, year and 12-hour time.
    :rtype: str
    """
    event_time = datetime.strptime(event_time[:16], '%Y-%m-%d %H:%M')
    return event_time.strftime('%B %d, %Y at %I:%M %p')
