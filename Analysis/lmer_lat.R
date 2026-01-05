# set environment
rm(list=ls())
setwd("C:/Users/User/OneDrive - UW/23-24/LING 499/Code/Aggregation/results") # where data is stored

# Load the required package
library(Matrix)
library(lme4)
library(lmerTest)
library(tidyr)

## TYPE DATA -----------------------------------------------------------------
# Load csv as dataframe
type_data <- read.csv("type_counts.csv") # INPUT TYPE
# Convert input_type to factors
type_data$input_type <- as.factor(type_data$input_type)

# Fit model
type_model<-lmer(log(count+1)~age*input_type+(1|subject_name), data=type_data) # use log(count+1) for normalizing

# Results
summary(type_model)
(type_output<-anova(type_model))

library(ggplot2)
ggplot(type_data, aes(x = age, y = log(count + 1), color = input_type)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm") +
  theme_minimal()

# SOURCE DATA ---------------------------------------------------------------
source_data <- read.csv("source_counts.csv") # INPUT SRC
# Convert input_type and input_source to factors
source_data$input_source <- as.factor(source_data$input_source)
source_data$input_type <- as.factor(source_data$input_type)

# Fit the linear mixed-effects model
source_model<-lmer(log(count+1) ~ age*input_type*input_source + (1|subject_name), data = source_data)

# Results
summary(source_model) #for betas
(source_output<-anova(source_model)) # for F and p

ggplot(source_data, aes(x = input_type, y = log(count + 1), fill = input_source)) +
  geom_boxplot() +
  theme_minimal() +
  labs(title = "Interaction between Input Type and Source")

# TARGET DATA ----------------------------------------------------------------
target_data <- read.csv("target_counts.csv") # INPUT TARGET
target_data$input_recipient <- as.factor(target_data$input_recipient)
target_data$input_type <- as.factor(target_data$input_type)

# Fit the linear mixed-effects model
target_model <- lmer(log(count+1) ~ age*input_type*input_recipient + (1|subject_name), data = target_data)

# Print the summary of the model
summary(target_model)
(target_output <- anova(target_model))

ggplot(target_data, aes(x = input_type, y = log(count + 1), fill = input_recipient)) +
  geom_boxplot() +
  theme_minimal() +
  labs(title = "Interaction between Input Type and Recipient")

ggplot(target_data, aes(x = age, y = log(count + 1), color = input_recipient)) +
  geom_smooth(method = "lm", se = TRUE) +
  facet_wrap(~ input_type) +
  labs(title = "Effect of Age and Recipient by Input Type")