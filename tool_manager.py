from tools import (
    get_current_time,
    roll_dice,
    generate_password
)

def execute_tool(user_input):
  user_prompt = user_input.lower()

  if "time" in user_prompt or "clock" in user_prompt:
    return f"The current time is {get_current_time()}"

  if "dice" in user_prompt or "die" in user_prompt:
    return f"You rolled {roll_dice()}"

  if "password" in user_prompt or "passcode" in user_prompt:
    return f"Your initial test password is {generate_password()}"

  return None
