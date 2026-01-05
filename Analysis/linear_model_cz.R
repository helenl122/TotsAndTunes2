# clear environment
rm(list=ls())
setwd("C:/Users/User/OneDrive - UW/23-24/LING 499/Code/Aggregation/results/TT1")

# Load the required package
library(Matrix)
library(lme4)
library(lmerTest)

# Load csv as dataframe
data_overall <- read.csv("tt1_type_counts.csv")

# Convert input_type and input_source to factors
data_overall$input_type <- as.factor(data_overall$input_type)
data_overall$age <- as.factor(data_overall$age)

model_overall<-lmer(count~age*input_type + (1 + age|subject_name), data=data_overall)

summary(model_overall)
(output_overall<-anova(model_overall))

posthoc_overall<-difflsmeans(model=model_overall,level=0.95, ddf = c("Satterthwaite","Kenward-Roger"))

SS_fixed_type <- output_overall$"Sum Sq"[2]
SS_fixed_interaction <- output_overall$"Sum Sq"[3]
SS_total <- sum(output_overall$"Sum Sq")
eta_squared_type <- SS_fixed_type / SS_total
eta_squared_interaction <- SS_fixed_interaction / SS_total

# model 2
data_source <- read.csv("tt1_source_counts.csv")

data_source$input_source <- as.factor(data_source$input_source)
data_source$input_type <- as.factor(data_source$input_type)
data_source$age <- as.factor(data_source$age)

# Fit the linear mixed-effects model
model_source <- lmer(count ~ age * input_type * input_source + (1 + age|subject_name), data = data_source)

# Print the summary of the model
summary(model_source) #for betas
(output_source<-anova(model_source)) # for F and p
(posthoc_source<-difflsmeans(model=model_source,level=0.95, ddf = c("Satterthwaite","Kenward-Roger")))

SS_total <- sum(output_source$"Sum Sq")
eta_squared_type <- output_source$"Sum Sq"[2] / SS_total
eta_squared_source <- output_source$"Sum Sq" [3] / SS_total
eta_squared_agetype <- output_source$"Sum Sq" [4] / SS_total
eta_squared_agesource <- output_source$"Sum Sq" [5] / SS_total
eta_squared_typesource <- output_source$"Sum Sq" [6] / SS_total
eta_squared_3way <- output_source$"Sum Sq" [7] / SS_total

# model 3
data_baby <- read.csv("tt1_target_counts.csv")

data_baby$input_recipient <- as.factor(data_baby$input_recipient)
data_baby$input_type <- as.factor(data_baby$input_type)
data_baby$age <- as.factor(data_baby$age)

# Fit the linear mixed-effects model
model_baby <- lmer(count ~ age * input_type * input_recipient + (1 + age|subject_name), data = data_baby)

# Print the summary of the model
summary(model_baby)
(output_baby <- anova(model_baby))
posthoc_baby<-difflsmeans(model=model_baby,level=0.95, ddf = c("Satterthwaite","Kenward-Roger"))

SS_total <- sum(output_baby$"Sum Sq")
eta_squared_type <- output_baby$"Sum Sq"[2] / SS_total
eta_squared_receipt <- output_baby$"Sum Sq" [3] / SS_total
eta_squared_agetype <- output_baby$"Sum Sq" [4] / SS_total
eta_squared_agereceipt <- output_baby$"Sum Sq" [5] / SS_total

eta_squared_3way <- output_baby$"Sum Sq" [7] / SS_total
# correlation by age
wide_table <-pivot_wider(names_from = c(age,input_type), values_from = count, data = data_overall)
cor.test(wide_table$"1_Speech",y=wide_table$"1_Music", method="pearson" )
cor.test(wide_table$"2_Speech",y=wide_table$"2_Music", method="pearson" )
cor.test(wide_table$"3_Speech",y=wide_table$"3_Music", method="pearson" )
cor.test(wide_table$"4_Speech",y=wide_table$"4_Music", method="pearson" )
cor.test(wide_table$"5_Speech",y=wide_table$"4_Music", method="pearson" )
