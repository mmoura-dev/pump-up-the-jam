library(testthat)
library(readr)
library(bit64)


test_that("read_trading_records_csv parses valid file correctly", {
  source("../src/csv_reader.R")
  file_path <- "test_assets/ARK_2022-08-13_18h00.csv"
  result <- read_trading_records_csv(file_path)

  # --- Check metadata from filename ---
  expect_equal(result$token_name, "ARK")
  expect_equal(result$event_date_str, "2022-08-13")
  expect_equal(result$event_time_str, "18:00")
  expect_s3_class(result$event_datetime, "POSIXlt")

  # --- Check dataframe is present ---
  expect_true("df" %in% names(result))
  df <- result$df

  # --- Check dataframe structure ---
  expect_s3_class(df, "data.frame")
  expect_gt(nrow(df), 0)
  expect_equal(ncol(df), 10)

  # --- Check column types ---
  expect_s3_class(df$timestamp, "integer64")
  expect_s3_class(df$datetime, "POSIXct")
  expect_type(df$symbol, "character")
  expect_type(df$side, "character")
  expect_type(df$price, "double")
  expect_type(df$amount, "double")
  expect_type(df$btc_volume, "double")
  expect_type(df$trade_id, "integer")
  expect_type(df$is_buyer_maker, "logical")
  expect_type(df$is_best_match, "logical")
})
