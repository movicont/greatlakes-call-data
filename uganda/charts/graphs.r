

## Read for usage data per user

peruser <- read.table("users_cost_dur_one_per.csv", header=TRUE, strip.white=TRUE, sep=',')
peruser$cost_per_min <- peruser$cost/peruser$duration


#### Statistics

## Get summary data, compare with t-test

summary(usage$duration)
#     Min.   1st Qu.    Median      Mean   3rd Qu.      Max.
#     907 309200000 324300000 322300000 345100000 494900000
summary(usage$cost)
#     Min.   1st Qu.    Median      Mean   3rd Qu.      Max.
# 2.281e+03 9.669e+08 9.845e+08 9.557e+08 1.003e+09 1.158e+09
summary(usage$calls)
#   Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
#    17 6263000 6402000 6290000 6648000 7467000
summary(usage$cost_per_min)
#   Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
#  1.994   2.777   2.999   2.983   3.235   3.562


users <- read.table("user_data_with_locs.csv", header=TRUE, strip.white=TRUE, sep=',')


pdf("user_degree.pdf", width=12, height=5)
hist(cleanusers$degree, breaks=1000, main="Unique Contacts per User", col="#ff3366cc", xlim=c(0,100), xlab="Number of Unique Contacts")
dev.off()
pdf("user_inoutdeg.pdf", width=12, height=5)
hist(cleanusers$in_degree, breaks=1200, main="Unique Contacts per User", col="#ff3366cc", xlim=c(0,100), xlab="Number of Unique Contacts")
hist(cleanusers$out_degree, breaks=500, main="Unique Contacts per User", col="#cccccccc", xlim=c(0,100), xlab="Number of Unique Contacts", add=TRUE)
dev.off()
pdf("user_calls.pdf", width=12, height=5)
hist(cleanusers$calls, breaks=700, main="# of Calls per User during January", col="#ff3366cc", xlim=c(0,500), xlab="Number of Calls")
dev.off()

userlocs <- read.table("user_locations.csv", header=TRUE, strip.white=TRUE, sep=',')
usersplus <- merge(cleanusers, userlocs, all=TRUE)

users <- read.table("user_data_with_locs.csv", header=TRUE, strip.white=TRUE, sep=',')
summary(users)
kampala <- subset(users, users$region == "KampalaCentral")
eastern <- subset(users, users$region == "Eastern")
western <- subset(users, users$region == "Western")
northern <- subset(users, users$region == "Northen")

pdf("user_deg_by_region.pdf", width=12, height=5)
hist(kampala$degree, breaks=300, xlim=c(0,500), main="# of Calls per User during January", col="#ff3366cc", xlab="Number of Calls")
hist(western$degree, breaks=250, col="#00ff55cc", add=TRUE)
hist(eastern$degree, breaks=150, col="#22cfffcc", add=TRUE)
hist(northern$degree, breaks=250, xlim=c(0,500), col="#ccff00cc", add=TRUE)
legend("topright", c("Kampala/Central","Western","Eastern","Northern"), 
   col=c("#ff3366cc","#00ff55cc","#22cfffcc","#ccff00cc"))

dev.off()


uganda <- read.table("C:\\Users\\yian\\code\\workspace\\TraceTransfer\\data\\MapUganda.csv", header=TRUE, strip.white=TRUE, sep=',')

users <- read.table("users_all.csv", header=TRUE, strip.white=TRUE, sep=',')
kampala <- subset(users, users$region == "KampalaCentral")
eastern <- subset(users, users$region == "Eastern")
western <- subset(users, users$region == "Western")
northern <- subset(users, users$region == "Northen")
pdf("calls_weekend_weekday_kampala.pdf", width=12, height=5)
#hist(eastern$workday, breaks=150, col="#22cfff33", main="# of Workday (M-F, 9-5) Calls during January", col="#ff336633", xlab="Number of Calls")
hist(kampala$weekend, breaks=200, xlim=c(0,500), col="#22cfff99", main="# of Weekday vs Weekend Calls during January in Kampala", )
hist(kampala$weekday, breaks=200, xlim=c(0,500),  col="#ccff0099", add=TRUE)
#hist(western$workday, breaks=250, col="#00ff5533", add=TRUE)
#hist(northern$workday, breaks=150, xlim=c(0,500), col="#ccff0033", add=TRUE)
#legend("topright", c("Kampala/Central","Western","Eastern","Northern"), 
#   col=c("#ff3366cc","#00ff55cc","#22cfffcc","#ccff00cc"))
dev.off()





hist(users$cost, breaks=quantile(users$cost,seq(0,1,.05)), col="black", main="User Revenue Distribution", xlim=c(0,30000), xlab="Revenue (UGX)", ylab="Percentage of Total")
rect(0, 0, 2021, 1, col="#FFA90699", lty="dashed", lwd="1")
rect(2021, 0, 5300, 1, col="#E8121299", lty="dashed", lwd="1")
rect(5300, 0, 11279, 1, col="#3E798799", lty="dashed", lwd="1")
rect(11279, 0, 40000, 1, col="#F6A6A699", lty="dashed", lwd="1")
abline(v=9112, lty="dashed", col="#aa33ff", lwd="2") # mean

hist(users$duration, breaks=quantile(users$duration,seq(0,1,.05)), col="black", main="Histogram of Call Duration", xlim=c(0,15000), xlab="Time per Call (seconds)", ylab="Count")
rect(0, 0, 602, 1, col="#FFA90699", lty="dashed", lwd="1")
rect(602, 0, 1647, 1, col="#E8121299", lty="dashed", lwd="1")
rect(1647, 0, 3666, 1, col="#3E798799", lty="dashed", lwd="1")
rect(3666, 0, 20000, 1, col="#F6A6A699", lty="dashed", lwd="1")

hist(users$duration, breaks=quantile(users$duration,seq(0,1,.05)), col="black", main="Histogram of Call Duration", xlim=c(0,15000), xlab="Time per Call (seconds)", ylab="Count")
rect(0, 0, 36, 1, col="#F6A6A699", lty="dashed", lwd="1")
rect(36, 0, 14699.27, 1, col="#3E798799", lty="dashed", lwd="1")
rect(14699.27, 0, 30000, 1, col="#F6A6A699", lty="dashed", lwd="1")

hist(users$calls, breaks=quantile(users$duration,seq(0,1,.01)), col="black", main="Number of Calls Distribution", xlim=c(0,600), xlab="Number of Calls", ylab="Percentage of Total")
rect(1, 0, 15, 1, col="#FFA90699", lty="dashed", lwd="1")
rect(15, 0, 38, 1, col="#E8121299", lty="dashed", lwd="1")
rect(38, 0, 78, 1, col="#3E798799", lty="dashed", lwd="1")
rect(78, 0, 3000, 1, col="#F6A6A699", lty="dashed", lwd="1")

abline(v=quantile(topone$calls), lty="dashed")
hist(topone$calls, breaks=quantile(users$duration,seq(0,1,.01)), col="black", 
main="Number of Calls - Top Ten Percent of Users", xlim=c(0,800), xlab="Number of Calls", 
ylab="Percentage of Total", lty="solid", lwd="1")
rect(1, 0, 136, 1, col="#FFA90677", lty="dashed", lwd="1")
rect(136, 0, 181, 1, col="#E8121277", lty="dashed", lwd="1")
rect(181, 0, 246, 1, col="#3E798799", lty="dashed", lwd="1")
rect(246, 0, 3000, 1, col="#F6A6A699", lty="dashed", lwd="1")

hist(topone$cost, breaks=quantile(topone$cost,seq(0,1,.05)), col="grey", 
main="Total Cost - Top One Percent of Users", xlim=c(0,100000), xlab="Number of Calls", 
ylab="Percentage of Total", lty="solid", lwd="1")

hist(topone$degree, breaks=quantile(topone$degree,seq(0,1,.01)), col="grey", 
main="Contacts - Top One Percent of Users", xlim=c(0,300), xlab="Number of Contacts", 
ylab="Percentage of Total", lty="solid", lwd="1", ylim=c(0,0.025))


hist(toponee$incoming, breaks=30, col="#2299cc", 
main="Total Number of Calls - Top One Percent of Users", xlim=c(0,600), xlab="Number of Calls", 
ylab="Percentage of Total", lty="solid", lwd="1")

hist(toponee$outgoing, breaks=50, col="#ff2222cc", 
main="Total Number of Calls - Top One Percent of Users", xlim=c(0,600), xlab="Number of Calls", 
ylab="Percentage of Total", lty="solid", lwd="1", add=TRUE)
legend("topright", legend = c("Outgoing Calls", "Incoming Calls"), col=c("#ff3366", "#2299cc"), lty=1, lwd=10)


hist(users$incoming, breaks=90, col="#2299cc", 
main="Total Number of Calls - All Users", xlim=c(0,200), xlab="Number of Calls", 
ylab="Count", lty="solid", lwd="1")

hist(users$outgoing, breaks=150, col="#ff2222cc", 
main="Total Number of Calls - All Users", xlim=c(0,200), xlab="Number of Calls", 
ylab="Count", lty="solid", lwd="1", add=TRUE)
legend("topright", legend = c("Outgoing Calls", "Incoming Calls"), col=c("#ff3366", "#2299cc"), lty=1, lwd=10)
#boxplot(users$outgoing, ylim=c(0,90), horizontal=TRUE, add=TRUE)

abline(v=7, lty="dashed", col="#22aaff",lwd="2")
abline(v=19, lty="dashed", col="#22aaff",lwd="2")
abline(v=40, lty="dashed", col="#22aaff",lwd="2")

abline(v=6, lty="dashed", col="#ff8866",lwd="2")
abline(v=17, lty="dashed", col="#ff88ee",lwd="2")
abline(v=38, lty="dashed", col="#ff88ee",lwd="2")

#
# Plot scatterplot of user calls vs revenue
#
plot(users$calls, users$cost, main="User Calls vs Revenue")
res=lm(users$cost~users$calls)
abline(res)
summary.lm(res)

# whale curve of revenue
plot(cumsum(as.numeric(costsorted)), xlab="# of customers", ylab="Cumulative Revenue", main="Cumulative Revenue Over All Users")
abline(h=quantile(cumsum(as.numeric(costsorted))), lty="dashed")
rect(0, 0, 2000000, 7507425085, col="#FFA90699", lty="dashed", lwd="1")
rect(0, 7507425085, 2000000, 9958868668, col="#E8121299", lty="dashed", lwd="1")
rect(0, 9958868668, 2000000, 11062894326, col="#3E798799", lty="dashed", lwd="1")
rect(0, 11062894326, 2000000, 11334632491, col="#F6A6A699", lty="dashed", lwd="1")

hist(users$degree, breaks=quantile(users$degree,seq(0,1,.05)), col="#ff2222cc", 
main="Distribution of the Number of Unique Contacts per User", xlim=c(0,75), xlab="Number of Unique Contacts", 
ylab="Percentage of Total", lty="solid", lwd="1")
hist(topone$degree, breaks=quantile(topone$degree,seq(0,1,.05)), col="#ff2222cc", 
main="Distribution of the Number of Contacts - Top 10%", xlim=c(0,75), xlab="Number of Unique Contacts", 
ylab="Percentage of Total", lty="solid", lwd="1")