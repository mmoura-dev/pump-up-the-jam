library(readr)


parse_filename_info <- function(file_name) {
  
  if (!is.character(file_name) || !file.exists(file_name)) {
    stop("`file_name` must be a string path to a CSV file.")
  }
  
  base_name <- basename(file_name)
  no_ext <- sub("\\.csv$", "", base_name)
  parts <- strsplit(no_ext, "_")[[1]]

  if (length(parts) != 3 ||
      !grepl("^[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$", parts[2]) ||
      !grepl("^([0-1][0-9])|(2[0-3])h[0-5][0-9]$", parts[3])
     ) {
    stop("File name must follow format: <token>_%Y-%m-%d_%Hh%M.csv")
  }

  event_time_str <- sub("h", ":", parts[3])
  return(list(
    token_name = parts[1],
    event_date_str = parts[2],
    event_time_str = event_time_str,
    event_datetime = strptime(paste0(parts[2], "T", event_time_str,"Z"),
                              format = "%Y-%m-%dT%H:%M", tz = "UTC")
  ))
}

read_trading_records_csv <- function(file_name) {
  event_info <- parse_filename_info(file_name)

  df <- read_csv(
    file = file_name,
    col_types = readr::cols(
      symbol = readr::col_character(),
      timestamp = readr::col_character(),
      datetime = readr::col_datetime(format = "%Y-%m-%dT%H:%M:%OSZ"),
      side = readr::col_character(),
      price = readr::col_double(),
      amount = readr::col_double(),
      btc_volume = readr::col_double(),
      trade_id = readr::col_integer(),
      is_buyer_maker = readr::col_logical(),
      is_best_match = readr::col_logical()
    )
  )

  df$timestamp <- bit64::as.integer64(df$timestamp)
  # df$timestamp <- as.POSIXct(df$timestamp / 1000, origin = "1970-01-01", tz = "UTC")

  event_info$df <- df
  return(event_info)
}

# trades <- read_trading_records_csv("datasets/bello2023/trading_records/ARK_2022-08-13_18h00.csv")
# print(head(trades, 15))
