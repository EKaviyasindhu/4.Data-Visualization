import pandas as pd
import numpy as np

class Univariate():

    def quanQual(dataset):
        quan=[]
        qual=[]
        for columnName in dataset.columns:
            #print(columnName)
            if(dataset[columnName].dtype=='O'): #Alphabet O not zero
                #print("qual")
                qual.append(columnName)
            else:
                #print("quan")
                quan.append(columnName)
        return quan,qual

    #descriptive table
    def descriptive_Univariate(dataset, quan):
        #Creates Table, calculate Mean, Median, Mode and Percentile, IQR Values and Assign Vales to the respective rows and columns.
        descriptive = pd.DataFrame(index=["Mean", "Median", "Mode", "Q1:25%", "Q2:50%", "Q3:75%", "99%", "Q4:100%", 
                                          "IQR","1.5Rule", "Lesser", "Greater", "Min","Max", "Skew", "Kurtosis"], columns=quan) 
        for ColumnName in quan:
            descriptive[ColumnName]["Mean"] = dataset[ColumnName].mean() #Mean
            descriptive[ColumnName]["Median"] = dataset[ColumnName].median() #Median
            descriptive[ColumnName]["Mode"] = dataset[ColumnName].mode()[0] #Mode   
            
            #percentile
            descriptive[ColumnName]["Q1:25%"] = dataset.describe()[ColumnName]["25%"]
            descriptive[ColumnName]["Q2:50%"] = dataset.describe()[ColumnName]["50%"]
            descriptive[ColumnName]["Q3:75%"] = dataset.describe()[ColumnName]["75%"]
            descriptive[ColumnName]["99%"] = np.percentile(dataset[ColumnName], 99)
            descriptive[ColumnName]["Q4:100%"] = dataset.describe()[ColumnName]["max"]
            
            #Interquartile Range
            descriptive[ColumnName]["IQR"] = descriptive[ColumnName]["Q3:75%"] - descriptive[ColumnName]["Q1:25%"] # IQR=Q3-Q1
            descriptive[ColumnName]["1.5Rule"] = 1.5 * descriptive[ColumnName]["IQR"] # 1.5*IQR
            descriptive[ColumnName]["Lesser"] = descriptive[ColumnName]["Q1:25%"] - descriptive[ColumnName]["1.5Rule"] # Lesser Range = Q1-1.5*IQR
            descriptive[ColumnName]["Greater"] = descriptive[ColumnName]["Q3:75%"] + descriptive[ColumnName]["1.5Rule"] # Lesser Range = Q3+1.5*IQR
            descriptive[ColumnName]["Min"] = dataset[ColumnName].min()
            descriptive[ColumnName]["Max"] = dataset[ColumnName].max()
            descriptive[ColumnName]["Skew"] = dataset[ColumnName].skew()
            descriptive[ColumnName]["Kurtosis"] = dataset[ColumnName].kurtosis()
        return descriptive

    #Function for Finding Outliers
    def FindOutliers(descriptive, quan):
        Lesser = []
        Greater = []
        for ColumnName in quan:
            if (descriptive[ColumnName]["Min"] < descriptive[ColumnName]["Lesser"]):
                Lesser.append(ColumnName)
            if (descriptive[ColumnName]["Max"] > descriptive[ColumnName]["Greater"]):
                Greater.append(ColumnName)
        return Lesser, Greater

    #Function to Replace Outlier
    def ReplaceOutliers(dataset, descriptive, Lesser, Greater):
        for ColumnName in Lesser:
            dataset[ColumnName][dataset[ColumnName] < descriptive[ColumnName]["Lesser"]] = descriptive[ColumnName]["Lesser"]
        for ColumnName in Greater:
            dataset[ColumnName][dataset[ColumnName] > descriptive[ColumnName]["Greater"]] = descriptive[ColumnName]["Greater"]   
        return dataset

    #Frequency Table
    def FreqTable(dataset, columnName):
        FreqTable = pd.DataFrame(columns = ["Unique_Values", "Frequency","Relative_Frequency", "Cumsum"])
        FreqTable["Unique_Values"] = dataset[columnName].value_counts().index
        FreqTable["Frequency"] = dataset[columnName].value_counts().values
        NumRows = FreqTable.shape[0]        
        FreqTable["Relative_Frequency"] = (FreqTable["Frequency"] / NumRows)
        FreqTable["Cumsum"] = FreqTable["Relative_Frequency"].cumsum()
        return FreqTable
                