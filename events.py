import pyautogui


def msg(text):
  pyautogui.alert(text)

def button_click(button, font):
  button.change_text("LMYAU", font)



