library(testthat)


test_that("parse_filename_info works for valid input", {
  source("../src/csv_reader.R")
  file_path <- "test_assets/ARK_2022-08-13_18h00.csv"
  result <- parse_filename_info(file_path)

  expect_equal(result$token_name, "ARK")
  expect_equal(result$event_date_str, "2022-08-13")
  expect_equal(result$event_time_str, "18:00")
  expect_s3_class(result$event_datetime, "POSIXlt")
  expect_equal(format(result$event_datetime, "%Y-%m-%d %H:%M"),
               "2022-08-13 18:00")
})

test_that("parse_filename_info fails if input is not a string", {
  expect_error(parse_filename_info(123), "`file_name` must be a string path to a CSV file.")
  expect_error(parse_filename_info(TRUE), "`file_name` must be a string path to a CSV file.")
})

test_that("parse_filename_info fails if file does not exist", {
  fake_file <- tempfile(pattern = "ARK_2022-08-13_18h00", fileext = ".csv")
  expect_error(parse_filename_info(fake_file), "`file_name` must be a string path to a CSV file.")
})

test_that("parse_filename_info fails with invalid date", {
  tmp <- tempfile(pattern = "ARK_2022-13-40_18h00", fileext = ".csv")
  file.create(tmp)
  expect_error(parse_filename_info(tmp), "File name must follow format")
  unlink(tmp)
})

test_that("parse_filename_info fails with invalid time", {
  tmp <- tempfile(pattern = "ARK_2022-08-13_25h99", fileext = ".csv")
  file.create(tmp)
  expect_error(parse_filename_info(tmp), "File name must follow format")
  unlink(tmp)
})
