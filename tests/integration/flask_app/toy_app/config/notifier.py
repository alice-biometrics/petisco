from petisco import INotifier, NotImplementedNotifier


def notifier_provider() -> INotifier:
    return NotImplementedNotifier()
