from django.core.management.base import BaseCommand, CommandError
from vasketur.machinestate.models import History

from vasketur.machinestate.utilities import (
    initiate_session,
    authenticate_session,
    request_cookie,
    extract_cookie,
    request_machine_state,
    extract_machine_state,
    parse_machine_state,
    write_machine_state_to_db,
)


class Command(BaseCommand):
    help = "Query the current machine state and store to DB"

    def handle(self, *args, **options):
        session = initiate_session()
        cookie = request_cookie(session)
        cookie = extract_cookie(cookie)
        session = authenticate_session(session)

        rms = request_machine_state(session, cookie)
        ms = extract_machine_state(rms)
        ms = parse_machine_state(ms)

        for entry in ms:
            write_machine_state_to_db(entry)
