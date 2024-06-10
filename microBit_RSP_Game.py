def on_button_pressed_a():
    global choice_index
    choice_index = (choice_index + 1) % 3
    if choices[choice_index] == "Rock":
        basic.show_leds("""
            . # # # .
            # # # # #
            # # # # #
            # # # # #
            . # # # .
            """)
    elif choices[choice_index] == "Scissors":
        basic.show_leds("""
            # . . . #
            . # . # .
            . . # . .
            . # . # .
            # . . . #
            """)
    elif choices[choice_index] == "Paper":
        basic.show_leds("""
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            """)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_ab():
    global result, current_user
    if current_user == 3:
        if user1_choice == user2_choice:
            result = "DRAW"
        elif user1_choice == "Rock" and user2_choice == "Scissors" or user1_choice == "Paper" and user2_choice == "Rock" or user1_choice == "Scissors" and user2_choice == "Paper":
            result = "A WIN"
        else:
            result = "B WIN"
        basic.show_string(result)
        current_user = 1
        basic.show_string("A")
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    global user1_choice, current_user, user2_choice
    if current_user == 1:
        user1_choice = choices[choice_index]
        basic.show_string("OK")
        current_user = 2
        basic.show_string("B")
    elif current_user == 2:
        user2_choice = choices[choice_index]
        basic.show_string("OK")
        current_user = 3
        basic.show_string("AB")
input.on_button_pressed(Button.B, on_button_pressed_b)

result = ""
user2_choice = ""
user1_choice = ""
choice_index = 0
choices: List[str] = []
current_user = 0
current_user = 1
basic.show_string("A")
choices = ["Rock", "Scissors", "Paper"]