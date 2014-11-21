
# Read in all the users and their features
allusers <- read.table("users_all.csv", header=TRUE, strip.white=TRUE, sep=',')
users <- read.table("users_mobility_0.csv", header=TRUE, strip.white=TRUE, sep=',')
# Merge the user mobility features
fullusers <- merge(allusers, users, by.x = "mobile", by.y="uid")

# Divide users up by region
kampala <- subset(fullusers, fullusers$region == "KampalaCentral")
eastern <- subset(fullusers, fullusers$region == "Eastern")
western <- subset(fullusers, fullusers$region == "Western")
northern <- subset(fullusers, fullusers$region == "Northen")

# Merge user locations with stats about each location
fusers <- merge(fullusers, towerstats, by.x="loc.x", by.y="sitename.C.254")
urbanusers <- subset(fusers, fusers$Urban.N.4.0 == 1)
ruralusers <- subset(fusers, fusers$Urban.N.4.0 == 0)
