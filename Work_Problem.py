# A gaming company uses some of its customers' features new level-based customer definitions (persona) create and
# segment segments according to these new customer definitions by creating new customers according to these segments.
# Estimating how much money the company can earn on average wants. For example: A 25-year-old male from Turkey who is
# an IOS user Determining how much the user can earn on average is wanted.

# Persona.csv data set includes the prices of products sold by an international game company and It contains some
# demographic information of the users who purchase the products. Data The set consists of records created in each
# sales transaction. What does this mean? The table is not deduplicated. In other words, a person with certain
# demographic characteristics The user may have made more than one purchase.

######################################## PROJECT TASKS ################################################

### MISSION 1 : Answer the questions

# Question 1 : Read the persona.csv file and show general information about the dataset

import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)

df = pd.read_csv(r"C:\Users\Mehmet\Desktop\Data Scientist\KuralTabanlıSınıflandırmaProje\persona.csv")

df.info()


# Question 2 : How many unique SOURCE are there? What are their frequencies?

df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# Question 3 : How many unique PRICEs are there?

df["PRICE"].nunique()

# Question 4 : How many sales were made from which PRICE?

df["PRICE"].value_counts()

# Question 5 : How many sales were made from which country?

df["COUNTRY"].value_counts()

# Question 6 : How much was earned from sales in total by country?

df.groupby("COUNTRY")["PRICE"].sum()

# Question 7 : What are the sales numbers by SOURCE types?

df["SOURCE"].value_counts()

# Question 8 : What are the PRICE averages by country?

df.groupby("COUNTRY")["PRICE"].mean()

# Question 9 : What are the PRICE averages according to SOURCEs?

df.groupby("SOURCE").agg({"PRICE": "mean"})

# Question 10 : What are the PRICE averages at the COUNTRY-SOURCE intersection?

df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})


### MISSION 2 : What are the average earnings at the intersection of COUNTRY, SOURCE, SEX, AGE?

df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE" : "mean"})


### MISSION 3 : Sort the output by PRICE :
# To better see the output in the previous question, apply the sort_values method in decreasing order of PRICE.
# Save the output as agg_df

agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values(by="PRICE", ascending=False)


### MISSION 4 : Convert the names in the index to variable names.

agg_df = agg_df.reset_index()


### MISSION 5 : Convert the age variable to a categorical variable and add it to agg_df
# Convert the numeric variable Age into a categorical variable
# For example: '0_18', '19_23', '24_30', '31_40', '41_70'

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0, 18, 23, 30, 40, 70], labels= ["0_18", "19_23", "24_30", "31_40", "41_70"])


### MISSION 6 : Define new level-based customers (personas)
# Define new level-based customers (personas) and add them to the data set as variables
# Name of the new variable to be added: customers_level_based
# You need to create the customers_level_based variable by combining the observations in the output you obtained in the previous question.

cols = [0, 1, 2, 5]
agg_df["customer_level_based"] = agg_df.iloc[:, cols].apply(lambda row: '_'.join(row), axis=1)
agg_df["customer_level_based"] = agg_df["customer_level_based"].str.upper()
agg_df = agg_df.groupby("customer_level_based").agg({"PRICE": "mean"})
agg_df = agg_df.reset_index()


### MISSION 7 : Divide new customers (personas) into segments
# Divide new customers (Example: USA_ANDROID_MALE_0_18) into 4 segments according to PRICE
# Add the segments to agg_df as variables with the name SEGMENT
# Describe the segments (Group by segments and get price mean, max, sum)

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels= ["D", "C", "B", "A"])


### MISSION 8 : Classify new customers and estimate how much income they can bring
# (The task was to find the class of a ready-made username. But I wrote a
# function that takes data from the user and finds it for each user)

def income_finder (dataframe):

    user_country = input("Country: ")[:3].upper()
    user_device = input("Android or ios: ").upper()
    user_sex = input("Male or Female :").upper()
    user_age = int(input("Age: "))
    if user_age <= 18:
        user_age = "0_18"
    elif 18 < user_age <= 23:
        user_age = "19_23"
    elif 23 < user_age <= 30:
        user_age = "24_30"
    elif 30 < user_age <= 40:
        user_age = "31_40"
    else:
        user_age = "41_70"

    user_info = [user_country, user_device, user_sex, user_age]

    new_user = '_'.join(word for word in user_info)

    filter = agg_df["customer_level_based"] == new_user

    if new_user in agg_df["customer_level_based"].values:
        print("Expected Income:", agg_df.loc[filter, "PRICE"].values[0])
        print("SEGMENT:", agg_df.loc[filter, "SEGMENT"].values[0])
    else:
        print("User Not Found!")















