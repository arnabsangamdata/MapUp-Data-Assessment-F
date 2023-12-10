import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
        
    ids = sorted(set(df['id_1'].unique()) | set(df['id_2'].unique()))

    matrix = pd.DataFrame(np.zeros((len(ids), len(ids))), index=ids, columns=ids)

    
    for row in df.itertuples(index=False):
        matrix.at[row.id_1, row.id_2] = row.car
        matrix.at[row.id_2, row.id_1] = row.car

  
    np.fill_diagonal(matrix.values, 0)

    return matrix

result_matrix = generate_car_matrix(df)
return result_matrix




def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    

   
    data['car_type'] = pd.cut(data['car'], bins=[-float('inf'), 15, 25, float('inf')],
                              labels=['low', 'medium', 'high'], right=False)

    
    type_counts = data['car_type'].value_counts().to_dict()

   
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts
result = get_type_count(df)
return result

    


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
     
    bus_mean = df['bus'].mean()
    bus_indices = df[df['bus'] > 2 * bus_mean].index.tolist()
    bus_indices.sort()
    return bus_indices
result_indices = get_bus_indexes(df)
return result_indices

    


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
        truck_mean = df['truck'].mean()
    filtered_routes = df.groupby('route')['truck'].mean().reset_index()
    filtered_routes = filtered_routes[filtered_routes['truck'] > 7]['route'].tolist()

    filtered_routes.sort()

    return filtered_routes
result_routes = filter_routes(df)
return result_routes

 


def multiply_matrix(result_matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    
    matrix = result_matrix.copy()
    matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    matrix = matrix.round(1)

    return matrix

    


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    df['duration'] = (df['end_datetime'] - df['start_datetime']).dt.total_seconds()
    expected_duration = 24 * 60 * 60
    df['incorrect_timestamp'] = ((df['duration'] < expected_duration) |
                                  (df['start_datetime'].dt.day_name() != df['end_datetime'].dt.day_name()))
    result_series = df.groupby(['id', 'id_2'])['incorrect_timestamp'].any()
    df = df.drop(['start_datetime', 'end_datetime', 'duration', 'incorrect_timestamp'], axis=1)
  result_series = time_check(df)
  return result_series


