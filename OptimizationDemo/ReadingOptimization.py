
# coding: utf-8

import Tkinter as tk
from gurobipy import *
from pulp import *
from itertools import compress #for boolean masking
import numpy as np
import pandas as pd
import re, timeit, datetime, tkMessageBox #might not need regular expressions anymore
import matplotlib.pyplot as plt

data = pd.read_csv('goodreads_library_export.csv')
#define my sets/technological coefficients 
#Ratings
data.reset_index(inplace=True)

data = pd.read_csv('goodreads_library_export.csv')
quarter = "2QFY16"
name = "Reading Optimization for %s" % quarter
hrs_wk = 15      #reading hours avail per week
wks = 13         #weeks per period (quarter)
read_speed = 80  #pages per hour

#hardcoding magic numbers
#Can build Tkinter UI to input
#mins and max numbers of book, by type
max_math = float('inf')
min_math = 2

max_hist = 2
min_hist = 1

max_phil = 1
min_phil = 1


#currently a minimum req'd percentage
percent_scifi = .3

#currently max percent already read
percent_read = .1
        
mins = [min_math, min_hist, min_phil]
maxs = [max_math, max_hist, max_phil]
pers = [percent_scifi, percent_read]
params = [hrs_wk, wks, read_speed]


def solveit(data, mins, maxs, pers, params, quarter):
    "Docstring for solveit function"
   
    ratings = data["Average Rating"].astype(float)
    my_ratings = data["My Rating"].astype(float)
    #data.shape

    #If I've rated a book, use my rating, not the average
    change = [0 if x > 0 else 1 for x in my_ratings]
    ratings = np.array(ratings * change)
    ratings = ratings + my_ratings

    ratings = ratings.to_dict()
    #Number of pages
    pages = data["Number of Pages"]
    pages = pages.to_dict()

    bookshelves = data['Bookshelves']
    math_books = bookshelves.isin(['math'])
    milhist_books = bookshelves.isin(['military-history'])
    phil_books = bookshelves.isin(['philosophy'])
    scifi_books = bookshelves.isin(['sci-fi'])
    read_books = data["Exclusive Shelf"].isin(['read'])
   
    p = pulp.LpProblem(quarter, pulp.LpMaximize)

    #init
    total_pages= ""
    total_books = ""
    total_math = ""
    total_phil = ""
    total_milhist =""
    per_scifi = ""
    per_read = ""
    dv = []
    
    
    #Sets and DVs
    for i in xrange(0, len(data)-1):
        #for rownum, row in data.iterrows():
        rownum = i + 1
        newDV = str(i)
        #binary decision variables for knapsack problem
        #relaxing the integer constraint could mean "read part/chapters of a book"
        newDV = pulp.LpVariable("x" + str(newDV), lowBound = 0, upBound = 1, cat= 'Integer')
        dv.append(newDV)
        
        
        total_pages   += dv[i] * pages[rownum]
        total_books   += (ratings[rownum] * pages[rownum]) * dv[i] 
       
        total_math    += math_books[rownum]    * dv[i] 
        total_phil    += (phil_books[rownum])    * dv[i] 
        total_milhist += (milhist_books[rownum]) * dv[i] 
    
        per_scifi += ((scifi_books[rownum])-(1-pers[0])) * dv[i] 
        per_read +=  ((read_books[rownum])-(1-pers[1]) ) * dv[i] 
    

    
    #Objective Function
    #defined as a utility function defined in units of "star-pages"
    p += total_books
 
    #constraints    
    #Limit page count to available reading time
    read_time_avail = params[0] * params[1] * params[2]
    p += (total_pages <= read_time_avail)
    
    #Hard limits on book numbers
    p += (maxs[0]  >= total_math    >= mins[0])
    p += (maxs[1]  >= total_milhist >= mins[1])
    p += (maxs[2]  >= total_phil    >= mins[2])

    #Proportional constraints
    p += LpConstraint(per_scifi, sense=1, name="Percent Scifi", rhs = 0) #pers[0] >= 0) 
#can I flag this in interface to <= or >=?
    p += LpConstraint(per_read, sense=-1, name="Percent Read" , rhs = 0) #pers[1] <= 0) 

    p.writeMPS("ReadingPlan%s.mps" % str(quarter))

    start = timeit.default_timer()
 #       results = p.solve(GLPK(msg=0))
    results = p.solve()
    gnutime=(timeit.default_timer() - start)
    printResults(p,gnutime)
    t= gnutime

    return t


def printResults(p,gnutime):
    
    print("Total Solver Time:" + str(gnutime))
    #error handling -- throw error? or message?
    #assert Results == pulp.LpStatusOptimal

    print("Status:" + str(LpStatus[p.status]))
    print("Optimal at:" + str(value(p.objective)))

    #print optimal solution
    print("Solution:\n")
    msg=""
    solution_mask =[]
    solution_count = 0

    for v in p.variables():
        if v.varValue != 0:
            msg = msg + (v.name + "=" + str(v.varValue) + "\n")
            solution_mask.append(True)
            solution_count += v.varValue
        else:
            solution_mask.append(False)
    #print(msg)
    #print(solution_count)
    #sol_titles = list(compress(data["Title"],solution_mask))
    sol_titles = [i for (i, v) in zip(data["Title"], solution_mask) if v]
    sol_msg = ('\n'.join(sol_titles))

    print(sol_msg)
    tkMessageBox.showinfo("Solution", sol_msg)
    return



        
solveit(data, mins, maxs, pers, params, quarter)










