import random
import math
import datetime
import tkinter
import matplotlib.pyplot as plot

#since tk doesn't implicitly import messagebox
import tkinter.messagebox

#sets datetime to current value
now = datetime.datetime.now()
#calling "tk" as Tkinter module, and same for messagebox
tk = tkinter
tkMsg = tkinter.messagebox

"""--BEGIN CLASS--"""
#person class. Includes attributes of person, eg health, age, etc
class person():
    def __init__(self):
        self.personHealth = 100 #start off everyone with full health
        self.personAge = 0 #choose random age for person
        self.personProbDisease = 0 #probability of person catching disease
        #initial values are false for caughtDisease and isDead
        self.caughtDisease = False #checks whether the person has caught the disease
        self.isDead = False #checks whether is dead. If so, don't affect this person further
        self.ageDeath = 0 #sets time of death

#class for window to input
class simulator(tk.Frame):
    def __init__(self, master):
        #takes from master class
        super().__init__(master)
        self.pack()
        #creates widget on application
        self.createWidgets()        
        #allows user interaction

        #initial/input values
        self.numPersonInitial = 0
        self.coefDens = 0
        self.coefFood = 0

        #list for variables; used for displaying graph
        self.listVarTime = [] #stores time cycle, starting at 0
        self.listVarPeopleAlive = [] #list of number of people still alive
        self.listVarPeopleDisease = [] #list of number of people with disease
        self.listVarPeopleDeadTotal = [] #list of number of dead people

        #current/output values
        self.timeCycle = 0
        self.rateDisease = 0
        self.numPersonTotal = 0
        self.numPersonAlive = 0
        self.numPersonDisease = 0
        self.numPersonDeadTotal = 0
        self.numChildrenBorn = 0
        #contains list of living people
        self.listPerson = [] #create empty list of people living
        self.enableInput()

    def enableInput(self):
        #enable input fields & disable output!
        #used to prevent user from entering into output fields when entering
        self.entryInputPop.config(state="normal")
        self.entryInputCoefHouse.config(state="normal")
        self.entryInputCoefFood.config(state="normal")
        self.buttonInputCheck.config(state="normal")
        #this part disables output so it can't tampered!
        self.entryOutputYearCurrent.config(state="disabled")
        self.entryOutputPopCurrent.config(state="disabled")
        self.entryOutputPopBirth.config(state="disabled")
        self.entryOutputPopDisease.config(state="disabled")
        self.entryOutputDeadCurrent.config(state="disabled")
        self.entryOutputDeadTotal.config(state="disabled")
        self.textOutput.config(state="disabled")
        self.buttonShowStatsAll.config(state="disabled")
        self.buttonShowStatsDiseased.config(state="disabled")
        self.buttonShowStatsLiving.config(state="disabled")
        self.buttonCycleNext.config(state="disabled")
        
    #begin define output entries
    def createWidgets(self):
        #draws objects on application, forming GUI
        """---BEGIN INPUT"""
        self.labelIntroInput1 = tk.Label(self, text="Enter your population values in the boxes below.").pack(fill=tk.X, padx=4, pady=4)
        self.labelIntroInput2 = tk.Label(self, text="The number of people per house/with food & water must be less than initial population. Then, press 'Validate' to check input validity and process output.").pack(fill=tk.X, padx=4, pady=4)

        #field for input population
        self.packInputPop = tk.Frame(self)
        self.labelInputPop = tk.Label(self.packInputPop, text="Initial Population: ").pack(side="left")
        self.entryInputPop = tk.Entry(self.packInputPop)
        self.entryInputPop.pack(side="left", fill=tk.X, expand=tk.YES)
        self.packInputPop.pack(fill=tk.X, padx=4, pady = 4)

        #field for input coefficient of population density
        self.packInputCoefHouse = tk.Frame(self)
        self.labelInputCoefHouse = tk.Label(self.packInputCoefHouse, text="Number of people per house: ").pack(side="left")
        self.entryInputCoefHouse = tk.Entry(self.packInputCoefHouse)
        self.entryInputCoefHouse.pack(side="left", fill=tk.X, expand=tk.YES)
        self.packInputCoefHouse.pack(fill=tk.X, padx=4, pady = 4)

        #field for input coefficient of resource availability
        self.packInputCoefFood = tk.Frame(self)
        self.labelInputCoefFood = tk.Label(self.packInputCoefFood, text="Number of people with food & water: ").pack(side="left")
        self.entryInputCoefFood = tk.Entry(self.packInputCoefFood)
        self.entryInputCoefFood.pack(side="left", fill=tk.X, expand=tk.YES)
        self.packInputCoefFood.pack(fill=tk.X, padx=4, pady = 4)

        self.buttonInputCheck = tk.Button(self, text="Validate Input & Continue", command=self.checkInput)
        self.buttonInputCheck.pack(fill=tk.X, padx=4, pady = 4, expand=tk.YES)

        self.dividerInputOutput = tk.Label(self, text="***").pack(pady=5, fill=tk.X, expand=tk.YES)
        """---BEGIN OUTPUT"""
        #show current year
        self.packOutputYearCurrent = tk.Frame(self)
        self.labelOutputYearCurrent = tk.Label(self.packOutputYearCurrent, text="Current year: ").pack(side="left")
        self.entryOutputYearCurrent = tk.Entry(self.packOutputYearCurrent)
        self.entryOutputYearCurrent.pack(side="left", fill=tk.X, expand=tk.YES)
        self.packOutputYearCurrent.pack(fill=tk.X, padx=4, pady = 4)
        #self.entryOutputYearCurrent.insert(tk.END, "test")
        
        #entry field for outputting population current
        self.packOutputPopCurrent = tk.Frame(self)
        self.labelOutputPopCurrent = tk.Label(self.packOutputPopCurrent, text="Current Population: ").pack(side="left")
        self.entryOutputPopCurrent = tk.Entry(self.packOutputPopCurrent)
        self.entryOutputPopCurrent.pack(side="left", fill=tk.X, expand=tk.YES)
        self.packOutputPopCurrent.pack(fill=tk.X, padx=4, pady = 4)

        #output entry field show number of successful births this year
        self.packOutputPopBirth = tk.Frame(self)
        self.labelOutputPopBirth = tk.Label(self.packOutputPopBirth, text="Number of successful births: ").pack(side="left")
        self.entryOutputPopBirth = tk.Entry(self.packOutputPopBirth)
        self.entryOutputPopBirth.pack(side="left", fill=tk.X, expand=tk.YES)
        self.packOutputPopBirth.pack(fill=tk.X, padx=4, pady = 4)

        #field outputting number of diseased people
        self.packOutputPopDisease = tk.Frame(self)
        self.labelOutputPopDisease = tk.Label(self.packOutputPopDisease, text="Number of people with disease: ").pack(side="left")
        self.entryOutputPopDisease = tk.Entry(self.packOutputPopDisease)
        self.entryOutputPopDisease.pack(side="left", fill=tk.X, expand=tk.YES)
        self.packOutputPopDisease.pack(fill=tk.X, padx=4, pady = 4)

        #outputs death toll in single year
        self.packOutputDeadCurrent = tk.Frame(self)
        self.labelOutputDeadCurrent = tk.Label(self.packOutputDeadCurrent, text="Number of people who died: ").pack(side="left")
        self.entryOutputDeadCurrent = tk.Entry(self.packOutputDeadCurrent)
        self.entryOutputDeadCurrent.pack(side="left", fill=tk.X, expand=tk.YES)
        self.packOutputDeadCurrent.pack(fill=tk.X, padx=4, pady = 4)

        #output death total
        self.packOutputDeadTotal = tk.Frame(self)
        self.labelOutputDeadTotal = tk.Label(self.packOutputDeadTotal, text="Total death toll: ").pack(side="left")
        self.entryOutputDeadTotal = tk.Entry(self.packOutputDeadTotal)
        self.entryOutputDeadTotal.pack(side="left", fill=tk.X, expand=tk.YES)
        self.packOutputDeadTotal.pack(fill=tk.X, padx=4, pady = 4)

        #used for displaying detailed output
        self.textOutput = tk.Text(self)
        self.textOutput.pack(side="left", fill=tk.X, padx=4, pady = 4, expand=tk.YES)

        self.packOutputButtonDisplay = tk.Frame(self)
        self.buttonShowStatsAll = tk.Button(self.packOutputButtonDisplay, text="Display All People", command=self.showStatsAll)
        self.buttonShowStatsAll.pack(fill=tk.X, expand=tk.YES)
        self.buttonShowStatsDiseased = tk.Button(self.packOutputButtonDisplay, text="Display Only Diseased", command=self.showStatsDiseased)
        self.buttonShowStatsDiseased.pack(fill=tk.X, expand=tk.YES)
        self.buttonShowStatsLiving = tk.Button(self.packOutputButtonDisplay, text="Display Only Living", command=self.showStatsLiving)
        self.buttonShowStatsLiving.pack(fill=tk.X, expand=tk.YES)
        self.packOutputButtonDisplay.pack(fill=tk.X, padx=4, pady=4)

        self.packOutputButtonCycle = tk.Frame(self)
        self.buttonCycleNext = tk.Button(self.packOutputButtonCycle, text="Continue to Next Cycle", command=self.gotoCycleNext)
        self.buttonCycleNext.pack(side="bottom", fill=tk.X, expand=tk.YES, padx=4, pady=4)
        self.labelOutputButtonInstruction = tk.Label(self.packOutputButtonCycle, text="Press either buttons above to display different output filters, or press 'Continue' below to go to next year.")
        self.labelOutputButtonInstruction.pack(side="top", fill=tk.X, padx=4, pady=4)
        self.labelOutputButtonInstruction.config(wraplength=140)
        self.packOutputButtonCycle.pack(fill=tk.X)

        #button to display graph
        self.buttonGraphShow = tk.Button(self, text="Show Population\n Graph", command=self.graphShow)
        self.buttonGraphShow.pack(side="bottom", fill=tk.X, expand=tk.YES, padx=4, pady=4)
    #begin define input entries
    def checkInput(self):
        #initially, set variables to inputs
        #set input to respective entry boxes
        valInputPop = self.entryInputPop.get()        
        valInputCoefHouse = self.entryInputCoefHouse.get()
        valInputCoefFood = self.entryInputCoefFood.get()
        
        #level 1 of validation: check whether input is blank. If so, reject
        if (valInputPop == "") or (valInputCoefHouse == "") or (valInputCoefFood == ""):
            self.showInputErrorBlank()
        else:
            #level 2: check if input is numeric. If not, reject
            if (valInputPop.isnumeric() == False) or (valInputCoefHouse.isnumeric() == False) or (valInputCoefFood.isnumeric() == False):
                self.showInputErrorNumeric()
            else:
                #level 3: check if input is within range
                if (int(valInputCoefHouse) > int(valInputPop)) or (int(valInputCoefHouse) < 0) or (int(valInputCoefFood) > int(valInputPop)) or (int(valInputCoefFood) < 0):
                    self.showInputErrorRange(valInputPop)
                else:
                    #sets list's contents to obtained value
                    #this must be done if the variables are to be mutable
                    self.numPersonInitial= int(valInputPop)
                    self.coefDens= int(valInputCoefHouse)
                    self.coefFood= int(valInputCoefFood)
                    self.setInitialOutput()

    def showInputErrorBlank(self):
        #displays error for blank input
        tkMsg.showerror("Invalid Input", "One or more inputs are blank!\n Please check your inputs & try again.")
    def showInputErrorNumeric(self):
        #displays error for non-numeric input
        tkMsg.showerror("Invalid Input", "One or more inputs are non-numeric integers!\n Please check your inputs & try again.")
    def showInputErrorRange(self, valInputPop):
        #displays error for input out of range (population for disease & housing must be less than or equal to total population)
        tkMsg.showerror("Invalid Input", "One or more inputs are below zero, or larger than " + valInputPop + "!\n Please check your values & try again.")
    #end

    def setInitialOutput(self):
        #for cycle time of 0, when program initially runs
        self.resetValues()
        for count in range(0, self.numPersonInitial): #generate population as indicated by input
            self.listPerson.append(person())
            self.listPerson[count].personAge = random.randint(1, 100)
        self.disableInput() #disables input so it can't be used further!
        self.runCycle()
    
    def resetValues(self): #resets variables to its initial states
        self.listPerson.clear()
        self.coefDens = 0
        self.coefFood = 0
        self.timeCycle = 0
        self.rateDisease = 0
        self.numPersonTotal = 0
        self.numPersonAlive = 0
        self.numPersonDisease = 0
        self.numPersonDeadTotal = 0
        self.numChildrenBorn = 0
        #clear graph lists
        plot.close()
        self.listVarTime.clear()
        self.listVarPeopleAlive.clear()
        self.listVarPeopleDeadTotal.clear()
        self.listVarPeopleDisease.clear()

    def disableInput(self):
        #disables input fields to prevent further modification
        self.entryInputPop.config(state="disabled")
        self.entryInputCoefHouse.config(state="disabled")
        self.entryInputCoefFood.config(state="disabled")
        self.buttonInputCheck.config(state="disabled")
        #this part enables output so it can display output of program
        self.entryOutputYearCurrent.config(state="normal")
        self.entryOutputPopCurrent.config(state="normal")
        self.entryOutputPopBirth.config(state="normal")
        self.entryOutputPopDisease.config(state="normal")
        self.entryOutputDeadCurrent.config(state="normal")
        self.entryOutputDeadTotal.config(state="normal")
        self.textOutput.config(state="normal")
        self.buttonShowStatsAll.config(state="normal")
        self.buttonShowStatsDiseased.config(state="normal")
        self.buttonShowStatsLiving.config(state="normal")
        self.buttonCycleNext.config(state="normal")

    #calculate probability of disease to 
    def calculateProbDisease(self, count):
        #run cycle of disease & death
        if (self.listPerson[count].personAge < 16):
            return round(((90-self.rateDisease)/2)*math.cos((math.pi/(16-0))*self.listPerson[count].personAge)+((90+self.rateDisease)/2))
        elif (self.listPerson[count].personAge <= 25) and (self.listPerson[count].personAge >= 16):
            #since people around 16 to 25 are strongest, rate is minimum
            return round(self.rateDisease)
        elif (self.listPerson[count].personAge > 25) and (self.listPerson[count].personAge <= 100):
            return round((-(90-self.rateDisease)/2)*math.cos((math.pi/(100-25))*self.listPerson[count].personAge)+((90+self.rateDisease)/2))
        elif (self.listPerson[count].personAge > 100):
            #if person is very old, return maximum probability
            return 90
    
    #run time cycle
    def runCycle(self):
        numPersonDeadCurrent = 0 #resets value for every cycle
        #closes graph every time next cycle is initiated
        plot.close()
        #returns reproduced list
        self.listPerson = reproducePerson()
        #calculates rate of disease
        self.rateDisease = (self.coefDens / self.numPersonInitial) * (1 - (self.coefDens / self.numPersonInitial)) * 100
        #returns total number of people alive
        self.numPersonAlive = checkNumAlive()
        self.numPersonTotal = int(len(self.listPerson))
        # for every person who is alive
        for count in range(0, len(self.listPerson)):
            #if person within list is not dead
            if self.listPerson[count].isDead != True:
                #sets probability of person catching disease
                self.listPerson[count].personProbDisease = self.calculateProbDisease(count)
                #if person has not caught disease, and probability is low, catch disease
                if (self.listPerson[count].caughtDisease == False) and (random.randint(1, 100) <= self.listPerson[count].personProbDisease):
                    #sets person to infected
                    self.listPerson[count].caughtDisease = True
                    #increment number of people with disease
                    self.numPersonDisease += 1
                #if time is ticking, increment 1 year every cycle
                if (self.timeCycle > 0):
                    self.listPerson[count].personAge += 1
                    #if time ticks, and person has disease
                    if (self.listPerson[count].caughtDisease == True):
                        #subtract person's health by factor of his own probability
                        self.listPerson[count].personHealth += int(-50 * (self.listPerson[count].personProbDisease / 100))
                        #if health is <= 0, kill
                        if self.listPerson[count].personHealth <= 0: 
                            #sets person to dead
                            self.listPerson[count].isDead = True
                            #records age of death, adding the person age
                            self.listPerson[count].ageDeath = self.listPerson[count].personAge + self.timeCycle
                            #person no longer has disease (because he's dead)
                            self.listPerson[count].caughtDisease = False
                            #increases counter for dead people, and thus total deaths
                            numPersonDeadCurrent += 1
                            self.numPersonDeadTotal += 1
                            #subtracts number of people alive by 1
                            self.numPersonAlive -= 1
        #store variables to graph
        self.storeGraph()
        #if there are more dead people than total, display final results
        if self.numPersonDeadTotal >= self.numPersonTotal:
            self.outputAllDead(numPersonDeadCurrent)
        else: #otherwise, display output as normal
            self.outputStandardDisplay(numPersonDeadCurrent)
    
    def storeGraph(self): #stores variables to list, to be displayed in graph
        self.listVarTime.append(int(self.timeCycle))
        self.listVarPeopleAlive.append(int(self.numPersonAlive))
        self.listVarPeopleDisease.append(int(self.numPersonDisease))
        self.listVarPeopleDeadTotal.append(int(self.numPersonDeadTotal))

    #show basic abridged output    
    def outputStandardDisplay(self, numPersonDeadCurrent): #outputs standard values
        self.outputStandardSmall(numPersonDeadCurrent)
        self.showStatsAll()
    
    def outputStandardSmall(self, numPersonDeadCurrent):
        #clears fields first, then output
        self.entryOutputYearCurrent.delete(0, tk.END)
        self.entryOutputYearCurrent.insert(tk.END, str(int(now.year) + self.timeCycle))
        #shows output of population & stuff
        self.entryOutputPopCurrent.delete(0, tk.END)
        self.entryOutputPopCurrent.insert(tk.END, str(self.numPersonAlive))
        self.entryOutputPopBirth.delete(0, tk.END)
        self.entryOutputPopBirth.insert(tk.END, str(self.numChildrenBorn))
        self.entryOutputPopDisease.delete(0, tk.END)
        self.entryOutputPopDisease.insert(tk.END, str(self.numPersonDisease))
        self.entryOutputDeadCurrent.delete(0, tk.END)
        self.entryOutputDeadCurrent.insert(tk.END, str(numPersonDeadCurrent))
        self.entryOutputDeadTotal.delete(0, tk.END)
        self.entryOutputDeadTotal.insert(tk.END, str(self.numPersonDeadTotal)) 
        #show all stats in big text box, by default

    def outputAllDead(self, numPersonDeadCurrent):
        #if everyone is dead, output in big text box that everyone died, and thus ends the program
        self.outputStandardSmall(numPersonDeadCurrent)
        self.textOutput.delete(1.0,tk.END)
        self.textOutput.insert(tk.END, "All " + str(len(self.listPerson)) + " people have died.\n")
        self.textOutput.insert(tk.END, "Your disease took " + str(self.timeCycle) + " years to exterminate everyone.")
        #allow user to input, allowing the program to run more calculations
        self.enableInput()

    #show all stats, living or dead
    def showStatsAll(self):
        self.textOutput.delete(1.0,tk.END)
        for count in range(0, len(self.listPerson)):
            if self.listPerson[count].isDead == False:
                self.textOutput.insert(tk.END, str(count) + ": " + str(self.listPerson[count].personAge) + " years | Diseased: " + str(self.listPerson[count].caughtDisease) + " | Current Health: " + str(self.listPerson[count].personHealth) + "\n")
            else:
                self.textOutput.insert(tk.END, str(count) + ": Person has died at " + str(self.listPerson[count].ageDeath) + " years.\n")

    #show stats of only diseased people
    def showStatsDiseased(self):
        self.textOutput.delete(1.0,tk.END)
        for count in range(0, len(self.listPerson)):
            if self.listPerson[count].caughtDisease == True:
                self.textOutput.insert(tk.END, str(count) + ": " + str(self.listPerson[count].personAge) + " years | Current Health: " + str(self.listPerson[count].personHealth) + "\n")

    #show stats of living people
    def showStatsLiving(self):
        self.textOutput.delete(1.0,tk.END)
        for count in range(0, len(self.listPerson)):
            if self.listPerson[count].isDead == False:
                self.textOutput.insert(tk.END, str(count) + ": " + str(self.listPerson[count].personAge) + " years | Diseased: " + str(self.listPerson[count].caughtDisease) + " | Current Health: " + str(self.listPerson[count].personHealth) + "\n")
    
    #increments time cycle
    def gotoCycleNext(self):
        self.timeCycle += 1
        #also, runs next time cycle
        self.runCycle()    

    def graphShow(self):
        #declares subplots
        subPlot = plot.subplot()
        #draws titles & labels
        plot.title("Population vs Disease")
        plot.xlabel("Time Cycle (Years)")
        plot.ylabel("Population")
        #plots graphs
        subPlot.plot(self.listVarTime, self.listVarPeopleAlive, linestyle="-")
        subPlot.plot(self.listVarTime, self.listVarPeopleDisease, lineStyle=":")
        subPlot.plot(self.listVarTime, self.listVarPeopleDeadTotal, lineStyle="--")
        #creates legend
        plot.legend(("Living Population", "Diseased Population", "Dead Population"))
        #displays graph!
        plot.show()
"""--END CLASS--"""

"""--BEGIN FUNCTION--"""
#generates people to list, according to initial input, and returns list
def generatePeople():
    for count in range(0, 100):
        simulator.listPerson.append(person())
        simulator.listPerson[count].personAge = random.randint(1, 100)
    return simulator.listPerson

#returns number of people alive
def checkNumAlive():
    total = 0 #number of people alive, to be returned
    for count in range(0, len(simulator.listPerson)):
        if (simulator.listPerson[count].isDead == False):
            total += 1
    return total

def reproducePerson():
    numCouple = 0
    for count in range(0, len(simulator.listPerson)):
        #if person is not dead, is within age of fertility, and does not have ill-enough health, then person is reproducible
        if (simulator.listPerson[count].isDead == False) and (simulator.listPerson[count].personAge < 60) and (simulator.listPerson[count].personAge > 15) and (simulator.listPerson[count].personHealth > 50):
            numCouple += 1
    numCouple = int(round(numCouple / 2))
    simulator.numChildrenBorn = 0 #counts how many successful births had been done
    for count in range(0, numCouple): #generates a child per possible couple
        #since trying for a child have equal probability of success, 50/50 chance is used
        if (random.randint(1, 100) > 50):
            #if successful, a person is appended
            simulator.listPerson.append(person())
            simulator.listPerson[count].personAge = 0
            simulator.numChildrenBorn += 1
    return simulator.listPerson
"""--END FUNCTION--"""

rootTk = tkinter.Tk()
rootTk.wm_resizable(0,0) #prevents resizing
simulator = simulator(rootTk)
rootTk.title("Disease Simulator")
simulator.mainloop()
