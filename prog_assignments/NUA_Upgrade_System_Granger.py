
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
        '''
        if we get here it means current flyer should have a higher priority so current_flyer < other_flyer is True
        this would also be the default for the same time in queue and same status since we need a result for something
        given that python implements a min heap this is sort of inverse so we have highest priority at root and can just pop off flyers

        end return is arbitrary so can be w/e
        '''
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

    def calculate_current_time(self) -> None:
        # assign current time on request add
        self.time_entered_queue = datetime.datetime.now()
    
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
        # Going to just store cancellation confirmation codes in a set and then check it whenever we wanna upgrade people on the flight or pull k flyers
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

    def generate_confirmation_code(self):
        #generates a random uuid value for use in confirmation code
        return uuid.uuid4()

    def cancel_upgrade(self, flyer: Flyer):
        if flyer.confirmation_code not in self.cancellations:
            self.cancellations.add(flyer.confirmation_code)

    def determine_upgrades_for_flight(self, number_of_available_seats: int):
        pass

# run this directly no importing
if __name__ == "__main__":
    # do stuff
    pass

# going to assume that it would be extremely rare for two flyers to enter system update at the exact same time so will handle in arbitrary way
# if this did occur the less than comparison would just return False by default anyway
# for now every new flyer add will differ by one second for testing
flyer_1 = Flyer("Cody", "gold", datetime.datetime.now())
flyer_2 = Flyer("Meghan", "gold", datetime.datetime.now() + datetime.timedelta(0, 1))
flyer_3 = Flyer("Chad", "platinum", datetime.datetime.now() + datetime.timedelta(0, 2))
flyer_4 = Flyer("Chuck", "silver", datetime.datetime.now() + datetime.timedelta(0, 3))
flyer_5 = Flyer("Steph", "super", datetime.datetime.now() + datetime.timedelta(0, 4))
flyer_6 = Flyer("Bryan", "platinum", datetime.datetime.now() + datetime.timedelta(0, 5))

flight = FlightUpgradeSystem("cool_flight_1")

print(flyer_1 < flyer_4)



flight.request_upgrade(flyer_1)
flight.request_upgrade(flyer_2)
flight.request_upgrade(flyer_3)
flight.request_upgrade(flyer_4)
flight.request_upgrade(flyer_5)
flight.request_upgrade(flyer_6)

# for _flyer in flight.upgrade_heap:
#     print(f"\n{_flyer}")

print(heapq.heappop(flight.upgrade_heap))
print(heapq.heappop(flight.upgrade_heap))
print(heapq.heappop(flight.upgrade_heap))
print(heapq.heappop(flight.upgrade_heap))
print(heapq.heappop(flight.upgrade_heap))
print(heapq.heappop(flight.upgrade_heap))

print(flight.upgrade_heap)
upgrade_system.txt
Displaying upgrade_system.txt.