from database import DB

def create_table():
    DB.execute("""CREATE TABLE IF NOT EXISTS users (
        product_name TEXT,
        product_price INT,
        product_count INT
    );""")
    print('Таблицы успешно созданы!')

if __name__ == '__main__':
    create_table()