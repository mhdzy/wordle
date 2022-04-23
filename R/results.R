library(dplyr)
library(readr)

results <- "data/test.csv" |>
  readr::read_csv(col_names = "score")

summary <- results |>
  dplyr::group_by(score) |>
  dplyr::summarise(count = n()) |>
  dplyr::mutate(pct = paste0(round(count/nrow(results) * 100, 2), "%"))

wins <- results |>
  dplyr::filter(score > 0)

hist(as.numeric(wins$score), breaks = length(unique(wins$score)))

mean(wins$score)
