from django.core.management import ManagementUtility
from django.core.management.base import BaseCommand, CommandError
from distributedlock import distributedlock, LockNotAcquiredError
import types


class Command(BaseCommand):
    """
    Dynamically invokes the command, patching its handle to use distributedlock and perfectly forwards arguments
    usage example:
    manage run_with_lock update_calendars --ignore-past
    """

    def handle(self, *args, **options):
        pass

    help = 'A wrapper command that runs a manage command with a distributed lock.'

    def run_from_argv(self, argv):
        try:
            command_name = argv[2]
            argv.pop(1)
            utility = ManagementUtility(argv)
            command_class = utility.fetch_command(command_name)
            handle = command_class.handle

            def locking_handle(self, *args, **options):
                with distributedlock(command_name):
                    handle(self, *args, **options)

            command_class.handle = types.MethodType(locking_handle, command_class)
            command_class.run_from_argv(utility.argv)
        except IndexError:
            raise CommandError('Missing arguments')
        except LockNotAcquiredError:
            raise CommandError('%s command is already locked' % command_name)
