# Diplomski

## TODO

- prey and predators are entities
- Only predators have hunger, preys must only survive
- each predator should have its own timer for hunger, instead of a global timer event
- cleanup the code and modularize it
- create a fitness function that works for both predators and preys
- repository is diplomski
- speed up the simulation by using number of steps instead of time and speed
- investigate how the network is performing, what it is doing and how it should be optimised


### 20.9
- preys must know if they are eaten  
- how will the network evolve? how do i know when prey die?-> try if all predators are dead, reset the simulation or give prey a lifespan if they aren't eaten by predators

- CLEAN UP THE CODE IT IS DISGUSTING

### 21.9
- predators now eat preys, preys disappear
- fixed the hunger timer
- preys now get rewarded for 
- trying to train both populations at the same time (this is called coevolution): I'm not sure this will work. I tried to add a different integer to the input based on which class the genome is,   but i have to check if this will work with neat, or if i will have to train them separately and then combine the trained neural networks
- alternative approach: 1. train predator on static prey 2. train prey on predator that constantly chases them 3. train predator on dynamic prey 4. train prey against multiple predators 4. combine into one world to observe results
