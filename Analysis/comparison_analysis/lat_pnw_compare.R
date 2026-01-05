# set environment
rm(list=ls())
setwd("C:/Users/User/OneDrive - UW/23-24/LING 499/Code/Analysis/comparison_analysis/sample_means") # where data is stored

# Load the required package
library(Matrix)
library(lme4)
library(lmerTest)
library(tidyr)

# Load data (bootstrap samples!)
tt1_type <- read.csv("TT1 Type_sample.csv")
tt2_type <- read.csv("TT2 Type_sample.csv")
tt1_source <- read.csv("TT1 Source_sample.csv")
tt2_source <- read.csv("TT2 Source_sample.csv")
tt1_target <- read.csv("TT1 Target_sample.csv")
tt2_target <- read.csv("TT2 Target_sample.csv")

## TYPE DATA -----------------------------------------------------------------
# add which dataset each belongs to, combine > type_data, then pivot speech & music columns into "sound"
tt1_type$dataset <- "PNW" 
tt2_type$dataset <- "LAT"
type_data <- rbind(tt1_type, tt2_type)
type_data <- type_data %>% pivot_longer(cols = c(speech, music), names_to = "type", values_to = "count")
type_data$type <- as.factor(type_data$type)
type_data$dataset <- as.factor(type_data$dataset)

# lm results
type_lm <-lm(count~type*dataset, data=type_data)
summary(type_lm)
(type_lm_output<-anova(type_lm))

# lmer results
#type_lmer<-lmer(count~sound+(1|dataset), data=type_data)
#summary(type_lmer)
#(type_lmer_output<-anova(type_lmer))

# SOURCE DATA ---------------------------------------------------------------
tt1_source$dataset <- "PNW"
tt2_source$dataset <- "LAT"
source_data <- rbind(tt1_source, tt2_source)
source_data <- source_data %>% pivot_longer(cols = c(music_device, music_person, speech_device, speech_person), names_to = "sound_source", values_to = "count")
# split sound_source into type & source columns
source_data <- separate_wider_delim(source_data, cols = sound_source, delim = "_", names = c("type", "source"))

source_data$type <- as.factor(source_data$type)
source_data$source <- as.factor(source_data$source)
source_data$dataset <- as.factor(source_data$dataset)

# lm results
source_lm<-lm(count~type*source*dataset, data=source_data)
summary(source_lm)
(source_lm_output<-anova(source_lm))

# lmer results
#source_lmer<-lmer(count ~ sound + (1|dataset), data=source_data)
#summary(source_lmer)
#(source_lmer_output<-anova(source_lmer))

# TARGET DATA ----------------------------------------------------------------
tt1_target$dataset <- "PNW"
tt2_target$dataset <- "LAT"
target_data <- rbind(tt1_target, tt2_target)
target_data <- target_data %>% pivot_longer(cols = c(music_baby, music_other, speech_baby, speech_other), names_to = "sound_target", values_to = "count")
# split sound_target into type & target columns
target_data <- separate_wider_delim(target_data, cols = sound_target, delim = "_", names = c("type", "target"))

target_data$type <- as.factor(target_data$type)
target_data$target <- as.factor(target_data$target)
target_data$dataset <- as.factor(target_data$dataset)

# lm results
target_lm<-lm(count~type*target*dataset, data=target_data)
summary(target_lm)
(target_lm_output <-anova(target_lm))

# lmer results
#target_lmer<-lmer(count ~ sound + (1|dataset), data=target_data)
#summary(target_lmer)
#(target_lmer_output <- anova(target_lmer))
