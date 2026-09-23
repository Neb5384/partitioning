# Partitioning and the small-files problem
You partitioned the dataset by day and the same query got slower. Where did the time go?

## YOUR PRESENTATION (15 MINUTES + 10 MIN Q&A)
This could be the structure of your talk. Nonetheless, you are free to improve or modify to ensure the topic will be more accessible 

1. Partitioning a dataset by making a directory for each value in a column (for example: "date")
2. Why that partition only works if analysis queries only for single days
3. If instead, you'd typically run 1000-day queries, then access cost raises
4. The demo uses the MeteoSuisse dataset to demonstrate the performance of two distant layouts

## YOUR DEMO (AIM AT 2 MIN, BUT FLEXIBLE IF YOU BLEND IT NICELY WITH THE PRESENTATION)
Take the MeteoSuisse measurements and write them twice, once with a directory per day and once with a directory per year.
Run a single-day query against both, then a query spanning three years against both. Report the read time and the number of files opened in each of the four cases.

Demo should run in about 2 minutes, and should be a demo unless a teacher allows you to bring pre-baked results.
## YOUR THREE DELIVERABLES
- C1 Angle - one slide: the topic in your own words, the question you answer, what your demo will show `Wednesday 23 September`
- C2 Demo runs - the code, a README, one command `Friday 25 September`
- C3 Deck - complete slides, demo embedded
`Sunday 27 September`

All three interim materials must be uploaded into ISC Learn by 18:00; the demo as a repository link. These deliverables are mandatory, and the teacher will provide feedback to improve your work.

## READING
Armbrust et al. (2020). Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores doi:10.14778/3415478.3415560

Matthew Powers. Optimizing Delta Parquet Data Lakes for Apache Spark www.youtube.com/watch?v=euBvYFTVN8s