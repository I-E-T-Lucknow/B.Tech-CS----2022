#installing necessary packages
#install and load package arules
#install.packages("arules")
library(arules)
#install and load arulesViz
#install.packages("arulesViz")
library(arulesViz)
#install and load tidyverse
#install.packages("tidyverse")
library(tidyverse)
#install and load readxml
#install.packages("readxml")
library(readxl)
#install and load knitr
#install.packages("knitr")
library(knitr)
#load ggplot2 as it comes in tidyverse
library(ggplot2)
#install and load lubridate
#install.packages("lubridate")
library(lubridate)
#install and load plyr
#install.packages("plyr")
library(plyr)
library(dplyr)

#DATA PREPROCESSING 
#read excel into R dataframe
retail <- read_excel("D:/Documents/Online_Retail.xlsx")
#complete.cases(data) will return a logical vector indicating which rows have no missing values. Then use the vector to get only rows that are complete using retail[,]
retail <- retail[complete.cases(retail), ]
retail %>% mutate(Description = as.factor(Description))
#
retail %>% mutate(Country = as.factor(Country)) 
#Converts character data to date. Store InvoiceDate as date in new variable
retail$Date <- as.Date(retail$InvoiceDate)
#Extract time from InvoiceDate and store in another variable
TransTime<- format(retail$InvoiceDate,"%H:%M:%S")
#Convert and edit InvoiceNo into numeric
InvoiceNo <- as.numeric(as.character(retail$InvoiceNo)) 

#Bind new columns TransTime and InvoiceNo into dataframe retail
cbind(retail,TransTime)
cbind(retail,InvoiceNo)

#get a glimpse of your data
glimpse(retail)

library(plyr) #deploying plyr
#ddply(dataframe, variables_to_be_used_to_split_data_frame, function_to_be_applied)
transactionData <- ddply(retail,c("InvoiceNo","Date"), function(df1)paste(df1$Description, collapse = ",")) #The R function paste() concatenates vectors to character and separated results using collapse=[any optional charcater string ]. Here ',' is use
#Viewing the DATA
transactionData

#SETTING NULL TO InvoiceNo AND Date
#set column InvoiceNo of dataframe transactionData  
transactionData$InvoiceNo <- NULL
#set column Date of dataframe transactionData
transactionData$Date <- NULL
#Rename column to items
colnames(transactionData) <- c("items")
#Show Dataframe transactionData
transactionData

#SAVING THE FILE TO MARKETBASKETTRANSACTIONS.CSV WITH ALL TRANSACTIONS
write.csv(transactionData,"D:/Documents/market_basket_transactions.csv", quote = FALSE, row.names = FALSE) 
#If TRUE it will surround character or factor column with double quotes. If FALSE nothing will be quoted

#LOADING TRANSACTIONS TO "tr" VARIABLE
tr <- read.transactions('D:/Documents/market_basket_transactions.csv', format = 'basket', sep=',')

#VIEWING THE "tr" OBJECT
tr

#SUMMARY OF THE "tr"
summary(tr)

# Create an item frequency plot for the top 20 items
if(!require("RColorBrewer")) 
{
		#install color package of R
		install.packages("RColorBrewer")
		#include library RColorBrewer
		library(RColorBrewer)
}

#PLOTTING THE FrequencyPLOT
itemFrequencyPlot(tr,topN=20,type="absolute",col=brewer.pal(8,'Pastel2'), main="Absolute Item Frequency Plot")

#PLOTTING RELATIVE Frequency
itemFrequencyPlot(tr,topN=20,type="relative",col=brewer.pal(8,'Pastel2'),main="Relative Item Frequency Plot")

# GENERATING RULES
# Min Support as 0.001, confidence as 0.8.
association.rules <- apriori(tr, parameter = list(supp=0.001, conf=0.8,maxlen=10))
#GETTING THE SUMMARY
summary(association.rules)

#VIEWING THE FIRST 10 RULES
inspect(association.rules[1:10])

#LIMITING THE SIZE OF RULES
shorter.association.rules <- apriori(tr, parameter = list(supp=0.001, conf=0.8,maxlen=3))

#REMOVING REDUNDANT RULES
subset.rules <- which(colSums(is.subset(association.rules, association.rules)) > 1) # get subset rules in vector
#which() returns the position of elements in the vector for which value is TRUE.
#colSums() forms a row and column sums for dataframes and numeric arrays.
#is.subset() Determines if elements of one vector contain all the elements of other
#GETTING THE LENGTH
length(subset.rules)
# remove subset rules.
subset.association.rules. <- association.rules[-subset.rules] 

#Finding Rules related to given items
metal.association.rules <- apriori(tr, parameter = list(supp=0.001, conf=0.8),appearance = list(default="lhs",rhs="METAL"))
inspect(head(metal.association.rules))

#postage.association.rules <- apriori(tr, parameter = list(supp=0.001, conf=0.8),appearance = list(default="lhs",rhs="POSTAGE"))
#inspect(head(postage.association.rules))

#INPUT THE ITEM WHOSE RULE HAS TO BE EVALUATED
print("Press 1 for new rules")
choice<-readline()
choice<-as.integer(choice)
while(choice==1)
{
	print("Enter Item Name:")
	newrule<-readline()
	newrule.association.rules <- apriori(tr, parameter = list(supp=0.001, conf=0.8),appearance = list(default="lhs",rhs=newrule))
	inspect(head(newrule.association.rules))
	print("Press 1 for new rules")
	choice<-readline()
	choice<-as.integer(choice)

}


# Customers who bought METAL also bought
metal.association.rules <- apriori(tr, parameter = list(supp=0.001, conf=0.8),appearance = list(lhs="METAL",default="rhs"))
inspect(head(metal.association.rules))

#Visualizing Association Rules
# Filter rules with confidence greater than 0.4 or 40%
subRules<-association.rules[quality(association.rules)$confidence>0.4]
#SCATTERPLOT
#Plot SubRules
plot(subRules)
#TWO KEY PLOT
plot(subRules,method="two-key plot")
plotly_arules(subRules)

#Graph-Based Visualizations
top10subRules <- head(subRules, n = 15, by = "confidence")
#INTERACTIVE
plot(top10subRules, method = "graph",  engine = "htmlwidget")

#SAVE Graph
saveAsGraph(head(subRules, n = 1000, by = "lift"), file = "rules.graphml")

#Individual Rule Representation
# Filter top 20 rules with highest lift
subRules2<-head(subRules, n=20, by="lift")
plot(subRules2, method="paracoord")


