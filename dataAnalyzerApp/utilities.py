import pandas
def rangeData(collection):
    return max(collection) - min(collection)

def getQuantile(data_frame, rate):
    if rate == 1:
        q = 0.25
    elif rate == 2:
        q = 0.5
    elif rate == 3:
        q = 0.75
    else:
        raise ValueError("Rate should be 1,2 or 3.")
    
    return data_frame.quantile(q=q)

def getIQR(data_frame):
    return getQuantile(data_frame,3) - getQuantile(data_frame,1)

def summaryFiveNumbers(data_frame):
    return (min(data_frame.tolist()), getQuantile(data_frame,1), data_frame.median(), getQuantile(data_frame,3), max(data_frame.tolist()))

def isnum(x):
    symbols_ = ('nan', 'NaN', 'Nan', '?', '')
    if x in symbols_:
        x = float('nan')
    try:
        float(x)
        return True
    except ValueError:
        return False

def isColumnNumeric(dataframe, columns):
    numeric_cols = []
    for column in columns:
        col_flag = True
        list_col = dataframe[column].tolist()
        for element in list_col:
            if isnum(element) != True:
                col_flag = False
                break
        if col_flag == True:
            numeric_cols.append(column)

    return numeric_cols






