# What I checked, and what the agent got wrong

I have checked all the files in the repo and how they are linked with each other to complete the flow of the task. Bob was also able to understand the flow as the task is supposed to be , But bob only found the 3 tests failing but not the need for another test for the crashing of task when there is a missing reading 

## 

## What the agent got wrong

## 

The script calculates pct (percentage difference) in a loop for each column, but then the conclusion just prints literal text like "km\_since\_service (+60.8%) ... " typed directly, rather than referencing the actual calculated pct value. It looks like the conclusion follows from the data, but it's decorative — if the CSV changed, that text wouldn't update.



The risk score weights km\_since\_service and load\_factor equally (50/50), even though the data showed km\_since\_service was a much stronger separator (+60.8% vs +18.8%). That's a design choice the agent made silently, not something derived from the data.



The analysis writes the car which missed the last servicing data as not broke down considering the service has done by time or the car is retired.(For example vehicle VOS-1217)



## What I checked before I accepted its work



I checked if the agent had done changes as per my requirements and if the tests pass after the changes. Also verified whether the agent did any changed to the script which were unnecessary or which breaks the flow of the task. Dead functions or lines unused were also deleted and tests are run to check whether this deletion causes bugs to raise.

## 

## What the data actually said





Looking at the data the factors that decide breakdown are kilometers since serviced and Load factor which contributes more for the Risk score. Also from  the data for the cars whose kms since last service is more than 15k are not flagged as broke down as they are neglected for missing the last service data.

