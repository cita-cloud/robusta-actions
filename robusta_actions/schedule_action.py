from robusta.api import *

class CldiParams(ActionParams):
    admin_sk: str
    rpc_endpoint: str


@action
def check_schedule(event: ScheduledExecutionEvent, params: CldiParams):
    event.add_enrichment([
        MarkdownBlock(f"check_schedule event={event}, params={params}, It's time to sleep or wakeup!"),
    ])
