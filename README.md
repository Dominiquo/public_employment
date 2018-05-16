# public_employment
Repository for scraping and parsing Chilean public employment data

## Goal
The goal of this project is to scrape and analyze  [Chilean Public Employment Data](http://www.empleospublicos.cl/). 

The Public Employment website provides an avenue for each ministry to post open positions. These postings include information on the requirements of the job as well as more descriptive features such as the ministry, vacancy type and gross salary. Each posting is either open, in evaluation or finalized, with most in the finalized state. 

These job posting provide insight into the Chilean Public Sector Job Market via the information in each posting. This data can also be linked to other databases as I have done here with the [Ministry Personnel Budget](http://www.dipres.gob.cl/). 

In this repository, I have provided the code used to retrieve each job posting and parse its content for useful information while storing the entire html file of the listing locally. I also have dive into some basic analysis of the data using Python Pandas. 

## The Data
In short, we have all data from individual postings, which can be seen in the `stored_pages/`  folder as well as results for the posting which can be found in the `data/` folder. 

The original data retrieved is a series of HTML files from the [Public employment website](http://www.empleospublicos.cl/). When selecting "ver ficha" on the right of each listing, there is a small form with filled information fields regarding the opening. This is the HTML file stored by the scraper. 

Originally the scraper was built to traverse the entire Public Employment Website, but this was not sufficient for retrieving past postings. To retrieve all posting back to August 2009, I had to iterate through each posting individually as they are indexed via their URL with a category type. Examples of job postings can be found in the `stored_pages/` folder of the repository.

The discovery of the indexed URL allowed for me retrieve files that were not readily available through links on the website, however, some of these postings are blank and if the index is beyond the most recent file, more blank files are returned. Essentially, the Public Employment Website fails silently, but this can be cleaned up during data analysis.

Within each posting, there is a large and varied amount of information. With my initial approach, I parsed the most easily obtainable and quantifiable data, which is the data in the main fields.  Again, check  `stored_pages/`  for examples of this. 

Main Fields Include:
- Ministerio
- Institución / Entidad
- Cargo
- Nº de Vacantes
- Área de Trabajo
- Región
- Ciudad
- Tipo de Vacante
- Calendarización del Proceso

Along with the body of the posting which can include information on "Objetivo del Cargo", "Mecanismo de Postulación" among others. The body of each post **varies greatly** from post to post. Though there is useful information in the body, it will take significantly more work to extract with diminishing returns on time. 

Outside of the posts themselves, there is information on the result of each finalized posting. These were scraped from the same website with the same ID matching to the post itself, but has a different base link meaning it needs to be scraped independently. Examples of results values are "EMPLEO AÚN SIN RESULTADO", "EMPLEO DECLARADO DESIERTO", "EMPLEO DEJADO SIN EFECTO", or the name of the person(s) that received the position. 

Prior to analysis, I also infer some values based on the information provided in the postings and results. I will examine this more in a later section.

## Retrieve

After finding the pattern of each URL, retrieving the files is easy. Review the `retreive/retreive_postings.py` file for more information. 

## Parsing
I currently do just about all of the work for each post in two files, `public_employment/parsing/PostingHandler.py` and `public_employment/parsing/calendar_parsing.py`. 

`PostingHandler.py` takes a post and extracts all of the mentioned fields and sends the process calendar off to `calendar_parsing.py` for information on the calendar.

To continue to build this parser, I would recommend just making more classes for sections of the post that you want and adding this as a method to `PostingHandler.py`. 

To describe the logic in  `calendar_parsing.py` a bit more, the idea was to infer things like `DAYS_OPEN`, `DAYS_SELECT`, and `PROC_TIME` by checking the calendars for key words like "Difusión" and "Finalización" in the calendar and check whether these dates are in fact the first and last date values to occur. The dates that don't meet this criterion are thrown away. About 5% total postings are thrown away for not meeting this criterion.

## Analysis

Before we can analyze, we need to take the parsed data and actually create a Pandas DataFrame. This is primarily done in `public_employment/parsing/aggregate.py`. Each field in the final CSV is taken from the parsed data, results or directly from the filename (page ID is inferred based on the string formatting).

After the CSV is made, `public_employment/analysis/transformation_pipeline.py` is used to add any changes to the csv (cleaning, transformations, etc). The idea is to just add a serialized list of transformation to have a single pipeline such that we can run the data from start to finish.

The final step is producing results from this data. In the `view_graphs.ipynb` file, it's possible to see the already created plots. Each plot is defined in the `public_employment/analysis/produce_results.py` file. These functions are grouped by those that actually produce a plot and those that produce the underlying dataframe that is used to plot. This is signified by the `_plot` or `_df` as the suffix to each function name. 

