library(dplyr)
library(rjson)
library(purrr)

json_file <- "data/first-move-simulation.json"
data <- rjson::fromJSON(file = json_file)

px <- data %>%
  lapply(function(x) as.vector(unlist(x))) %>%
  lapply(function(x) x / length(data))

logpx <- px %>%
  lapply(function(x) log(1 / x, base = 2))

pxlogpx <- purrr::map2(px, logpx, function(x, y) x * y)

score  <- pxlogpx %>% 
  lapply(function(x) sum(x, na.rm = TRUE))
