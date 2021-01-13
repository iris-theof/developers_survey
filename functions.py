import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency


def create_percentage(df_cur, column_name, column_rename, melt):
    '''
    It creates a new dataframe df_new that contains the percentage of entries that correspond to each value 
    of the categorical variable column_name appears. There is not calculated one percantage for each entry but
    two ones, one for women and one for  men.
    
    INPUT
    df_cur - pandas dataframe
    column_name - name of column (categorical variable) fow which the percentage of its one of each entries will
                  be calculated
    column_rename - how to rename the index of the new dataframe
    melt - True : Adds a categorical column Gender to the dataframe df_new that takes values Man or Woman
           False : creates two columns one for Man and another one for Woman
           
    OUTPUT
    df_new - new dataframe
    
    '''
    study_df_women = (df_cur[df_cur['Gender'] == 'Woman'][column_name].value_counts()/len(df_cur[df_cur['Gender'] == 'Woman'][column_name])*100).reset_index()
    study_df_men = (df_cur[df_cur['Gender'] == 'Man'][column_name].value_counts()/len(df_cur[df_cur['Gender'] == 'Man'][column_name])*100).reset_index()
    study_df_women.rename(columns={'index': column_rename, column_name: 'Women'}, inplace=True)
    study_df_men.rename(columns={'index': column_rename, column_name: 'Men'}, inplace=True)
    study_df = pd.merge(study_df_women, study_df_men, on=column_rename)

    if melt:
        df_new = pd.melt(study_df, id_vars=[column_rename], value_vars=['Men', 'Women'], var_name='Gender')
    else:
        df_new = study_df

    return df_new

def create_frequency(df_cur, column_name, list_field):
    '''
    Outputs a contingency table for the categorical variable column_name which takes values given in list_name
    and for the Gender variable which takes the values Woman or Man
    
    INPUT
    df_cur - pandas dataframe
    column_name - the one out of the two categorical variables from which the continengency matrix will be build
    list_field - list that contains values of the categorical variable column_name 

    OUTPUT
    table - contingency matrix
    '''

    table_w = []
    table_m = []
    for i in range(len(list_field)):
        table_w.append(len(df_cur[(df_cur[column_name] == list_field[i]) & 
                                  ((df_cur['Gender'] == 'Woman'))]))
        table_m.append(len(df_cur[(df_cur[column_name] == list_field[i]) & 
                                  ((df_cur['Gender'] == 'Man'))]))
        table = [table_w, table_m]
    
    return table

def show_values_on_bars(axs, h_v="v", space=0.3):
    '''
    Displays values of numerical entries in a barplot
    
    INPUT
    axs - input barplot
    h_v - vertical(v) or horizontal(h) positioning of the barplot, when
          v the categorical variable will be displayed in x axis
    space - how much space to leave after the bar
    '''
    
    if h_v == "v":
        for pos in axs.patches:
            _x = pos.get_x() + pos.get_width() / 2
            _y = pos.get_y() + pos.get_height()
            value = round(pos.get_height(), 1)
            axs.text(_x, _y, value, ha="center", fontsize=18) 
    elif h_v == "h":
        for pos in axs.patches:
            _x = pos.get_x() + pos.get_width() + float(space)
            _y = pos.get_y() + pos.get_height() - float(space) / 4
            a_number = round(pos.get_width(), 1)
            value = "{}%".format(a_number)
            if a_number > 0:
                axs.text(_x, _y, value, ha="left", fontsize=18)
            else:
                axs.text(_x + 5 * float(space), _y, value, ha="center", fontsize=18)
        
def plot(y_input, df_cur):
    '''
    Creates a barplot which plots for each entry of the categorical variable 'y_input' the corresponding
    numerical value the column 'value' of the dataframe df_cur.
    
    INPUT 
    y_input - categorical variable, each of its entries will correspond to a different bar
    df_cur - pandas dataframe
    '''
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot()

    sns.set_color_codes("pastel")
    sns_t = sns.barplot(x="value", y=y_input, hue="Gender", data=df_cur)
 
    plt.ylabel("")
    plt.xlabel("")

    ax.legend(loc='center right', frameon=False, prop={'size':20})

    show_values_on_bars(sns_t, "h", 0.3)
    sns.despine(left=True, bottom=True, right=True)
    sns_t.set(xticklabels=[])  
    ylabels = sns_t.get_yticklabels()
    sns_t.set_yticklabels(ylabels, fontsize=18)
    
    fig.savefig(y_input+'.png', bbox_inches='tight')

    plt.show()
    
    
def chi_squared_test(table):
    '''
    It perofrms chi-squared test on the input contingency table
    and returns the pvalue according to which the null
    hypothesis (HO) is accepted or rejected
    
    INPUT
    table - contingency table, i.e. table that contains the observed frequencies of the categorical variables
            from which we have built the contingency matrix
    
    OUTPUT
    pvalue - p-value of the test, level of significance
    '''
    
    alpha = 0.05
    pvalue = chi2_contingency(table)[1]
    if pvalue <= alpha:
        print("The p value is: {}, i.e. smaller than the level of signficance p=0.05, thus the null hypothesis is rejected. ".format(pvalue))
    else:
        print("The p value is: {}, i.e. larger than the level of signficance p=0.05, thus the null hypothesis is accepted.".format(pvalue)) 
    return pvalue
