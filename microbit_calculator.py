operator = ""
num1 = 0
num2 = 0
result = 0

def on_button_pressed_a():
    global num1, num2
    if operator == "":
        num1 += 1
        if num1 > 9:
            num1 = 0
        basic.show_number(num1)
    else:
        num2 += 1
        if num2 > 9:
            num2 = 0
        basic.show_number(num2)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_ab():
    global result
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "×":
        result = num1 * num2
    elif operator == "÷":
        if num2 == 0:
            basic.show_string("E")
            return
        else:
            result = num1 / num2
    basic.show_number(result)
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    global operator
    if operator == "":
        basic.show_leds("""
            . . # . .
            . . # . .
            # # # # #
            . . # . .
            . . # . .
            """)
        operator = "+"
    elif operator == "+":
        basic.show_leds("""
            . . . . .
            . . . . .
            # # # # #
            . . . . .
            . . . . .
            """)
        operator = "-"
    elif operator == "-":
        basic.show_leds("""
            # . . . #
            . # . # .
            . . # . .
            . # . # .
            # . . . #
            """)
        operator = "×"
    elif operator == "×":
        basic.show_leds("""
            . . # . .
            . . . . .
            # # # # #
            . . . . .
            . . # . .
            """)
        operator = "÷"
    elif operator == "÷":
        operator = "+"
        basic.show_leds("""
            . . # . .
            . . # . .
            # # # # #
            . . # . .
            . . # . .
            """)
input.on_button_pressed(Button.B, on_button_pressed_b)
