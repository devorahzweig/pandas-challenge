#!/usr/bin/env python
# coding: utf-8

# In[45]:


import os
import csv
import pandas as pd
import numpy as np
#Read the two files given
school_data = pd.read_csv("schools_complete.csv")
student_data = pd.read_csv("students_complete.csv")
#Merge the data from the two files
total_school = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])

#District Summary
#Find the total amount of unique schools and students
total_school_count = len(total_school["school_name"].unique())
total_student_count = total_school["Student ID"].count()
#Find the total budget
budget = total_school["budget"].sum()
budget_per_student = budget / total_student_count
#Find the average math and reading scores, 
average_math_score = total_school["math_score"].mean()
average_reading_score = total_school["reading_score"].mean()
#Finding the inidividual passing percentages
passing_math_count = total_school[(total_school["math_score"] >= 70)].count()["student_name"]
passing_math_percent = passing_math_count / float(total_student_count) * 100
passing_reading_count = total_school[(total_school["reading_score"] >= 70)].count()["student_name"]
passing_reading_percent = passing_reading_count / float(total_student_count) * 100
#Find the overall passing rate
overall_passing_rate = (average_math_score + average_reading_score) / 2
#Create a DataFrame to summarize key metrics about district
district_summary = pd.DataFrame({"Total Schools":[total_school_count], 
                                 "Total Students": [total_student_count], 
                                 "Total School Budget": [budget],
                                 "Per Student Budget": [budget_per_student],
                                 "Average Math Score": [average_math_score], 
                                 "Average Reading Score": [average_reading_score],
                                 "% Passing Math": [passing_math_percent],
                                 "% Passing Reading": [passing_reading_percent],
                                 "% Overall Passing": [overall_passing_rate]})
district_summary = district_summary[["Total Schools", "Total Students", "Total School Budget",
                                     "Per Student Budget","Average Math Score", "Average Reading Score",
                                     "% Passing Math", "% Passing Reading","% Overall Passing"]]

district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total School Budget"] = district_summary["Total School Budget"].map("${:,.2f}".format)
district_summary.head()


# In[46]:


#SchoolSummary
# Find School Type
school_types = school_data.set_index(["school_name"])["type"]
# Total student count
school_counts = total_school["school_name"].value_counts()
# Calculate the total school budget and per capita spending
school_budget = total_school.groupby(["school_name"]).mean()["budget"]
school_capita = school_budget / school_counts
# Average test scores
school_math = total_school.groupby(["school_name"]).mean()["math_score"]
school_reading = total_school.groupby(["school_name"]).mean()["reading_score"]
# Passing scores
passing_math = total_school[(total_school["math_score"] >= 70)]
passing_reading = total_school[(total_school["reading_score"] >= 70)]
percent_passing_math = passing_math.groupby(["school_name"]).count()["student_name"] / school_counts * 100
percent_passing_reading = passing_reading.groupby(["school_name"]).count()["student_name"] / school_counts * 100
overall_passing_rate = (percent_passing_math + percent_passing_reading) / 2
# Make a new data frame
school_summary = pd.DataFrame({"School Type": school_types,
                                   "Total Students": school_counts,
                                   "Total School Budget": school_budget,
                                   "Per Student Budget": school_capita,
                                   "Average Math Score": school_math,
                                   "Average Reading Score": school_reading,
                                   "% Passing Math": percent_passing_math,
                                   "% Passing Reading": percent_passing_reading,
                                   "% Overall Passing Rate": overall_passing_rate})
school_summary = school_summary[["School Type", "Total Students", "Total School Budget", "Per Student Budget",
                                         "Average Math Score", "Average Reading Score", 
                                         "% Passing Math", "% Passing Reading", 
                                         "% Overall Passing Rate"]]
school_summary["Total School Budget"] = school_summary["Total School Budget"].map("${:,.2f}".format)
school_summary["Per Student Budget"] = school_summary["Per Student Budget"].map("${:,.2f}".format)

# Display the data frame
school_summary.head()


# In[47]:


#Highest-Performing Schools
highest_schools = school_summary.sort_values(["% Overall Passing Rate"], ascending=False)
highest_schools.head()


# In[48]:


#Lowest-Performing Schools
lowest_schools = school_summary.sort_values(["% Overall Passing Rate"], ascending=True)
lowest_schools.head()


# In[49]:


#Math Scores by Grade
#Data series by grade levels
ninth_grade = total_school[(total_school["grade"] == "9th")]
tenth_grade = total_school[(total_school["grade"] == "10th")]
eleventh_grade = total_school[(total_school["grade"] == "11th")]
twelfth_grade = total_school[(total_school["grade"] == "12th")]
# Grouped by school
ninth_grade_math_scores = ninth_grade.groupby(["school_name"]).mean()["math_score"]
tenth_grade_math_scores = tenth_grade.groupby(["school_name"]).mean()["math_score"]
eleventh_grade_math_scores = eleventh_grade.groupby(["school_name"]).mean()["math_score"]
twelfth_grade_math_scores = twelfth_grade.groupby(["school_name"]).mean()["math_score"]
#DataFrame
math_scores_by_grade = pd.DataFrame({"9th Grade": ninth_grade_math_scores, 
                                "10th Grade": tenth_grade_math_scores,
                                "11th Grade": eleventh_grade_math_scores, 
                                "12th Grade": twelfth_grade_math_scores})
math_scores_by_grade = math_scores_by_grade[["9th Grade", "10th Grade", "11th Grade", "12th Grade"]]
math_scores_by_grade.index.name = None
math_scores_by_grade.head()


# In[50]:


#Reading Scores by Grade
#Data series by grade levels
ninth_grade_reading_scores = ninth_grade.groupby(["school_name"]).mean()["reading_score"]
tenth_grade_reading_scores = tenth_grade.groupby(["school_name"]).mean()["reading_score"]
eleventh_grade_reading_scores = eleventh_grade.groupby(["school_name"]).mean()["reading_score"]
twelfth_grade_reading_scores = twelfth_grade.groupby(["school_name"]).mean()["reading_score"]
#DataFrame
reading_scores_by_grade = pd.DataFrame({"9th Grade": ninth_grade_reading_scores, 
                                "10th Grade": tenth_grade_reading_scores,
                                "11th Grade": eleventh_grade_reading_scores, 
                                "12th Grade": twelfth_grade_reading_scores})
reading_scores_by_grade = reading_scores_by_grade[["9th Grade", "10th Grade", "11th Grade", "12th Grade"]]
reading_scores_by_grade.index.name = None
reading_scores_by_grade.head()


# In[51]:


#Scores by School Spending
#Make bins 
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]
# Oragnize the spending ranges
school_summary["Spending Ranges (Per Student)"] = pd.cut(school_capita, spending_bins, labels=group_names)
spending_math_scores = school_summary.groupby(["Spending Ranges (Per Student)"]).mean()["Average Math Score"]
spending_reading_scores = school_summary.groupby(["Spending Ranges (Per Student)"]).mean()["Average Reading Score"]
spending_passing_math = school_summary.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Math"]
spending_passing_reading = school_summary.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Reading"]
overall_passing_rate = (spending_passing_math + spending_passing_reading) / 2
#Make a DataFrame
spending_summary = pd.DataFrame({"Average Math Score" : spending_math_scores,
                                 "Average Reading Score": spending_reading_scores,
                                 "% Passing Math": spending_passing_math,
                                 "% Passing Reading": spending_passing_reading,
                                 "% Overall Passing Rate": overall_passing_rate})
spending_summary = spending_summary[["Average Math Score", "Average Reading Score", "% Passing Math", 
                                     "% Passing Reading","% Overall Passing Rate"]]
spending_summary.head()


# In[52]:


#Scores by School Size
#Make bins 
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
#Organize the spending
school_summary["School Size"] = pd.cut(school_summary["Total Students"], size_bins, labels=group_names)
size_math_scores = school_summary.groupby(["School Size"]).mean()["Average Math Score"]
size_reading_scores = school_summary.groupby(["School Size"]).mean()["Average Reading Score"]
size_passing_math = school_summary.groupby(["School Size"]).mean()["% Passing Math"]
size_passing_reading = school_summary.groupby(["School Size"]).mean()["% Passing Reading"]
overall_passing_rate = (size_passing_math + size_passing_reading) / 2
#DataFrame
size_summary = pd.DataFrame({"Average Math Score" : size_math_scores,
                             "Average Reading Score": size_reading_scores,
                             "% Passing Math": size_passing_math,
                             "% Passing Reading": size_passing_reading,
                             "% Overall Passing Rate": overall_passing_rate})
size_summary = size_summary[["Average Math Score", 
                             "Average Reading Score", 
                             "% Passing Math", "% Passing Reading",
                             "% Overall Passing Rate"]]
size_summary.head()


# In[53]:


#Scores by School Type
type_math_scores = school_summary.groupby(["School Type"]).mean()["Average Math Score"]
type_reading_scores = school_summary.groupby(["School Type"]).mean()["Average Reading Score"]
type_passing_math = school_summary.groupby(["School Type"]).mean()["% Passing Math"]
type_passing_reading = school_summary.groupby(["School Type"]).mean()["% Passing Reading"]
overall_passing_rate = (type_passing_math + type_passing_reading) / 2
#DataFrame
type_summary = pd.DataFrame({"Average Math Score" : type_math_scores,
                             "Average Reading Score": type_reading_scores,
                             "% Passing Math": type_passing_math,
                             "% Passing Reading": type_passing_reading,
                             "% Overall Passing Rate": overall_passing_rate})
type_summary = type_summary[["Average Math Score", 
                             "Average Reading Score",
                             "% Passing Math",
                             "% Passing Reading",
                             "% Overall Passing Rate"]]
type_summary.head()


# In[ ]:




