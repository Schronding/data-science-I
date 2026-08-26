'''1. I believe that the reason why it is an anti-pattern is that simply
doing averages, doesn't really give you any useful information. 
Satisfaction, the cost, the number of articles or the code of the 
menu are all information that doesn't provide anything meaningful to
answer why the service is slow.'''

'''2. How can we measure the difference between the time of purchase
and delivery of food, in both turns of students, in order to minimize
the service time of the cafeterias in the ENES without hiring more
people? '''

'''3. A register in this table is equivalent to a purchase of food
in a cafeteria in the ENES. '''

'''4. 
`Codigo_Menu` it is cualitative and nominal, as each represents a number that doesn't
has any significant meaning with the other besides being IDs. 
`Num_Articulos` It is a cuantitative and discrete, as it is derived
from a limited set of elements (in this case positive integers)
`Satisfaccion_App` It is cualitative and ordinal, as there is a clear
hierarchy of what is a good level of satisfaction and what is a poor
level of satisfaction. 
'''

'''5.
The IDs are simply unique identifiers that are useful to access specific
records in the data, but they confer no real meaning, not even of 
precedence and procedence. In `Codigo_Menu` we have the same problem as 
the numbers in there are also identifiers. '''

data = [4, 5, 5, 6, 7, 8, 42]
mean = sum(data) / len(data)
print(mean)

def findMedian(array):
    mid_point = len(array) // 2
    if len(array) % 2 == 0:
        return (array[mid_point + 1] + array[mid_point]) // 2
    else:
        return array[mid_point]


print(findMedian(data))
'''6. I got 11.0 and 6.0. As the mean is more sensitive to outliers
it is worse in this scenario, as the outlier of 42 really weights
the average up. In this scenario the median is much more robust'''

'''7. The main two reasons that come to my mind are:
a) The order was ready but the student was distracted and didn't pick
it up
b) The people at the cafeteria forgot about the meal and realized only
after about 35 minutes. '''

'''8. I believe the best metric for this case is the standard deviation.
As it is in the same measured unit that the data (unlike the variance)
it provides us with a clear perspective of how spread out the values
are, particularly if it is a normal distribution (which more likely
will be considering the nature of cafeterias).'''

'''9. I would use the boxplot, as then it will be very clear that
the number 42 went very far away of what is usually the wait times
of the cafeteria. With more values it might even prove that the 
statement of the wait times being high is an exaggeration. 

The main visual difference between the histogram and the boxplot is
that in the histogram outliers are visible by going to the extremes
without a clear understanding of what is classified as an outlier,
while the boxplot with his "whiskers" shows you with points what
is an outlier.'''

'''10. One idea is that there might be a lot of simultaneous students
in the cafeteria at any given time, so even if the cafeterias were 
functioning at full speed, they might be overwhelmed by the sheer
number of simultaneous students.'''

'''11. If this were the case, we would indeed need back to step one
in order to register how many students were at the cafeteria at 
any given time, in order to see if the hypothesis of the cafeterias
being overwhelmed makes any sense or if we need to look for another
blind spot. '''