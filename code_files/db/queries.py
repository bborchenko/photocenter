import os
import pandas as pd

from psycopg2 import connect


class DataBase:
    def __init__(self):
        self.conn = DataBase.get_conn()

    @classmethod
    def get_conn(cls):
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASS')

        conn = connect(
            host=host,
            port=port,
            dbname=db_name,
            user=user,
            password=password,
        )
        conn.autocommit = True
        return conn

    def close(self):
        self.conn.close()

    def get_orders_in_period(self, start_time, end_time):
        query = """
            SELECT 
                id, 
                office_id, 
                photos_amount, 
                format, 
                paper_type, 
                order_date, 
                urgency
            FROM public.logic_orders
            WHERE order_date >= '{}' AND order_date <= '{}'
            ORDER BY order_date DESC
        """.format(start_time, end_time)

        data = pd.read_sql_query(query, self.conn)
        return data

    def get_amount_of_orders_in_office_type(self, office_type, start_time, end_time):
        if office_type == 'По всем':
            query = """
            SELECT 
                COUNT(*) as amount
            FROM public.logic_orders
            """
        else:
            query = """
            SELECT 
                office_id,
                COUNT(orders.id) as amount
            FROM public.logic_orders as orders
                INNER JOIN public.logic_office as office
                ON orders.office_id = office.id
            WHERE office.description = '{}' AND orders.order_date >= '{}' AND  orders.order_date <= '{}'
            GROUP BY office_id
            """.format(office_type, start_time, end_time)

        data = pd.read_sql_query(query, self.conn)
        return data

    def get_orders_in_office_by_id(self, office_id):
        query = """
        SELECT 
            *
        FROM public.logic_orders
        WHERE office_id = '{}'
        """.format(office_id)

        data = pd.read_sql_query(query, self.conn)
        return data

    def get_orders_with_price_bigger(self, price):
        query = """
        SELECT 
            *
        FROM public.logic_orders
        GROUP BY id
        HAVING price > {}
        """.format(price)

        data = pd.read_sql_query(query, self.conn)
        return data

    def get_number_of_clients_with_discount(self, description, discount):
        query = """
        SELECT 
            id, 
            description, 
            discount_card,
            cards.discount as discount
        FROM public.logic_clients as clients
        FULL OUTER JOIN public.logic_discountcards as cards
            ON clients.discount_card = cards.number_id
        WHERE clients.description = '{}' AND cards.discount = {}
        """.format(description, discount)

        data = pd.read_sql_query(query, self.conn)
        return data

    def get_clients_and_cards(self):
        query = """
        SELECT 
            id, 
            description, 
            discount_card,
            cards.discount as discount
        FROM public.logic_clients as clients
        FULL OUTER JOIN public.logic_discountcards as cards
            ON clients.discount_card = cards.number_id
        """

        data = pd.read_sql_query(query, self.conn)
        return data

    def get_amount_of_orders_in_photocenter(self):
        query = """
        SELECT
            id,
            address,
            description,
            (SELECT
                COUNT(*)
            FROM public.logic_orders as orders
            WHERE orders.office_id = office.id) as amount_of_orders
        FROM public.logic_office as office
        """

        data = pd.read_sql_query(query, self.conn)
        return data

    def get_amount_of_equipment(self, equipment_type):
        query = """
        SELECT 
            id, 
            name, 
            company,
            (SELECT 
                SUM(amount)
            FROM public.logic_officeequipment as office_equipment
            WHERE office_equipment.equipment_id = {}) as amount
        FROM public.logic_equipment as equipment
        WHERE id = {}
        """.format(equipment_type, equipment_type)

        data = pd.read_sql_query(query, self.conn)
        return data


if __name__ == '__main__':
    db = DataBase()
    orders = db.get_amount_of_orders_in_photocenter()
    my_dict = orders.to_dict(orient='records')
    print(orders)
