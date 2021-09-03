import enum
import random
import json
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import copy
import math

from matplotlib.patches import Rectangle
from planar import BoundingBox


target_data = []
sensor_data_s1 = []
sensor_data_s2 = []
sensor_data_s3 = []
sensor_data_comb = []
sensor_data_TO = []
cost_trend = []


# Placement optimization for each type
target_dict = {}
placement_type_s1 = {}
placement_type_s2 = {}
placement_type_s3 = {}
placement_type_comb = {}
placement_TO_type = {}

target_dict_type = {}
placement_dict_type_s1 = {}
placement_dict_type_s2 = {}
placement_dict_type_s3 = {}
placement_dict_type_comb = {}
placement_dcit_TO_type = {}


class SensorType(enum.Enum):
    Type_s1 = 1  # Cost 300
    Type_s2 = 2  # Cost 170
    Type_s3 = 3  # Cost 65


class SensorRange(enum.Enum):
    Type_s1 = 100
    Type_s2 = 70
    Type_s3 = 30


class SensorCost(enum.Enum):
    Type_s1 = 300
    Type_s2 = 170
    Type_s3 = 65


class Target:
    def __init__(self, width, height, targetId):
        self.pos_x = random.randint(0, width)
        self.pos_y = random.randint(0, height)
        self.target_id = targetId
        self.coverage = 0
        self.coverage_list = []
        pass


class Sensor:

    def __init__(self, width, height, sensorType, sensorRange, sensorCost, sensorId):
        self.sensor_type = sensorType
        self.sensor_id = sensorId
        self.sensor_cost = sensorCost
        self.pos_x = random.randint(0, 500)
        self.pos_y = random.randint(0, 500)
        self.range = sensorRange
        self.coverage = 0
        self.coverage_list = []
        self.sensor_present = True
        self.sensor_area = round((math.pi * ((sensorRange)**2)), 2)
        self.used_status = True
        pass


class Layout:

    def __init__(self, width, height, sensorCount, targetCount, kCoverage):
        self.width = width
        self.height = height
        self.k = kCoverage
        self.sensor_count = sensorCount
        self.target_count = targetCount
        pass

    def generate_sensors(self, sensorType, combination, calcPlacement, targetDict):
        if ((calcPlacement == False) & (combination == False)):
            if sensorType == SensorType.Type_s1.value:
                for s1 in range(0, 8):
                    sensor_s1 = Sensor(self.width, self.height,
                                       sensorType, SensorRange.Type_s1.value, SensorCost.Type_s1.value, s1)
                    sensor_s1_pos = [sensor_s1.pos_x, sensor_s1.pos_y]
                    placement_type_s1[s1] = tuple(sensor_s1_pos)
                    placement_dict_type_s1[s1] = sensor_s1
                    sensor_data_s1.append(sensor_s1)
            if sensorType == SensorType.Type_s2.value:
                for s2 in range(0, 17):
                    sensor_s2 = Sensor(self.width, self.height,
                                       sensorType, SensorRange.Type_s2.value, SensorCost.Type_s2.value, s2)
                    sensor_s2_pos = [sensor_s2.pos_x, sensor_s2.pos_y]
                    placement_type_s2[s2] = tuple(sensor_s2_pos)
                    placement_dict_type_s2[s2] = sensor_s2
                    sensor_data_s2.append(sensor_s2)
            if sensorType == SensorType.Type_s3.value:
                for s3 in range(0, 200):
                    sensor_s3 = Sensor(self.width, self.height,
                                       sensorType, SensorRange.Type_s3.value, SensorCost.Type_s3.value, s3)
                    sensor_s3_pos = [sensor_s3.pos_x, sensor_s3.pos_y]
                    placement_type_s3[s3] = tuple(sensor_s3_pos)
                    placement_dict_type_s3[s3] = sensor_s3
                    sensor_data_s3.append(sensor_s3)
        elif combination == True:
            count_test = 0
            for s1 in range(0, 8):
                count_test = count_test+1
                sensor_s1 = Sensor(self.width, self.height,
                                   SensorType.Type_s1.value, SensorRange.Type_s1.value, SensorCost.Type_s1.value, count_test)
                sensor_s1_pos = [sensor_s1.pos_x, sensor_s1.pos_y]
                placement_type_comb[count_test] = tuple(sensor_s1_pos)
                placement_dict_type_comb[count_test] = sensor_s1
                sensor_data_comb.append(sensor_s1)
            for s2 in range(0, 17):
                count_test = count_test+1
                sensor_s2 = Sensor(self.width, self.height,
                                   SensorType.Type_s2.value, SensorRange.Type_s2.value, SensorCost.Type_s2.value, count_test)
                sensor_s2_pos = [sensor_s2.pos_x, sensor_s2.pos_y]
                placement_type_comb[count_test] = tuple(sensor_s2_pos)
                placement_dict_type_comb[count_test] = sensor_s2
                sensor_data_comb.append(sensor_s2)
            for s3 in range(0, 89):
                count_test = count_test+1
                sensor_s3 = Sensor(self.width, self.height,
                                   SensorType.Type_s3.value, SensorRange.Type_s3.value, SensorCost.Type_s3.value, count_test)
                sensor_s3_pos = [sensor_s3.pos_x, sensor_s3.pos_y]
                placement_type_comb[count_test] = tuple(sensor_s3_pos)
                placement_dict_type_comb[count_test] = sensor_s3
                sensor_data_comb.append(sensor_s3)
        elif calcPlacement == True:
            for key, value in targetDict.items():
                sensor1 = Sensor(self.width, self.height,
                                 SensorType.Type_s3.value, SensorRange.Type_s3.value, SensorCost.Type_s3.value, key)
                sensor1.pos_x = value.pos_x
                sensor1.pos_y = value.pos_y
                sensor1_pos = [value.pos_x, value.pos_y]
                placement_TO_type[key] = tuple(sensor1_pos)
                placement_dcit_TO_type[key] = sensor1
                sensor_data_TO.append(sensor1)
        pass

    def generate_targets(self):
        for a in range(0, self.target_count):
            target = Target(self.width, self.height, a)
            target_pos = [target.pos_x, target.pos_y]
            target_dict[a] = tuple(target_pos)
            target_dict_type[a] = target
            target_data.append(target)

    def print_location(self):
        for loc in target_data:
            print("TargetID: " + str(loc.target_id) + " Location X: " +
                  str(loc.pos_x) + " Location Y: " + str(loc.pos_y))

    def print_targetDict(self):
        target_display = json.dumps(target_dict)
        print(target_display)

    def print_sensorDict(self, sensor, combination, calcPlacement):
        if (combination == False) & (calcPlacement == False):
            if sensor == SensorType.Type_s1.value:
                sensor_display = json.dumps(placement_type_s1)
            if sensor == SensorType.Type_s2.value:
                sensor_display = json.dumps(placement_type_s2)
            if sensor == SensorType.Type_s3.value:
                sensor_display = json.dumps(placement_type_s2)
        elif combination == True:
            sensor_display = json.dumps(placement_type_comb)
        elif calcPlacement == True:
            sensor_display = json.dumps(placement_TO_type)
        print(sensor_display)

    def calculate_coverage(self, sensorDict, targeDict, finalCovList):
        for tD in targeDict.items():
            for sD in sensorDict.items():
                if sD[1].used_status == True:
                    if sD[1].sensor_present == True:
                        status = self.calculate_distance(tD[1], sD[1])
                        if status:
                            tD[1].coverage_list.append(
                                sD[0]) if sD[0] not in tD[1].coverage_list else tD[1].coverage_list
                            sD[1].coverage_list.append(
                                tD[0]) if tD[0] not in sD[1].coverage_list else sD[1].coverage_list
                    else:
                        if (sD[0] in tD[1].coverage_list) & (tD[0] in sD[1].coverage_list):
                            tD[1].coverage_list.remove(sD[0])
                            sD[1].coverage_list.remove(tD[0])
            tD[1].coverage = len(tD[1].coverage_list)
            sD[1].coverage = len(sD[1].coverage_list)
        if (finalCovList == True):
            count = 0
            final_covered = []
            for s in sensorDict.items():
                if s[1].sensor_present == True:
                    if count == 0:
                        count = count+1
                        final_covered = s[1].coverage_list
                    else:
                        final_covered = list(
                            set(s[1].coverage_list) | set(final_covered))
            return final_covered

    def sensor_opt(self, sensorDict, kCoverage):
        change_list = []
        for a in sensorDict.items():
            if a[1].coverage < kCoverage:
                change_list.append(a[1].sensor_id)
        return change_list

    def remove_unused(self, sensorDict, targetDict):
        checked_list = []
        for ranSensor in sensorDict.keys():
            if len(sensorDict[ranSensor].coverage_list) == 0:
                sensorDict[ranSensor].sensor_present = False
                sensorDict[ranSensor].used_status = False
                if ranSensor not in checked_list:
                    checked_list.append(ranSensor)
        remName = "RemovedSensors"
        print("Sensors not in use :" + str(len(checked_list)))
        generate_map(sensorDict, targetDict, remName, True, 'Valid Sensors')
        self.calculate_coverage(sensorDict, targetDict, False)
        print("Removed Cost :" + str(self.cost_function(sensorDict, targetDict)))
        pass

    def optmize_sa(self, sensorDict, targetDict):
        init_temp = 90
        final_temp = 10
        no_of_iterations = 0
        alpha = 0.5
        current_temp = init_temp
        cost_trend = []
        atleast = 0
        while current_temp > final_temp:
            no_of_iterations += 1
            self.calculate_coverage(sensorDict, targetDict, False)
            prev_cost = self.cost_function(sensorDict, targetDict)
            random_sensor = random.choice(list(sensorDict.keys()))
            if sensorDict[random_sensor].used_status == True:
                sensorDict[random_sensor].sensor_present = False
                cov_list = self.calculate_coverage(
                    sensorDict, targetDict, True)
                if (len(cov_list)/self.target_count)*100 >= 99:
                    new_cost = self.cost_function(sensorDict, targetDict)
                    cost_difference = (prev_cost - new_cost)
                    coverage_condition = True
                    for a in targetDict.items():
                        if len(a[1].coverage_list) <= self.k:
                            pass
                        else:
                            coverage_condition = False
                    if coverage_condition:
                        if cost_difference > 0:
                            atleast += 1
                            print("No of Iter_"+str(no_of_iterations) +
                                  "----"+str(new_cost))
                            cost_trend.append(new_cost)
                        else:
                            if random.uniform(0, 1) < math.exp(-cost_difference / current_temp):
                                sensorDict[random_sensor].sensor_present = True
                        current_temp -= alpha
                    else:
                        sensorDict[random_sensor].sensor_present = True
                        if ((no_of_iterations > 10000) & (atleast == 0)):
                            break
                else:
                    sensorDict[random_sensor].sensor_present = True
        if atleast == 0:
            print("Unable to optimize for coverage : "+str(self.k))
        else:
            saName = "After_SA"
            generate_graph(cost_trend, 'SA_Swap_Trend', 'SA Swap Trend', True)
            generate_map(sensorDict, targetDict, saName, True, 'SA Placement')
            print("Final Cost "+"----" +
                  str(self.cost_function(sensorDict, targetDict)))
        pass

    def optmize_cost_one(self, sensorDict, targetDict):
        checked_list = []
        step = 0
        for a in sensorDict.items():
            step = step + 1
            target_count = len(a[1].coverage_list)
            if a[1].sensor_id not in checked_list:
                if len(a[1].coverage_list) > self.k:
                    if a[1].sensor_type == SensorType.Type_s2.value:
                        dummySensor = copy.deepcopy(a[1])
                        newSensor = Sensor(self.width, self.height,
                                           SensorType.Type_s1.value, SensorRange.Type_s1.value, SensorCost.Type_s1.value, a[1].sensor_id)
                        newSensor.pos_x = a[1].pos_x
                        newSensor.pos_y = a[1].pos_y
                        self.update_sensor_type(
                            sensorDict, newSensor, a[1].sensor_id)
                    elif a[1].sensor_type == SensorType.Type_s3.value:
                        dummySensor = copy.deepcopy(a[1])
                        newSensor = Sensor(self.width, self.height,
                                           SensorType.Type_s3.value, SensorRange.Type_s3.value, SensorCost.Type_s3.value, a[1].sensor_id)
                        newSensor.pos_x = a[1].pos_x
                        newSensor.pos_y = a[1].pos_y
                        self.update_sensor_type(
                            sensorDict, newSensor, a[1].sensor_id)
                    while target_count > 0:
                        target_count = target_count - 1
                        if targetDict[a[1].coverage_list[target_count]].target_id != a[1].sensor_id:
                            if self.calculate_distance(targetDict[a[1].coverage_list[target_count]], a[1]):
                                sensorDict[a[1].coverage_list[target_count]
                                           ].sensor_present = False
                                checked_list.append(
                                    a[1].coverage_list[target_count])
                                nameMap = "Layout_"+str(step)+"_map"+".png"
                                generate_map(
                                    sensorDict, targetDict, nameMap, False)
                                self.calculate_coverage(
                                    sensorDict, targetDict, False)
                                print("M1_"+str(step)+"-------"+str(self.cost_function(
                                    sensorDict, targetDict)))
                            else:
                                a[1] = copy.deepcopy(dummySensor)

        pass

    def optimize_cost_sa_swap(self, sensorDict, targetDict):
        initial_temp = 90
        final_temp = 0.1
        no_of_iterations = 0
        alpha = 0.25
        current_temp = initial_temp
        cost_trend = []
        atleast = 0
        while current_temp > final_temp:
            no_of_iterations += 1
            self.calculate_coverage(sensorDict, targetDict, False)
            prev_cost = self.cost_function(sensorDict, targetDict)
            random_sensor_one = random.choice(list(sensorDict.keys()))
            random_sensor_two = random.choice(list(sensorDict.keys()))
            if sensorDict[random_sensor_one].range != sensorDict[random_sensor_two].range:
                self.generate_swap(
                    sensorDict, targetDict, random_sensor_one, random_sensor_two)
                cov_list = self.calculate_coverage(
                    sensorDict, targetDict, True)
                if (len(cov_list)/self.target_count)*100 > 90:
                    new_cost = self.cost_function(sensorDict, targetDict)
                    cost_diff = (prev_cost - new_cost)
                    coverage_condition = True
                    for a in targetDict.items():
                        if len(a[1].coverage_list) <= self.k:
                            pass
                        else:
                            coverage_condition = False
                    if coverage_condition:
                        if cost_diff > 0:
                            atleast += 1
                            print("No of Iter_"+str(no_of_iterations) +
                                  "----"+str(new_cost))
                            cost_trend.append(new_cost)
                        else:
                            if random.uniform(0, 1) < math.exp(-cost_diff / current_temp):
                                pass
                            else:
                                self.generate_swap(
                                    sensorDict, targetDict, random_sensor_two, random_sensor_one)
                        current_temp -= alpha
                    else:
                        self.generate_swap(
                            sensorDict, targetDict, random_sensor_two, random_sensor_one)
                        if ((no_of_iterations > 10000) & (atleast == 0)):
                            break
                        pass
                else:
                    self.generate_swap(
                        sensorDict, targetDict, random_sensor_two, random_sensor_one)
                    pass
        if atleast == 0:
            print("Unable to optimize by swap for coverage : "+str(self.k))
            saTwoName = "After_SA_Swap"
            generate_map(sensorDict, targetDict, saTwoName,
                         True, 'SA Swap unsuccessful')
            print("Final Cost "+"----" +
                  str(self.cost_function(sensorDict, targetDict)))
        else:
            saName = "After_SA_Swap"
            generate_map(sensorDict, targetDict, saName,
                         True, 'SA Swap Placement')
            generate_graph(cost_trend, 'SA_Swap_Trend', 'SA Swap Trend', True)
            print("Final Cost "+"----" +
                  str(self.cost_function(sensorDict, targetDict)))
        pass

    def cost_function(self, sensorDict, targetDict):
        coverage_cost = 0
        for tD in targetDict.items():
            for a in tD[1].coverage_list:
                if sensorDict[a].sensor_present == True:
                    coverage_cost = coverage_cost + sensorDict[a].sensor_cost
        return coverage_cost

    def calculate_distance(self, target, sensor):
        isCovered = False
        dist = math.sqrt(((target.pos_x - sensor.pos_x)**2) +
                         ((target.pos_y - sensor.pos_y)**2))
        if dist <= sensor.range:
            isCovered = True
            return isCovered
        else:
            return isCovered

    def coverage_ration(self, finalList):
        return len(finalList/self.k)

    def update_sensor_type(self, sensorDict, newSensor, keyVal):
        sensorDict[keyVal] = copy.deepcopy(newSensor)
        pass

    def generate_swap(self, sensorDict, targetDict, keyOne, keyTwo):
        temp_x = sensorDict[keyOne].pos_x
        temp_y = sensorDict[keyOne].pos_y
        temp_covList = []

        sensorDict[keyOne].pos_x = sensorDict[keyTwo].pos_x
        sensorDict[keyOne].pos_y = sensorDict[keyTwo].pos_y
        sensorDict[keyOne].coverage_list = []

        sensorDict[keyTwo].pos_x = temp_x
        sensorDict[keyTwo].pos_y = temp_y
        sensorDict[keyTwo].coverage_list = temp_covList

        self.calculate_coverage(
            sensorDict, targetDict, False)
        pass


def generate_graph(costTrend, name, titleName, showGraph):
    x = list(range(0, len(costTrend)))
    y = costTrend
    plt.plot(x, y)

    plt.xlabel('Iterations')
    plt.ylabel('Cost of the Network')
    plt.title(titleName)
    plt.savefig(name, bbox_inches='tight', dpi=150)
    if showGraph == True:
        plt.show()
    pass


def generate_map(sensorDict, targetDict, name, showMap, titleName):

    plt.axis([0, 500, 0, 500])
    plt.clf()
    plt.axis("equal")

    x_pos_target = []
    y_pos_target = []
    x_pos_sens = []
    y_pos_sens = []
    sens_range = []
    sens_ids = []
    target_ids = []
    bbox_list = []

    for a in targetDict.items():
        x_pos_target.append(a[1].pos_x)
        y_pos_target.append(a[1].pos_y)
        bbox_list.append(tuple([a[1].pos_x, a[1].pos_y]))
        target_ids.append(a[1].target_id)
    x_pos_target = np.asarray(x_pos_target)
    y_pos_target = np.asarray(y_pos_target)

    c = []
    for b in sensorDict.items():
        if b[1].sensor_present == True:
            x_pos_sens.append(b[1].pos_x)
            y_pos_sens.append(b[1].pos_y)
            sens_range.append(b[1].range)
            sens_ids.append(b[1].sensor_id)
            if ((b[1].sensor_type == SensorType.Type_s1.value) & (b[1].sensor_present == True)):
                c.append(plt.Circle(
                    (b[1].pos_x, b[1].pos_y), radius=b[1].range, alpha=0.35, color='blue', label="S1"))
            if ((b[1].sensor_type == SensorType.Type_s2.value) & (b[1].sensor_present == True)):
                c.append(plt.Circle(
                    (b[1].pos_x, b[1].pos_y), radius=b[1].range, alpha=0.35, color='green', label="S2"))
            if ((b[1].sensor_type == SensorType.Type_s3.value) & (b[1].sensor_present == True)):
                c.append(plt.Circle(
                    (b[1].pos_x, b[1].pos_y), radius=b[1].range, alpha=0.35, color='orange', label="S3"))
    x_pos_sens = np.asarray(x_pos_sens)
    y_pos_sens = np.asarray(y_pos_sens)
    sens_range = np.asarray(sens_range)
    sens_ids = np.asarray(sens_ids)

    # plt.scatter(
    #     x=x_pos_sens,
    #     y=y_pos_sens,
    #     s=sens_range*70,
    #     alpha=0.3,
    # )
    # for i, txt in enumerate(sens_ids):
    #     plt.annotate(
    #         txt, (x_pos_sens[i], y_pos_sens[i]), fontsize=10, color='red')

    for a in c:
        plt.gca().add_artist(a)

    for i, txt in enumerate(sens_ids):
        plt.annotate(
            txt, (x_pos_sens[i], y_pos_sens[i]), fontsize=10, color='red')

    plt.scatter(
        x=x_pos_target,
        y=y_pos_target,
        marker="*",
    )
    for i, txt in enumerate(target_ids):
        plt.annotate(
            txt, (x_pos_target[i]+0.25, y_pos_target[i]), fontsize=10)

    bbox = BoundingBox(bbox_list)
    plt.title(titleName)
    plt.gca().add_patch(Rectangle((bbox.min_point.x, bbox.min_point.y),
                                  bbox.width, bbox.height, edgecolor='red', facecolor='none', lw=2))

    plt.savefig(name, bbox_inches='tight', dpi=150)
    if showMap == True:
        plt.show()


def main():
    random.seed(2)
    sensor_layout = Layout(500, 500, 600, 17, 20)

    sensor_layout.generate_targets()
    # sensor_layout.print_location()
    print("#######################The Target positions##################################")
    sensor_layout.print_targetDict()
    print("#############################################################################")

    # For a Combination of sensors

    sensor_layout.generate_sensors(1, True, False, target_dict_type)
    print("########################The Sensor positions#################################")
    sensor_layout.print_sensorDict(1, True, False)
    print("#############################################################################")
    finalList = sensor_layout.calculate_coverage(
        placement_dict_type_comb, target_dict_type, True)
    print("#######################List of targets covered###############################")
    print(finalList)
    print("#############################################################################")
    generate_map(placement_dict_type_comb,
                 target_dict_type, 'Layout_First.png', True, 'Initial Random Placement')
    cost_of_ntwrk = sensor_layout.cost_function(
        placement_dict_type_comb, target_dict_type)
    print("########################Cost of the Network##################################")
    print(cost_of_ntwrk)
    print("#############################################################################")
    print("------------------------Remove sensors not used------------------------------")
    sensor_layout.remove_unused(placement_dict_type_comb, target_dict_type)
    print("-----------------------------------------------------------------------------")
    print("------------------------Simulated Annealing----------------------------------")
    sensor_layout.optmize_sa(placement_dict_type_comb, target_dict_type)
    #print("------------------------Simulated Annealing -2-------------------------------")
    # sensor_layout.optimize_cost_sa_swap(
    # placement_dict_type_comb, target_dict_type)

    # Not used
    # For sensors of a particular type at random location

    # sensor_layout.generate_sensors(1, False, False)
    # sensor_layout.print_sensorDict(1, False, False)
    # finalList = sensor_layout.calculate_coverage(
    #     placement_dict_type_s1, target_dict_type, True)

    # print(finalList)
    # sensor_layout.generate_map(placement_dict_type_s1, target_dict_type)

    # For sensor of type 1 near each targets
    # sensor_layout.generate_sensors(1, False, True, target_dict_type)
    # print("########################The Sensor positions#################################")
    # sensor_layout.print_sensorDict(1, False, True)
    # print("#############################################################################")
    # finalList = sensor_layout.calculate_coverage(
    #     placement_dcit_TO_type, target_dict_type, True)
    # print("#######################List of targets covered###############################")
    # print(finalList)
    # print("#############################################################################")
    # generate_map(placement_dcit_TO_type, target_dict_type,
    #              'Layout_First.png', True)
    # cost_of_ntwrk = sensor_layout.cost_function(
    #     placement_dcit_TO_type, target_dict_type)
    # print("########################Cost of the Network##################################")
    # print(cost_of_ntwrk)
    # print("#############################################################################")
    # print("-------------Method: 1-------Lets optimize-----------------------------------")
    # sensor_layout.optmize_cost_one(placement_dcit_TO_type, target_dict_type)
    # print("-------------Method: 2-------Lets optimize-----------------------------------")
    # sensor_layout.optimize_cost_two(
    #     placement_dcit_TO_type, target_dict_type, 1)


if __name__ == '__main__':
    main()
