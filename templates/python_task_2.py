import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
       
    unique_ids = sorted(set(df['id_start'].unique()) | set(df['id_end'].unique()))
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids)
    distance_matrix = distance_matrix.fillna(0)  # Initialize with zeros

   
    for index, row in df.iterrows():
        id_start, id_end, distance = row['id_start'], row['id_end'], row['distance']
        distance_matrix.at[id_start, id_end] += distance
        distance_matrix.at[id_end, id_start] += distance  # Ensure symmetry

    return distance_matrix

   


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
     
    pairs = []
    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                pairs.append((id_start, id_end))

    
    unrolled_df = pd.DataFrame(pairs, columns=['id_start', 'id_end'])

    
    unrolled_df['distance'] = unrolled_df.apply(lambda row: distance_matrix.at[row['id_start'], row['id_end']], axis=1)

    return unrolled_df




def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
       
    reference_rows = df[df['id_start'] == reference_value]

   
    if reference_rows.empty:
        return []

    # Calculate the average distance for the reference value
    average_distance = reference_rows['distance'].mean()

   
    threshold_lower = average_distance * 0.9
    threshold_upper = average_distance * 1.1
    within_threshold = df[(df['distance'] >= threshold_lower) & (df['distance'] <= threshold_upper) & (df['id_start'] != reference_value)]

  
    unique_ids_within_threshold = sorted(within_threshold['id_start'].unique())

    return unique_ids_within_threshold


result_list = find_ids_within_ten_percentage_threshold(unrolled_df, reference_value)
return result_list


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
        # Rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Add columns for toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        unrolled_df[vehicle_type] = unrolled_df['distance'] * rate_coefficient

    return unrolled_df

# Example usage:
# Assuming unrolled_df is the output from unroll_distance_matrix function
result_df_with_toll_rates = calculate_toll_rate(unrolled_df)
return result_df_with_toll_rates

    


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
      
    time_ranges = [
        {'start_time': time(0, 0, 0), 'end_time': time(10, 0, 0), 'weekday_factor': 0.8, 'weekend_factor': 0.7},
        {'start_time': time(10, 0, 0), 'end_time': time(18, 0, 0), 'weekday_factor': 1.2, 'weekend_factor': 0.7},
        {'start_time': time(18, 0, 0), 'end_time': time(23, 59, 59), 'weekday_factor': 0.8, 'weekend_factor': 0.7}
    ]

    dfs = []

   
    for time_range in time_ranges:
        # Apply weekday discount factor
        weekday_df = df.copy()
        weekday_df[['moto', 'car', 'rv', 'bus', 'truck']] *= time_range['weekday_factor']
        weekday_df['start_day'] = 'Monday'
        weekday_df['end_day'] = 'Sunday'
        weekday_df['start_time'] = time_range['start_time']
        weekday_df['end_time'] = time_range['end_time']
        dfs.append(weekday_df)

        
        weekend_df = df.copy()
        weekend_df[['moto', 'car', 'rv', 'bus', 'truck']] *= time_range['weekend_factor']
        weekend_df['start_day'] = 'Saturday'
        weekend_df['end_day'] = 'Sunday'
        weekend_df['start_time'] = time_range['start_time']
        weekend_df['end_time'] = time_range['end_time']
        dfs.append(weekend_df)

   
    result_df = pd.concat(dfs, ignore_index=True)

    return result_df


result_df_with_time_based_toll_rates = calculate_time_based_toll_rates(result_df_with_toll_rates)
return result_df_with_time_based_toll_rate

