# Elevator
An elevator API 
A controller for Elevator in a building of M floors. On every floor there is two call buttons (Up and Down) to call for elevator and the screen showing elevator's current state (floor and direction). In the Elevator there are M buttons, every button is associated with one floor. 

o Call from any floor, will be treated when Elevator is free
o The call from inside of elevator has higher priority than the call for the elevator
o Elevator will stop on floor if someone from inside asked for this floor or if someone outside ask for elevator in the same direction the elevator is going
