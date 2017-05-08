Title: SQL Server and macOS --- my first take
Date: 2017-05-08
Tags: SQL, atom, python, mac
Status: published
Summary: The 90s are back and it turns out that cross platform approach doesn't apply for MS SQL Server.

Recently, I started working at [reBuy](http://www.rebuy.com) and discovered that the data warehouse has recently migrated to [MS SQL Server](https://en.wikipedia.org/wiki/Microsoft_SQL_Server).
Naively, I thought that it would not be much of an impediment; I was wrong.
Over the past 7 years I am mostly using Mac, and beforehand I used to have Linux boxes for couple of years.
The last time I really worked on a Windows machine was 10+ years ago.
By sharing this history with you, I try to explain why I didn't consider switching to Microsoft OS.

Not too surprisingly, as a data scientist, the first step on day $1 + \epsilon$ was to access the data.
At this point my affection to macOS and the company's DWH conflicted.
One of the first stops in the journey to solve the conflict was this [SO thread](http://stackoverflow.com/q/3452/671013).
This thread is a good example of a question whose answer is not really solving the problem introduced by the poster.

## Desktop client

Before diving into hacky workarounds, I tried virtually all the clients suggested in that post.
To cut a long story short, I ended up using [DBVisualizer](https://www.dbvis.com/).
Its free version is OK and at least allows one to execute SQL queries.
To be honest, I didn't try to evaluate any kind of more fancy features.
It managed to address the immediate need --- first look at the data checked.

## What's next?

I feel relatively comfortable with SQL, but I am much more comfortable and productive with Pandas.
So, the next step for me was to figure out how to query the DWH from Python.
For example, I wanted to take advantage of [`pandas.read_sql_query`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_sql_query.html).
This led me to investigate how to connect [SQLalchemy](https://www.sqlalchemy.org/) to MS SQL *from a macOS box*.
Ultimately I found two ways: one using [`pymssql`](http://pymssql.org/en/stable/) alone and the other together with SQLalchemy.

### `pymssql` alone

In order to establish the connection I ran:

```python
conn = pymssql.connect(server="my.great.server", user="WINDOWSDOMAIN\username", password="mysecretpassword", port=1433)
```

Note the need to provide the domain (in capital letters).
In turn, an actual query can be executed:

```python
query = "select top 10 * from db.schema.table1"
pd.read_sql(query, conn)
```

### `pymssql` and SQLalchemy together

I also managed to query the DWH using a combination of `pymssql` and SQLalchemy.

```python
eng = sqlalchemy.create_engine("mssql+pymssql://WINDOWSDOMAIN\username:mysecretpassword@my.great.server:1433/db")
connection = eng.connect()
result = connection.execute("select top 10 * from schema.table1")
pd.DataFrame([x for x in result])
```

As a side remark, which probably deserve a post of its own, once using SQLalchemy I also managed to connect [Superset](https://github.com/airbnb/superset) to the DWH. YAY.

## Atom-ic connection?

DBVisualizer is/was OK.
Nothing more.
I like using my keyboard and as my editor of choice is Atom, I decided to try and utilize it.
It worked out *fabulously*.
The needed package is [Data Atom](https://atom.io/packages/data-atom) and the setting up is rather straightforward.
You might want to fiddle with the [`Timeout` setting](https://github.com/lukemurray/data-atom/issues/125) but as long as the results set is limited this works like a charm.

Interestingly, I failed to connect Visual Studio Code to the DWH.
I thought that as MS are developing VSC, it is likely that the DWH and the celebrated editor will be able to communicate.
In theory this is [possible](https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-develop-use-vscode), but in practice, from a macOS box, [it is not](https://github.com/Microsoft/vscode-mssql/issues/824#issuecomment-296846325).

## Securing the passwords

I ended up, for the time being, using Atom and DBVisualizer.
I spend most of my time on the DWH using Atom, and revert to the latter tool when I need to explore the schema of the database.
Once I know what I need, I take the results set offline into Pandas.
The biggest concern I have at the moment is the securing of the passwords.
Both for `pymssql` and the Data Atom package, the passwords are stored as strings.
I didn't find a way around it yet albeit I'm sure there must be one; after all Superset manages the passwords somehow.
