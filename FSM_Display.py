import Tkinter
import time
#import shm

global state_dict
state_dict = {}
global state_name
state_name = ""
global state_history
state_history = []
#global memory_segment
#memory_segment = shm.ShmWrapper('MEMORY SEGMENT NAME HERE');

root = Tkinter.Tk() # We need to define root as the main Tkinter class to call other Tkinter items later

def start_draw_state_machine(input_states, input_transitions):
    class MainWindow: # This code generates our main window. It doesn't create any of the buttons or
                      # entry fields used in any functions - only the purely cosmetic items, like labels and
                      # empty space. It must be a class in order to make it the main window - which means other
                      # windows are anchored to it, and the entire program will close if it is closed.
        def __init__(self, root): # This sets the main window's name as root (a tkinter convention) - you'll notice
                                  # that the first argument in any new tkinter object is the window's name. This
                                  # tells tkinter which window the object 'belongs' to.
            background = Tkinter.Canvas(root, width=1000, height=600) # The Canvas object is blank space.
                                                                             # Other items can be drawn on it, and
                                                                             # we will use it to draw the finite 
                                                                             # state machine.
            background.grid(row=0, column=0) # The .grid() method actually draws our object (in this case 
                                             # anchored at the top left of our screen).
    
    
            quitButton = Tkinter.Button(root, text="Exit", command=quit) #This generates our exit button
            quitButton.grid(row=1, column=1) # This places the exit button
            
            
            def draw_fsm(states, transitions):
                global state_dict
                state_name_dict = {}
                transition_dict = {}
                state_pointer = 0
                transition_pointer = 0
                letter_pointer = 0
                first_state = ""
                transition_return = ""
                second_state = ""
                word_number_pointer = 1 # Will be 0, 1, or 2, depending on if we're in the first state, the transition, or the second state
                x1 = 100
                y1 = 50
                x2 = 200
                y2 = 150
                textX = 120
                textY = 100
                while state_pointer < len(states):
                    state_dict[states[state_pointer]] = background.create_oval(x1,y1,x2,y2, fill='white')
                    state_name_dict[states[state_pointer]] = background.create_text(textX, textY, text = str(states[state_pointer]))
                    if x2 < 1000:
                        x1 += 200
                        x2 += 200
                        textX += 200
                    else:
                        x1 = 100
                        y1 = 250
                        x2 = 200
                        y2 = 350
                        textX = 120
                        textY = 300
                    state_pointer += 1
                while transition_pointer < len(transitions):
                    while letter_pointer < len(transitions[transition_pointer]):
                        if transitions[transition_pointer][letter_pointer] != ":":
                            if word_number_pointer == 1:
                                first_state += transitions[transition_pointer][letter_pointer]
                            elif word_number_pointer == 2:
                                transition_return += transitions[transition_pointer][letter_pointer]
                            elif word_number_pointer == 3:
                                second_state += transitions[transition_pointer][letter_pointer]
                            letter_pointer += 1
                        elif transitions[transition_pointer][letter_pointer] == ":":
                            if word_number_pointer == 1:
                                word_number_pointer = 2
                            elif word_number_pointer == 2:
                                word_number_pointer = 3
                            elif word_number_pointer == 3:
                                word_number_pointer = 1
                            letter_pointer += 1
                    letter_pointer = 0

                    # Draw the arrow here
                    line_x_1 = background.coords(state_dict[first_state])[2]
                    line_y_1 = background.coords(state_dict[first_state])[3] - 50
                    line_x_2 = background.coords(state_dict[second_state])[0]
                    line_y_2 = background.coords(state_dict[second_state])[1] + 50
                    background.create_line(line_x_1, line_y_1, line_x_2, line_y_2)
                    if line_x_1 > line_x_2 and line_y_1 > line_y_2:
                        background.create_line(line_x_2,line_y_2,line_x_2,line_y_2+10)
                        background.create_line(line_x_2,line_y_2,line_x_2+10,line_y_2)
                    elif line_x_1 > line_x_2 and line_y_1 < line_y_2:
                        background.create_line(line_x_2,line_y_2,line_x_2,line_y_2-10)
                        background.create_line(line_x_2,line_y_2,line_x_2+10,line_y_2)
                    elif line_x_1 < line_x_2 and line_y_1 > line_y_2:
                        background.create_line(line_x_2,line_y_2,line_x_2,line_y_2+10)
                        background.create_line(line_x_2,line_y_2,line_x_2-10,line_y_2)
                    elif line_x_1 < line_x_2 and line_y_1 < line_y_2:
                        background.create_line(line_x_2,line_y_2,line_x_2,line_y_2-10)
                        background.create_line(line_x_2,line_y_2,line_x_2-10,line_y_2)
                    elif line_y_1 == line_y_2:
                        background.create_line(line_x_2,line_y_2,line_x_2-10,line_y_2-10)
                        background.create_line(line_x_2,line_y_2,line_x_2-10,line_y_2+10)
                    elif line_x_1 == line_x_2:
                        background.create_line(line_x_2,line_y_2,line_x_2+10,line_y_2-10)
                        background.create_line(line_x_2,line_y_2,line_x_2-10,line_y_2-10)
  
                    # Then we reset everything and check the next arrow
                    first_state = ""
                    transition_return = ""
                    second_state = ""
                    word_number_pointer = 1 # Will be 0, 1, or 2, depending on if we're in the first state, the transition, or the second state
                    transition_pointer += 1
            
            
            def highlight_current_state():
		# if (whatever's saved as the current state) != state_name: 
		# state_history += state_name
		state_name = 'b' # This will be grabbed from shared memory, using the global variable memory_segment set earlier
		if state_name in state_dict:
		    background.itemconfigure(state_dict[state_name],fill="blue")
		else:
		    print "ERROR: UNKNOWN STATE"
		# else:
			# Do nothing        


            highlight_state = Tkinter.Button(root, text='Highlight Current State', command=highlight_current_state)
            highlight_state.grid(row=1,column=0)

            
            draw_fsm(input_states, input_transitions)

    window = MainWindow(root) # This tells Tkinter to draw our MainWindow class as the main window
    Tkinter.mainloop() # This starts the mainloop which draws everything and begins our program

start_draw_state_machine(["a", "b", "c", "d", "e", "f"],["a:foo:b", "c:bar:f"])
