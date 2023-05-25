# 任务分配
import random

num1=1
num2=2
num3=3
seed = num1 + num2 + num3

tasks = ["任务(1)", "任务(2)", "任务(3)"]
people = ["罗", "肖", "曾"]

random.seed(seed)
random.shuffle(tasks)

print("任务分配结果:")
for i in range(len(tasks)):
    print(people[i] + " -> " + tasks[i])