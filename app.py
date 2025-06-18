from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# --- Database connection ---
def get_db_connection():
    return psycopg2.connect(
        dbname="eventdb",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

# # --- Homepage: search + category filter ---
# @app.route('/')
# def index():
#     search = request.args.get('search', '')
#     category = request.args.get('category', '')

#     query = f"""
#         SELECT events.id, description, title, event_date, categories.name
#         FROM events
#         JOIN categories ON events.category_id = categories.id
#         WHERE is_vip_only = FALSE
#         AND title ILIKE '%{search}%'
#         {f"AND categories.id = {category}" if category else ""}
#         ORDER BY event_date ASC
#     """

#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT id, name FROM categories")
#         all_categories = cur.fetchall()

#         cur.execute(query)
#         events = cur.fetchall()
#         # print(events)
#     except Exception as e:
#         print(f"Query error: {e}")
#         events = []
#         all_categories = []
#     finally:
#         cur.close()
#         conn.close()

#     return render_template("index.html", events=events, categories=all_categories)

# # --- Event details: vulnerable to blind SQLi ---
# @app.route('/event')
# def event():
#     event_id = request.args.get('event_id', '')

#     query = f"""
#         SELECT title, description, event_date, categories.name, is_vip_only
#         FROM events
#         JOIN categories ON events.category_id = categories.id
#         WHERE is_vip_only = FALSE 
#         AND events.id = '{event_id}'
#     """

#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute(query)
#         event = cur.fetchone()
#     except Exception as e:
#         print(f"Query error: {e}")
#         event = None
#     finally:
#         cur.close()
#         conn.close()

#     if event:
#         return render_template("event.html", event=event)
#     else:
#         return "Event not found or access restricted.", 404
    

# --- Homepage: search + category filter - PROTECTED BY QUERY PARAMETERIZATION ---
@app.route('/')
def index():
    search = request.args.get('search', '')
    category = request.args.get('category', '')

    query = """
        SELECT events.id, description, title, event_date, categories.name
        FROM events
        JOIN categories ON events.category_id = categories.id
        WHERE is_vip_only = FALSE
        AND title ILIKE %s
    """
    params = [f"%{search}%"]

    if category:
        query += " AND categories.id = %s"
        params.append(category)

    query += " ORDER BY event_date ASC"

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(query, params)
        events = cur.fetchall()

        cur.execute("SELECT id, name FROM categories")
        all_categories = cur.fetchall()
    except Exception as e:
        print(f"Query error: {e}")
        events = []
        all_categories = []
    finally:
        cur.close()
        conn.close()

    return render_template("index.html", events=events, categories=all_categories)



# --- Event details: PROTECTED BY TYPE CASTING ---
@app.route('/event')
def event():
    try:
        event_id = int(request.args.get("event_id", ""))
    except ValueError:
        return "Invalid ID", 400

    query = """
        SELECT title, description, event_date, categories.name, is_vip_only
        FROM events
        JOIN categories ON events.category_id = categories.id
        WHERE is_vip_only = FALSE
        AND events.id = %s
    """

    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(query, (event_id,))
        event = cur.fetchone()
    except Exception as e:
        print(f"Query error: {e}")
        event = None
    finally:
        cur.close()
        conn.close()

    if event:
        return render_template("event.html", event=event)
    else:
        return "Event not found or access restricted.", 404


if __name__ == '__main__':
    app.run(host='127.0.0.2', port=80, debug=True)
