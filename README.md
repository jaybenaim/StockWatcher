---
title: StockWatcher
description: Get alerts and watch your favourite stocks
date: "2021-10-15"
repository: /jaybenaim/StockWatcher
published: false
---

Get live stock data from Yahoo and create alerts when they hit the set price

## Features

- **Pull Live Stock Data:** Obtain recent stock prices directly from NASDAQ.
- **Custom Alerts:** Set price thresholds to receive notifications, ensuring you're informed when stock prices meet your criteria.

The front-end code can be found [here](https://github.com/jaybenaim/StockWatcherClient).

## Built with

StockWatcher is built using the following technologies:

### Front-end

- [React](https://reactjs.org/): Converted into a React project to improve UI design.
- [Django](https://www.djangoproject.com/): A high-level Python web framework that encourages rapid development and clean, pragmatic design.

### Back-end

- [Python](https://www.python.org/): A high-level programming language known for its simplicity and readability.
- [Django](https://www.djangoproject.com/): A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- [Celery](https://docs.celeryq.dev/en/stable/index.html): A distributed task queue that helps execute tasks asynchronously or scheduled. Used to get live updates incrementally throughout the opening-closing hours of the market.
