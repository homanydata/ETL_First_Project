# ETL_First_Project
Updates habits data from new data from Telegram Bot into Postgresql DB using python script and updates real-time PowerBI Dashboard


## PROJECT OVERVIEW:
- postgresql for database, 4 tables:
    - dim_habits
    - dim_users
    - fact_records
    - staging_table
- telegram bot built using python telebot library that receives new records
- python script that handles new records and initiates migration
- migration to create/update warehouse tables (dim tables and agg_tables and views) using psycopg2 library
- PowerBI Dashboard is connected to views
- Quick Brief text summaries or plot images can be provided through telegram bot (pandas, matplotlib & excel in background)

## Components
### BOT:
- when initiated:
    - a bot is created with attributes token (from .env) and db_session from Enums in lookups module
    - migration is scheduled on regular basis (time is specified from lookups module)
- commands:
    - `start`: sends bot description and use
    - `record`: starts recording process, asks and reads habit, duration, and records user and timestamp, adds that to staging table
    - `add category`: adds a new category
    - `day`/`week`/`month`/`year`: sends text message summary of this week/month/year
    - `alldata`: asks for confirmation and sends excel file of all of this user records
    - `summarize`: chooses a habit and gets a plot image summary for it

### DATABASE HANDLER:
Offers basic methods to connect to db:
- Create connection
- Refresh connection (will be used after every migration)
- Close connection
- Execute query a helper method for any query needs to be executed
- Get query result (helper method)
- Get query result as pandas dataframe
- Add new category to dim_category because it is independent from others
- Get distinct categories
- Get distinct habits
- Get habit category (to simplify recordig process with user)

### LOOKUPS:
Messages, markups, enums, erros outputs, directories... and any needed saved values will be here

### MIGRATION:
For flyway migration we will only use the logic, loop over sql_files and run them in order, which are:
- **V0**: Create schema
- **V1**: Create staging table
- **V2**: Insert record into staging table, it contains habit_name, user_id and all its details, duration, timestamp
- **V3**: Create dim_category, dim_habit & dim_user
- **V4**: If new record contains a new habit or new user, add that to dim_habits or dim_users accordingly
- **V5**: Create fact table
- **V6**: Add record to fact_records table with habit_id and user_id needed
- **V7**: Create agg_daily table
- **V8**: Update agg_daily (or V9 if it is a test)
- **V10**: Create views
- **V11**: Truncate staging table

### DASHBOARD:
We will create a real-time dashboard that shows:
- Line graph of number of active users over time
- Line graph of total duration over time
- Bar chart of favourite habits
- Pie chart of categories

with a slicer by users full names

### VIEWS:
- For the 3 line graphs, all get their data from same table, daily_view
which includes daily total records and total_duration for each user for each habit
- For the last bar graph we need a view that shows for each habit total records and total_duration for each user

### PANDAS HANDLER:
Offers basic methods to get specific results for users:
- Return query as text
- Get user records
- Get user this day/week/month/year summary
- Get plot image (runs query to get needed df, then, uses create_plot_image from plot_creator module to return plot image)

It uses prepared summaries sql commands

### Plot Creator:
Its goal is to use matplotlib to create plots from 2 columns dataframes and return it as image
    - Has general create_plot_image method that uses either create_bar_chart or create_line_graph method
    - Then return_plot_as_image method to change a dataframe to image of a plot

### Excel Handler:
- DataFrame to excel method
- Delete excel file method

### SUMMARIES SQL COMMANDS:
Needed sql queries to get data for any type of summary for user
- All user records
- Interval summary (this day/week/month/year): results grouped by habits over a specific interval
- Variable summary
- Variable type parts distribution (totals for each habit/category)

### MAIN:
Create a bot instance

An independent thread is created to run any pending job in schedule
run the bot instance