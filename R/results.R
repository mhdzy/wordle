library(dplyr)
library(readr)

results <- "data/test.csv" %>%
  readr::read_csv(col_names = "score")

summary <- results %>%
  dplyr::group_by(score) %>%
  dplyr::summarise(count = n()) %>%
  dplyr::mutate(pct = paste0(round(count / nrow(results) * 100, 2), "%"))

wins <- results %>%
  dplyr::filter(score > 0)

hist(as.numeric(wins$score), breaks = length(unique(wins$score)))

mean(wins$score)

### NEW STUFF ? ###

library(dplyr)
library(ggplot2)
library(readr)

read2 <- function(id = "", tbl) {
  tbl %>%
    readr::read_csv(col_names = "score") %>%
    dplyr::mutate(id = id)
}

summary2 <- function(tbl) {
  tbl %>%
    dplyr::group_by(id, score) %>%
    dplyr::summarise(count = n()) %>%
    dplyr::mutate(pct = paste0(round(count / nrow(tbl) * 100, 2), "%"))
}

# comparing runtimes
results <- list(
  "old" = read2("old", "data/test-old-100k.csv"),
  "new" = read2("new", "data/test-new-100k.csv")
)

summary <- dplyr::bind_rows(lapply(results, summary2))

wins <- dplyr::bind_rows(results) %>%
  dplyr::filter(score > 0)

mean(wins$score)
hist(as.numeric(wins$score), breaks = length(unique(wins$score)))

wins %>%
  ggplot2::ggplot(aes(x = score, color = id, fill = id)) +
  ggplot2::geom_histogram(
    binwidth = 1.2,
    alpha = 0.8,
    position = "dodge"
  ) +
  ggplot2::labs(title = "\nWordle Solver before & after\n", x = "\n# of turns\n", y = "\nfrequency\n") +
  ggplot2::theme(plot.title = element_text(hjust = 0.5))


wins_barchart <- wins %>%
  dplyr::group_by(id, score) %>%
  dplyr::summarise(
    count = n(),
    ratio = count / (nrow(wins) / length(unique(id))),
    pct = round(ratio * 100, 2),
    pct_str = paste0(pct, "%")
  )

wins_barchart %>%
  ggplot2::ggplot(aes(x = score, y = pct, fill = id)) +
  ggplot2::geom_col(width = 1, position = position_dodge(0.7), alpha = 0.9) +
  ggplot2::labs(
    title = paste0(
      "\nWordle Solver before & after (games=",
      prettyNum(
        formatC(nrow(wins) / length(unique(wins$id)), format = "d"),
        big.mark = ","
      ),
      ")\n"
    ),
    x = "\n# of turns (n)\n",
    y = "\nfrequency (pct)\n"
  ) +
  ggplot2::theme(plot.title = element_text(hjust = 0.5))
