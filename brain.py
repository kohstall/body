import cerebellum

cerebellum = cerebellum.Cerebellum()




#while 1:

    #wait for speech to text --> text

    #create prompt <-- text, current position, touch

    # ask LLM

    # exec output from LLM
    #speak 
    # or motion

    #for loop over list of commands:

        #cerebellum.move([0, 1], 1, "continue")
current_postion, touch = cerebellum.move([0, 5], 1, "continue")
print('[brain] done',current_postion, touch)
current_postion, touch = cerebellum.move([0, 0], 5, "stop")
print('[brain] done',current_postion, touch)
