import time
import threading
M =10
UP=1
DOWN=-1

class Elevator():
    """An elevator class. Elevator has its position- floor number, direction- -1 is down and 1 is up ,
     and an array of floors pressed from inside the elevator"""
    def __init__(self):
        self.current_floor = 0
        self.direction = UP
        self.pressed_buttons= [0] * M

    def moveOne(self):
        """Step function for elevator movement. In every step elevator come one floor higher or one floor lower."""
        self.current_floor += self.direction
        time.sleep(1)
        print("elevator on floor", self.current_floor)
        # HW - MoveOneFloor(self)

    def StopOnFloor(self):
        """Function to clear the elvator's pressed buttons array when floor was stopped at """
        if self.direction==UP:
            print("all passengers going up get on board")
        if self.direction == DOWN:
            print("all passengers going down get on board")
        # HW - OpenDoors(self)
        time.sleep(2)
        self.pressed_buttons[self.current_floor] = 0
        print("be carful, doors are closing")
        #HW - CloseDoors(self)
        time.sleep(1)

    def PressFromInside(self, floor):
        """Function to add a customer's request from inside the floor """
        self.pressed_buttons[floor]=1
        #HW-    ButtonPushed

    def MostExtremeFloor(self):
        """Function finds the lowest floor asked for from inside the elevator if elevator is going down,
          or highest floor if it's going up"""
        if self.direction==UP:
            for i in range(M-1,0,-1):
                if self.pressed_buttons[i]==1:
                    return i
        if self.direction == DOWN:
            for i in range (0,M,1):
                if self.pressed_buttons[i] == 1:
                    return i
        # should not get here because we check if elevator is empty before
        return -1

    def GoRestAtFloor(self,target):
        if target < self.current_floor:
            self.direction = DOWN
        if target >self.current_floor:
            self.direction = UP
        while self.current_floor is not target:
            self.moveOne()


    def isElevatorFree(self):
        """Function returns 1 if elevator is not free and -1 if it is  """
        for i in range(0, M):
            if self.pressed_buttons[i] == 1:
                return False
        return True

    def ChangDirection(self):
        self.direction= self.direction * -1
        # HW - ChangeDirection(self)

class Building():
    """A building class. Building has number of floors, an elevator class, and two arrays for requests from
    outside of the elevator- floors were a button requesting up was pressed, and where down was asked"""
    def __init__(self):
        self.going_up = [0] * M
        self.going_down = [0] * M
        self.elevator = Elevator()

    def EnterCustomers(self, floor, direction):
        """Function to add a passenger's request from outside the elevator. the passenger presses the
        button at a certain floor and asked for up/down direction"""
        if direction == UP:
            self.going_up[floor]=1
        if direction == DOWN:
            self.going_down[floor] = 1

    def PeopleWaiting(self):
        """checks if somene asked for the elevator from outside """
        for i in range(0, M):
            if self.going_up[i] == 1 or self.going_down[i]==1:
                return True
        return False

    def GoToTarget(self,target):
        """makes the elevator go to a specific target, and checks if to stop at floors in the middle  """
        # shouldnt get here...
        if target == -1:
            print('waiting for some buttons to be pushed')
        if target < self.elevator.current_floor:
            self.elevator.direction = DOWN
        if target > self.elevator.current_floor:
            self.elevator.direction = UP
        while self.elevator.current_floor is not target:
            self.elevator.moveOne()
            if (self.elevator.pressed_buttons[self.elevator.current_floor] ==1 ) or \
            (self.elevator.direction == UP and self.going_up[self.elevator.current_floor] == 1) or \
            (self.elevator.direction == DOWN and self.going_down[self.elevator.current_floor] == 1):
                 self.elevator.StopOnFloor()
                 if self.elevator.direction == UP:
                    self.going_up[self.elevator.current_floor] = 0
                 if self.elevator.direction == DOWN:
                    self.going_down[self.elevator.current_floor] = 0
            elif self.going_up[self.elevator.current_floor] == 1 or self.going_down[self.elevator.current_floor] == 1:
                print('get inside please')
                self.going_down[self.elevator.current_floor] = 0
                self.going_up[self.elevator.current_floor] = 0
        return

    def UppestFloorAsked(self):
        """looking for the highest floor that was asked- no matter if to keep going up or start going down.
          that way we cant starve last floor"""
        for i in range(M -1, self.elevator.current_floor, -1):
            if self.going_up[i] == 1 or self.going_down[i] == 1:
                return i
        """we are on the highest floor asked for"""
        return -1

    def LowestFloorAsked(self):
        """looking for the lowest floor that was asked- no matter if to keep going up or start going down.
          that way we cant starve first floor"""
        for i in range(0, self.elevator.current_floor , 1):
            if self.going_up[i] == 1 or self.going_down[i] == 1:
                return i
        """we are on the lowest floor asked for"""
        return -1

    def run(self):
        """Core step function. works all the time and searching for it's target depending on costumers requests"""
        while True:
        # Elevator not asked for at all. wait at the entrance of the building. on different logic could be the middle of the building

            #if self.elevator.isElevatorFree()==True and self.PeopleWaiting()==False:
              #  self.elevator.GoRestAtFloor()
               # self.elevator.direction= UP

            # when there are no requests from inside we'll go to the elevators most extreme requested floor in the same direction
            if self.elevator.isElevatorFree()==True and self.PeopleWaiting()==True:
                if self.elevator.direction == UP:
                    target = self.UppestFloorAsked()
                    if target == -1:
                        self.elevator.ChangDirection()
                        target = self.LowestFloorAsked()
                else:
                    target = self.LowestFloorAsked()
                    if target == -1:
                        self.elevator.ChangDirection()
                        target = self.UppestFloorAsked()
                self.GoToTarget(target)
            # there are requests from inside the elevator. get to highest/lowest floor, depending on directions, and go there
            if self.elevator.isElevatorFree()==False:
                if self.elevator.direction == UP:
                     target = self.elevator.MostExtremeFloor()
                     if target < self.elevator.current_floor:
                        target = self.UppestFloorAsked()
                        if target == -1:
                            self.elevator.ChangDirection()
                            target = self.LowestFloorAsked()
                if self.elevator.direction == DOWN:
                    target = self.elevator.MostExtremeFloor()
                    if target > self.elevator.current_floor:
                        target = self.LowestFloorAsked()
                        if target == -1:
                            self.elevator.ChangDirection()
                            target = self.UppestFloorAsked()
                self.GoToTarget(target)



    def Input(self):
        """ inputs for trials"""
        time.sleep(2)
        self.EnterCustomers(2, UP)
        self.elevator.PressFromInside(4)
        time.sleep(2)
        self.elevator.PressFromInside(1)
        self.EnterCustomers(8, UP)
        self.elevator.PressFromInside(9)


def main():
    """main function. creates a thread for input handling and a thread for elevator scheduling and operates"""
    building_main = Building()
    t1 = threading.Thread(target=building_main.Input)
    t2 = threading.Thread(target=building_main.run)
    t1.start()
    t2.start()


if __name__ == "__main__":
    main()