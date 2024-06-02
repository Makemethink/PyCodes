from abc import ABC, abstractmethod
from dataclasses import dataclass
from ticket.ticket import Ticket


@dataclass
class Vehicle(ABC):

    @abstractmethod
    def check_availability(self, ticket: Ticket) -> None:
        pass

    @classmethod
    @abstractmethod
    def remove_people(cls, pnr: str, count: int) -> None:
        pass

