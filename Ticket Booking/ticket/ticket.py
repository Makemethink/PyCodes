from dataclasses import dataclass
from uuid import uuid4, UUID


@dataclass
class Ticket:
    # instance variable as no value got assigned
    passenger_name: str
    passenger_age: int
    passenger_gender: str
    journey_source: str
    journey_dest: str
    ticket_count: int

    ticket_uuid: UUID

    # Magic method which will triggered after the object creation
    def __post_init__(self) -> None:
        self.ticket_uuid = uuid4()
        print(f'Your PNR number is : {self.ticket_uuid}')





















