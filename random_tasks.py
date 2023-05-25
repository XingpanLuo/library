# 任务分配
import random

num1=1234
num2=1958
num3=2023
seed = num1 + num2 + num3

tasks = ["任务(1)", "任务(2)", "任务(3)"]
people = ["罗", "肖", "曾"]

random.seed(seed)
random.shuffle(tasks)

print("任务分配结果:")
for i in range(len(tasks)):
    print(people[i] + " -> " + tasks[i])