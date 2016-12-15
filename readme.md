# Project Summary

When companies listed on the Australian Stock Exchange (ASX) have price sensitive information they need to release to the market, they release it via a public announcement. This announcement is normally accompanied by a movement in the price of the stock of the company up or down due to the new information.
Also released by companies on a day-to-day basis are other announcements which are not price sensitive individually, however when combined together, may provide predictive information as to future price sensitive announcements.

This codebase was used in studying whether or not historical non-price sensitive ASX announcements can be used as predictors for future price sensitive announcements.

# Project Motivation

Profit :)

# Data Availability

Data for this project was sourced available from the ASX website in html and pdf form.

# Project Components

The following tasks were carried out as part of this work:
* ASX announcement data sourcing and insertion into a database.
* Data grouping according to whether or not an announcement is followed (after a certain predetermined time) by a price sensitive announcement.
* Data labelling according to grouping and associated price move.
* Creation of text corpora and usage of these corpora to to generate a term-matrix for use as features in a predictive model.
* Dimensionality reduction.
* Predictive model build and test.
* Result reporting.

# Usage

Analysis is run out of text_mining.py.

# Last Words

That fact that I'm publishing this code base should be telling as to the success of the predictive model :)
That being said there's some possible ways to improve the model but I'll leave that up to the user.

# License

Copyright (c) 2016 Andre de San Miguel

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
