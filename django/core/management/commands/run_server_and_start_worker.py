from django.core.management.commands.runserver import Command as BaseRunserverCommand
from django_q.cluster import Cluster

class Command(BaseRunserverCommand):
    def handle(self, *args, **options):
        q = Cluster()
        q.start()
        super().handle(*args, **options)
