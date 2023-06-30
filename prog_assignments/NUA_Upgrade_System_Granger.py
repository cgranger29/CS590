
"""
This Programming Assignment is based on Application Exercise 5.7.29:

Describe an algorithm for the New Unknown Airline (NUA) Upgrade System.
Develop a program that processes the request and cancellations for upgrade and provides the list of k-highest priority flyers among the n frequent flyers on the waiting list.
Your implementation must process the request and cancellations in O(logn) time and find the k-highest-priority flyers in O(k logn) times using the data structures in Chapter 5.
In your submission, you must upload two files:

Submit a typed Word or PDF document with description of your solution on Canvas.
Your answers should be very clear, in proper order, and use complete sentences.
Review your work several times before submission to be sure the steps of the algorithm are clearly and properly stated and in the correct order.
Provide pseudocode for the main algorithms, except for user interface, input/output, etc.
Submit a single zip file named NUA_Upgrade_System_Lastname.zip containing the code file and test files.
Here are some further guidelines for programming code:

Use an OOP language, such as Java, Python or C++. 
Comment your code.
Your code file must compile and accept any number of inputs in the format you specified.
"""

import heapq
import datetime
import uuid
import sys

"""
Status will map to an int for easy comparison for the heap.
super will be highest priority at 1 and silver lowest at 4. Will be utilized in a min heap
"""

# making this global for class access to priority mappings to be used in the min heap.
STATUS_MAPPINGS = {
    "super": 1,
    "platinum": 2,
    "gold": 3,
    "silver": 4
}

MENU_OPTIONS = {
    1: "Add a flyer to the upgrade queue.",
    2: "Cancel a flyers upgrade request.",
    3: "Get top priority flyers for flight upgrades.",
    4: "Display all flyers currently in the upgrade queue. (This is in order of upgrade priority)",
    5: "Exit the system."
}
class Flyer:
    def __init__(self, flyer_name: str, status: str, time_entered_queue = None):
        # default to 0 so in case of invalid status input. Can be used for checks later.
        self.flyer_name = flyer_name
        self.status = STATUS_MAPPINGS.get(status, 0)
        self.status_to_str = status
        #assigment of the confirmation code and queue time will be the responsibility of the flight upgrade class since its not needed till the request is made
        self.time_entered_queue = time_entered_queue
        self.confirmation_code = None

    def __lt__(self, other_flyer):
        '''
        going to override comparison operator so we can account for the Flyer object struct on heap adds and deletes
        this is not completely intuitive since the less than comparison is now going to function as more of a priority comparison
        so if current_flyer < other_flyer it means that it has a higher priority so will be higher on the heap (higher meaning closer to root)
        '''
        if self.status == other_flyer.status:
            # if current flyer time is greater it means they were added to queue after so lower priority on same status
            if self.time_entered_queue > other_flyer.time_entered_queue:
                return False
        # lower status (greater int value in this case) means lower priority so current_flyer < other_flyer
        elif self.status > other_flyer.status:
            return False

        # end return is arbitrary so can be w/e, will default to True in this case.
        return True

    def __le__(self, other_flyer):
        # mimics the __lt__ override so we can use less than equal or greater than equal comprison
        if self.status == other_flyer.status:
            if self.time_entered_queue > other_flyer.time_entered_queue:
                return False
        elif self.status > other_flyer.status:
            return False

        return True

    def __str__(self):
        # lets also print the flyer info instead of the object on print() for each peek
        return f"Flyer: {self.flyer_name}\nStatus: {self.status_to_str}\nTime entered queue: {self.time_entered_queue}\nConfirmation Code: {self.confirmation_code}"

    # assign current time on request add, use for fallback comparison if status are equal between two flyers.
    def set_current_time(self, time_to_set = None):
        self.time_entered_queue = time_to_set
    
    #setter for confirmation code
    def set_confirmation_code(self, confirmation_code: int):
        self.confirmation_code = confirmation_code
    
    #getter for confirmation code
    def get_confirmation_code(self):
        return self.confirmation_code

class FlightUpgradeSystem:
    def __init__(self, flight_name: str):
        self.flight_name = flight_name
        self.upgrade_heap = []
        # Going to just store cancellation confirmation codes in a set and then check it whenever we want to upgrade people on the flight or pull k flyers
        # this should give us the O(logn) 'deletion' without having to search the heap and instead can just remove when we encounter it naturally
        # In other words, for each heap pop we will always check the set for the confirmation code existence and if encountered we can just ignore / discard as encountered
        self.cancellations = set()

    def request_upgrade(self, flyer: Flyer):
        # add Flyer to the queue
        # this will also need to set the confirmation code on the Flyer

        #since this just needs to be O(logn) thats a typical heap insertion that will bubble up
        heapq.heappush(self.upgrade_heap, flyer)
        # set confirmation code to each flyer
        flyer.set_confirmation_code(self.generate_confirmation_code())

        print(f"Your flight upgrade confirmation code for flyer {flyer.flyer_name} is {flyer.confirmation_code}.\n")

        return flyer.confirmation_code

    def generate_confirmation_code(self):
        #generates a random uuid value for use in confirmation code
        return uuid.uuid4()

    def cancel_upgrade(self, flyer: Flyer = None, confirmation_code = None):
        if flyer:
            if flyer.confirmation_code not in self.cancellations:
                self.cancellations.add(flyer.confirmation_code)
        elif confirmation_code:
            self.cancellations.add(confirmation_code)
    
    def find_highest_priority_flyers_for_upgrade(self, number_of_available_seats: int):
        _start = 0
        res = []
        # two cases will break this loop, _start >= number_of_available_seats or the upgrade_heap is empty
        while _start < number_of_available_seats and self.upgrade_heap:
            current_flyer = heapq.heappop(self.upgrade_heap)
            if str(current_flyer.confirmation_code) not in self.cancellations:
                res.append(current_flyer)
                _start += 1
                print(f"{current_flyer}\n")
            else:
                # if confirmation code is in the cancellation pop flyer off the heap but ignore adding to upgrades
                print(f"{current_flyer.flyer_name} was found in cancellations. Skipping flyer add and removing from heap.\n")

        return res
class FlightSystemUI:
    def __init__(self):
        self.possible_user_inputs = set([1,2,3,4,5])
        self.system = FlightUpgradeSystem("Flight Whatever")

    def display_main_menu(self):
        print("\n#####Please select from the system options below:#####\n")
        for option_num, option_val in MENU_OPTIONS.items():
            print(f"{option_num}: {option_val}")

    def add_flyer(self):
        flyer_name = input("Please enter the flyers name: ")
        flyer_status = input("Please enter the flyers status (silver, gold, platinum, super): ")

        if flyer_status not in STATUS_MAPPINGS:
            print(f"Unknown status of {flyer_status} entered. Please run again with a valid status input.")
            return

        flyer_to_add = Flyer(flyer_name, flyer_status)

        flyer_to_add.set_current_time(datetime.datetime.now())
        confirm_code = self.system.request_upgrade(flyer_to_add)

        print(f"Confirmation code for flyer {flyer_name} is {confirm_code}. Please store this as it will be needed if you would like to make a cancellation.\n*PLEASE NOTE that confirmation codes can also be viewed using option 4.")

    def upgrade_highest_priority_flyers(self):
        try:
            flyers_to_upgrade = int(input("Please enter the the number of flyers to upgrade: "))
            if flyers_to_upgrade <= 0:
                raise ValueError
            print("\n###The below flyers have been upgraded in order of appearance.###\n")
            self.system.find_highest_priority_flyers_for_upgrade(flyers_to_upgrade)

        except ValueError:
            print("\nInvalid entry. Value must be an int greater than 0")

    def cancel_flyer_upgrade_request(self):

        confirmation_code = input("Please enter a valid confirmation code: ")
        self.system.cancel_upgrade(confirmation_code = confirmation_code)

        print(f"Confirmation code {confirmation_code} was added to the system.")

    def display_all_flyers_currently_in_queue(self):
        print("\n#####Flyers currently in the upgrade queue:#####\n")
        for _flyer in self.system.upgrade_heap:
            if str(_flyer.confirmation_code) not in self.system.cancellations:
                print(f"\n{_flyer}\n")

    def run_system(self):
        user_input = 0
        print("###Welcome to Flight Upgrade System for FooBar flights. Please select an option below:###\n")

        while user_input != 5:
            self.display_main_menu()
            try:
                user_input = int(input("\nOption: "))
            except ValueError:
                print(f"!!! Only int values 1-5 are valid inputs. No characters are allowed. !!!\n")

            if user_input not in self.possible_user_inputs:
                print(f"\n{user_input} is not a valid input. Please select one of the input option numbers listed.\n\n")
                continue
            # theres only 5 options so ill just chain some if / elif statements otherwise would handle this differently with dict mappings
            if user_input == 1:
                self.add_flyer()
            elif user_input == 2:
                self.cancel_flyer_upgrade_request()
            elif user_input == 3:
                self.upgrade_highest_priority_flyers()
            elif user_input == 4:
                self.display_all_flyers_currently_in_queue()
            elif user_input == 5:
                print("Exiting system.")
                sys.exit(0)
            

# run this directly no importing
if __name__ == "__main__":
    flight_system = FlightSystemUI()
    flight_system.run_system()