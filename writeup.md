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
across time by a time slider </li>
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
</ul></p>

<p>With the insights gained from the earlier visualizations, we now wanted to look into how coid affected the demography of the US.<br> 
Did it affect Males more than Females?  <br>
How did it affected the various age groups in through time over the past two years?<br>
<ul>
<li>We employed a pie chart showing the cumulative distribution </li>
<li>An interactive multi-view coordination which connects the progression in cases across gender and age groups through time.</li> 
</ul></p>

<p>
Preventive measures such as restrictions and lockdowns were imposed by countries to control the spread of the Coronavirus. 
To understand the outcome of the measures, we will now observe the change in moblity of the citizen's of the US by comparing
them to that of New Zealand because New Zealand is known to have very strict restrictions in place. 
<ul>
<li>We employed static visualizations since we wanted to compare only 2 countries</li>
<li>We used a streamgraph to depict this phenomenon since there were multiple categories and the streamgraph could be
used to interpret the change in trend of mobility of the people of the country</li>
</ul></p>

<p>
Another dimension that we wanted to touch upon was how parameters of weather influenced the number of cases
<ul>
<li>We used a correlation matrix to demonstrate the dependence between variables such as rainfall, temperature et. with 
the number of cases </li>
</ul>
</p>
Finally, a question we had in mind was whether the condition of the weather affects the covid rises. Because the user might notice
that the 3 peaks seen occur usually during the cooler seasons. So we tried to analyze if there existed any correlation to the user. 


Page content - Did you notice in the second visualization? It seems that the covid cases increases in the months of October-Janunary?
Does it spread more in cooler temperature? Let's check the correlation between some weather parameters and the cases!
Page content - We know that different governments impose varying levels of containment measuers such as lockdowns. 
lets now see how the US govt approached it and compare it with how the NZ govt appraoched this
## Development

TODO: **An overview of your development process.** Describe how the work was split among the team members. Include a commentary on the development process, including answers to the following questions: Roughly how much time did you spend developing your application (in people-hours)? What aspects took the most time?

<p>
First, we had an hour long discussion to choose the domain of the data and appropriate questions we wanted to answer from datasets in these domains.
We then divide the task of dataset selection by trying to explore existing datasets and identify ones that interested us.
Each one of use analyzed the data present in the datasets we could find and perform some data statistics and exlporatory analysis to explore the feasibility and quality of the datasets in order to answer the identified questions and also look at the possibility of identifying new questions
This took around 3 hrs per person. 
Next, we discussed our findings and chose the <a href = 'https://goo.gle/covid-19-open-data'>Google health COVID-19 Open Dataset </a>. 
We split the visualizations between the two team members and coded them separately.
This took around 10 hours in total to make. More than half of this time was mostly spent on the Map visualization as Altair did not have very good support for map interface.
Since the range of covid cases was very big, deciding the size of the circles also took time as we needed to get representative and comparable sizes while ensuring that they aren't very huge
due to scale imbalance that one country would eclipse the entire continent!
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