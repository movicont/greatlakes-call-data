## Read in the data, separate into weekends and weekdays
## and calculate cost per minute

usage <- read.table("agg_by_date.csv", header=TRUE, strip.white=TRUE, sep=',')
usage$date <- as.POSIXct(strptime(usage$date, format="%d-%b-%y"))
usage <- subset(usage, usage$calls > 100)
weekends <- subset(usage, usage$is_weekend == "True")
weekdays <- subset(usage, usage$is_weekend == "False")
usage$cost_per_min <- usage$cost/usage$duration
weekends$cost_per_min <- weekends$cost/weekends$duration
weekdays$cost_per_min <- weekdays$cost/weekdays$duration

usage <- rev(usage[order(usage$date),])
levels(usage$is_weekend) <- gsub("False", "#111111", levels(usage$is_weekend))
levels(usage$is_weekend) <- gsub("True", "#ff336600", levels(usage$is_weekend))

## END reorganize data ##

## START graphing ##
par(mar=c(4.1, 4.1, 1.1, .1))
pdf("calls_by_day.pdf", width=10, height=8)
barplot(usage$calls, main="Total Number of Calls per Day", horiz=TRUE, names.arg=usage$date, axis.lty=1, las=2, beside=TRUE, col=usage$is_weekend, cex.lab=0.5)
dev.off()

pdf("cost_by_day.pdf", width=10, height=8)
barplot(usage$cost_per_min, main="Cost per Minute by Day", horiz=TRUE, names.arg=usage$date, axis.lty=1, las=2, beside=TRUE, col=usage$is_weekend, cex.lab=0.5)
dev.off()

pdf("weekend_calls.pdf", width=12, height=5)
hist(weekends$calls, breaks=20, main="Weekends Calls", col="#ff3366cc")
dev.off()

pdf("weekdays_calls.pdf", width=12, height=5)
hist(weekdays$calls, breaks=20, main="Weekdays Calls", col="#cccccc88")
dev.off()

pdf("weekend_cost_per_min.pdf", width=12, height=5)
hist(weekends$cost_per_min, breaks=20, main="Weekends - Cost per Minute", col="#ff3366cc")
dev.off()

pdf("weekdays_cost_per_min.pdf", width=12, height=5)
hist(weekdays$cost_per_min, breaks=20, main="Weekdays - Cost per Minute", col="#cccccc88")
dev.off()

pdf("weekend_vs_weekdays_calls.pdf", width=12, height=5)
hist(weekdays$calls, breaks=200, col="#cccccc88", freq=F)
hist(weekends$calls, breaks=200, main="Calls", col="#ff3366cc", add=TRUE, freq=F)
dev.off()
