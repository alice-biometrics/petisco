from petisco.base.domain.errors.critical_error import CriticalError


class BusCannotPublish(CriticalError):
    def get_specify_detail(cls) -> str:
        return "Unable to finish all the actions of this operation"
