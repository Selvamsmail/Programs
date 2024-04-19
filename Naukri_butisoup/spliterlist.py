import pandas as pd 

def spliter():
    st = 0
    linksdf = pd.read_parquet('links.parquet')
    linksdf.drop_duplicates(inplace=True)
    linksdf.dropna(inplace=True)
    linksdf.reset_index(drop=True, inplace=True)
    end = linksdf.shape[0]
    split_count = 3

    # Calculate the step size for each split
    step = (end - st) // split_count

    # Initialize an empty list to store the splits
    splits = []

    # Generate the splits
    for i in range(split_count):
        start_split = st + i * step
        end_split = start_split + step
        # For the last split, make sure it includes the end value
        if i == split_count - 1:
            end_split = end
        splits.append([start_split, end_split])
    print(splits)
    return splits
splits = spliter()