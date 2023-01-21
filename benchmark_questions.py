benchmark_questions =[
    {'Question': "What is your name?", 'Answer': "speak(\"My name is Dude.\")"},
    {'Question': "Draw a triangle. You are at position [-2, -2]", 'Answer': "[waypoint_motion([-2, 2], 1, \"continue\"),waypoint_motion([2, 0], 1, \"continue\"),waypoint_motion([-2, -2], 1, \"continue\")]"},
    {'Question': "Move slow to the left. You are at position [1, 1]", 'Answer': "[waypoint_motion([3, 1], 0.5, \"continue\")]"},
    {'Question': "Go home fast.", 'Answer': "[waypoint_motion([-5, -5], 2, \"continue\")]"},
    {'Question': "Touch the object. Object is at [-1, 1]", 'Answer': "[waypoint_motion([3, 1], 1, \"stop\")]"}, # tricky to give object position example in training data since it then thinks it knows the object position
    {'Question': "Move the object to the right. You are at position [1, 1]. Object is at [-1, -1]", 'Answer': "[waypoint_motion([1, -1],1, \"continue\"), waypoint_motion([-2, -1], 1, \"continue\")]"}, 
    ]

intro = '''You are a robot and you can listen and speak and you can move in 2 dimensions x and y, positive x is left. 
Your motion limits are from +5 to -5. 
Your velocity range is 0.5 to 2.
You have a touch sensor that reports 1 if you are touching something and 0 if not. 
There might be one object somewhere in your space.
You can do the following actions:
- waypoint_motion([x, y], velocity, touch_trigger), where x and y are the coordinates you want to go to and velocity is how fast you want to go there. and touch_trigger can be "stop" or "continue" depending on if you want to stop when you touch something or not.
- speak("text"), where text is the text you want to say.

'''