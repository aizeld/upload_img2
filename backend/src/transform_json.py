import numpy as np
import json

def transform(data):
    avg_value = data.get("avg_ndvi", 0)
    by_1_100 = data.get("by_1_100", {})
    
  
    filtered_by_1_100 = {int(k): v for k, v in by_1_100.items() if k.isnumeric()}
    
   
    values = np.array(list(filtered_by_1_100.keys()), dtype=int)
    areas = np.array(list(filtered_by_1_100.values()), dtype=float)
    
   
    non_zero_indices = areas > 0
    filtered_values = values[non_zero_indices]
    filtered_areas = areas[non_zero_indices]
    distribution = [{"area": float(area), "value": int(value)} for value, area in zip(filtered_values, filtered_areas) if value >= 1]
    

    by_1_255 = normalize(filtered_by_1_100)

   
    normalized_values = np.array(list(by_1_255.keys()), dtype=int)
    normalized_areas = np.array(list(by_1_255.values()), dtype=float)
    
    if normalized_areas.size > 0:
    
        valid_indices = (normalized_areas > 0) & (normalized_areas < 254)
        valid_values = normalized_values[valid_indices]
        
    
        min_value = int(np.min(valid_values))  
        max_value = int(np.max(valid_values))  
        
        # Calculate homogenty using the formula
        homogeneity_index = (255 - (max_value - min_value)) / 255
        variability_values = [float(homogeneity_index), float(min_value), float(max_value)]
    else:
        variability_values = [None, None, None]


    result = {
        "metrics": {
            "avg_value": float(avg_value),
            "variability": variability_values,
            "distribution": distribution,
            "cloud_coverage": float(data["cloud_coverage"])  
        }
    }
    
    return result

def normalize(data):
    # Create a new dictionary for normalized values
    transformed_data = {}
    scale_factor = 255 / 100  # Scale factor to normalize the values to 0-255

    for i in range(255):
        original_index = i / scale_factor
        lower_index = int(np.floor(original_index))
        upper_index = lower_index + 1
        fractional_part = original_index - lower_index
        
        if lower_index < 1:
            transformed_data[i] = data[1]
        elif upper_index > 100:
            transformed_data[i] = data[100]
        else:
            lower_value = data[lower_index]
            upper_value = data[upper_index]
            interpolated_value = lower_value + fractional_part * (upper_value - lower_value)
            transformed_data[i] = interpolated_value

    
    return {int(k): float(v) for k, v in transformed_data.items()}


def extract_map_type(meta_filename: str) -> str:
    parts = meta_filename.split("_")
    return parts[2]

def extract_map_info(meta_filename: str) -> dict:

    parts = meta_filename.split("_")
    print(parts)
    map_info = {
        "version": 0,
        "satellite": parts[4][:3]  # Removing "_meta" from the end
    }
    return map_info