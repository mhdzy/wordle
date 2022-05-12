library(dplyr)
library(forcats)
library(magrittr)
library(plotly)
library(purrr)
library(rjson)
library(tibble)

json_file <- "data/first-move-simulation-new-mp.json"
data <- rjson::fromJSON(file = json_file)

px <- data %>%
  lapply(function(x) as.vector(unlist(x))) %>%
  lapply(function(x) x / length(data))

logpx <- px %>%
  lapply(function(x) log(1 / x, base = 2))

pxlogpx <- purrr::map2(px, logpx, function(x, y) x * y)

scores <- pxlogpx %>%
  lapply(function(x) sum(x, na.rm = TRUE))

scoredf <- tibble::tibble(
  word = names(scores),
  score = unlist(scores)
)

arranged_scores <- scoredf %>%
  arrange(desc(score))

r2 <- sapply(strsplit(arranged_scores$word, ""), anyDuplicated, fixed = TRUE)

nonduplicated <- arranged_scores[which(r2 == 0), ]

ans <- readr::read_csv("data/answers.txt", col_names = "word")
ans_scores <- dplyr::left_join(ans, scoredf, by = 'word')
ans_scores %>%
  arrange(desc(score))

word_df_list <- lapply(data, function(x) tibble(feedback = names(x), remainder = unlist(x)))
word_df <- purrr::map2(word_df_list, names(word_df_list), function(x, y) dplyr::mutate(x, word = y))
word_tbl <- dplyr::bind_rows(word_df)

(word_tbl %>%
  dplyr::filter(
    word == 'slate',
    remainder > 0
  ) %>%
  dplyr::mutate(
    feedback = forcats::fct_reorder(
      factor(feedback, ordered = TRUE),
      desc(remainder)
    ),
    remainder_pct = remainder / length(unique(scoredf$word))
  ) %>%
  ggplot2::ggplot(aes(x = feedback, y = remainder_pct)) +
  ggplot2::geom_bar(stat = 'identity') +
  ggplot2::theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1))

) %>%
plotly::ggplotly()
