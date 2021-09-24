library(ipfp)

int_expand_vector <- function(x){
  index <- 1:length(x)
  rep(index, round(x))
}

## read data
ind <- read.csv("franklin/microdata/ipf/ohio_ind.csv")
ind_sub <- ind[sample(nrow(ind), as.integer(nrow(ind) * 0.3)), ]
cons <- read.csv("franklin/microdata/ipf/franklin_cons_3904107.csv")

## some pre-processing
cons <- subset(cons, select = -c(GEOID10))
weights <- array(NA, dim=c(nrow(ind_sub),nrow(cons))) # Create 2D weight matrix (individuals, areas)
cons <- apply(cons, 2, as.numeric) # convert the constraints to 'numeric'
ind_sub <- apply(ind_sub, 2, as.numeric) # convert the individuals to 'numeric'
ind_subt <- t(ind_sub) # transpose the dummy variables for ipfp
x0 <- rep(1, nrow(ind_sub)) # set the initial weights

## ipf
weights <- apply(cons, 1, function(x)
  ipfp(x, ind_subt, x0, maxit = 20))
weights2 <- weights[ , colSums(is.na(weights)) == 0]

## check if weights are appropriate
ind_agg <- t(apply(weights2, 2, function(x) colSums(x * ind_sub)))
cor(as.numeric(ind_agg), as.numeric(cons)) # fit between contraints and estimate

## generate integerised result
ints <- unlist(apply(weights, 2, function(x) int_expand_vector(int_trs(x)))) 
