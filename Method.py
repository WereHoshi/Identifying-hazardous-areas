import os
import sys
import traci

def init_sumo():
    sumoBinary = "sumo-gui"
    sumoCmd = [sumoBinary, "-c", "C:\\Windows\\System32\\2024-06-12-11-18-41\\osm.sumocfg"] #сюда загружать конфиг SUMO
    traci.start(sumoCmd)

def collect_data():
    data = {}
    for edge in traci.edge.getIDList():
        lane_count = traci.edge.getLaneNumber(edge)
        lane_ids = [f"{edge}_{i}" for i in range(lane_count)]
        length = sum(traci.lane.getLength(lane_id) for lane_id in lane_ids)
        if length == 0:
            continue
        vehicle_count = traci.edge.getLastStepVehicleNumber(edge)
        data[edge] = {
            'vehicle_count': vehicle_count,
            'length': length
        }
    return data

def calculate_danger_coefficient(data):
    danger_coefficients = {}
    for edge, info in data.items():
        density = info['vehicle_count'] / info['length']
        danger_coefficient = density
        danger_coefficients[edge] = danger_coefficient
    return danger_coefficients

def detect_dangerous_sections(danger_coefficients, threshold=0.6):
    dangerous_sections = {}
    for edge, coefficient in danger_coefficients.items():
        if coefficient > threshold:
            dangerous_sections[edge] = coefficient
    return dangerous_sections

def print_dangerous_sections(dangerous_sections):
    for edge, coefficient in dangerous_sections.items():
        print(f"Edge ID: {edge}, Danger Coefficient: {coefficient}")
        # Здесь можно добавить код для визуализации опасных участков на карте, если это поддерживается SUMO-GUI

def main():
    init_sumo()
    step = 0
    try:
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            data = collect_data()
            danger_coefficients = calculate_danger_coefficient(data)
            dangerous_sections = detect_dangerous_sections(danger_coefficients)
            print_dangerous_sections(dangerous_sections)
            step += 1
    except Exception as e:
        print("An error occurred:", e)
    finally:
        traci.close()

if __name__ == "__main__":
    main()
