# COVID-19 Coronavirus Data Dashboard

![A screenshot of the dashboard](screenshot.png)

This dashboard informs the user about the spread of the <b>Coronavirus</b> in the <b>United States</b>. Through the visualizations the viewer
can gain insight into various parameters such as the trend in cases, vaccination, hospitalizations and deaths. The dashboard also aids in 
finding out whether the Coronavirus has affected Males more than Females and which Age groups are most affected. 
Through this dashboard we aim to inform the user about the trends and spread of the 
COVID-19 Coronavirus. 

## Project Goals

TODO: **A clear description of the goals of your project.** Describe the question that you are enabling a user to answer. The question should be compelling and the solution should be focused on helping users achieve their goals. 
<p>The main goal of this dashboard is for the user to find out what was the <b>progression</b> and <b>nature</b>
of the COVID-19 Coronavirus in the United States. The user can also gain insight into the 
effect of the virus across the <b>demography</b> of the US and. </p>

## Design

TODO: **A rationale for your design decisions.** How did you choose your particular visual encodings and interaction techniques? What alternatives did you consider and how did you arrive at your ultimate choices?
<p>We wanted to first give the user a high level perspective about the trend in COVID-19 cases across the countries of the world.
<ul><li>We decided to use a map visualization which depicts the cases in the countries
across time by a time slider </li>. 
<li>Using area of the bubble to indicate the number of cases, it becomes easy for the viewer to perceive 
the general trend</li></ul>
Since the motive of this visualization was to give context and not exact numbers, it made sense to use a general estimate such as a bubble over having 
a bar chart which would make it very noisy to understand.</p>

<p>With the understanding from the previous graph that the United States has experienced the highest number of cases, we now wanted to shift the viewer's focus onto the United States in 
terms of the variation in cases, vaccination, hospitalization and
deaths in the US. 
<ul>
<li>The viewer can compare them and gain insight into
the nature of the disease as well as the effect of vaccinations</li>
<li> We decided to have a multi select line chart and the user can choose which parameter(s) to visualize</li>
<li>A static line chart to compare a fee import lines was also made due to scale imbalance between them. 
This provided flexibility to the user to explore.</li>
</ul>
 </p>

<p>With the insights gained from the earlier visualizations, we now wanted to look into how coid affected the demography of the US. 
Did it affect Males more than Females?  <br>
How did it affected the various age groups in through time over the past two years?<br>
<ul>
<li>We employed a pie chart showing the cumulative distribution </li>
<li>An interactive multi-view coordination which connects the progression in cases across gender and age groups through time.</li> 
</ul>
</p>

As we know that preventive measures were taken differently in countries at varying levels. Let's compare how the US did Vs NZ. 
We wanted to show the effect of preventive/ containment measures such as lockdown in US. We thought it would be best to 
compare it with a vcountry that did it strictly i.e NZ. 
Now that the viewer had an idea about the general progression of Covid in the US. We wanted to give a view about
how two countries might have seen effect on their mobility via lockdowns and strict covid measures. We wanted to depict how the
mobility changed in the last two years. We wanted to show how the US and NZ approached this issue. Since the scales of their cases was very 
different, we employed static visualizations. 

Finally, a question we had in mind was whether the condition of the weather affects the covid rises. Because the user might notice
that the 3 peaks seen occur usually during the cooler seasons. So we tried to analyze if there existed any correlation to the user. 


Page content - Did you notice in the second visualization? It seems that the covid cases increases in the months of October-Janunary?
Does it spread more in cooler temperature? Let's check the correlation between some weather parameters and the cases!
Page content - We know that different governments impose varying levels of containment measuers such as lockdowns. 
lets now see how the US govt approached it and compare it with how the NZ govt appraoched this
## Development

TODO: **An overview of your development process.** Describe how the work was split among the team members. Include a commentary on the development process, including answers to the following questions: Roughly how much time did you spend developing your application (in people-hours)? What aspects took the most time?

First, we had an hour long discussion to choose the domain of the data and appropriate questions we wanted to answer from datasets in these domains.
We then divide the task of dataset selection by having one team member look at COVID datasets and another at weather datasets.
Each one of use analyzed the data present in the datasets we could find and perform some data statistics and exlporatory analysis to explore the feasablity and quality of the datasets in order to answer the identified questions and also look at the possibility of identifying new questions
This took around 3 hrs per person. 
Next, we discussed our findings and chose the COVID-19 dataset (include name) as the ideal dataset to answer our questions
We next identified 5 visualizations to address the 5 questions.
We split the visualizations between the two team members and coded them separately.
This took around 10 hours in total to make. More than half of this time was mostly spent on the Map visualization as altair did not have a very good map interface.
Since the range of covid cases was very big, deciding the size of the circles also took time as we needed to get representative and comaparable sizes while ensuring that they arent so big due to scale imbalance that one country eclipsed the entire continent!
After this we worked on writing some textual descriptions and content to engage the user.
Then we worked on alignment and providing a nice aesthetic to the dashboard which took another 3 hrs.
In total, we spent around 16 hrs per person for this assignment over the past month. 

## Success Story

TODO:  **A success story of your project.** Describe an insight or discovery you gain with your application that relates to the goals of your project.

It was interesting to see that the cases peaked around Winter time the past two years. So
we wanted to investigate if weather affected it so plotted a correlation plot.
Upon plotting we found no significant correlation. We then realised that it must be a spurious(some other word is there)
correlation. The cases must have actually increased due to Christmas and holidays rather than the temperature aspect.
So it showed us how it is important to not just jump to conclusions and verify the result as best as possible before reporting it.

We also saw the possible effect of vaccinations as even though cases increased by a large amount , the deaths remained around the same level.
But in order to actually find if it was the vaccinations or maybe characterestic of the mutation of teh COVID19 virus that behaved differently from the earlier ones need to be explored before we can again conclude the efficacy of vaccinations