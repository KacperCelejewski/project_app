from project import db
import pendulum


class Project:
    def __init__(
        self, name, author, members=[], years_to_end=0, months_to_end=0, days_to_end=0
    ) -> None:
        self.name = name
        self.members = []
        if members is not None:
            for i, member in enumerate(members):
                self.members.append((member, i))

        self.time_to_end = {}
        self.author = author

    def deadline(self):
        utc_time = pendulum.now("UTC")
        return utc_time.add(
            years=self.years_to_end, months=self.months_to_end, days=self.days_to_end
        )
