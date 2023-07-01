
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

"""
Status will map to an int for easy comparison for the heap.
super will be highest priority at 1 and silver lowest at 4. Will be utilized in a min heap
"""

STATUS_MAPPINGS = {
    "Super": 1,
    "Platinum": 2,
    "Gold": 3,
    "Silver": 4
}
class Flyer:
    def __init__(self, flyer_name: str, status: str, time_in_queue = None, confirmation_code = None):
        self.flyer_name = flyer_name
        self.status = STATUS_MAPPINGS.get(status, 0)
        self.status_to_str = status
        self.time_in_queue = time_in_queue
        self.confirmation_code = confirmation_code

    def __lt__(self, other_flyer):
        '''
        going to override comparison operator so we can account for the Flyer object struct on heap adds and deletes
        so if current_flyer > other_flyer it means that it has a higher priority so will be higher on the heap (higher meaning closer to root)
        '''
        if self.status == other_flyer.status:
            # if current flyer time is greater it means they were added to queue after so lower priority on same status
            if self.time_in_queue > other_flyer.time_in_queue:
                return True
        # lower status (greater int value in this case) means lower priority so current_flyer < other_flyer
        elif self.status > other_flyer.status:
            return False

        # end return is arbitrary so can be w/e, will default to True in this case.
        return True

    def __le__(self, other_flyer):
        # mimics the __lt__ override so we can use less than equal or greater than equal comprison
        if self.status == other_flyer.status:
            if self.time_in_queue > other_flyer.time_in_queue:
                return True
        elif self.status > other_flyer.status:
            return False

        return True

    def __str__(self):
        # lets also print the flyer info instead of the object on print() for each peek
        return f"Flyer: {self.flyer_name}\nStatus: {self.status_to_str}\nTime in queue: {self.time_in_queue}\nConfirmation Code: {self.confirmation_code}"

class FlightUpgradeSystem:
    def __init__(self):
        self.upgrade_heap = []
        # Going to just store cancellation confirmation codes in a set and then check it whenever we call for highest k flyers
        # this should give us the O(logn) 'deletion' without having to search the heap and instead can just remove when we encounter it naturally
        # In other words, for each heap pop we will always check the set for the confirmation code existence and if encountered we can just ignore / discard as encountered
        self.cancellations = set()

    def add_to_upgrade_queue(self, flyer: Flyer):
        # add Flyer to the queue
        # since this just needs to be O(logn) thats a typical heap insertion that will bubble up
        heapq.heappush(self.upgrade_heap, flyer)
    
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

        return res
       
def main(file):
    
    flight_system = FlightUpgradeSystem()

    with open(file) as fs:

        file_output = [line.split(" ") for line in fs.read().splitlines() if line != ""]

        number_of_flyers, k_highest_priority_flyer, num_cancellations = file_output[0]

        # convert text file flyers to Flyer class.
        for i in range(1, len(file_output) - int(num_cancellations)):
            flyer_name = file_output[i][0]
            flyer_id = file_output[i][1]
            flyer_time = file_output[i][2]
            flyer_status = file_output[i][3]
            
            _flyer = Flyer(flyer_name=flyer_name, status = flyer_status, time_in_queue=int(flyer_time), confirmation_code=flyer_id)

            flight_system.add_to_upgrade_queue(_flyer)

        # get the cancellation numbers
        for i in range(int(number_of_flyers) + 1, len(file_output)):
            flight_system.cancellations.add(file_output[i][0])

    flight_system.find_highest_priority_flyers_for_upgrade(int(k_highest_priority_flyer))

if __name__ == "__main__":
    """
    n = Number of flyers in waiting list
    k = Required K highest priority flyers
    c = Number of cancellation requests
    
    First line of file is n,k,c respectively

    middle section of file are the flyer info up to n flyers. (flyer name, flyer_id, flyer time in queue, flyer status)

    last section are the flyer id of cancellations

    Example file below:
    
    ###FILE START###
    4 1 2

    A 1 30 Platinum
    B 2 60 Gold
    C 3 90 Silver
    D 4 120 Super

    2
    4
    
    ###FILE END###

    Output will print each flyer in order of priority

    Flyer: A
    Status: Platinum
    Time in queue: 30
    Confirmation Code: 1
    """
    main("./test_cases.txt")