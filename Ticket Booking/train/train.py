from ticket.ticket import Ticket
from base.vehicle import Vehicle


class Train(Vehicle):
    # class variable as value got assigned already
    total_seats = 5
    available_seats = 5
    station_list: list[str] = ['tokyo', 'kyoto', 'hiroshima', 'osaka', 'shibuya']
    source_station: str = station_list[0]
    dest_station: str = station_list[-1]
    current_station = 'tokyo'

    accepted_tickets = []  # If data grows use array
    awaiting_tickets = []  # If data grows use array

    def check_availability(self, ticket: Ticket) -> int:
        # Check source and destination (If the train already left the station or not)
        if Train.current_station != ticket.journey_source:
            print('Try out next train')
            return -1   # Try next train
        # Check the availability of seats, if no seat put it in waiting list
        if Train.available_seats < ticket.ticket_count:
            print('Putting you on waiting list')
            Train.awaiting_tickets.append(ticket)
            return 0    # Waiting list
        # Then reserve seat of person and change the available_seats
        Train.available_seats = Train.available_seats - ticket.ticket_count
        Train.accepted_tickets.append(ticket)
        return 1

    @classmethod
    def check_fill_removed(cls) -> None:
        for obj in cls.awaiting_tickets:
            if obj.ticket_count <= cls.available_seats:
                Train.accepted_tickets.append(obj)
                cls.available_seats = cls.available_seats - obj.ticket_count
                print(f'The {obj.ticket_uuid} booking is confirmed, happy journey!')
                cls.awaiting_tickets.remove(obj)
                if cls.available_seats == 0:
                    break

    # noinspection SpellCheckingInspection
    @staticmethod
    def current_train_name() -> str:   # Does nothing just a normal function but included in this class
        return 'Jan Sadapti'

    @classmethod
    def remove_people(cls, pnr: str, count: int) -> int:
        try:
            searching_obj = None
            for obj in Train.accepted_tickets:
                if str(obj.ticket_uuid) == pnr:
                    searching_obj = obj
                    break

            status: int
            if searching_obj is not None:
                # Ticket with the given PNR found
                if searching_obj.ticket_count < count:
                    status = -1
                elif searching_obj.ticket_count > count:
                    Train.available_seats = Train.available_seats + count
                    searching_obj.ticket_count = searching_obj.ticket_count - count
                    status = 1
                else:
                    # Remove all ticket count
                    Train.accepted_tickets.remove(searching_obj)
                    Train.available_seats = Train.available_seats + count
                    status = 2
            else:
                # Ticket with the given PNR not found
                status = -1

            Train.check_fill_removed()
            return status
        except Exception as e:
            print('Error occurred', e)

    @classmethod
    def move_train(cls) -> None:
        print(f"Current train station : {cls.current_station} and available seats : {cls.available_seats}")
        index: int = cls.station_list.index(cls.current_station)
        if len(cls.station_list)-1 == index:
            print("Train arrived last station")
        else:
            cls.current_station = cls.station_list[index+1]
            print(f"The next station was {cls.current_station}")
        print(f"Passengers in train {Train.total_seats - Train.available_seats}")
        print(f'Waiting lists {len(Train.awaiting_tickets)}')

        # What if the passengers dest station arrived, need to drop them and update values
