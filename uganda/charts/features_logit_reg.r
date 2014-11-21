# Read in all user features, clean up
users <- read.table("users_all.csv", header=TRUE, strip.white=TRUE, sep=',')
users <- na.omit(users)

# Create two new values for testing predictions
users$difference <- users$incoming - users$outgoing
users$moreout <- users$incoming < users$outgoing

# Test out logit regs
mylogit<- glm(users$moreout~users$degree + users$in_degree + users$out_degree + users$calls + users$duration + users$workday + users$nonworkday + 
users$weekday + users$weekend, family=binomial(link="logit"), na.action=na.pass)
mylogit<- glm(users$moreout~users$degree, family=binomial(link="logit"), na.action=na.pass)
exp(mylogit$coefficients)
mylogit <- glm(users$moreout~users$in_degree, family=binomial(link="logit"), na.action=na.pass)
exp(mylogit$coefficients)
mylogit <- lm(users$moreout~users$weekday + users$region + users$degree + users$in_degree + users$out_degree, family=binomial(link="logit"), na.action=na.pass)
exp(mylogit$coefficients)
