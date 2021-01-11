import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency


def create_percentage(df, column_name, column_rename, melt):
    '''
    INPUT
    df - pandas dataframe
    column_name - name of column fow which the percentage of entries will be found
    column_rename - how to rename the index of the new dataframe
    melt - when True created a dataframe with a column Gender that could be Man or Woman
           when False creates two columns one for Man and another one for Woman
    
    It creates a dataframe that contains the percentage of entries that correspond to a 'column_name' column and rows that
    correspond to Man or Woman. 
    '''
    study_df_women=(df[df['Gender']=='Woman'][column_name].value_counts()/len(df[df['Gender']=='Woman'][column_name])*100).reset_index()
    study_df_men = (df[df['Gender']=='Man'][column_name].value_counts()/len(df[df['Gender']=='Man'][column_name])*100).reset_index()
    study_df_women.rename(columns={'index': column_rename, column_name: 'Women'}, inplace=True)
    study_df_men.rename(columns={'index': column_rename, column_name: 'Men'}, inplace=True)
    study_df = pd.merge(study_df_women, study_df_men, on=column_rename )

    if melt == True:
        df_new = pd.melt(study_df, id_vars=[column_rename], value_vars=['Men','Women'], var_name='Gender')
    else:
        df_new = study_df

    return df_new

def create_frequency(df, column_name, list_field):
    '''
    INPUT
    df - pandas dataframe
    column_name - the column name from which it will search for the entries in list_field
    list_field - list that contains names of the categorical variables 

    OUTPUT
    table - contingency matrix
    
    Outputs a contingency table for the categorical variables in list_name
    for the classes Woman and Man
    '''

    table_w =[]
    table_m =[]
    for i in range(len(list_field)):
        table_w.append( len(df[(df[column_name]==list_field[i]) & 
                    ((df['Gender']=='Woman')) ]))
        table_m.append( len(df[(df[column_name]==list_field[i]) & 
               ((df['Gender']=='Man')) ]))
        table = [table_w,table_m ]
    
    return table

def show_values_on_bars(axs, h_v="v", space=0.3):
    '''
    INPUT
    axs - input boxplot
    h_v - vertical(v) or horizontal(h)
    space - how much space to leave after the bar
    
    
    Adds values of entries in boxplot
    '''
    def _show_on_single_plot(ax):
        if h_v == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height()
                value = round(p.get_height(),1)
                ax.text(_x, _y, value, ha="center", fontsize = 18) 
        elif h_v == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height() - float(space) / 4
                a_number = round(p.get_width(),1)
                value = "{}%".format(a_number)
                if a_number > 0:
                    ax.text(_x, _y, value, ha="left", fontsize = 18)
                else:
                    ax.text(_x + 5 * float(space), _y, value, ha="center", fontsize = 18)

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax)
    else:
        _show_on_single_plot(axs)
        
def plot(y_input, df):
    '''
    INPUT 
    y_input - input of y axis
    df - pandas dataframe
    
    Creates a boxplot with entries for Men and Women for a given input categorical variable y. 
    '''
    
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot()

    sns.set_color_codes("pastel")
    sns_t = sns.barplot(x="value", y=y_input, hue="Gender", data=df)
 
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
    INPUT
    table - contingency table, i.e. table that contains the observed frequencies in each category
    
    OUTPUT
    pvalue - p-value of the test, level of significance
    
    It perofrms chi-squared test on the input contingency table
    and returns the pvalue according to which the null
    hypothesis (HO) is accepted or rejected
    '''
    alpha = 0.05
    pvalue = chi2_contingency(table)[1]
    if pvalue <= alpha:
        print("The p value is: {}, i.e. smaller than the level of signficance p=0.05, thus the null hypothesis is rejected. ".format(pvalue))
    else:
        print("The p value is: {}, i.e. larger than the level of signficance p=0.05, thus the null hypothesis is accepted.".format(pvalue)) 
    return pvalue