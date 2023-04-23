# tht
take home test; submission for review

General:
_______________________________________________________________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________________________________________________________

Tools used (and needed): 
	- PostgreSQL
	- pgAdmin 4,
	- Python 3.10.4,
	- Anaconda (Spyder)
	- CMD (Windows 10)
_______________________________________________________________________________________________________________________________________________________________________

Python libraries used:
	- psycopg2 for establishing a connection to DB,
	- Pandas for conversion of query results to readable dataframes,
	- json for conversion of dataframes to json objects,
	- fast API for API implementation,
	- plotly for chart creation,
	- streamlit for quick web app creation
_______________________________________________________________________________________________________________________________________________________________________

Steps I followed:

1. DB creation:

Source: https://github.com/pthom/northwind_psql

- In pgAdmin, go to Object > Create > Server Group, name as needed (in my case, it's tht_alikhalaf_northwind)
- Right-click on newly-generated server group from previous step, then choose Register > Server
- Name server as needed (in my case, it's tht_alikhalaf_northwind_server)
- In the Connection tab, set hostname / address to "localhost" and enter the master password in the relevant tab; keep all else same, and click Save
- Right-click on newly-generated server, then Create > Database; under General, name DB as needed (my case, tht_alikhalaf_northwind_db)
- Make sure you're in the required DB domain in the tree view (e.g., left click once on tht_alikhalaf_northwind_db), then from the ribbon menu: Tools > Query Tool; then paste content from provided .sql file and run (press F5 on keyboard) to create the schema and constituent tables; you should see a success message with the runtime (to see the created tables in the tree view, I had to restart pgAdmin)

2. Establishing a connection to DB, API, and "web app" creation:

- Please see commentary in the provided .py file; you will need to make sure that the passed values for the psycopg2 connection instance, including database and password, conform to the set values for the DB (from pgAdmin).
- You will also find the queries that were written to process the data and arrive at the results required for this exercise (they will be defined as variables consisting of string text and represent the largest chunk of the code.
- I'll be very honest here; for the API, chart creation, and web app creation (to local hosting), I went for the path of least resistance and chose libraries easy to work with! :)

3. To view the result:
Start with the CMD:

Assuming Python is installed (3.10.4 in my case), you'd need to make sure that the supporting libraries / modules (those used in the python file) are also installed with pip:
pip install psycopg2
pip install pandas
pip install fastapi
pip install plotly
pip install streamlit

Next, make sure that you're working in the same directory / path as the provided .py file (tht_alikhalaf_northwind_etl); you can do this by executing cd "C:\Users\Abdulaziz\Desktop" for example (assuming files are on desktop).

Finally, execute:

streamlit run tht_alikhalaf_northwind_etl.py;

Browser should open (fingers crossed) and show the required charts; full disclosure, I wish I had explored the plotly library earlier and in more detail for nicer outputs!

P.S. Should new records be added to the DB (e.g., new orders and order_details, the results should be reflected on the web app after a refresh - at least, worked for me!)
