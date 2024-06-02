from ticket.ticket import Ticket
from train.train import Train
from argparse import ArgumentParser, Namespace
import os


def get_user_details() -> Ticket:
    """This function will get all details of ticket from user"""
    name, gender = str(input("Enter name and gender : ")).split(" ")
    age: int = int(input("Enter the age : "))
    source, dest = str(input("Enter the source and dest : ")).lower().split(" ")
    count: int = int(input("Enter the ticket count : "))
    ticket: Ticket = Ticket(name, age, gender, source, dest, count)

    print("Registered the details you entered\n", ticket)
    print("The PNR number : ", ticket.ticket_uuid)
    return ticket


def reserve_seat() -> None:
    """Reserving process will happen here"""
    train = Train()
    status: int = train.check_availability(get_user_details())
    if status == -1:
        # We need to implement some logic here to alert people for next train ..
        print('You missed out your train, try out next')
    elif status == 0:
        print('You put into waiting list')
    else:
        print('Hurray, seats booked!')


def remove_seat() -> None:
    """Ticket cancelling process happens here"""
    pnr: str = str(input("Enter the PNR number to cancel : ")).lower()
    counts: int = int(input("How many seats you want to remove : "))
    status: int = Train.remove_people(pnr, counts)
    if status == -1:
        print('Some issue occurred')
    elif status == 1:
        print('Ticket got updated')
    else:
        print('The ticket was removed successfully!')


def capture_current_station() -> None:
    """This will note down the last station name in file while exiting"""
    try:
        with open('Train_station.txt', 'w') as files:
            files.write(Train.current_station)
    except Exception as exp:
        print('Some error occurred while capturing the current station', exp)


if __name__ == '__main__':
    """
    options:
      -h, --help   show this help message and exit
    
      -t, --train  This indicate train vehicle
      -b, --bus    This indicate bus vehicle
    """
    parser = ArgumentParser()
    parser.usage = "python MainFrame.py [-t / --train] [-b / --bus]"
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--train', help='This indicate train vehicle', action='store_true')
    group.add_argument('-b', '--bus', help='This indicate bus vehicle', action='store_true')

    args: Namespace = parser.parse_args()

    current_stop: str = 'Tokyo'
    try:
        with open('Train_station.txt', 'r') as file:
            current_stop = file.read()
    except FileNotFoundError:
        # print('File Not Found in the location')
        ...

    if args.train:
        print(f'Welcome to train reservation platform of {current_stop} station')
    elif args.bus:
        print(f'Welcome to bus reservation platform of {current_stop} stand')

    repeat_process: bool = True
    while repeat_process:
        try:
            options: list[str] = ['Reserve', 'Cancel', 'Track', 'Exit']
            for index, option in enumerate(options, start=1):
                print(f'{index}. {option}')
            choice: int = int(input("Enter you're choice : "))

            match choice:
                case 1:
                    reserve_seat()
                    pass
                case 2:
                    # If any one canceled the ticket then waiting list people need to get it.
                    remove_seat()
                    pass
                case 3:
                    # Tracking the ticket status and train
                    ...
                case 4:
                    repeat_process = False
                    capture_current_station()
                    break
                case 5:
                    # Move the train to one station to next nearby station
                    os.system('cls')
                    Train.move_train()
                    pass
                case _:
                    ...
        except Exception as e:
            print("Exception occurred : ", e)

