# COVID-19 Coronavirus Data Dashboard

![A screenshot of the dashboard](screenshot.png)

This dashboard informs the user about the spread of the Coronavirus in the United States. Through the visualizations the viewer
can gain insight into various parameters such as the trend in cases, vaccination, hospitalizations and deaths. The dashboard also aids in 
finding out whether the Coronavirus has affected Males more than Females and which Age groups are most affected. 
Through this dashboard we aim to inform the user about the trends and spread of the 
COVID-19 Coronavirus. 

## Project Goals

TODO: **A clear description of the goals of your project.** Describe the question that you are enabling a user to answer. The question should be compelling and the solution should be focused on helping users achieve their goals. 
The main goal of this dashboard is for the user to find out what was the progression and nature
of the COVID-19 Coronavirus in the United States. The user can also gain insight into the 
effect of the virus across the demography of the US and. 

## Design

TODO: **A rationale for your design decisions.** How did you choose your particular visual encodings and interaction techniques? What alternatives did you consider and how did you arrive at your ultimate choices?
We wanted to first give the user a broad overview wrt to how covid cases have changed in the world. 
Show the viewer the progression of US wrt to the world. 
For this we decided to use a map visualization which depicts the cases in the countries
across time by sliding across time and the size of the point is scaled according to the case. 
We did not want to provide exact numbers but only like a comparative study. 

With this context, we wanted viewer to focus on the US. 
Wanted them to see cases as well as cases, vaccination, hospitalization, 
deaths in the US. So the viewer can compare them and gain insight into
the nature of the disease as well as the effect of vaccinations
To do this we decided to have a multi select line chart and the user can choose what to see. 
A static line chart to compare a fee import lines was also made due to scale imbalance between them. 
This provided flexibility to the user to explore. 

We wanted to look into how coid affected the demography of the US. Did it affect Males more than Females, 
how it affected the various age groups in through time over the past two year. 
To do this, we employed a pie chart showing the cumulative distribution and also employed an interactive multi-view coordination
which connects the progression in cases across gender and age groups through time. 

As we know that preventive measures were taken differently in countries at varying levels. Let's compare how the US did Vs NZ. 
We wanted to show the effect of preventive/ containment measures such as lockdown in US. We thought it would be best to 
compare it with a vcountry that did it strictly i.e NZ. 
Now that the viewer had an idea about the general progression of Covid in the US. We wanted to give a view about
how two countries might have seen effect on their mobility via lockdowns and strict covid measures. We wanted to depict how the
mobility changed in the last two years. We wanted to show how the US and NZ approached this issue. Since the scales of their cases was very 
different, we employed static visualizations. 

Finally, a question we had in mind was whether the condition of the weather affects the covid rises. Because the user might notice
that the 3 peaks seen occur usually during the cooler seasons. So we tried to analyze if there existed any correlation to the user. 


Did you notice in the second visualization? It seems that the covid cases increases in the months of October-Janunary?
Does it spread more in cooler temperature? Let's check the correlation between some weather parameters and the cases!

## Development

TODO: **An overview of your development process.** Describe how the work was split among the team members. Include a commentary on the development process, including answers to the following questions: Roughly how much time did you spend developing your application (in people-hours)? What aspects took the most time?

## Success Story

TODO:  **A success story of your project.** Describe an insight or discovery you gain with your application that relates to the goals of your project.
