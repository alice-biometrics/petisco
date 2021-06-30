from petisco.legacy import INotifier, NotImplementedNotifier


def notifier_provider() -> INotifier:
    return NotImplementedNotifier()
