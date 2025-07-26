from calendar_adder import authenticate_calendar, add_event

calendar_service = authenticate_calendar()

add_event(
    service=calendar_service,
    summary="Test Deadline",
    description="This is a test deadline added from Python.",
    date_string="07/30/2025"  # change this to tomorrow
)
