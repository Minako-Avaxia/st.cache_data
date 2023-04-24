import streamlit as st
import snowflake.connector

# import snowflake.connector

# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    

@st.cache_data
def long_function(date, init):
    rows = run_query("select * from SNOWFLAKE_SAMPLE_DATA.TPCDS_SF100TCL.STORE;")
    return rows

if __name__ == "__main__":
    date = "2022-01-01"
    init = "init"
    rows = long_function(date, init)


# pattern 2 without cache

# rows = run_query("select * from SNOWFLAKE_SAMPLE_DATA.TPCDS_SF100TCL.STORE;")
# if __name__ == "__main__":
#     data = long_function(date, init)

# # Print results.
for row in rows:
    st.write(f"{row[0]}--{row[1]}")
  
