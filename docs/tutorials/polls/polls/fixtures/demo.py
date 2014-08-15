from django.conf import settings
from django.utils import timezone

from polls.models import Poll
from polls.models import Choice
from django.contrib.auth.models import User

DATA = """
What is your preferred colour? | Blue | Red | Yellow | other
Do you like Django? | Yes | No | Not yet decided
Do you like ExtJS? | Yes | No | Not yet decided
"""

def objects():
    for ln in DATA.splitlines():
        if ln:
            a = ln.split('|')
            p = Poll(question=a[0].strip(),pub_date=timezone.now())
            yield p
            for choice in a[1:]:
                yield Choice(choice_text=choice.strip(),poll=p,votes=0)
                
    yield User.objects.create_superuser('root', 'root@example.com', '1234')
