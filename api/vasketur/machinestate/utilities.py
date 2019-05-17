import requests
import os
from requests_html import HTMLSession

from vasketur.machinestate.models import History

URL_COOKIE = "https://web.vasketur.dk/PPW0083/Default.aspx"
URL_MSTATE = "https://web.vasketur.dk/PPW0083/Machine/MachineGroupStat.aspx"


USER_FIELD_KEY = "tbUsername"
PW_FIELD_KEY = "tbPassword"
USER_FIELD = "ctl00$ContentPlaceHolder1$" + USER_FIELD_KEY
PW_FIELD = "ctl00$ContentPlaceHolder1$" + PW_FIELD_KEY

USER = os.environ[USER_FIELD_KEY]
PW = os.environ[PW_FIELD_KEY]


STATE_IDs = {
    "V1_ID": "ctl00_ContentPlaceHolder1_Repeater1_ctl00_Repeater2_ctl00_Repeater3_ctl01_",
    "V2_ID": "ctl00_ContentPlaceHolder1_Repeater1_ctl00_Repeater2_ctl01_Repeater3_ctl01_",
    "V3_ID": "ctl00_ContentPlaceHolder1_Repeater1_ctl00_Repeater2_ctl02_Repeater3_ctl01_",
    "T1_ID": "ctl00_ContentPlaceHolder1_Repeater1_ctl02_Repeater2_ctl00_Repeater3_ctl01_",
    "T2_ID": "ctl00_ContentPlaceHolder1_Repeater1_ctl02_Repeater2_ctl01_Repeater3_ctl01_",
    "T3_ID": "ctl00_ContentPlaceHolder1_Repeater1_ctl02_Repeater2_ctl02_Repeater3_ctl01_",
}
STATUS_FIELD = "LabelStatus"
TIMELEFT_FIELD = "divTimeLeft"


def initiate_session():
    """Initiate a session such that cookies, ... persist"""
    session = HTMLSession()
    return session


def request_cookie(session):
    """Requests a cookie and returns it in form of session object"""
    r = session.get(URL_COOKIE)
    return r


def extract_cookie(session):
    """Extract the WebBoka cookie value from the session"""
    cookie = session.cookies.get_dict()
    return cookie.get("RCARDM5WebBoka")


def authenticate_session(session):
    payload = {
        "__EVENTTARGET": "ctl00$ContentPlaceHolder1$btOK",
        "__VIEWSTATE": "/wEPDwUJLTY3OTUyMjQ4D2QWAmYPZBYCAgMPZBYGAgEPDxYCHgdWaXNpYmxlaGQWAmYPFQEHTG9nIGluZGQCAw9kFgICAQ9kFgoCAQ8PFgIeBFRleHQFGVBheSBQZXIgV2FzaCAtIFZpc2lvbiBXZWJkZAIDDw8WAh8BBQVOYXZuOmRkAgcPDxYCHwEFDEFkZ2FuZ3Nrb2RlOmRkAgsPDxYCHwEFB0xvZyBpbmRkZAINDw8WAh8BBQpHbGVtdCBrb2RlZGQCBQ8PFgIfAQU9VmVyc2lvbiAxLjIuMC43IENvcHlyaWdodCBFbGVjdHJvbHV4IExhdW5kcnkgU3lzdGVtIFN3ZWRlbiBBQmRkZHV3sCE6+xQ8w+uXTPKP1NGfB5as",
        "__EVENTVALIDATION": "/wEWBgLuutq8DQKi8/y9CAKqgsX1DAKZ7b30DgKg+M/XDwLg74q7AoEwyLUwFkDrEBarE68QVPUAqPrg",
        USER_FIELD: USER,
        PW_FIELD: PW,
    }
    session.post(URL_COOKIE, data=payload)

    return session


def request_machine_state(session, cookie_string):
    """Request the html page for the machine state"""
    s = session

    headers = {"Cookie": "RCARDM5WebBoka={}; ASP.NET_SessionId=".format(cookie_string)}
    payload = {USER_FIELD: USER, PW_FIELD: PW}

    r = s.get(URL_MSTATE, headers=headers, data=payload)

    return r


def extract_machine_state(machine_state_response):
    state_list = []
    r = machine_state_response
    for key in STATE_IDs:
        field_id = STATE_IDs.get(key)
        if field_id:
            field_id = "#" + field_id + STATUS_FIELD
            state = r.html.find(field_id)
            state_list.extend(state)
    return state_list


def convert_scandi_chars(snippet):
    return snippet.encode("latin-1").decode("UTF-8")


def parse_machine_state(state_list):
    for i, state in enumerate(state_list):
        r = {}
        state = state.text.split(" ")

        machine_type = convert_scandi_chars(state[0])
        if "vask" in machine_type.lower():
            machine_type = "Wash"
        elif "tørr" in machine_type.lower():
            machine_type = "Dry"

        machine_status = convert_scandi_chars(state[2])
        if "afslut" in machine_status.lower():
            machine_status = "Finished"
        elif "start" in machine_status.lower():
            machine_status = "Started"
        elif "klar" in machine_status.lower():
            machine_status = "In Progress"

        time = ""
        if machine_status == "In Progress":
            time = state[4]
        else:
            time = state[3]

        r["machine_type"] = machine_type
        r["machine_num"] = state[1]
        r["machine_status"] = machine_status
        r["time"] = time

        state_list[i] = r

    return state_list


def write_machine_state_to_db(state):
    obj, created = History.objects.get_or_create(
        machine_type=state["machine_type"],
        machine_num=state["machine_num"],
        machine_status=state["machine_status"],
        machine_time_value=state["time"],
    )

    return (obj, created)
