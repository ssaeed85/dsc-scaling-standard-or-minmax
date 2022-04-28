import pandas as pd
import matplotlib.pyplot as plt

# Color swatches
bToG = ['#0300c3', '#042492', '#053b83', '#055274', '#05616a',
          '#067a59', '#068c4d', '#07ad37', '#08c626', '#09ff00']
yToR = ['#fcb045', '#fc8439', '#fc5e2f', '#fc4227', '#fd1d1d']


def colInfo(col):
    """
    Helper function to print out information regarding a pandas Series (DataFrame column)
    
    col = pd.Series
    
    float: bar plot
    int: histogram plot
    object: bar plot of top 10 occurcences. If number of itmes > 15, plot additional bottom 5 occurences
    """
    len_Col = col.shape[0]
    num_zeroes = (col == 0).sum()
    num_missing = col.isna().sum()
    mean = 0
    median = 0
    uniques = len(col.unique())
    try:
        num_unknowns = (col.map(lambda x: x.lower() in ['unknown', ' ', '']).sum())
    except:
        num_unknowns = 0

    try:
        mean = col.mean()
        median = col.median()
    except:
        mean = 0
        median = 0

    data = [
        ['Zeroes',  f'{num_zeroes:,}',  f'{(num_zeroes/len_Col *100):.2f} %'],
        ['Missing', f'{num_missing:,}',  f'{(num_missing/len_Col *100):.2f} %'],
        ['Unknown', f'{num_unknowns:,}',
            f'{(num_unknowns/len_Col *100):.2f} %'],
        ['Uniques', f'{uniques:,}', f'{(uniques/len_Col *100):.2f} %'],
        ['Mean', f'{mean:.2f}', '-'],
        ['Median', f'{median:.2f}', '-'],
    ]
    
    info_table = pd.DataFrame(data, columns=['', 'Number', 'Percentage']).set_index('').style.set_caption("Table Info")
    
    #Creating Value Count Table
    vCountNum = col.value_counts()
    vCountPct = col.value_counts(normalize=True)*100
    vCountNum.name = 'Value Count'
    vCountPct.name = '% Value Count'
    
    #Limiting Table to top 10
    value_count_table = pd.concat([vCountNum,vCountPct], axis=1)
    value_count_table = value_count_table.iloc[:10].style.set_caption("Top 10 Value Count Info")
    
    # Display Tables as Panda DataFrames
    display(info_table,value_count_table)

    # Display plots depending upon datatype
    if col.dtype == 'float64':
        fig, ax = plt.subplots(figsize=(15, 8))
        plt.plot(col)
        plt.axhline(y=mean, color='r', linestyle='-.', label='Mean')
        plt.axhline(y=median, color='b', linestyle='-.', label='Median')
        plt.title('Bar plot: '+col.name)
        plt.legend()
        plt.ylabel(col.name)

    elif col.dtype == 'int64':
        fig, ax = plt.subplots(figsize=(15, 8))
        plt.hist(col)
        plt.title('Histogram plot: '+col.name)
        plt.ylabel(col.name)
        
        if len(col.value_counts()) < 30:
            fig, ax = plt.subplots(figsize=(15, 8))
            col.value_counts().iloc[:10].plot(kind='bar', color = bToG)
            plt.title('Frequency of top 10: '+col.name)
            plt.ylabel(col.name)
    
    elif col.dtype == 'O':
        fig, ax = plt.subplots(figsize=(15, 8))
        col.value_counts().iloc[:10].plot(kind='bar', color = bToG)
        plt.title('Frequency of top 10: '+col.name)
        plt.ylabel(col.name)
        
        if len(col.value_counts()) > 15:
            fig, ax = plt.subplots(figsize=(15, 8))
            col.value_counts().iloc[-5:].plot(kind='bar', color = yToR)
            plt.title('Frequency of bottom 5: '+col.name)
            plt.ylabel(col.name)
            
 