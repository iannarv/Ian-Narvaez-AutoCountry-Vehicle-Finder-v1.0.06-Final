import os
import json
import sys

def get_json_file_path():
    """
    Determine a safe location to store the vehicles JSON file
    """
    # Try multiple locations for writing the file
    possible_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'authorized_vehicles.json'),
        os.path.join(os.getcwd(), 'authorized_vehicles.json'),
        os.path.join(os.path.expanduser('~'), 'authorized_vehicles.json')
    ]
    
    for path in possible_paths:
        try:
            # Try to create/write to the file
            with open(path, 'a') as f:
                f.close()
            return path
        except (PermissionError, IOError):
            continue
    
    # If all attempts fail, use an in-memory list
    print("Warning: Unable to create a JSON file. Using in-memory vehicle list.")
    return None

def load_vehicles(filename=None):
    """
    Load authorized vehicles from a JSON file or use default list
    """
    # Default vehicle list
    default_vehicles = [
        {'id': 1, 'name': 'Ford F-150', 'category': 'Truck'},
        {'id': 2, 'name': 'Chevrolet Silverado', 'category': 'Truck'},
        {'id': 3, 'name': 'Tesla CyberTruck', 'category': 'Electric Truck'},
        {'id': 4, 'name': 'Toyota Tundra', 'category': 'Truck'},
        {'id': 5, 'name': 'Rivian R1T', 'category': 'Electric Truck'},
        {'id': 6, 'name': 'Ram 1500', 'category': 'Truck'}
    ]

    if filename is None:
        return default_vehicles
    
    try:
        # If file doesn't exist, create it with initial vehicles
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump(default_vehicles, f, indent=4)
        
        # Read vehicles from JSON file
        with open(filename, 'r') as f:
            vehicles = json.load(f)
        
        return vehicles
    
    except (PermissionError, IOError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file: {e}")
        return default_vehicles

def save_vehicles(vehicles, filename=None):
    """
    Save the current list of vehicles to the JSON file
    """
    if filename is None:
        # If no filename, we can't save
        return
    
    try:
        with open(filename, 'w') as f:
            json.dump(vehicles, f, indent=4)
    except (PermissionError, IOError) as e:
        print(f"Error saving to JSON file: {e}")

def generate_new_id(vehicles):
    """
    Generate a new unique ID for a vehicle
    """
    return max(vehicle['id'] for vehicle in vehicles) + 1 if vehicles else 1

def main():
    # Get a safe file path for JSON
    data_file_path = get_json_file_path()
    
    # Load vehicles from JSON file
    AllowedVehiclesList = load_vehicles(data_file_path)
    
    while True:
        try:
            # Display header with formatting
            print('********************************')
            print('AutoCountry Vehicle Finder v1.0')
            print('********************************')
            print('Please Enter the following number below from the following menu:\n')
            
            # Display Menu
            menu_options = [
                'PRINT all Authorized Vehicles',
                'SEARCH for Authorized Vehicle',
                'ADD Authorized Vehicle',
                'DELETE Authorized Vehicle',
                'Exit'
            ]
            
            for i, option in enumerate(menu_options, 1):
                print(f'{i}. {option}')
            
            print('********************************')
            
            # Get user choice
            choice = input("\nPlease select an option (1-5): ").strip()
            
            # Process user choice
            if choice == '1':
                print_vehicles(AllowedVehiclesList)
            elif choice == '2':
                search_vehicles(AllowedVehiclesList)
            elif choice == '3':
                result = add_vehicle(AllowedVehiclesList)
                if result:
                    AllowedVehiclesList = result
                    if data_file_path:
                        save_vehicles(AllowedVehiclesList, data_file_path)
            elif choice == '4':
                result = remove_vehicle(AllowedVehiclesList)
                if result:
                    AllowedVehiclesList = result
                    if data_file_path:
                        save_vehicles(AllowedVehiclesList, data_file_path)
            elif choice == '5':
                print("\nThank you for using the AutoCountry Vehicle Finder, good-bye!")
                break
            else:
                print("\nInvalid selection. Please try again.")
            
            # Pause and wait for any key press before next iteration
            input("\nPress Enter to continue...")
        
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            input("Press Enter to continue...")

def print_vehicles(vehicles):
    """
    Function to print authorized vehicles in the specified format
    """
    if not vehicles:
        print("No vehicles in the authorized list.")
        return
    
    print("The AutoCountry sales manager has authorized the purchase and selling of the following vehicles:")
    for vehicle in vehicles:
        print(f"ID: {vehicle['id']}, Name: {vehicle['name']}, Category: {vehicle['category']}")

def search_vehicles(vehicles):
    """
    Function to search for vehicles in the vehicles list
    """
    if not vehicles:
        print("No vehicles in the authorized list.")
        return
    
    # Get search query from user
    search_query = input("\nEnter the vehicle name to search: ").strip().lower()
    
    # Search for matching vehicles
    found_vehicles = [
        vehicle for vehicle in vehicles 
        if search_query in vehicle['name'].lower()
    ]
    
    if found_vehicles:
        print("\nVehicle(s) Found:")
        for vehicle in found_vehicles:
            print(f"ID: {vehicle['id']}, Name: {vehicle['name']}, Category: {vehicle['category']}")
    else:
        print("\nNo vehicle found. Please try another search.")
        print("Current Authorized Vehicles:")
        for vehicle in vehicles:
            print(f"- {vehicle['name']}")

def add_vehicle(vehicles):
    """
    Function to add a new vehicle to the vehicles list
    """
    # Prompt for new vehicle details
    new_vehicle_name = input("\nEnter the FULL name of the new vehicle to add: ").strip()
    new_vehicle_category = input("Enter the vehicle category: ").strip()
    
    # Validate input
    if not new_vehicle_name or not new_vehicle_category:
        print("\nError: Vehicle name and category cannot be empty.")
        input("\nPress Enter to continue...")
        return vehicles
    
    # Check if vehicle already exists
    if any(vehicle['name'].lower() == new_vehicle_name.lower() for vehicle in vehicles):
        print("\nError: This vehicle is already in the authorized list.")
        input("\nPress Enter to continue...")
    else:
        # Create new vehicle with unique ID
        new_vehicle = {
            'id': generate_new_id(vehicles),
            'name': new_vehicle_name,
            'category': new_vehicle_category
        }
        
        # Add the new vehicle to the list
        vehicles.append(new_vehicle)
        print(f"\nVehicle '{new_vehicle_name}' has been added to the authorized list.")
    
    return vehicles

def remove_vehicle(vehicles):
    """
    Function to remove a vehicle from the vehicles list
    """
    # Check if list is empty
    if not vehicles:
        print("\nNo vehicles to remove. The list is empty.")
        input("\nPress Enter to continue...")
        return vehicles
    
    # Print current list of vehicles
    print("\nCurrent Authorized Vehicles:")
    for vehicle in vehicles:
        print(f"ID: {vehicle['id']}, Name: {vehicle['name']}, Category: {vehicle['category']}")
    
    # Prompt for vehicle to remove
    remove_vehicle_id = input("\nEnter the ID of the vehicle you want to remove: ").strip()
    
    try:
        remove_vehicle_id = int(remove_vehicle_id)
        # Check if vehicle exists in the list
        vehicle_to_remove = next((vehicle for vehicle in vehicles if vehicle['id'] == remove_vehicle_id), None)
        
        if vehicle_to_remove:
            # Confirmation prompt
            confirm = input(f"Are you sure you want to remove \"{vehicle_to_remove['name']}\" from the Authorized Vehicles List? (yes/no): ").strip().lower()
            
            # Remove vehicle if confirmed
            if confirm == 'yes':
                vehicles = [vehicle for vehicle in vehicles if vehicle['id'] != remove_vehicle_id]
                print(f"\nVehicle '{vehicle_to_remove['name']}' has been removed from the authorized list.")
            else:
                print("\nVehicle removal cancelled.")
        else:
            print("\nError: Vehicle ID not found in the Authorized Vehicles List.")
    
    except ValueError:
        print("\nError: Please enter a valid vehicle ID.")
    
    input("\nPress Enter to continue...")
    return vehicles

# Run the main program
if __name__ == "__main__":
    main()