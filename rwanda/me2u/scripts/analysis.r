## process.r
##
## Generates graphs based on the person aggregate csv files.
##

## Read in data from aggregated text files

#data <-read.table("join.date.unique.contacts.txt", header=TRUE, sep="|", strip.white=TRUE)
#data$date <- as.Date(data$date, "%Y-%m-%d")

#png("join.date.unique.contacts.png", width=8000,height=700)
#plot.new()
#plot(data$date, data$count, xlab="Joined Date", ylab="# of Unique Contacts for All Years")
#daterange=c(as.POSIXlt(min(data$date)),as.POSIXlt(max(data$date)))
#axis.POSIXct(1, at=seq(daterange[1], daterange[2], by="month"), format="%b")
#lines(lowess(data$date,data$count, f=3/10))
#title("Join Date + Unique Contacts")
#dev.off()

#png("join.date.amount.png", width=1000, height=700)
#plot.new()
#plot(data$date, data$amount, xlab="Joined Date", ylab="Total Amount of Transfers Per User")
#daterange=c(as.POSIXlt(min(data$date)),as.POSIXlt(max(data$date)))
#axis.POSIXct(1, at=seq(daterange[1], daterange[2], by="month"), format="%b")
#lines(lowess(data$date,data$amount, f=3/10))
#title("Join Date + Total Amount Received")
#dev.off()

#data <-read.table("amount.transfers.likelihood.to.join.txt", header=TRUE, sep="|", strip.white=TRUE)
#png("amount.transfers.likelihood.png", width=8000, height=700)
#plot.new()
#data2 = aggregate(data$joined, list(data$amount), sum)
#plot(data2$Group.1, data2$x, xlab="Total Amount of Transfers Per User", ylab="Incidences of Joining", xlim = c(0, 50000))
#title("Amount of Transfers vs Likelihood to Join")
#dev.off()

#data <-read.table("amount.transfers.likelihood.to.join.txt", header=TRUE, sep="|", strip.white=TRUE)
#png("amount.transfers.likelihood0-1000-50000.png", width=8000, height=700)
#plot.new()
#hist(data$amount, breaks=50000, xlim=c(0,1000))
#plot(data2$Group.1, data2$x, xlab="Total Amount of Transfers Per User", ylab="Incidences of Joining", xlim = c(0, 1000))
#title("Amount of Transfers vs Likelihood to Join")
#dev.off()

data <-read.table("didnt_receive_before_joining", header=TRUE, sep="\n", strip.white=TRUE)
png("didnt-receive-before-joining.png", width=1000, height=700)
plot.new()
hist(c(data$distance), breaks=1000, xlim=c(0,1000))
title("Distance between Sender and Receiver; didn't receive before joining")
dev.off()

data <-read.table("received_before_joining", header=TRUE, sep="\n", strip.white=TRUE)
png("received-before-joining.png", width=1000, height=700)
plot.new()
hist(c(data$distance), breaks=1000, xlim=c(0,1000))
title("Distance between Sender and Receiver; Did receive before joining")
dev.off()

histplot <- function(dat, breaks="Sturges", ncurve=TRUE, maxnorm = 0, ...) 
{ 
        #compute the histogram and density of "dat" 
        hdat <- hist(dat, breaks=breaks, plot=F) 
        ddat <- density(dat) 
        
        #compute the xlim and ylim of the plot 
        # i.e. the min and max of the different superimposed 
        #plots (hist, density and normal curves) 
        xlim <- range(ddat$x) 
        if(ncurve) 
        { 
                #max of the normal curve	
                #maxnorm <- pnorm(mean(dat), mean=mean(dat), sd=sd(dat)) 
                ylim <- c(0,  max(hdat$density,ddat$y,maxnorm)) 
        } 
        else 
        { 
                ylim <- c(0,  max(hdat$density,ddat$y)) 
        } 
        
        #plotting 
        plot(hdat, 
                #freq=F, 
                xlim=xlim, ylim=ylim, ...) 
        lines(ddat) 
        if (ncurve) curve(dnorm(x, mean=mean(dat), sd=(sd(dat))), 
                                lty=3, add=TRUE) 
} 

data <-read.table("received_before_joining", header=TRUE, sep="\t", strip.white=TRUE)
png("incoming-amt-received-before-joining-hist-3000.png", width=1000, height=700)
plot.new()
#histplot(data$incomingamt, breaks=50000, maxnorm = 3000)
#histplot(data$incomingamt, ncurve=F)
#histplot(data$incomingamt, col="blue")
hist(c(data$incomingamt), breaks=50000, col="red", xlim=c(0,3000), ylim=c(0,2500))
#plot(density(data$incomingamt), col='green', xlim=c(0,3000), add=TRUE)
#curve(dnorm(data$incomingamt, mean=mean(data$incomingamt), sd=sd(data$incomingamt)),col='blue', add=TRUE)
#d <- density(data$incomingamt) # returns the density data 
#density(data$outgoingamt, add = TRUE) # returns the density data 
#plot(d)
#hist(c(data$outgoingamt), breaks=50000, col="green", xlim=c(0,3000), add=TRUE)
#curve(dnorm, col = 3, add = TRUE)
title("Incoming amount for users who received before joining")
dev.off()

png("incoming-amt-received-before-joining-hist.png", width=1000, height=700)
plot.new()
hist(c(data$incomingamt), breaks=50000, col="red", ylim=c(0,2500))
title("Incoming amount for users who received before joining")
dev.off()

png("incoming-amt-received-before-joining-curve-3000.png", width=1000, height=700)
plot.new()
plot(density(data$incomingamt), col='green', xlim=c(0,3000))
title("Incoming amount for users who received before joining")
dev.off()

png("incoming-amt-received-before-joining-curve.png", width=1000, height=700)
plot.new()
plot(density(data$incomingamt), col='green')
title("Incoming amount for users who received before joining")
dev.off()

png("outgoing-amt-received-before-joining-curve.png", width=1000, height=700)
plot.new()
plot(density(data$outgoingamt), col='green')
title("Outgoing amount for users who received before joining")
dev.off()

png("outgoing-amt-received-before-joining-curve-3000.png", width=1000, height=700)
plot.new()
plot(density(data$outgoingamt), col='green', xlim=c(0,3000))
title("Outgoing amount for users who received before joining")
dev.off()

png("outgoing-amt-received-before-joining-hist-3000.png", width=1000, height=700)
plot.new()
hist(c(data$outgoingamt), breaks=50000, col="red", xlim=c(0,3000), ylim=c(0,2500))
title("Outgoing amount for users who received before joining")
dev.off()

png("outgoing-amt-received-before-joining-hist.png", width=1000, height=700)
plot.new()
hist(c(data$outgoingamt), breaks=50000, col="red", ylim=c(0,2500))
title("Outgoing amount for users who received before joining")
dev.off()


###############

data <-read.table("didnt_receive_before_joining", header=TRUE, sep="\t", strip.white=TRUE)
png("incoming-amt-didnt-receive-before-joining-hist-3000.png", width=1000, height=700)
plot.new()
hist(c(data$incomingamt), breaks=50000, col="red", xlim=c(0,3000), ylim=c(0,2500))
title("Incoming amount for users who didn't receive before joining")
dev.off()

png("incoming-amt-didnt-receive-before-joining-hist.png", width=1000, height=700)
plot.new()
hist(c(data$incomingamt), breaks=50000, col="red", ylim=c(0,2500))
title("Incoming amount for users who didn't receive before joining")
dev.off()

png("incoming-amt-didnt-receive-before-joining-curve-3000.png", width=1000, height=700)
plot.new()
plot(density(data$incomingamt), col='green', xlim=c(0,3000))
title("Incoming amount for users who didn't receive before joining")
dev.off()

png("incoming-amt-didnt-receive-before-joining-curve.png", width=1000, height=700)
plot.new()
plot(density(data$incomingamt), col='green')
title("Incoming amount for users who didn't receive before joining")
dev.off()

png("outgoing-amt-didnt-receive-before-joining-curve.png", width=1000, height=700)
plot.new()
plot(density(data$outgoingamt), col='green')
title("Outgoing amount for users who didn't receive before joining")
dev.off()

png("outgoing-amt-didnt-receive-before-joining-curve-3000.png", width=1000, height=700)
plot.new()
plot(density(data$outgoingamt), col='green', xlim=c(0,3000))
title("Outgoing amount for users who didn't receive before joining")
dev.off()

png("outgoing-amt-didnt-receive-before-joining-hist-3000.png", width=1000, height=700)
plot.new()
hist(c(data$outgoingamt), breaks=50000, col="red", xlim=c(0,3000), ylim=c(0,2500))
title("Outgoing amount for users who didn't receive before joining")
dev.off()

png("outgoing-amt-didnt-receive-before-joining-hist.png", width=1000, height=700)
plot.new()
hist(c(data$outgoingamt), breaks=50000, col="red", ylim=c(0,2500))
title("Outgoing amount for users who didn't receive before joining")
dev.off()



###############

data <-read.table("didnt_join", header=TRUE, sep="\t", strip.white=TRUE)
png("incoming-amt-didnt-join-hist-3000.png", width=1000, height=700)
plot.new()
hist(c(data$incomingamt), breaks=50000, col="red", xlim=c(0,3000), ylim=c(0,2500))
title("Incoming amount for users who didn't join")
dev.off()

png("incoming-amt-didnt-join-hist.png", width=1000, height=700)
plot.new()
hist(c(data$incomingamt), breaks=50000, col="red", ylim=c(0,2500))
title("Incoming amount for users who didn't join")
dev.off()

png("incoming-amt-didnt-join-curve-3000.png", width=1000, height=700)
plot.new()
plot(density(data$incomingamt), col='green', xlim=c(0,3000))
title("Incoming amount for users who didn't join")
dev.off()

png("incoming-amt-didnt-join-curve.png", width=1000, height=700)
plot.new()
plot(density(data$incomingamt), col='green')
title("Incoming amount for users who didn't join")
dev.off()





png("incoming-no-didnt-join-hist.png", width=1000, height=700)
plot.new()
hist(c(data$incomingno), breaks=1000, col="red")
title("Incoming # for users who didn't join")
dev.off()

png("incoming-no-didnt-join-curve.png", width=1000, height=700)
plot.new()
plot(density(data$incomingno), col='green')
title("Incoming # for users who didn't join")
dev.off()



#data <-read.table("received_before_joining", header=TRUE, sep="\t", strip.white=TRUE)
#png("outgoing-amt-received-before-joining.png", width=1000, height=700)
#plot.new()
#hist(c(data$outgoingamt), breaks=50000, xlim=c(0,3000))
#title("Outgoing amount for users who received before joining")
#dev.off()

png("incoming-no-didnt-join-curve.png", width=1000, height=700)
plot.new()

didnt_receive <-read.table("didnt_receive_before_joining.csv", header=TRUE, sep="\t", strip.white=TRUE)
received <-read.table("received_before_joining.csv", header=TRUE, sep="\t", strip.white=TRUE)
didnt_join <- read.table("didnt_join.csv", header=TRUE, sep="\t", strip.white=TRUE)
d <- density(didnt_receive$distance) 
plot(d)

library(sm)
attach(didnt_receive)
attach(received)
#cyl.f <- factor(cyl, levels= c(4,6,8),
#  labels = c("4 cylinder", "6 cylinder", "8 cylinder")) 

sm.density.compare(didnt_receive$distance, received$distance, xlab="Distance")
title(main="Distance between Sender and Receiver for Two Groups")

# add legend via mouse click
#colfill<-c(2:(2+length(levels(cyl.f)))) 
#legend(locator(1), levels(cyl.f), fill=colfill)

library(ggplot2)
png("density_plots/comparing-incoming-between-received-didnt-receive.png", width=1000, height=700)
plot.new()
plot(density(didnt_receive$incomingamt),col='green')
lines(density(received$incomingamt),col='blue')
lines(density(didnt_join$incomingamt),col='red')
dev.off()

library(ggplot2)
png("density_plots/comparing-outgoing-between-received-didnt-receive.png", width=1000, height=700)
plot.new()
plot(density(didnt_receive$outgoingamt),col='green')
lines(density(received$outgoingamt),col='blue')
lines(density(didnt_join$outgoingamt),col='red')
dev.off()

library(ggplot2)
png("density_plots/comparing-incomingno.png", width=1000, height=700)
plot.new()
plot(density(didnt_join$incomingno),col='red')
lines(density(received$incomingno),col='blue')
lines(density(didnt_receive$incomingno),col='green')
dev.off()


png("density_plots/comparing-outgoingno.png", width=1000, height=700)
plot.new()
plot(density(received$outgoingno),col='blue')
lines(density(didnt_receive$outgoingno),col='green')
dev.off()