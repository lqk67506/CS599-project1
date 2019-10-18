import numpy as np
import csv
import random

# Function to calculate the Euler distance between two point


def distance_calculate(vec1, vec2):
    return np.sqrt(np.power(vec1[0]-vec2[0], 2) + np.power(vec1[1]-vec2[1], 2))

# Function to generate 5 random centers, to make sure the result is similar with the figure, the seed is gave out


def center_generator(pointers):
    centers = []
    counter = 0
    random.seed(122)
    while counter < 5:
        index = random.randint(0, 99)
        centers.append(pointers[index])
        counter += 1
    return centers

# K_mean function, return the final center for draw the figure. Because there are 10 center points on the figure,
# The value of K has been set to 10


def k_mean(pointers, centers):
    center_change = True
    # Keep running when the value of centers change
    while center_change:
        # Set loop flag to False
        center_change = False
        clusters = [[] for a in range(len(centers))]

        # Travel through all points and put them into best cluster
        for point in pointers:
            best_index = 0
            center_index = 0
            min_distance = 100

            # Travel through all centers to find the center that close to the point
            for center in centers:
                distance = distance_calculate(center, point)
                if distance < min_distance:
                    best_index = center_index
                    min_distance = distance
                center_index += 1
            clusters[best_index].append(point)

        # Set a list to store old centers
        temp = []
        index = 0
        while index < len(centers):
            temp.append(centers[index])
            index += 1

        # Update the centers according to the mean of cluster
        centers_index = 0
        for cluster in clusters:
            if len(cluster) > 0:
                cluster = np.array(cluster)
                x1 = np.mean(cluster[:, 0])
                x2 = np.mean(cluster[:, 1])
                centers[centers_index][0] = x1
                centers[centers_index][1] = x2
            centers_index += 1

        # Check whether the old centers are same with new centers, if so, end the loop, if not, change the loop flag
        # to True and start new loop round
        check_index = 0
        while check_index < len(centers):
            if temp[check_index][0] != centers[check_index][0] or temp[check_index][1] != centers[check_index][1]:
                center_change = True
            check_index += 1
    return centers

# Calculate the distance between every lattice point to centers, and mark lattices with true or false according to
# the value of center points


def lattice_print(x_new, centers):
    x_new_true = []
    x_new_false = []
    for lattice in x_new:
        min_dis = 100
        center_index = 0
        for center in centers:
            distance = distance_calculate(lattice, center)
            if distance < min_dis:
                min_dis = distance
                best_index = center_index
            center_index += 1
        if best_index < 5:
            x_new_true.append(lattice)
        else:
            x_new_false.append(lattice)
    x_new_true = np.array(x_new_true)
    x_new_false = np.array(x_new_false)
    return [x_new_true, x_new_false]

# Read csv files and put the data of them into a list which is easy to calculate


csv_x = csv.reader(open('x.csv', encoding='utf-8'))
list_x = []
for row_x in csv_x:
    if row_x[1] != 'V1':
        x1 = float(row_x[1])
        x2 = float(row_x[2])
        temp = np.array([x1, x2])
        list_x.append(temp)
csv_y = csv.reader(open('y.csv', encoding='utf-8'))
list_y = []
for row_y in csv_y:
    if row_y[1] != 'x':
        y = int(row_y[1])
        list_y.append(y)
csv_x = csv.reader(open('xnew.csv', encoding='utf-8'))
list_x_new = []
for row_x in csv_x:
    if row_x[1] != 'x1':
        x_new1 = float(row_x[1])
        x_new2 = float(row_x[2])
        temp = np.array([x_new1, x_new2])
        list_x_new.append(temp)
csv_prob = csv.reader(open('prob.csv'))
list_prob = []
for row_prob in csv_prob:
    if row_prob[1] != 'x':
        prob = row_prob[1]
        list_prob.append(prob)

# Run the function above and give out finial centers, training data with mark
x_true = []
x_false = []
index = 0
while index < 200:
    if list_y[index] == 0:
        x_false.append(list_x[index])
    elif list_y[index] == 1:
        x_true.append(list_x[index])
    index += 1
x_true = np.array(x_true)
x_false = np.array(x_false)
centers1 = center_generator(x_true)
centers2 = center_generator(x_false)
new_center1 = k_mean(x_true, centers1)
new_center2 = k_mean(x_false, centers2)

# Write the result of final centers into csv file so that Rstudio can read them and calculate
file4 = open("center_true.csv", 'a', encoding='utf-8')
file4.write("x1" + "," + "x2" + "," + "type" + "\n")
for point in new_center1:
    file4.write(str(point[0]) + "," + str(point[1]) + "," + str(1) + "\n")
file4.close()

file5 = open("center_false.csv", 'a', encoding='utf-8')
file5.write("x1" + "," + "x2" + "," + "type" + "\n")
for point in new_center2:
    file5.write(str(point[0]) + "," + str(point[1]) + "," + str(0) + "\n")
file5.close()

# Using final center to mark the lattice points
new_center1.extend(new_center2)
new_center1 = np.array(new_center1)

lattice_true = lattice_print(list_x_new, new_center1)[0]
lattice_false = lattice_print(list_x_new, new_center1)[1]

# Write other data into csv files
file = open("training_true.csv", 'a', encoding='utf-8')
file.write("x1" + "," + "x2" + "," + "type" + "\n")
for point in x_true:
    file.write(str(point[0]) + "," + str(point[1]) + "," + str(1) + "\n")
file.close()

file1 = open("training_false.csv", 'a', encoding='utf-8')
file1.write("x1" + "," + "x2" + "," + "type" + "\n")
for point in x_false:
    file1.write(str(point[0]) + "," + str(point[1]) + "," + str(0) + "\n")
file1.close()

file2 = open("lattice.csv", 'a', encoding='utf-8')
file2.write("x1" + "," + "x2" + "," + "type" + "\n")
for point in lattice_true:
    file2.write(str(point[0]) + "," + str(point[1]) + "," + str(1) + "\n")
for point in lattice_false:
    file2.write(str(point[0]) + "," + str(point[1]) + "," + str(0) + "\n")
file2.close()

file3 = open("lattice_prob.csv", 'a', encoding='utf-8')
file3.write("x1" + "," + "x2" + "," + "prob" + "\n")
index = 0
for point in list_x_new:
    file3.write(str(point[0]) + "," + str(point[1]) + "," + str(list_prob[index]) + "\n")
    index += 1
file3.close()
