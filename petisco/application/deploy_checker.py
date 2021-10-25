from datetime import datetime, timedelta

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class DeployChecker:
    def __init__(self, deploy_time: str, courtesy_minutes: int):
        self.deploy_time = deploy_time
        deploy_datetime = datetime.strptime(self.deploy_time[:-6], TIME_FORMAT)
        self.comparison_time = deploy_datetime + timedelta(minutes=courtesy_minutes)

    def was_recently_deployed(self, now: datetime) -> bool:
        return now < self.comparison_time

    def get_deploy_time(self) -> str:
        return self.deploy_time
